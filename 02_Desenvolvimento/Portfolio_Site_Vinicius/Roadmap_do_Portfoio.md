---
title: "Roadmap do Portfólio"
type: "project"
created: 2026-05-19
updated: 2026-05-19

category: "02_Desenvolvimento"
status: "active"
priority: 1

tags:
  - skill:desenvolvimento
  - skill:design
  - tool:astro
  - tool:tailwind
  - tool:figma
  - project:portfolio
  - status:in-progress
  - roi:financial

aliases:
  - "FOTOGRAFIA-VINICIUS-SITE Roadmap"
  - "Portfolio Development Log"
related:
  - "[[02_Desenvolvimento/Portfolio_Site_Vinicius/Portfolio_Site_Vinicius]]"
  - "[[🎯 MAPA DE EXPANSÃO - Vinicius Rafael]]"
  - "[[📊 DASHBOARD DE VIDA - Vinicius Rafael]]"

author: "Vinicius Rafael"
reviewed_by: "Casal"
next_review: 2026-05-26
time_estimate: "40h MVP"
roi: "financial"
---

# 🚀 Roadmap do Portfólio
## FOTOGRAFIA-VINICIUS-SITE | Vinicius Rafael

> Documento vivo. Registra decisões técnicas, checklists, aprendizados diários.  
> Atualizado conforme progresso em VSCode.

---

## 📋 FASE 1: DECISION & SETUP (19-26 Maio)

### 1.1 Framework Decision: Astro vs Next.js

**Status:** 🔄 EM DECISÃO

#### Astro ✨
**Pros:**
- Rápido (static by default)
- Ideal para portfolio (content-focused)
- SEO nativo excelente
- Menos JavaScript

**Cons:**
- Menos dinâmico (blog não é super interativo)
- Comunidade menor que Next

**Custo:** ⚡ Muito rápido setup

#### Next.js 🔷
**Pros:**
- Full-stack (backend opcional)
- Dinâmico se precisar depois
- Melhor se quiser API integrada
- Comunidade enorme

**Cons:**
- Mais JavaScript (performance)
- Mais setup inicial

**Custo:** ⏱️ Mais complexo

#### DECISÃO RECOMENDADA: **ASTRO**
**Razão:** Portfolio é content-first. SEO importante. Astro bate mais.  
Se precisar dinâmico depois, migra fácil.

---

### 1.2 Checklist: Setup Inicial

- [ ] Criar diretório `/portfolio-vinicius` no VSCode
- [ ] `npm create astro@latest` (ou Next.js)
- [ ] Escolher template mínimo (blank)
- [ ] Setup Git + repo inicial
- [ ] Deploy provider decidido (Vercel? Netlify? Self-hosted?)
- [ ] Instalar Tailwind CSS
- [ ] Criar componentes base (Header, Footer, Layout)

**Tempo estimado:** 2-3 horas

---

## 📐 FASE 2: DESIGN & WIREFRAMES (20-31 Maio)

### 2.1 Seções do Site

```
/
├─ Home (Hero + CTA)
├─ Portfolio (Galeria filtrada)
│  ├─ Fotografia (esporte, vídeo, produto, retrato)
│  └─ Desenvolvimento (3D, web, automação)
├─ Case Studies (3-5 estudos detalhados)
├─ Blog (Artigos técnicos)
├─ Sobre (Bio, valores, skills)
└─ Contato (Form + social links)
```

### 2.2 Wireframes TODO

- [ ] Homepage (hero, featured works, cta)
- [ ] Galeria (grid + filtros, lazy loading)
- [ ] Case study template (imagens, texto, processo)
- [ ] Blog post template (MDX, code syntax)
- [ ] Sobre página
- [ ] Contato (form, email integration)

**Ferramenta:** Figma (rápido, exportável)  
**Tempo estimado:** 6-8 horas

---

### 2.3 Design System (Tailwind)

#### Paleta
```css
/* Mantiqueira aesthetic */
Primary: #10b981 (emerald, serrana green)
Secondary: #f59e0b (gold, warm)
Dark: #1f2937 (graphite)
Light: #f9fafb (almost white)
Accent: #8b5cf6 (purple, criatividade)
```

#### Typography
- Heading: Inter Bold (modern, tech-forward)
- Body: Poppins Regular (friendly, approachable)
- Code: JetBrains Mono (technical credibility)

#### Spacing
- Base: 4px grid
- Card padding: 24px
- Section gap: 64px (desktop), 32px (mobile)

---

## 💻 FASE 3: DESENVOLVIMENTO (Junho)

### 3.1 Homepage

**Componentes:**
- [ ] Navbar (sticky, dark mode toggle)
- [ ] Hero section (imagem de fundo, CTA)
- [ ] Featured works (3-4 melhores projetos)
- [ ] CTA section ("Ver portfolio completo")
- [ ] Footer (social links, email)

**Core Web Vitals target:**
- LCP: < 2.5s
- CLS: < 0.1
- FID: < 100ms

**Tempo:** 8-10 horas

---

### 3.2 Galeria & Filtros

**Funcionalidade:**
- [ ] Grid responsivo (3 colunas desktop, 2 tablet, 1 mobile)
- [ ] Filtros por tipo (fotografia, código, 3D)
- [ ] Subtipo (esporte, vídeo, produto, retrato, web, blender)
- [ ] Lazy loading de imagens
- [ ] Modal (click → detalhes da foto)

**Tech:**
- Image optimization (sharp, webp)
- Intersection Observer API (lazy load)
- URL params para filtros (shareable)

