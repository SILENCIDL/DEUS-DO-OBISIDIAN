---
title: "ÍNDICE - Sistema e Templates"
type: "reference"
created: 2026-05-19
updated: 2026-05-19

category: "00_Sistema"
status: "active"
priority: 3

tags:
  - system:infrastructure
  - system:templates
  - project:vault-management
  - status:active
---

# ⚙️ Sistema e Templates
## Infraestrutura do Vault | Padrões Reutilizáveis

[[🏠 ÍNDICE|← Voltar ao Índice Geral]]

---

## 🎯 Visão Geral

Documentação operacional do vault. Templates reutilizáveis (briefing, case study, etc.), padrões de metadados, automações, e logs do sistema.

**Status:** Ativo | **Última atualização:** 2026-05-19

---

## 📂 SUB-ÍNDICES

### [[00_Sistema/Templates|📋 Templates]]
**Modelos reutilizáveis para projetos**

- `Template-Briefing-Evento` (Fotografia)
- `Template-Case-Study` (Portfolio)
- `Template-Blog-Post` (Desenvolvimento)
- `Template-Projeto` (Geral)

---

### 📏 **PADRÕES**

#### [[📋 PADRÃO - Frontmatter YAML|YAML Frontmatter]]
**Standard de metadados**

Documentação normativa para YAML frontmatter em todas as notas. Define:
- Tags estruturadas (skill, tool, project, lang, status, roi)
- Campos obrigatórios (title, type, created, updated)
- Exemplos reais de uso

**Regra:** Toda nota nova segue este padrão.

---

### 🔧 **AUTOMAÇÕES**

#### [[02_Desenvolvimento/Automacoes_Obsidian_API/Automacoes_Obsidian_API|Obsidian API]]
**REST API local + webhooks**

Scripts e automações para sincronizar vault com sistemas externos (Anki, Git, Slack, etc.).

**Status:** Backlog Q3

---

### 📋 **LOGS & DOCUMENTAÇÃO**

#### [[memory/concilio-log|Concílio Log]]
**Registro da Fase 1: limpeza estrutural + padrões**

- Tarefas executadas (Frontmatter, MOCs, Dashboard, etc.)
- Artefatos criados
- Regras normativas documentadas
- Próximo Concílio: 2026-06-19

---

## 🚨 REGRAS NORMATIVAS

### ✅ FAZER
- ✅ YAML frontmatter em **toda nota nova**
- ✅ Nomes em **snake_case** (sem parênteses, sem acentos longos)
- ✅ Atualizar `updated:` quando editar
- ✅ Usar tags estruturadas (min 3 tags)
- ✅ Documentar decisões críticas

### ❌ EVITAR
- ❌ Pastas com nomenclaturas longas
- ❌ Caracteres especiais nos nomes
- ❌ Tags genéricas ("importante", "later")
- ❌ `updated:` desatualizado

---

## 🔄 PRÓXIMA REVISÃO

**Data:** 2026-06-19 (mensal)

---

*Documentação viva. Atualizada conforme necessário.*
