---
arquivo: plano de reorganização e extensão do vault
ler-quando: revisão de aprovação antes da execução
versão: 1.0 (proposta)
criado: 2026-04-26
status: aguardando aprovação
---

# 🔧 PLANO — Reorganização e Extensão do Vault

> **TL;DR.** Vault tem **282 notas .md + 35 canvas** distribuídos em 13 pastas top-level com dois sistemas paralelos brigando entre si (pastas legadas curadas + pastas emoji em modo content-dump). 134 notas (47%) sem frontmatter, 41 órfãs, 39 stubs em pastas ativas. Proposta: **11 áreas top-level numeradas**, fusão dos dois sistemas, plano de extensão em 4 ondas. Nada será movido até você aprovar.

---

## 1. Diagnóstico — o que está acontecendo

### 1.1 Dois sistemas paralelos que não se falam

| Sistema | Pastas | Estilo | Frontmatter? | Indexação |
|---|---|---|---|---|
| **Legado curado** (Mar/2026) | `Conteudo/`, `Fotografia/`, `Pessoal/`, `Tech/` | Curado, "Área/Tags/Status" | Não (cabeçalho manual) | `MOC — Claude × Vinícius.md` |
| **Emoji content-dump** | `📸 Fotografia/`, `📱 Conteúdo/`, `💼 Negócios/`, `💰 Finanças/`, `📚 Estudos/`, `👕 VRGS/`, `🔒 Seguro/`, `🗂️ Arquivo/` | Dump cru de notas antigas | YAML automático | Plugin Zoottelkeeper (auto-índice) |
| **Sistema separado** | `SISTEMA_IDIOMAS_Completo/` | Estrutura HUB com templates | Sim | `00_HUB/IDIOMAS-HUB-Central.md` |

**Conflito real:** o `MOC — Claude × Vinícius.md` lista 22 notas que vivem nas pastas legadas, mas o `_Index_of_ponto 000.md` (autogerado pelo Zoottelkeeper) só vê as pastas emoji. **Os dois mapas mentais nunca se cruzam.** Um operador que abre o vault hoje vê 13 pastas e não sabe qual é a fonte da verdade.

### 1.2 O bootstrap (`INSTRUÇÕES-INICIAIS.md`) declara 6 módulos que não existem

O bootstrap diz que o vault é organizado em: 📸 FOTOGRAFIA, 💻 CODIFICAÇÃO + IA, 📱 REDES SOCIAIS, 🌐 SITE FOTOGRAFIA VINÍCIUS, 📂 ORGANIZAÇÃO DE ARQUIVOS, 💡 PROJETOS E IDEIAS.

**Realidade:** apenas FOTOGRAFIA e algo parecido com REDES SOCIAIS existem como pasta. SITE, ORGANIZAÇÃO DE ARQUIVOS e PROJETOS E IDEIAS não têm pasta nenhuma. O conteúdo desses módulos está espalhado em `Tech/`, `Fotografia/Site de Portfólio.md` e arquivos soltos no root.

### 1.3 Saúde geral

- **282 notas** em 13 pastas top-level
- **134 notas (47%) sem frontmatter** — quebra a regra do bootstrap (item 5)
- **41 notas órfãs** (zero links bidirecionais entrantes)
- **39 notas curtas (<600 bytes) em pastas ativas** — stubs com potencial de expansão
- **26 notas micro (<200 bytes) no Arquivo** — dia-a-dia datado, fragmentos, candidatos a consolidar/deletar
- **`PROJETOS-ATIVOS.md`** quase 100% `[a definir]` — dashboard sem dados não orienta nada

---

## 2. Taxonomia proposta — 11 áreas, prefixo numérico

Mesmo número de pastas top-level que hoje (11 vs 13), porém **sem duplicação**, com prefixo numérico pra ordenação consistente, e cada área com sub-pastas semânticas em vez de dump plano.

