import { Notice, requestUrl } from "obsidian";
import type { ContextPayload } from "./ContextBuilder";
import type { AbsoluteExpanderSettings } from "./Settings";

const CLAUDE_ENDPOINT = "https://api.anthropic.com/v1/messages";
const GEMINI_ENDPOINT =
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";

const API_TIMEOUT_MS = 20_000;
const MAX_LINKS_IN_PROMPT = 50;

// ---------------------------------------------------------------------------
// Timeout wrapper — requestUrl não tem timeout nativo.
// ---------------------------------------------------------------------------
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(
      () => reject(Object.assign(new Error("timeout"), { status: 408 })),
      ms
    )
  );
  return Promise.race([promise, timeout]);
}

// ---------------------------------------------------------------------------
// Retry automático para 429 (rate-limit) com back-off linear.
// ---------------------------------------------------------------------------
async function withRetry<T>(
  fn: () => Promise<T>,
  retries = 2,
  delayMs = 2500
): Promise<T> {
  let lastErr: unknown;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      const status = (err as { status?: number })?.status;
      if (status === 429 && attempt < retries) {
        await new Promise((r) => setTimeout(r, delayMs * (attempt + 1)));
        continue;
      }
      throw err;
    }
  }
  throw lastErr;
}

// ---------------------------------------------------------------------------
// System prompt — com truncamento defensivo para evitar estouro de tokens.
// ---------------------------------------------------------------------------
function buildSystemPrompt(payload: ContextPayload): string {
  const fmt = (arr: string[]) => (arr.length ? arr.join(", ") : "nenhum");

  const backlinks = payload.backlinks.slice(0, MAX_LINKS_IN_PROMPT);
  const outlinks  = payload.outlinks.slice(0, MAX_LINKS_IN_PROMPT);

  const truncNote =
    payload.backlinks.length > MAX_LINKS_IN_PROMPT ||
    payload.outlinks.length  > MAX_LINKS_IN_PROMPT
      ? `\n(lista truncada para os primeiros ${MAX_LINKS_IN_PROMPT} itens)`
      : "";

  return `Você é um especialista em expansão de conhecimento para sistemas PKM (Zettelkasten / Obsidian).

CONTEXTO DA NOTA ATIVA:
- Arquivo: ${payload.activeFile}
- Tags: ${fmt(payload.tags)}
- Backlinks — ${backlinks.length} notas citam esta: ${fmt(backlinks)}${truncNote}
- Outlinks  — ${outlinks.length} notas citadas por esta: ${fmt(outlinks)}${truncNote}

INSTRUÇÃO:
Considere as conexões semânticas acima e gere EXATAMENTE 3 variações do trecho recebido.
Retorne apenas as variações, sem explicações ou texto adicional, neste formato estrito:

TECNICA: [reformulação objetiva e terminologicamente precisa, adequada para documentação]
CRIATIVA: [reformulação narrativa com metáforas, adequada para síntese pessoal e reflexão]
SINTETICA: [compressão em uma única frase densa, apta a servir como título de nota ou link-âncora]`;
}

// ---------------------------------------------------------------------------
// Parser robusto — aceita labels com ou sem acento, com ou sem espaço extra.
// ---------------------------------------------------------------------------
function parseVariations(raw: string): string[] {
  const extract = (label: string): string => {
    const pattern = new RegExp(
      `${label}:\\s*([\\s\\S]+?)(?=TECNICA:|CRIATIVA:|SINTETICA:|$)`,
      "i"
    );
    return pattern.exec(raw)?.[1]?.trim() ?? "";
  };

  return [
    extract("T[EÉ]CNICA"),
    extract("CRIATIVA"),
    extract("SINT[EÉ]TICA"),
  ];
}

// ---------------------------------------------------------------------------
// Notificações de erro — centralizadas e descritivas.
// ---------------------------------------------------------------------------
function notifyError(err: unknown): void {
  const status = (err as { status?: number })?.status;
  const msg    = err instanceof Error ? err.message : String(err);

  const notices: Record<number, string> = {
    401: "Chave de API inválida ou expirada.",
    403: "Acesso negado — verifique as permissões da chave.",
    408: "Tempo limite esgotado (20 s). Verifique sua conexão.",
    429: "Limite de requisições atingido. Tente novamente em instantes.",
    400: "Requisição malformada — verifique o modelo selecionado nas configurações.",
    500: "Erro interno no servidor da API. Tente novamente.",
  };

  const text = status !== undefined && status in notices
    ? notices[status]
    : `Falha na requisição — ${msg}`;

  new Notice(`Absolute Expander: ${text}`);
}

// ---------------------------------------------------------------------------
// Chamada Claude
// ---------------------------------------------------------------------------
async function callClaude(
  payload: ContextPayload,
  settings: AbsoluteExpanderSettings
): Promise<string[]> {
  const response = await withTimeout(
    requestUrl({
      url: CLAUDE_ENDPOINT,
      method: "POST",
      headers: {
        "x-api-key": settings.claudeApiKey,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model: settings.claudeModel,
        max_tokens: 1024,
        system: buildSystemPrompt(payload),
        messages: [
          {
            role: "user",
            content: `Expanda este trecho:\n\n"${payload.selectedText}"`,
          },
        ],
      }),
    }),
    API_TIMEOUT_MS
  );

  const text: string = (response.json?.content?.[0]?.text as string) ?? "";
  console.debug("[AbsoluteExpander] Claude raw response:", text);
  return parseVariations(text);
}

// ---------------------------------------------------------------------------
// Chamada Gemini
// ---------------------------------------------------------------------------
async function callGemini(
  payload: ContextPayload,
  apiKey: string
): Promise<string[]> {
  const response = await withTimeout(
    requestUrl({
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
    }),
    API_TIMEOUT_MS
  );

  const text: string =
    (response.json?.candidates?.[0]?.content?.parts?.[0]?.text as string) ?? "";
  console.debug("[AbsoluteExpander] Gemini raw response:", text);
  return parseVariations(text);
}

// ---------------------------------------------------------------------------
// Ponto de entrada público
// ---------------------------------------------------------------------------
export async function generateExpansions(
  payload: ContextPayload,
  settings: AbsoluteExpanderSettings
): Promise<string[]> {
  const { activeModel, claudeApiKey, geminiApiKey } = settings;

  if (activeModel === "claude" && !claudeApiKey.trim()) {
    new Notice("Absolute Expander: adicione sua Claude API Key nas configurações.");
    return [];
  }
  if (activeModel === "gemini" && !geminiApiKey.trim()) {
    new Notice("Absolute Expander: adicione sua Gemini API Key nas configurações.");
    return [];
  }

  try {
    return await withRetry(() =>
      activeModel === "claude"
        ? callClaude(payload, settings)
        : callGemini(payload, geminiApiKey)
    );
  } catch (err: unknown) {
    notifyError(err);
    return [];
  }
}
