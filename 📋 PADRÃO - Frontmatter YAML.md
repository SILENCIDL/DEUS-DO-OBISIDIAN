# 📋 PADRÃO DE FRONTMATTER YAML
## Vinicius Rafael | Concílio Obsidian - Fase 1

> Documento normativo. **Todas as novas notas** devem seguir este padrão.  
> Leitura recomendada para compreender a taxonomia do vault.

---

## 🎯 Objetivo

Padronizar metadados em YAML no topo de cada nota para:
- Rastreabilidade (tags, status, datas)
- Busca avançada (Obsidian e análise externa)
- Automação futura (API, scripts, exportação)
- Consistência visual + organizacional

---

## 📝 TEMPLATE PADRÃO

```yaml
---
# Identificação
title: "Título da Nota"
type: "project|study|reference|checklist|decision|template"
created: 2026-05-19
updated: 2026-05-19

# Classificação
category: "01_Fotografia|02_Desenvolvimento|03_Idiomas|04_Projetos_Pessoais|memory"
status: "active|paused|archived|completed"
priority: 1-5  # 1=crítico, 5=nice-to-have

# Tags estruturadas
tags:
  - skill:fotografia  # skill:DOMÍNIO
  - tool:lightroom    # tool:SOFTWARE
  - project:portfolio # project:CODENAME
  - lang:português    # lang:IDIOMA
  - status:draft      # status:ESTÁGIO

# Relacionamentos
aliases:
  - "Alias 1"
  - "Alias 2"
related: 
  - "[[Link Relacionado 1]]"
  - "[[Link Relacionado 2]]"

# Metadados úteis
author: "Vinicius Rafael"
reviewed_by: ""
next_review: 2026-06-19

# Custom (opcional)
difficulty: "beginner|intermediate|advanced"
time_estimate: "30 min|2h|1 day"
roi: "financial|creative|learning|wellness"
---

# Título da Nota

Conteúdo aqui...
```

---

## 🔍 GUIA DE CAMPOS

### 1. **Identificação**

| Campo | Valores | Exemplo | Obrigatório |
|-------|---------|---------|-------------|
| `title` | String | "Pack Filmic Mantiqueira v2" | ✅ Sim |
| `type` | project / study / reference / checklist / decision / template | "project" | ✅ Sim |
| `created` | YYYY-MM-DD | 2026-05-19 | ✅ Sim |
| `updated` | YYYY-MM-DD | 2026-05-19 | ✅ Sim |

---

### 2. **Classificação**

| Campo | Valores | Exemplo | Obrigatório |
|-------|---------|---------|-------------|
| `category` | Pasta principal | "01_Fotografia" | ✅ Sim |
| `status` | active/paused/archived/completed | "active" | ✅ Sim |
| `priority` | 1-5 | 2 | ✅ Sim |

**status legend:**
- **active** - Em progresso ou uso contínuo
- **paused** - Suspenso temporariamente (retomar em Q3?)
- **archived** - Concluído, referência histórica
- **completed** - Finalizado com sucesso (meta atingida)

---

### 3. **Tags Estruturadas**

**Formato:** `PREFIX:VALUE`

#### skill:DOMÍNIO
```
skill:fotografia
skill:desenvolvimento
skill:idiomas
skill:iot
skill:3d
skill:color-grading
```

#### tool:SOFTWARE
```
tool:lightroom
tool:photoshop
tool:blender
tool:obsidian
tool:anki
tool:italki
```

#### project:CODENAME
```
project:portfolio       # Portfolio Site Vinicius
project:mandarim        # Mandarim Learning
project:horta           # Horta Automação
project:pack-filmic     # Pack Filmic Mantiqueira
project:obsidian-api    # Obsidian API Automation
```

#### lang:IDIOMA
```
lang:português
lang:mandarim
lang:espanhol
lang:francês
lang:english
```

#### status:ESTÁGIO
```
status:draft       # Rascunho, não validado
status:review      # Aguardando revisão
status:approved    # Aprovado, publicável
status:published   # Publicado/entregue
```

#### roi:RETORNO
```
roi:financial      # Gera renda ou economiza
roi:creative       # Portfólio, skill visual
roi:learning       # Educação, crescimento
roi:wellness       # Qualidade de vida, relacionamento
```

---

### 4. **Relacionamentos**

**aliases:**  
Nomes alternativos para busca rápida.
```yaml
aliases:
  - "Site Vinicius"
  - "Portfolio Web"
  - "FOTOGRAFIA-VINICIUS-SITE"
```

**related:**  
Links internos para notas conectadas.
```yaml
related:
  - "[[02_Desenvolvimento/Portfolio_Site_Vinicius/Portfolio_Site_Vinicius]]"
  - "[[🎯 MAPA DE EXPANSÃO - Vinicius Rafael]]"
```

---

### 5. **Metadados Úteis**