```
ponto 000/
├── 📋 00 — SISTEMA
│   ├── INSTRUÇÕES-INICIAIS.md             [movido do root]
│   ├── PROJETOS-ATIVOS.md                 [movido do root, preenchido]
│   ├── _MOC-Vault.md                      [novo — fusão dos 2 MOCs]
│   ├── VINICIUS — Meu universo.md         [movido do root]
│   ├── PLANEJAMENTO — Direções.md         [movido do root]
│   └── Templates/
│       ├── Template-Nota-Padrão.md
│       ├── Template-Briefing-Evento.md
│       └── Template-Resenha-Livro.md
│
├── 📸 01 — FOTOGRAFIA
│   ├── _MOC-Fotografia.md                 [novo]
│   ├── Arte/                              [estética, linguagem, projetos]
│   │   ├── FOTO - Arte.md
│   │   ├── A LINGUAGEM FOTOGRÁFICA.canvas
│   │   ├── Fotografia e estética.canvas
│   │   ├── PROJETO OLHAR.md
│   │   └── ...
│   ├── Técnica/                           [equipamento, configurações]
│   │   ├── FOTO - Técnica.md
│   │   ├── LISTA DE EQUIPAMENTOS.md
│   │   ├── METAS DE EQUIPAMENTOS.md
│   │   ├── NIKON.md / LENTE 105MM.md
│   │   ├── Lightroom Classic.md           [vindo de Tech/]
│   │   └── ...
│   ├── História/                          [200 anos de fotografia]
│   │   ├── HISTÓRIA DA FOTOGRAFIA - 200 anos.md
│   │   ├── Era Pré-Fotográfica.md
│   │   ├── Era da Fotografia Química.md
│   │   ├── Era da Fotografia Moderna.md
│   │   ├── Era da Fotografia Digital.md
│   │   ├── Era da Fotografia Contemporânea.md
│   │   ├── Heliografia de Niépce.md
│   │   └── Glossário Completo.md
│   ├── Negócio/                           [clientes, portfólio, plataformas]
│   │   ├── FOTO - Negócio.md
│   │   ├── CLIENTES E ORÇAMENTOS.md
│   │   ├── PORTFÓLIO FOTOGRÁFICO.md
│   │   ├── Plano de Renda e Negócio.md   [vindo de Fotografia/]
│   │   ├── Plataformas Freelance.md      [vindo de Fotografia/]
│   │   ├── Concursos e Visibilidade.md   [vindo de Fotografia/]
│   │   ├── Eventos e Calendário.md       [vindo de Fotografia/]
│   │   └── Serviço de Edição com IA.md   [vindo de Fotografia/]
│   ├── Coberturas/                        [novo — briefings por tipo]
│   │   ├── Casamentos/
│   │   ├── Esportes-Vôlei/
│   │   ├── Paisagem-Mantiqueira/
│   │   └── Rua/
│   └── Fotos-DSC/                         [📷 Fotos DSC atual]
│
├── 📱 02 — REDES & CONTEÚDO
│   ├── _MOC-Redes.md                      [novo]
│   ├── Estratégia/
│   │   ├── PRESENÇA DIGITAL - Hub Central.md
│   │   ├── CRIATIVIDADE.md
│   │   └── Calendário-Editorial.md       [novo, fundindo Calendário de Conteúdo]
│   ├── Instagram/
│   │   ├── INSTAGRAM - Minha vitrine visual.md
│   │   ├── ESTRATEGIAS DE ENGAJAMENTO.md
│   │   ├── HASGTAGS.md → Hashtags.md     [renomear typo]
│   │   ├── HORÁRIOS DE ALTO ENGAJAMENTO.md
│   │   ├── MUSICAS VIRAIS.md
│   │   ├── PROGRAMAÇÃO DE PUBLICAÇÕES.md
│   │   ├── RETENÇÃO.md
│   │   ├── TRENDS E TENDENCIAS DO MOMENTO.md
│   │   ├── Instagram e Estratégia de Conteúdo.md  [vindo de Fotografia/]
│   │   └── (canvas existentes)
│   ├── YouTube/
│   │   ├── YOUTUBE - Meu canal de vídeos.md
│   │   ├── YT - Análise de Concorrência.md
│   │   ├── YT - Crescimento e Comunidade.md
│   │   ├── YT - Edição e Pós-Produção.md
│   │   ├── YT - Monetização e Parcerias.md
│   │   ├── YT - Roteiros e Storytelling.md
│   │   ├── YT - SEO e Algoritmo.md
│   │   ├── YT - Séries e Formatos Recorrentes.md
│   │   ├── YT - Thumbnails e Design.md
│   │   ├── IDEIAS DE VIDEO.md
│   │   └── YouTube.md                    [vindo de Conteudo/]
│   └── Áudio-Vídeo/
│       ├── AUDIO.md
│       ├── VIDEO.md
│       ├── Street Photography.md         [vindo de Conteudo/]
│       └── Prompts de IA para Imagens.md [vindo de Conteudo/]
│
├── 💼 03 — NEGÓCIOS & MARCA
│   ├── _MOC-Negocios.md                   [novo]
│   ├── Framework-15-Passos/
│   │   ├── 01 - Personal Branding.md
│   │   ├── 02 - Construção da Imagem.md
│   │   └── ... (até 15)
│   ├── Tráfego/
│   │   ├── TRAFEGO ORGANICO.md
│   │   ├── TRAFEGO PAGO.md
│   │   ├── ANUNCIOS.md
│   │   ├── CRIATIVOS (ANUNCIOS).md
│   │   ├── PLANEJAMENTO DE ANUNCIOS (CRIATIVOS).md
│   │   └── REMARKETING.md → Remarketing.md [renomear typo]
│   ├── Pipeline/
│   │   ├── LEADS.md
│   │   ├── FUNIL.md
│   │   ├── COPY.md
│   │   ├── ROI.md
│   │   └── Calendário de Conteúdo.md
│   ├── Marca-Pessoal/
│   │   ├── Meu Perfil.md
│   │   ├── Logo e Identidade Visual.md   [vindo de Fotografia/]
│   │   ├── Analisando a concorrência.md
│   │   ├── ENTENDIMENTOS DO CONSUMO.md
│   │   ├── LINGUAGEM DO MERCADO.md
│   │   └── INFLUENCIADORES VIRTUAIS - Framework de Criação.md
│   ├── Produtos-Digitais/
│   │   ├── PRODUTO DIGITAL - Presets e Cursos.md
│   │   ├── Pack-Filmic-Mantiqueira.md     [novo, hub do produto principal]
│   │   └── Banco de Ideias.md
│   └── Recursos/
│       ├── Biblioteca de Recursos.md
│       ├── Ideas Extraordinárias - Monetização e Escala.md
│       └── Roteiro de Estudos.md
│
├── 💰 04 — FINANÇAS
│   ├── _MOC-Financas.md                   [novo]
│   ├── Pessoal/
│   │   ├── DINHEIRO (CONTROLE DE GASTOS).md
│   │   ├── gastos mensais fixos.md
│   │   ├── Planejamento Financeiro.md
│   │   ├── RESERVAS.md
│   │   ├── Finanças e Metas de Renda.md  [vindo de Pessoal/]
│   │   └── FINANCEIRO - Dinheiro e metas.md
│   ├── Investimentos/
│   │   ├── AÇÕES.md
│   │   ├── CRYPTO.md
│   │   ├── RENDA FIXA.md
│   │   ├── TRADE.md
│   │   ├── SPREAD.md
│   │   └── LOW TICKT.md → Low-Ticket.md  [renomear typo]
│   ├── Educação-Financeira/
│   │   ├── ESTUDOS DE FINANÇAS..md
│   │   ├── FORMAS DE AUMENTAR O DINHEIRO.md
│   │   └── 11 - Gestão Financeira.md     [referência cruzada com Negócios]
│   └── (canvas existentes — FINANCEIRO PESSOAL.canvas etc)
│
├── 📚 05 — ESTUDOS
│   ├── _MOC-Estudos.md                    [novo]
│   ├── ENEM-2026/
│   │   ├── _Plano-27-Semanas.md           [novo, baseado em PROJETOS-ATIVOS]
│   │   ├── Linguagens/  (ENEM - LING - *)
│   │   ├── Humanas/     (ENEM - HUM - *)
│   │   ├── Matemática/  (ENEM - MAT - *)
│   │   ├── Natureza/    (ENEM - NAT - *)
│   │   ├── Redação/
│   │   └── Preparação-Geral/
│   ├── ANHANGUERA/
│   │   ├── Estética e História da Arte/
│   │   │   └── (UNIDADE 1-4, AULA 2-3)
│   │   ├── Empreendedorismo e Inovação/
│   │   │   └── (UNIDADE 1-4)
│   │   └── Educação — UNIVAP FATEC ENEM.md  [vindo de Pessoal/]
│   ├── Idiomas/                           [substitui SISTEMA_IDIOMAS_Completo]
│   │   ├── _IDIOMAS-HUB.md
│   │   ├── Espanhol/
│   │   ├── Russo/
│   │   ├── Outros/
│   │   ├── Recursos/
│   │   └── Templates/
│   ├── Leitura/
│   │   ├── LEITURA - Livros e conhecimento.md
│   │   ├── LIDOS Q.md → Livros-Lidos.md
│   │   ├── NÃO LIDOS.md → Livros-Para-Ler.md
│   │   └── Resenhas/
│   │       ├── O HOMEM MAIS RICO DA BABILONIA.md
│   │       ├── O ATO CRIATIVO UMA FORMA DE SER.md
│   │       ├── O PODER DA AUTO RESPONSABILIDADE.md
│   │       ├── NADA PODE ME FERIR.md
│   │       ├── FRAGMENTOS (PAULO ROBERTO DA SILVA).md
│   │       ├── O RICO TEM PENSAMENTO INDEPENDENTE.md
│   │       └── CONHECIMENTO QUE CONDUZ A VIDA ETERNA.md
│   └── Geral/
│       ├── ESTUDOS DIRECIONAIS.md
│       ├── ESTUDOS E CURSOS - Meu aprendizado.md
│       └── POEMAS & TEXTOS.md
│
├── 👕 06 — VRGS
│   ├── _MOC-VRGS.md                       [novo]
│   ├── Estratégia/
│   │   ├── LOJA VRGS - E-commerce de roupas.md
│   │   ├── LOJA DE ROUPAS.md
│   │   ├── MINHA LOJA DE ROUPAS.md       [merge com LOJA DE ROUPAS]
│   │   └── VRGS - Estrategia Instagram 2026.canvas
│   ├── Catálogo/
│   │   ├── CAMISAS.md / CAMISETAS.md / BLUSAS.md / REGATAS.md
│   │   ├── BAGS.md / SAPATOS.md
│   │   ├── ACESSORIOS BRINCOS, PRATA, PULSEIRAS E COLAR.md
│   │   ├── TOCAS , BONES.md → Tocas-e-Bonés.md
│   │   └── BRINDES.md
│   ├── Crochê/
│   │   ├── CROCHE.md / CROCHE, COMO COMECEI..md
│   │   └── TIPOS DE ROUPAS E ACESSORIOS DE CROCHE.md
│   └── Design/
│       ├── DESENHO.md
│       ├── desing.md → Design.md          [renomear typo]
│       └── PREÇOS DOS PRODUTOS VRGS.canvas
│
├── 💻 07 — TECH & SISTEMAS
│   ├── _MOC-Tech.md                       [novo]
│   ├── IA/
│   │   ├── MCP e Automação.md             [vindo de Tech/]
│   │   ├── GitHub e Claude Code.md        [vindo de Tech/]
│   │   └── Prompt-Engineering.md          [novo, hub]
│   ├── Ferramentas/
│   │   ├── VS Code.md                     [vindo de Tech/]
│   │   ├── Adobe — Erros e Suporte.md     [vindo de Tech/]
│   │   ├── LIGHTROOM.md → Lightroom-Notas-Rápidas.md  [⚠️ NÃO confundir com Lightroom Classic.md de Fotografia/Técnica/]
│   │   └── PHOTOSHOOP.md → Photoshop.md   [vindo de Arquivo/, renomear]
│   ├── Automação/
│   │   ├── PowerShell e Organização de Arquivos.md  [vindo de Tech/]
│   │   ├── COMO ME ORGANIZO.md            [vindo de 📸 Fotografia/]
│   │   └── ORGANIZAÇÃO-DE-ARQUIVOS-Hub.md [novo, módulo do bootstrap]
│   ├── Vault/
│   │   ├── Obsidian Vault — DEUS-DO-OBSIDIAN.md  [vindo de Tech/]
│   │   └── (decisões e roadmap do próprio vault)
│   └── Site/                              [módulo SITE FOTOGRAFIA VINÍCIUS do bootstrap]
│       ├── _MOC-Site.md                   [novo]
│       ├── Site de Portfólio.md           [vindo de Fotografia/]
│       ├── Decisões-Stack.md              [novo]
│       ├── Roadmap-Features.md            [novo]
│       ├── SEO-Copy.md                    [novo]
│       └── Bugs-Conhecidos.md             [novo]
│
├── 🙋 08 — PESSOAL
│   ├── _MOC-Pessoal.md                    [novo]
│   ├── Identidade/
│   │   ├── Identidade e Preferências.md   [vindo de Pessoal/]
│   │   └── QUEM SOU EU.md                 [vindo de Arquivo/, recuperar]
│   ├── Mobilidade/
│   │   └── CNH, Moto e Mobilidade.md      [vindo de Pessoal/]
│   ├── Hábitos-Rotina/
│   │   ├── HABITOS.md                     [vindo de Arquivo/, expandir]
│   │   └── ROTINA.md                      [vindo de Arquivo/, expandir]
│   └── Reflexões/
│       ├── A GRANDE CONTROVERSA.md
│       └── (textos pessoais curtos com valor — selecionar caso a caso)
│
├── 🗂️ 09 — ARQUIVO
│   ├── _MOC-Arquivo.md                    [novo, com critérios]
│   ├── 2025/                              [notas datadas: 2025-05-20.md, 2025-07-31.md, 31.08.2025.md]
│   ├── Projetos-Pausados/
│   │   ├── HORTA.md / PLANEJAMENTO DA HORTA.md
│   │   ├── PEOJETO MY LOVE.md → Projeto-MY-LOVE.md
│   │   ├── JIU-JITSU, 1 TREINO COMIGO.md
│   │   └── DIRETO DE CUBA.md
│   ├── Originais-Fragmentos/
│   │   ├── PENDÊNCIAS.md / LISTA DE A FAZERES.md / ORGANIZAÇÕA URGÊNCIA.md
│   │   └── (consolidar em uma única nota e descartar duplicatas)
│   └── Diário-Solto/                      [notas micro <100b: candidatas a deletar]
│
└── 🔒 10 — SEGURO
    └── senhas perfis.md
```

