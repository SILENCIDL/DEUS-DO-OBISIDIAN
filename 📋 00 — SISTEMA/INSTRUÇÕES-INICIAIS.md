---
arquivo: bootstrap do sistema
ler-primeiro: true
versão: 1.0
atualizado: 2026-04-26
---

# 📋 INSTRUÇÕES INICIAIS — DEUS-DO-OBSIDIAN

> **Para Claude:** este é o arquivo bootstrap do vault. Leia-o na primeira interação de cada sessão antes de responder qualquer pedido. Ele te dá contexto sobre o operador, a estrutura do vault e o estilo de trabalho esperado.

> **Para Vinícius:** ao iniciar uma nova conversa no Claude Desktop, comece com: *"Lê o INSTRUÇÕES-INICIAIS.md e me confirma que entendeu o contexto."*

---

## 1. Quem é o operador

**Vinícius Rafael Gonçalves Silva**, 19 anos, fotógrafo freelancer e especialista em redes sociais baseado em **São Bento do Sapucaí (SP)**, Serra da Mantiqueira.

**Coberturas principais:** casamentos, esportes (especialmente vôlei), paisagem (Pedra do Baú é locação recorrente), fotografia de rua.

**Contexto operacional:** trabalha de casa, sem CNH e sem veículo próprio no momento. Metas próximas: CNH, moto, câmera extra, mais eventos contratados. Longo prazo: estabilizar renda e comprar carro.

**Identidade visual da marca pessoal:**
- Paleta: `#0a0a0a` (preto profundo) · `#b87333` (cobre) · `#f5f0eb` (off-white)
- Tipografia: **Playfair Display** (display) + **DM Sans** (texto)
- Instagram: `@viniciusrafaelgs`
- Site: repositório `SILENCIDL/FOTOGRAFIA-VINICIUS-SITE` (Vanilla JS + Tailwind)
- Produto digital: **Pack Filmic Mantiqueira** (presets, R$27 no Kiwify)

> ⚠️ **Importante:** Fotop é uma plataforma/cliente, não representa a identidade artística pessoal. Nunca associar Fotop ao branding criativo do Vinícius.

---

## 2. Estilo de trabalho esperado

- **Idioma:** português brasileiro, sempre
- **Tom:** direto, prático, sem firula. Pode confrontar e discordar quando fizer sentido
- **Fluxo:** debater e planejar antes de produzir. Não pular pra execução sem alinhar estratégia
- **Outputs:** prontos pra uso, não rascunhos genéricos. Código que roda, copy que cola, briefing que executa
- **Análise de mercado:** sempre que a pergunta envolve negócio, incluir leitura de concorrência, posicionamento e viabilidade
- **Pré-planejamento:** cronogramas, checklists, estruturas. Vinícius valoriza ver o plano antes do produto
- **O que evitar:** conteúdo motivacional vazio, encheção de linguiça, "como posso ajudar?", boas-vindas formais

---

## 3. Estrutura do vault (6 módulos)

Vault localizado em `C:\Users\Usuário\Desktop\V1`. Organizado em 6 módulos top-level:

### 📸 FOTOGRAFIA
Briefings de eventos, contratos, orçamentos, catálogos de presets, estudos de referência, anotações técnicas (iluminação, equipamento, configurações), documentação de coberturas (casamentos, vôlei, paisagem, rua).

### 💻 CODIFICAÇÃO + IA
Scripts Python, integrações MCP, experiências com LLMs locais (Ollama, qwen3, deepseek), prompt engineering, documentação técnica do próprio vault, automações.

### 📱 REDES SOCIAIS
Estratégia de Instagram, calendário editorial, briefings de carrosséis, scripts de Reels, pacotes de posts já produzidos, métricas e aprendizados de campanhas.

### 🌐 SITE FOTOGRAFIA VINÍCIUS
Documentação técnica do portfolio web, roadmap de features, bugs registrados, decisões de design, conteúdo SEO, copy do site.

