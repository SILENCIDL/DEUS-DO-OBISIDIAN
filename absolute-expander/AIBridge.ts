import { Notice, requestUrl } from "obsidian";
import type { ContextPayload } from "./ContextBuilder";
import type { AbsoluteExpanderSettings } from "./Settings";

const CLAUDE_ENDPOINT = "https://api.anthropic.com/v1/messages";
const GEMINI_ENDPOINT =
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent";

function buildRecursivePrompt(payload: ContextPayload, settings: AbsoluteExpanderSettings): string {
  const fmt = (arr: string[]) => (arr.length ? arr.join(", ") : "nenhum");

  return `Você é um arquiteto de conhecimento recursivo para Obsidian.
Seu objetivo é transformar um TEMA em uma estrutura profunda de SUBTEMAS.

CONTEXTO DA NOTA ATIVA:
- Arquivo: ${payload.activeFile}
- Conteúdo Base: ${payload.selectedText}
- Tags: ${fmt(payload.tags)}
- Conexões: ${payload.backlinks.length} backlinks, ${payload.outlinks.length} outlinks.

INSTRUÇÃO:
1. Analise o "Conteúdo Base" e identifique até ${settings.maxSubthemes} subtemas lógicos.
2. Para cada subtema, crie um título curto e uma descrição de uma frase.
3. Formate a resposta EXATAMENTE como uma lista Markdown de Wikilinks:

ESTRUTURA:
- [[Nome do Subtema 1]]: Descrição breve.
- [[Nome do Subtema 2]]: Descrição breve.
...`;
}

function parseSubthemes(raw: string): string[] {
  const lines = raw.split("\n");
  const subthemes: string[] = [];
  for (const line of lines) {
    const match = line.match(/\[\[(.*?)\]\]/);
    if (match) {
      subthemes.push(match[1]);
    }
  }
  return subthemes;
}

async function callClaude(
  payload: ContextPayload,
  settings: AbsoluteExpanderSettings
): Promise<string> {
  const response = await requestUrl({
    url: CLAUDE_ENDPOINT,
    method: "POST",
    headers: {
      "x-api-key": settings.claudeApiKey,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: "claude-3-5-sonnet-20240620",
      max_tokens: 4096,
      system: buildRecursivePrompt(payload, settings),
      messages: [{ role: "user", content: "Gere a estrutura de subtemas." }],
    }),
  });

  return (response.json?.content?.[0]?.text as string) ?? "";
}

async function callGemini(
  payload: ContextPayload,
  settings: AbsoluteExpanderSettings
): Promise<string> {
  const response = await requestUrl({
    url: `${GEMINI_ENDPOINT}?key=${settings.geminiApiKey}`,
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      system_instruction: {
        parts: [{ text: buildRecursivePrompt(payload, settings) }],
      },
      contents: [{ parts: [{ text: "Gere a estrutura de subtemas." }] }],
      generationConfig: { maxOutputTokens: 4096 },
    }),
  });

  return (response.json?.candidates?.[0]?.content?.parts?.[0]?.text as string) ?? "";
}

export async function generateRecursiveExpansions(
  payload: ContextPayload,
  settings: AbsoluteExpanderSettings
): Promise<{ raw: string; subthemes: string[] }> {
  const { activeModel, claudeApiKey, geminiApiKey } = settings;

  try {
    const raw = activeModel === "claude"
      ? await callClaude(payload, settings)
      : await callGemini(payload, settings);
    
    return { raw, subthemes: parseSubthemes(raw) };
  } catch (err: unknown) {
    new Notice(`Erro na IA: ${String(err)}`);
    return { raw: "", subthemes: [] };
  }
}