> **Por que prefixo numérico:** o Obsidian ordena alfabeticamente. Sem prefixo, ano novo `🗂️` viria depois de `🙋` mas antes de `🔒`. Com `00`–`10`, a ordem reflete prioridade real e bate com o `INSTRUÇÕES-INICIAIS.md` (sistema primeiro, arquivo no fim).

---

## 3. Plano de migração — destino de cada pasta atual

| Pasta atual | Status | Destino | Ação |
|---|---|---|---|
| `Conteudo/` (3) | legado | `📱 02 — REDES & CONTEÚDO/` | Mesclar em sub-pastas correspondentes |
| `Fotografia/` (8) | legado | `📸 01 — FOTOGRAFIA/Negócio/` (maioria) e `📱 02 — REDES.../Instagram/` (uma) | Mesclar |
| `Pessoal/` (4) | legado | Espalhado: `🙋 08`, `📚 05`, `💰 04` | Distribuir |
| `Tech/` (7) | legado | `💻 07 — TECH & SISTEMAS/` | Mesclar com sub-pastas |
| `SISTEMA_IDIOMAS_Completo/` (13) | sistema separado | `📚 05 — ESTUDOS/Idiomas/` | Mover inteiro renomeando estrutura |
| `📸 Fotografia/` (50) | emoji | `📸 01 — FOTOGRAFIA/` | Distribuir entre Arte / Técnica / História / Negócio |
| `📱 Conteúdo/` (28) | emoji | `📱 02 — REDES & CONTEÚDO/` | Distribuir entre Estratégia / Instagram / YouTube / Áudio-Vídeo |
| `💼 Negócios/` (38) | emoji | `💼 03 — NEGÓCIOS & MARCA/` | Distribuir entre Framework / Tráfego / Pipeline / Marca / Produtos / Recursos |
| `💰 Finanças/` (14) | emoji | `💰 04 — FINANÇAS/` | Distribuir entre Pessoal / Investimentos / Educação |
| `📚 Estudos/` (60) | emoji | `📚 05 — ESTUDOS/` | Reorganizar ENEM por área, separar Resenhas |
| `👕 VRGS/` (18) | emoji | `👕 06 — VRGS/` | Distribuir entre Estratégia / Catálogo / Crochê / Design |
| `🔒 Seguro/` (2) | emoji | `🔒 10 — SEGURO/` | Renomear pasta |
| `🗂️ Arquivo/` (31) | emoji | `🗂️ 09 — ARQUIVO/` | Sub-organizar em 2025 / Projetos-Pausados / Fragmentos / Diário |
| `copilot/`, `.makemd/`, `.smart-env/`, `.space/` | meta | manter como estão | Plugins do Obsidian, não tocar |

