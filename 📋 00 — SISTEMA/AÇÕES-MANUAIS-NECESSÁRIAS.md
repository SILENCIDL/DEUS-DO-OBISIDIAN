---
created: 2026-04-26
módulo: SISTEMA
tags: [sistema, manual, acoes, pendencia]
status: ativo
tipo: checklist
---

# 🛠️ AÇÕES MANUAIS NECESSÁRIAS

> Coisas que **só você consegue fazer** porque o sandbox do Cowork não tem permissão (Windows trancou os arquivos) ou porque é GUI do Obsidian.

Marca aqui conforme for fazendo. ~5 min de trabalho total.

---

## 1. ⚡ Git commit final (1 min)

O sandbox criou um `.git/index.lock` que o Windows trancou. Sem o commit, o trabalho de F1–F5 não tem checkpoint no histórico.

**No PowerShell:**

```powershell
cd "C:\ponto 000"
Remove-Item .git\index.lock -ErrorAction SilentlyContinue
git add -A
git commit -m "reorganizacao: F1-F5 executadas (11 areas, 308 arquivos movidos, 11 MOCs, 0 orfas)"
git log --oneline | Select-Object -First 5
```

**Confirma:** os últimos 3 commits devem ser:
- `reorganizacao: F1-F5 executadas...` (novo)
- `checkpoint: estado pre-reorganizacao` (`332f3fa`)
- `Initial commit` (`6dc6a22`)

- [ ] Feito

---

## 2. 🗑️ Apagar pastas legadas vazias (1 min)

Foram esvaziadas pelo script de migração mas continuam aparecendo no painel do Obsidian.

**No PowerShell:**

```powershell
cd "C:\ponto 000"
Remove-Item -Recurse -Force "Conteudo","Fotografia","Pessoal","Tech","SISTEMA_IDIOMAS_Completo"
```

- [ ] Feito

---

## 3. 🗑️ Apagar `_Index_of_*.md` deprecados (1 min)

Sobreviveram à migração porque o Windows tinha lock. Foram reescritos pra conter só `%% DEPRECATED... %%` mas continuam aparecendo. Eles vivem nas pastas emoji legadas que ainda têm 1-2 arquivos cada.

**No PowerShell:**

```powershell
cd "C:\ponto 000"
Remove-Item -Recurse -Force "📸 Fotografia","📱 Conteúdo","💼 Negócios","💰 Finanças","📚 Estudos","👕 VRGS","🔒 Seguro","🗂️ Arquivo"
Remove-Item "_Index_of_ponto 000.md"
```

> ⚠️ **Antes de rodar:** confirma com `Get-ChildItem "📸 Fotografia"` que só tem o `_Index_of_*.md` lá dentro (e nenhum arquivo "real"). O script de migração esvaziou tudo, mas confere.

- [ ] Feito

---

## 4. 🔌 Desativar plugin Zoottelkeeper no Obsidian (2 min)

Esse plugin é o que cria automaticamente os `_Index_of_*.md`. Se não desativar, ele vai recriar todos os índices na próxima abertura do vault — vai bagunçar o trabalho.

**Como desativar:**

1. Abre o Obsidian no vault `C:\ponto 000`
2. `Ctrl + ,` (ou Settings)
3. Sidebar → **Community plugins**
4. Procura "**Zoottelkeeper**" na lista de instalados
5. **Toggle off** (desativa)
6. Opcional: clica no botão de lixeira pra desinstalar de vez

**Verificação:** depois de desativar, abre `📸 01 — FOTOGRAFIA/` no Obsidian. Não deve aparecer nenhum `_Index_of_*.md` autogerado. Os MOCs novos (`_MOC-Fotografia.md`) são manuais e ficam.

- [ ] Feito

---

## 5. 👁️ Abrir o Obsidian e validar a estrutura nova (5 min)

Confere se está tudo onde deve:

1. Abre o vault no Obsidian
2. Painel lateral esquerdo deve mostrar **11 pastas** com prefixo `00`–`10` em ordem
3. Clica em `📋 00 — SISTEMA/_MOC-Vault.md` — deve renderizar com links pros 11 MOCs de área
4. Testa `Ctrl + Click` em alguns wikilinks pra ver se resolvem certo
5. Abre o **Graph View** (`Ctrl + G`) — deve estar **muito mais conectado** do que antes (zero ilhas)

- [ ] Feito

---

## 6. ⚙️ (Opcional) Ajustar settings de Obsidian pro novo modelo

- **Files & Links → Default location for new notes:** mudar pra `📋 00 — SISTEMA/` (raiz do sistema, depois você move pra área certa)
- **Files & Links → New link format:** "Shortest path when possible" (assim wikilinks `[[Nota]]` funcionam mesmo entre pastas)
- **Files & Links → Use [[Wikilinks]]:** ON
- **Templates → Template folder location:** `📋 00 — SISTEMA/Templates`

- [ ] Feito

---

## ✅ Quando tudo acima estiver feito

- Apaga este arquivo (já cumpriu seu papel)
- Ou marca status: arquivado no frontmatter
- Próxima sessão começa direto na pauta de conteúdo (PROJETOS-ATIVOS, stubs, expansões)

---

*Criado em 2026-04-26 — pós-execução F1-F5. Detalhes completos em [[RELATORIO-EXECUCAO]].*