**Tempo:** 10-12 horas

---

### 3.3 Case Studies

**Template:**
```markdown
# Case Study: [Projeto]

## Contexto
[Brief do cliente, objetivo]

## Desafio
[Problema a resolver]

## Solução
[Abordagem técnica/criativa]

## Resultado
[KPIs, feedback, learning]

## Gallery
[Imagens do processo]

## Tools Used
[Softwares, técnicas]

## Reflection
[O que aprendeu]
```

**Meta:** 3 case studies até fim junho  
**Tópicos:**
1. Esporte: técnica de congelamento + cliente story
2. Vídeo: color grading (Pack Filmic) + cinematic process
3. Web: portfolio itself (meta, muito legal)

**Tempo:** 12-15 horas (1 por semana)

---

### 3.4 Blog Setup

**Tech:**
- [ ] MDX support (Astro MDX integration)
- [ ] Markdown files em `/src/pages/blog/`
- [ ] Auto-generate índice de posts
- [ ] Code syntax highlighting (Shiki)
- [ ] RSS feed

**Posts Q2:**
1. "Choosing a Framework: Astro vs Next.js"
2. "Core Web Vitals: Why They Matter"
3. "Color Grading Philosophy: Mantiqueira Aesthetic"
4. "Full-Stack Photography: Technique + Tech"

**Tempo:** 8-10 horas

---

## 🔍 FASE 4: OTIMIZAÇÃO & SEO (Julho)

### 4.1 SEO Checklist

- [ ] Meta tags (title, description)
- [ ] Open Graph (social previews)
- [ ] Sitemap.xml auto-gerado
- [ ] robots.txt
- [ ] Google Analytics 4 integration
- [ ] Search Console setup

**Tempo:** 2-3 horas

---

### 4.2 Performance Optimization

- [ ] Image optimization (WebP, srcset)
- [ ] CSS/JS minification
- [ ] Lighthouse audit (target: 95+)
- [ ] Mobile testing (real device)
- [ ] Network throttle testing (3G)

**Tempo:** 4-5 horas

---

## 🚀 FASE 5: DEPLOY & PUBLICAÇÃO (Fim Julho)

### 5.1 Deploy Setup

**Opção 1: Vercel** (Recomendado)
```bash
npm i -g vercel
vercel deploy
```
Pros: One-click, auto-CI/CD, analytics  
Cons: Vendor lock-in

**Opção 2: Netlify**
```bash
npm install -g netlify-cli
netlify deploy
```
Pros: Generous free tier, form handling  
Cons: Slightly slower

**Opção 3: Self-hosted**
Servidor próprio / VPS  
Pros: Total controle  
Cons: Manutenção, custo

**Recomendação:** Vercel (simplicidade + performance)

### 5.2 DNS & Domain

- [ ] Domínio registrado (namecheap? godaddy?)
- [ ] DNS apontado para Vercel/Netlify
- [ ] HTTPS ativo (automático)
- [ ] Email setup (opcional, catch-all)

---

## 📊 MÉTRICAS DE SUCESSO

| Métrica | Meta | Q2 | Q3 |
|---------|------|-----|-----|
| **Performance (Lighthouse)** | 95+ | 90 | 95 |
| **Time to First Byte** | <500ms | <800ms | <500ms |
| **Core Web Vitals** | ✅ | 🟡 | ✅ |
| **Mobile score** | 90+ | 85 | 90 |
| **Monthly visits** | — | 200 | 1k |
| **Case studies** | 3+ | 1 | 3+ |
| **Blog posts** | 10+ | 2 | 6+ |

---

## 🧠 DECISÕES TÉCNICAS DOCUMENTADAS

### Decision 1: Astro vs Next.js
**Escolha:** Astro  
**Data:** 2026-05-19  
**Reviewer:** Claude  
**Status:** Aprovada  
**Revisão:** 2026-06-15

### Decision 2: Deploy provider
**Escolha:** Vercel  
**Data:** TBD  
**Reviewer:** Casal (test experience)  
**Status:** Pending  
**Revisão:** 2026-06-15

### Decision 3: Database for dynamic content
**Escolha:** Nenhum (pure static + CMS later se precisar)  
**Data:** 2026-05-19  
**Reviewer:** Claude  
**Status:** Aprovada  
**Revisão:** 2026-07-01

---

## 📝 APRENDIZADOS DIÁRIOS

### 2026-05-19
- Decisão Astro: análise de tradeoffs completa
- MOCs melhoradas = navegação mais clara no vault
- Frontmatter padrão vai ativar automações depois

---

## 🔗 LINKS ÚTEIS

- [Astro Docs](https://docs.astro.build)
- [Tailwind CSS](https://tailwindcss.com)
- [Core Web Vitals Guide](https://web.dev/vitals/)
- [Open Graph Meta Tags](https://ogp.me/)
- [MDX Astro Integration](https://docs.astro.build/en/guides/integrations-guide/mdx/)

---

## 📞 PRÓXIMA REVISÃO

**Data:** 2026-05-26 (semanal)  
**Checklist:**
- [ ] Astro setup completo?
- [ ] Wireframes 50%?
- [ ] Algum blocker?
- [ ] Andamento realista?

---

**Criado:** 2026-05-19  
**Última atualização:** 2026-05-19  
**Responsável:** Vinicius Rafael  
**Reviewer:** Casal (testes UX)

*Documento vivo. Atualizar conforme progresso em VSCode. Decisões críticas registrar aqui.*
---
*Pai: [[_MOC-Tech]]*