**Conflitos detectados zero:** confirmei via `comm` que `Fotografia/` vs `📸 Fotografia/` e `Conteudo/` vs `📱 Conteúdo/` **não têm nomes de arquivo iguais**. Logo, não vai sobrescrever nada na fusão.

**Renomeações (typos):** `HASGTAGS` → `Hashtags`, `LOW TICKT` → `Low-Ticket`, `REMARKETING` → `Remarketing`, `desing` → `Design`, `LIGHTROOM` → `Lightroom-Notas-Rápidas`, `PHOTOSHOOP` → `Photoshop`, `PEOJETO` → `Projeto`.

**⚠️ Conflito de nome semelhante:** `Lightroom Classic.md` (de Tech/, curado, robusto) vs `LIGHTROOM.md` (do 📸 Fotografia/, dump curto). **Manter os dois, em pastas diferentes**, com nomes claros: o curado vai pra `Fotografia/Técnica/Lightroom-Classic.md`, o dump vai pra `Tech/Ferramentas/Lightroom-Notas-Rápidas.md`.

---

## 4. Plano de extensão — 4 ondas

Em ordem de retorno-sobre-esforço. Cada onda tem critério claro de "feito".

### 🌊 Onda 1 — Fundação (preencher o que está vazio)

**Objetivo:** Tirar o vault da ficção. Hoje os dois arquivos mais importantes (`PROJETOS-ATIVOS.md` e o futuro `_MOC-Vault.md`) estão vazios ou inconsistentes.

