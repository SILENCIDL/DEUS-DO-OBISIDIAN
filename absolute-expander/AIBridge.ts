import { Notice, requestUrl } from "obsidian";
import type { ContextPayload } from "./ContextBuilder";
import type { AbsoluteExpanderSettings } from "./Settings";

const CLAUDE_ENDPOINT = "https://api.anthropic.com/v1/messages";
const GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent";
const KIMI_ENDPOINT = "https://api.moonshot.cn/v1/chat/completions";

const PROMPTS = {
    claude: "Você atua como um Arquiteto de Ontologias. Decomponha o tema em subtemas MECE, focando em precisão técnica e hierarquia lógica.",
    gemini: "Você é um motor de busca semântica. Identifique 30 subtemas, incluindo nichos raros e conexões interdisciplinares.",
    kimi: "Você é um especialista em Zettelkasten. Gere subtemas para notas atômicas, mantendo descrições densas e estruturadas."
};

function buildRecursivePrompt(payload: ContextPayload, settings: AbsoluteExpanderSettings): string {
  const systemBase = PROMPTS[settings.activeModel as keyof typeof PROMPTS] || PROMPTS.claude;
  
  return `${systemBase}

CONTEXTO DA NOTA:
- Arquivo: ${payload.activeFile}
- Conteúdo: ${payload.selectedText}

INSTRUÇÃO:
Gere até ${settings.maxSubthemes} subtemas como uma lista de Wikilinks:
- [[Nome do Subtema]]: Descrição.`;
}

async function callKimi(payload: ContextPayload, settings: AbsoluteExpanderSettings): Promise<string> {
    // KimiAI usa interface compatível com OpenAI
    const response = await requestUrl({
        url: KIMI_ENDPOINT,
        method: "POST",
        headers: {
            "Authorization": `Bearer ${settings.kimiApiKey}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model: "moonshot-v1-8k",
            messages: [
                { role: "system", content: buildRecursivePrompt(payload, settings) },
                { role: "user", content: "Gere a estrutura." }
            ]
        })
    });
    return response.json?.choices?.[0]?.message?.content ?? "";
}

// ... (Manter callClaude e callGemini com as mesmas lógicas de endpoint, mas usando o novo buildRecursivePrompt)

export async function generateRecursiveExpansions(
  payload: ContextPayload,
  settings: AbsoluteExpanderSettings
): Promise<{ raw: string; subthemes: string[] }> {
  const { activeModel } = settings;
  let raw = "";

  try {
    if (activeModel === "claude") raw = await callClaude(payload, settings);
    else if (activeModel === "gemini") raw = await callGemini(payload, settings);
    else if (activeModel === "kimi") raw = await callKimi(payload, settings);
    
    return { raw, subthemes: parseSubthemes(raw) };
  } catch (err: unknown) {
    new Notice(`Erro na IA (${activeModel}): ${String(err)}`);
    return { raw: "", subthemes: [] };
  }
}

function parseSubthemes(raw: string): string[] {
  const subthemes: string[] = [];
  const matches = raw.matchAll(/\[\[(.*?)\]\]/g);
  for (const match of matches) {
    subthemes.push(match[1]);
  }
  return subthemes;
}

// Funções callClaude e callGemini simplificadas para o exemplo (devem seguir o padrão anterior)
async function callClaude(payload: ContextPayload, settings: AbsoluteExpanderSettings): Promise<string> {
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
      messages: [{ role: "user", content: "Gere a estrutura." }],
    }),
  });
  return (response.json?.content?.[0]?.text as string) ?? "";
}

async function callGemini(payload: ContextPayload, settings: AbsoluteExpanderSettings): Promise<string> {
  const response = await requestUrl({
    url: `${GEMINI_ENDPOINT}?key=${settings.geminiApiKey}`,
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: buildRecursivePrompt(payload, settings) + "\n\nGere a estrutura." }] }],
      generationConfig: { maxOutputTokens: 4096 },
    }),
  });
  return (response.json?.candidates?.[0]?.content?.parts?.[0]?.text as string) ?? "";
}