| Campo | Valores | Exemplo |
|-------|---------|---------|
| `author` | Nome | "Vinicius Rafael" |
| `reviewed_by` | Nome ou vazio | "Casal" |
| `next_review` | YYYY-MM-DD | 2026-06-19 |
| `difficulty` | beginner/intermediate/advanced | "intermediate" |
| `time_estimate` | String | "2h", "1 day", "30 min" |
| `roi` | financial/creative/learning/wellness | "creative" |

---

## 📚 EXEMPLOS REAIS

### Exemplo 1: Nota de Projeto Ativo

```yaml
---
title: "Portfólio Site Vinicius"
type: "project"
created: 2026-05-18
updated: 2026-05-19

category: "02_Desenvolvimento"
status: "active"
priority: 1

tags:
  - skill:desenvolvimento
  - tool:astro
  - tool:tailwind
  - project:portfolio
  - status:in-progress
  - roi:financial

aliases:
  - "FOTOGRAFIA-VINICIUS-SITE"
  - "Portfolio Web"
related:
  - "[[🎯 MAPA DE EXPANSÃO - Vinicius Rafael]]"
  - "[[📊 DASHBOARD DE VIDA - Vinicius Rafael]]"

author: "Vinicius Rafael"
reviewed_by: "Casal"
next_review: 2026-06-19
difficulty: "intermediate"
time_estimate: "40h"
roi: "financial"
---

# Portfólio Site Vinicius

...conteúdo...
```

### Exemplo 2: Nota de Estudo

```yaml
---
title: "Core Web Vitals: LCP, CLS, FID"
type: "study"
created: 2026-05-17
updated: 2026-05-19

category: "02_Desenvolvimento"
status: "active"
priority: 2

tags:
  - skill:desenvolvimento
  - skill:performance
  - tool:astro
  - project:portfolio
  - status:approved
  - roi:learning

aliases:
  - "Web Performance"
related:
  - "[[02_Desenvolvimento/Portfolio_Site_Vinicius/Portfolio_Site_Vinicius]]"

author: "Vinicius Rafael"
next_review: 2026-06-19
difficulty: "advanced"
time_estimate: "3h"
roi: "learning"
---

# Core Web Vitals...
```

### Exemplo 3: Checklist

```yaml
---
title: "Checklist: Deploy Portfólio v1"
type: "checklist"
created: 2026-05-19
updated: 2026-05-19

category: "02_Desenvolvimento"
status: "active"
priority: 1

tags:
  - skill:desenvolvimento
  - project:portfolio
  - status:in-progress

related:
  - "[[02_Desenvolvimento/Portfolio_Site_Vinicius/Portfolio_Site_Vinicius]]"

author: "Vinicius Rafael"
time_estimate: "4h"
roi: "financial"
---

# Checklist: Deploy Portfólio v1

- [ ] Homepage responsive (mobile + tablet + desktop)
- [ ] Galeria filtrada por categoria
...
```

---

## 🚨 REGRAS NORMATIVAS

### ✅ FAZER

- ✅ Atualizar `updated:` sempre que editar
- ✅ Usar YAML frontmatter em **toda nota nova**
- ✅ Manter `tags:` com pelo menos 3 tags
- ✅ Revisar `status:` mensalmente
- ✅ Documentar `related:` para navegar o vault
- ✅ Use nomes em **snake_case** para pastas/arquivos (SEM parênteses, SEM acentos longos)

### ❌ EVITAR

- ❌ Tags genéricas ("importante", "random", "later")
- ❌ Nomes com caracteres especiais ou muito longos
- ❌ Deixar `updated:` desatualizado por semanas
- ❌ `status:` indefinido (sempre escolher um)
- ❌ Pastas com nomenclaturas longas ou entre parênteses

---

## 🔄 SINCRONIZAÇÃO COM AUTOMAÇÕES

Quando implementar **Obsidian API**, este frontmatter permitirá:

```javascript
// Exemplo: buscar todas as notas "ativas" de "Fotografia"
const activePhotoNotes = notes
  .filter(n => n.category === "01_Fotografia" && n.status === "active")
  .sort((a, b) => a.priority - b.priority);

// Exemplo: próximas notas para revisar
const needsReview = notes
  .filter(n => new Date(n.next_review) <= today)
  .sort((a, b) => new Date(a.next_review) - new Date(b.next_review));
```

---

## 📅 PRÓXIMA REVISÃO

- **Próxima atualização:** 2026-06-19 (mensal)
- **Pontos a revisar:**
  - Novas tags emergentes (adicionar à lista?)
  - Campos unused (remover?)
  - Feedback de uso (ajustes?)

---

## 🏁 CONCLUSÃO

Este padrão é **evolutivo, não dogmático**. Atualize conforme aprenda.

**Criado:** 2026-05-19  
**Responsável:** Vinicius Rafael + Concílio Claude  
**Status:** APROVADO PARA USO