| Tarefa | Como |
|---|---|
| Preencher `PROJETOS-ATIVOS.md` | Sessão de 30 min comigo: você fala o que tá rolando, eu estruturo no formato existente. Foco da semana, eventos contratados, entregas, projetos longos, ENEM (semana atual?), bloqueios. |
| Criar `_MOC-Vault.md` central | Fundir `MOC — Claude × Vinícius.md` + `_Index_of_ponto 000.md` + `VINICIUS — Meu universo.md` num MOC único e atualizado, com links pros 11 _MOCs de área. |
| Criar 11 `_MOC-{Área}.md` | Um MOC por área top-level, listando notas-chave, sub-pastas e linking pro MOC central. |
| Padronizar frontmatter nas 134 notas que não têm | Script Python que adiciona o YAML mínimo (created, módulo, tags, status) com inferência baseada na pasta. Você revisa por amostragem. |

**Entregável da Onda 1:** dashboard `PROJETOS-ATIVOS` real + 12 MOCs (1 vault + 11 áreas) + 100% das notas com frontmatter.

### 🌊 Onda 2 — Conectar órfãs (41 notas perdidas)

**Objetivo:** Toda nota tem ao menos 1 link bidirecional. Notas órfãs viram nó morto no grafo.

Top 10 órfãs com maior potencial de conexão:

