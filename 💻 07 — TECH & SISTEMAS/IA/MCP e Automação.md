---
created: 2026-04-26
módulo: TECH
tags: [tech, ferramentas, ia]
status: ativo
---

# MCP e Automação

**Área:** Tecnologia & Ferramentas
**Tags:** #mcp #obsidian #automacao #python #servidor-local
**Status:** Servidor criado ✅
**Links:** [[Obsidian Vault — DEUS-DO-OBSIDIAN]] | [[GitHub e Claude Code]]

---

## Contexto

Servidor MCP em Python conectando Claude ao vault do Obsidian via stdio.
Local, sem internet, 100% na máquina.

---

## Ferramentas do servidor (10)

- Ler notas
- Criar notas
- Editar notas
- Deletar notas (usa `.trash/` — seguro)
- Buscar por conteúdo
- Listar notas por pasta
- Sincronizar contexto
- + 3 auxiliares

---

## Setup

1. `pip install mcp`
2. Editar `claude_desktop_config.json` — caminho do `.py` + caminho do vault
3. Reiniciar Claude Desktop

**Variável de ambiente:** `OBSIDIAN_VAULT_PATH`

---

## Entregável

`obsidian_mcp_server.zip`
- `obsidian_mcp.py`
- `setup_windows.bat`
- `README.md`

---

## Conversa de referência

https://claude.ai/chat/1a5b6283-65d8-43c4-b400-25d467b541a4
---
*Pai: [[_MOC-Tech]]*
