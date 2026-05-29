---
created: 2026-05-29
tags:
  - projeto
  - obsidian
  - plugin
  - absolute-expander
  - desenvolvimento
---

# Absolute Expander v1.1.0 — Status do Build

Plugin Obsidian para expandir texto selecionado via IA, gerando 3 variações contextualizadas (Técnica, Criativa, Sintética) a partir do grafo da nota ativa.

## Estado atual

- **Build**: ✅ Concluído — `main.js` (18 KB) gerado sem erros
- **TypeScript**: ✅ Sem erros de tipo (`tsc --noEmit` limpo)
- **Versão**: 1.1.0

## Correções aplicadas (v1.1.0)

- Modelo Claude atualizado para `claude-sonnet-4-6`
- Gemini atualizado para `gemini-2.0-flash`
- Timeout de 20 s com `withTimeout()`
- Retry automático em erro 429 com back-off linear
- `parseVariations` robusto (aceita labels com/sem acento)
- Truncamento de backlinks/outlinks em até 50 itens
- Notice persistente durante o carregamento (`timeout: 0`)
- Bounds check no modal (fallback `EMPTY_META` para variações extras)

## Arquitetura

| Arquivo | Responsabilidade |
|---|---|
| `main.ts` | Ponto de entrada, comandos Obsidian |
| `ContextBuilder.ts` | Captura seleção, backlinks, outlinks e tags |
| `AIBridge.ts` | Chamadas Claude e Gemini com retry/timeout |
| `ExpansionModal.ts` | Modal de seleção com 3 cards visuais |
| `Settings.ts` | Configurações e aba de preferências |

## Próximos passos

- [ ] Copiar `main.js` + `manifest.json` para `C:\Users\Usuário\Desktop\V1\.obsidian\plugins\absolute-expander\`
- [ ] Reativar o plugin em Obsidian → Configurações → Plugins da comunidade
- [ ] Inserir Claude API Key e/ou Gemini API Key nas configurações do plugin
- [ ] Testar o comando **Expandir Texto Selecionado** com uma nota do vault

## Relacionado

- [[DEUS-DO-OBSIDIAN]]
- [[ponto 000]]