| Nota órfã | Conectar a | Tipo de link |
|---|---|---|
| `INFLUENCIADORES VIRTUAIS - Framework de Criação.md` | `08 - Produtos Digitais.md`, `Pack-Filmic-Mantiqueira.md` | filho-de |
| `Meu Perfil.md` | `_MOC-Negocios.md`, `01 - Personal Branding.md`, `Identidade e Preferências.md` | irmão-de |
| `CPU.md` (em Estudos) | `ENEM - NAT - Eletricidade.md` ou mover pra `💻 Tech` | reclassificar |
| `Analise.md` (em Estudos) | sem contexto claro — pedir leitura sua | requer triagem |
| `Coloque suas ideas para fora.md` | `CRIATIVIDADE.md`, `Banco de Ideias.md` | irmão-de |
| `ENSAIO FOTOGRAFICO AO INVES DE FESTA.md` | `FOTO - Negócio.md`, `CLIENTES E ORÇAMENTOS.md` | exemplo-de |
| `PADDING PRETO e BRANCO.md` | `FOTO - Técnica.md`, `Glossário Completo.md` | técnica-de |
| `O RICO TEM PENSAMENTO INDEPENDENTE..md` | `Resenhas/`, `Educação-Financeira/` | resenha-de |
| `Templates/IDI-*` | `_IDIOMAS-HUB.md` | template-de |
| `senhas perfis.md` | (mantém isolada por razão óbvia) | OK assim |

