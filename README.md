# DEUS-DO-OBISIDIAN

> **Especialista Absoluto e Agente Autônomo de Engenharia do Obsidian.**  
> Framework de automação, análise e gerenciamento de cofres Obsidian com suporte a MCP, Python, DataviewJS e Templater.

---

## 📐 Arquitetura do Vault

```
DEUS-DO-OBISIDIAN/
├── .obsidian/                    # Configurações internas do Obsidian
│   ├── app.json                  # Links absolutos, pasta de assets
│   ├── community-plugins.json    # Plugins habilitados
│   └── plugins/
│       ├── obsidian-dataview/    # DataviewJS — enableDataviewJs: true
│       ├── templater-obsidian/   # Templater — pasta: templates/
│       ├── quickadd/             # QuickAdd — choices + macros
│       └── obsidian-claude-code-mcp/  # MCP dual-transport (WS:22360 / SSE:22361)
├── notes/
│   ├── inbox/                    # Zona de captura rápida
│   ├── projects/                 # Projetos activos
│   ├── areas/                    # Áreas de responsabilidade
│   └── resources/                # Referências e recursos
├── templates/
│   ├── note-template.md          # Template genérico com MetadataCache
│   └── project-template.md      # Template de projeto
├── scripts/
│   └── dataview/
│       ├── orphan-detector.js    # Detecta notas órfãs
│       ├── tag-index.js          # Índice de tags com contagens
│       └── frontmatter-table.js  # Tabela de YAML frontmatter filtrada
├── macros/
│   └── capture-macro.js          # QuickAdd macro com try/catch MacroAbortError
├── automation/
│   ├── requirements.txt          # Dependências Python
│   ├── analyze_vault.py          # Análise topológica via NetworkX
│   ├── find_orphans.py           # Detecção e triagem de notas órfãs
│   └── extract_frontmatter.py    # Extração em lote de YAML frontmatter
└── assets/                       # Imagens e ficheiros estáticos
```

---

## 🔑 Princípios Operacionais

### 1. Supremacia do Texto e Links Absolutos

- `app.json` força `"newLinkFormat": "absolute"` para que todos os links sejam resolvidos a partir da raiz do vault.
- Imagens usam links Markdown padrão `![descrição](assets/imagem.png)` em vez de Wikilinks.
- Todo metadado indexável fica no **YAML Frontmatter** (campos `title`, `status`, `tags`, `created`, etc.).

### 2. Infraestrutura `.obsidian`

| Ficheiro | Função |
|----------|--------|
| `app.json` | Links absolutos, pasta de assets, sem editor legacy |
| `community-plugins.json` | Activa: `dataview`, `templater-obsidian`, `quickadd`, `obsidian-claude-code-mcp` |
| `plugins/obsidian-dataview/data.json` | `enableDataviewJs: true`, inline queries activos |
| `plugins/templater-obsidian/data.json` | `trigger_on_file_creation: true`, pasta `templates/` |
| `plugins/quickadd/data.json` | Choices de captura, templates e macro de criação de notas |
| `plugins/obsidian-claude-code-mcp/data.json` | Dual transport: WebSocket 22360 + HTTP/SSE 22361 |

---

## ⚙️ DataviewJS — Módulos Centralizados

Nunca espalhe código DataviewJS pelas notas. Use `dv.view()` para importar módulos externos:

### Detector de Órfãs
```dataviewjs
await dv.view("scripts/dataview/orphan-detector", { folder: "notes" })
```

### Índice de Tags
```dataviewjs
await dv.view("scripts/dataview/tag-index", { sortBy: "count" })
```

### Tabela de Frontmatter Filtrada
```dataviewjs
await dv.view("scripts/dataview/frontmatter-table", {
  folder: "notes/projects",
  fields: ["status", "priority", "due"],
  filter: { status: "active" }
})
```

---

## 📝 Templater — Templates

Os templates em `templates/` usam o objeto `tp` e o **MetadataCache nativo** do Obsidian para mapear conexões dinamicamente:

```javascript
// Dentro de note-template.md (bloco <%* ... %>)
const resolvedLinks = app.metadataCache.resolvedLinks;
const unresolvedLinks = app.metadataCache.unresolvedLinks;
```

---

## ⚡ QuickAdd — Macro de Captura

O macro `macros/capture-macro.js` usa `app.plugins.plugins.quickadd.api` e envolve toda a execução em `try/catch` para interceptar `MacroAbortError`:

```javascript
try {
  const title = await api.inputPrompt("Note title", "", "");
  // ... coleta de dados ...
} catch (err) {
  if (err.message === "MacroAbortError") {
    new Notice("ℹ️ Note creation cancelled.");
    return;
  }
  throw err;
}
```

---

## 🐍 Automação Python

### Instalação de dependências

```bash
pip install -r automation/requirements.txt
```

### Análise Topológica do Vault

```bash
python automation/analyze_vault.py --vault /caminho/para/vault --output report.json
```

Gera métricas de grafo via `obsidiantools` + `NetworkX`:
- Número de nós e arestas
- Top 10 notas por grau de entrada (incoming links)
- Notas órfãs
- Componentes conectados

### Detectar e Triar Notas Órfãs

```bash
# Apenas listar
python automation/find_orphans.py --vault /caminho/para/vault

# Mover para inbox para triagem manual
python automation/find_orphans.py --vault /caminho/para/vault --fix --output orphans.json
```

### Extrair Frontmatter em Lote

```bash
# Todos os campos, todas as notas, saída JSON
python automation/extract_frontmatter.py --vault /caminho/para/vault

# Campos específicos, pasta específica, saída CSV
python automation/extract_frontmatter.py \
  --vault /caminho/para/vault \
  --folder notes/projects \
  --fields status,priority,due \
  --output frontmatter.csv
```

---

## 🤖 MCP — Model Context Protocol

O plugin `obsidian-claude-code-mcp` expõe um servidor Dual Transport:

| Transporte | Porta | Uso |
|------------|-------|-----|
| WebSocket | 22360 | CLI / scripts headless |
| HTTP/SSE | 22361 | Claude Desktop |

### Ferramentas MCP disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `obsidian_get_workspace_files` | Lista ficheiros abertos no espaço de trabalho |
| `obsidian_get_frontmatter` | Retorna metadados YAML de uma nota em JSON |
| `obsidian_search_notes` | Busca notas via NLP/texto |
| `obsidian_list_tags` | Lista todas as tags com caminhos relativos |
| `str_replace` | **Edição cirúrgica** — substitui apenas o trecho alvo |
| `create` | Cria nota nova com conteúdo semântico |

> **Regra de ouro:** Nunca reescreva um ficheiro inteiro para alterar um parágrafo. Use sempre `str_replace` para proteger a integridade do documento.

---

## 🔗 Protocolo `obsidian://advanced-uri`

Para acções headless sem interface gráfica:

```bash
# Abrir uma nota específica
open "obsidian://advanced-uri?vault=DEUS-DO-OBISIDIAN&filepath=notes%2Finbox%2FInbox.md"

# Executar um comando do Obsidian
open "obsidian://advanced-uri?vault=DEUS-DO-OBISIDIAN&commandid=quickadd%3Acapture-inbox"
```