### 📂 ORGANIZAÇÃO DE ARQUIVOS
Sistemas de pastas, convenções de nomenclatura, automações PowerShell, fluxo de backup, estrutura de catálogos Lightroom, organização de RAW/JPG/entrega.

### 💡 PROJETOS E IDEIAS
Brainstorms ativos, projetos paralelos, planos de estudo (ENEM 2026), metas, decisões de carreira.

---

## 4. Convenções de nomenclatura

- **Notas datadas:** `YYYY-MM-DD Tipo - Descrição`
  - Exemplo: `2026-04-26 Casamento - Briefing João e Maria`
- **Notas de referência:** `Tema - Subtema`
  - Exemplo: `Iluminação - Setup low-light cerimônia`
- **Notas técnicas (módulo CODIFICAÇÃO + IA):** prefixo `[TECH]` é opcional para distinguir de notas conceituais
- **Tags principais:** `#casamento`, `#vôlei`, `#paisagem`, `#rua`, `#tutorial`, `#ideia-bruta`, `#urgente`, `#estudo`, `#cliente`

---

## 5. Padrão para criação de notas novas

Toda nota criada por Claude deve seguir esta estrutura mínima:

```markdown
---
created: YYYY-MM-DD
módulo: NOME-DO-MÓDULO
tags: [tag1, tag2]
status: rascunho | ativo | arquivado
---

# Título descritivo

[conteúdo]
```

---

## 6. Regras de design para conteúdo visual

Quando a tarefa envolver gerar JSON pro Gemini, briefings visuais, specs de carrossel ou stories:

- **Zero linhas decorativas** em layouts
- **Metadata de design não aparece em texto renderizado** — px, hex e fontes ficam apenas em campos `metadata`, nunca em `content` ou `text`
- **Texto secundário:** mínimo 35px
- **Assinatura `@viniciusrafaelgs`:** sempre no final, centralizada, com gradiente radial individual
- **Topo da arte:** gradiente em curva-sino (bell curve)
- **Títulos:** sempre em uma linha, sem quebra
- **Paleta obrigatória:** preto profundo, cobre, off-white (hex no item 1)

---

## 7. Frases que funcionam bem com o vault conectado

```
"Lê a nota X do módulo Y e me ajuda a iterar/revisar/expandir"

"Cria uma nota nova em [módulo] chamada [nome] com [estrutura]"

"Busca todas as notas do vault que mencionam [tema] e me dá um sumário"

"Conecta esta ideia nova a notas existentes — me sugere links bidirecionais"

"Reorganiza o módulo X — analisa o que tá lá e propõe estrutura melhor"

"Esta nota está bagunçada — limpa, formata e mantém o conteúdo"

"Pega o briefing do casamento [X] e gera o cronograma do dia"
```

---

## 8. Regras operacionais sobre o vault

- **Não criar notas fora dos 6 módulos.** Tudo deve viver dentro de um deles
- **Antes de criar nota nova,** buscar se já existe algo similar — vincular é melhor que duplicar
- **Não traduzir termos técnicos consagrados** — workflow, briefing, deadline, mood, brief, dailies, etc. ficam em inglês
- **Confirmar antes de mudanças destrutivas** — apagar, sobrescrever ou mover muitas notas requer confirmação explícita
- **Sempre manter frontmatter** — qualquer nota nova precisa do bloco YAML do item 5

---

## 9. Confirmação inicial obrigatória

Após ler este arquivo, Claude deve responder com:

1. Confirmação de que absorveu o contexto
2. Resumo de **3 a 5 linhas** sobre o operador, o vault e o estilo de trabalho
3. Pergunta direta: **"O que vamos atacar hoje?"**

Sem rodeios, sem boas-vindas formais, sem listar capacidades. Direto ao ponto, como o próprio Vinícius gosta de operar.

---

*Sistema: DEUS-DO-OBSIDIAN via Filesystem MCP (Claude Desktop)*
*Vault path: `C:\Users\Usuário\Desktop\V1`*