**Entregável da Onda 2:** órfãs ≤ 10 (apenas as legitimamente isoladas, ex.: senhas, templates).

### 🌊 Onda 3 — Expandir stubs (39 notas curtas em pastas ativas)

Priorizo as que **alimentam projetos ativos** (PROJETOS-ATIVOS.md, Pack Filmic Mantiqueira, ENEM, Instagram).

**Top 12 stubs pra expandir** (em ordem de prioridade):

1. `📱 Conteúdo/Instagram/HORÁRIOS DE ALTO ENGAJAMENTO.md` (43b) → expandir com dados reais, melhores horários para foto/Mantiqueira, fonte
2. `📱 Conteúdo/Instagram/ESTRATEGIAS DE ENGAJAMENTO.md` (214b) → playbook de 5–7 estratégias testadas
3. `📱 Conteúdo/Instagram/RETENÇÃO.md` (234b) → técnicas de hook, cortes, ritmo
4. `📱 Conteúdo/Instagram/HASGTAGS.md` (137b, renomear) → 3 sets de hashtags por nicho (paisagem, casamento, vôlei)
5. `📱 Conteúdo/Instagram/MUSICAS VIRAIS.md` (111b) → processo de descoberta + biblioteca atual
6. `📚 Estudos/ANHANGUERA/UNIDADE 1–4 (todas)` (37–339b) → resumo + flashcards de cada unidade
7. `📸 Fotografia/CRIATIVO.md` (67b) → o que é seu criativo, exemplos, série em produção
8. `📸 Fotografia/ENSAIO FOTOGRAFICO AO INVES DE FESTA.md` (147b) → pacote/preço/pitch pra clientes
9. `📸 Fotografia/Fotografia.md` (93b) → mover ou deletar (overlap com FOTO - Arte/Técnica/Negócio)
10. `📚 Estudos/Estudos.md` (173b) → idem, possível MOC de Estudos
11. `📱 Conteúdo/Instagram/PROGRAMAÇÃO DE PUBLICAÇÕES.md` (104b) → template + janela atual
12. `📸 Fotografia/TECNOLOGO FOTOGRAFIA.md` (179b) → seu plano de formação (se for projeto ativo)

**Critério de "expandida":** mínimo 1500 caracteres, com seções claras e ao menos 2 links bidirecionais.

### 🌊 Onda 4 — Limpar arquivo (26 micro-notas <200b)

A maioria são fragmentos diários sem contexto. Proposta:

| Nota | Decisão sugerida |
|---|---|
| `Daguerreótipo.md` (0b — vazio) | Deletar |
| `2025-05-20.md`, `2025-07-31.md`, `31.08.2025.md`, `2025-08-31.md` | Consolidar em `Diário-2025.md` se o conteúdo for relevante; senão deletar |
| `HABITOS.md`, `ROTINA.md` (49–65b) | Mover pra `🙋 Pessoal/Hábitos-Rotina/` e expandir na Onda 3 |
| `JIU-JITSU, 1 TREINO COMIGO.md` (49b) | Deletar (memória solta, sem projeto ativo) |
| `TRABALHE, TREINE, FOQUE...md` (49b), `MODELE A CONCORRÊNCIA E FAÇA MELHOR.md` | Frase motivacional — deletar ou consolidar em `Reflexões/` |
| `FIM DA ESCOLA INICIO DOS MEUS PLANOS.md`, `000 - Um novo Eu...md`, `SUMI POR ALGUNS MESES, OQUE MUDOU....md` | Marco pessoal — manter em `🙋 Pessoal/Reflexões/` |
| `PHOTOSHOOP.md` | Renomear, mover pra `💻 Tech/Ferramentas/Photoshop.md`, expandir |
| `HORTA.md` + `PLANEJAMENTO DA HORTA.md` | Manter em `Projetos-Pausados/` (decisão clara: pausado, não morto) |
| `PEOJETO MY LOVE.md` | Pedir contexto — não dá pra decidir cego |
| `PENDÊNCIAS.md`, `LISTA DE A FAZERES.md`, `ORGANIZAÇÕA URGÊNCIA.md` | Migrar conteúdo ativo pro `PROJETOS-ATIVOS.md` e arquivar originais |

