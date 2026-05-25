import { Notice, requestUrl } from "obsidian";
import type { ContextPayload } from "./ContextBuilder";
import type { AbsoluteExpanderSettings } from "./Settings";

const CLAUDE_ENDPOINT = "https://api.anthropic.com/v1/messages";
const GEMINI_ENDPOINT =
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";

// Constrói o system prompt injetando a teia de contexto da nota.
// Backlinks e outlinks fornecem ao LLM a semântica de vizinhança —
// crucial para que as variações permaneçam coerentes com a vault.
function buildSystemPrompt(payload: ContextPayload): string {
  const fmt = (arr: string[]) => (arr.length ? arr.join(", ") : "nenhum");

  return `Você é um especialista em expansão de conhecimento para sistemas PKM (Zettelkasten / Obsidian).

CONTEXTO DA NOTA ATIVA:
- Arquivo: ${payload.activeFile}
- Tags: ${fmt(payload.tags)}
- Backlinks — ${payload.backlinks.length} notas citam esta: ${fmt(payload.backlinks)}
- Outlinks — ${payload.outlinks.length} notas citadas por esta: ${fmt(payload.outlinks)}

INSTRUÇÃO:
Considere as conexões semânticas acima e gere EXATAMENTE 3 variações do trecho recebido.
Retorne apenas as variações, sem explicações ou texto adicional, neste formato estrito:

TÉCNICA: [reformulação objetiva e terminologicamente precisa, adequada para documentação]
CRIATIVA: [reformulação narrativa com metáforas, adequada para síntese pessoal e reflexão]
SINTÉTICA: [compressão em uma única frase densa, apta a servir como título de nota ou link-âncora]`;
}

// Regex tolerante a quebras de linha dentro de cada variação.
function parseVariations(raw: string): string[] {
  const técnica =
    /TÉCNICA:\s*([\s\S]+?)(?=CRIATIVA:|$)/i.exec(raw)?.[1]?.trim() ?? "";
  const criativa =
    /CRIATIVA:\s*([\s\S]+?)(?=SINTÉTICA:|$)/i.exec(raw)?.[1]?.trim() ?? "";
  const sintética =
    /SINTÉTICA:\s*([\s\S]+?)$/i.exec(raw)?.[1]?.trim() ?? "";
  return [técnica, criativa, sintética];
}

async function callClaude(
  payload: ContextPayload,
  apiKey: string
): Promise<string[]> {
  const response = await requestUrl({
    url: CLAUDE_ENDPOINT,
    method: "POST",
    headers: {
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: "claude-opus-4-7",
      max_tokens: 1024,
      system: buildSystemPrompt(payload),
      messages: [
        {
          role: "user",
          content: `Expanda este trecho:\n\n"${payload.selectedText}"`,
        },
      ],
    }),
  });

  const text: string = (response.json?.content?.[0]?.text as string) ?? "";
  console.debug("[AbsoluteExpander] Claude raw response:", text);
  return parseVariations(text);
}

async function callGemini(
  payload: ContextPayload,
  apiKey: string
): Promise<string[]> {
  const response = await requestUrl({
    url: `${GEMINI_ENDPOINT}?key=${apiKey}`,
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      system_instruction: {
        parts: [{ text: buildSystemPrompt(payload) }],
      },
      contents: [
        {
          parts: [
            {
              text: `Expanda este trecho:\n\n"${payload.selectedText}"`,
            },
          ],
        },
      ],
      generationConfig: { maxOutputTokens: 1024 },
    }),
  });

  const text: string =
    (response.json?.candidates?.[0]?.content?.parts?.[0]?.text as string) ?? "";
  console.debug("[AbsoluteExpander] Gemini raw response:", text);
  return parseVariations(text);
}

function notifyError(err: unknown): void {
  const status = (err as { status?: number })?.status;
  if (status === 401) {
    new Notice("Absolute Expander: chave de API inválida ou expirada.");
  } else if (status === 429) {
    new Notice(
      "Absolute Expander: limite de requisições atingido. Aguarde alguns segundos."
    );
  } else if (status === 400) {
    new Notice("Absolute Expander: requisição malformada — verifique o modelo selecionado.");
  } else {
    const msg = err instanceof Error ? err.message : String(err);
    new Notice(`Absolute Expander: falha na requisição — ${msg}`);
  }
}

export async function generateExpansions(
  payload: ContextPayload,
  settings: AbsoluteExpanderSettings
): Promise<string[]> {
  const { activeModel, claudeApiKey, geminiApiKey } = settings;

  if (activeModel === "claude" && !claudeApiKey) {
    new Notice("Absolute Expander: adicione sua Claude API Key nas configurações.");
    return [];
  }
  if (activeModel === "gemini" && !geminiApiKey) {
    new Notice("Absolute Expander: adicione sua Gemini API Key nas configurações.");
    return [];
  }

  try {
    return activeModel === "claude"
      ? await callClaude(payload, claudeApiKey)
      : await callGemini(payload, geminiApiKey);
  } catch (err: unknown) {
    notifyError(err);
    return [];
  }
}