---

## 5. Decisões pendentes — preciso de você

Antes de executar, 5 decisões que mudam o desenho:

1. **Loja VRGS é prioridade ativa ou pausada?** O bootstrap não menciona, mas tem 18 notas. Se pausada, viraria sub-pasta dentro de `💼 Negócios/Projetos-Pausados/`. Se ativa, fica como `06 — VRGS` top-level. *(estou propondo ativa por default).*

2. **Idiomas merecem destaque ou ficam dentro de Estudos?** Você tem um sistema completo (HUB + Espanhol + Russo + Outros + Recursos + Templates). Top-level `🌐 06 — IDIOMAS` ou sub-pasta de Estudos? *(estou propondo sub-pasta).*

3. **`MOC — Claude × Vinícius.md` vs `VINICIUS — Meu universo.md` vs `_MOC-Vault.md` novo:** dá pra fundir os 3 num só? Ou cada um tem propósito específico? *(proposta: `_MOC-Vault.md` como índice operacional do vault, `VINICIUS — Meu universo.md` como manifesto pessoal — mantém os dois mas cada um tem papel claro).*

4. **Plugin Zoottelkeeper:** ele autogerou os `_Index_of_*.md` em cada pasta. Quer manter (atualiza sozinho mas polui o grafo) ou desativar e usar só os MOCs manuais que vou criar? *(proposta: desativar e usar MOCs manuais — você ganha controle, perde automação).*

5. **Pasta `📷 Fotos DSC/` em `📸 Fotografia/`:** isso parece ser pasta de imagens cruas (binários), não notas. Confirma? Mantenho fora do escopo de organização semântica.

---

## 6. Como vai ser a execução (depois de aprovar)

Em fases, com check-ins. Cada fase você revisa antes da próxima.

| Fase | Duração estimada | Reversível? |
|---|---|---|
| F1 — Criar nova estrutura de pastas vazia | 5 min | sim (rmdir) |
| F2 — Mover arquivos (sem deletar nada) | 30 min | sim (git checkout) |
| F3 — Padronizar frontmatter | 20 min | sim (git checkout) |
| F4 — Criar 12 MOCs | 1h | adicionar nada destrutivo |
| F5 — Onda 2 (conectar órfãs) | 1h | só adiciona links |
| F6 — Onda 3 (expandir stubs) | sessões de 30 min cada | só adiciona conteúdo |
| F7 — Onda 4 (limpar arquivo) | 30 min | confirmar cada delete |

**Vault tem `.git`** — vou commitar antes de cada fase. Se algo der errado, `git reset --hard` resolve.

---

## 7. O que NÃO vou fazer sem você mandar

- Deletar qualquer nota (mesmo as 0 bytes)
- Mexer em `.obsidian/`, `.makemd/`, `.smart-env/`, `.space/` (configs do Obsidian)
- Mover arquivos `.canvas` (você desenhou esses — pode ter contexto mental que não tô vendo)
- Tocar no `copilot/` (parece ser dump de conversas com IA)
- Mexer em `obsidian-mcp-server/` se eu encontrar (referenciado no `_Index_of_ponto 000.md` mas não vi)
- Reescrever notas grandes existentes (>2000b) que já têm conteúdo curado

---

## ✅ O que preciso de você agora

Responde os 5 pontos da seção 5 e me diz:

- **Aprovado todo, executa em fases?**
- **Aprovado com mudanças (quais)?**
- **Reprovado (refaz como)?**

Quando aprovar, começo pela F1 (criar estrutura vazia). Vou commitar cada fase no git pra você ter checkpoints.

---

*Plano gerado em 2026-04-26 a partir de varredura completa de 282 notas + 35 canvas. Investigação detalhada disponível nos logs da sessão se quiser auditar.*

