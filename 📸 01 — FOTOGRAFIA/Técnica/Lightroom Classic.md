---
created: 2026-04-26
módulo: FOTOGRAFIA
tags: [fotografia, tecnica]
status: ativo
---

# Lightroom Classic

**Área:** Tecnologia & Ferramentas
**Tags:** #lightroom #edicao #panoramica #mascaramento #adobe
**Status:** Suporte fornecido ✅
**Links:** [[Adobe — Erros e Suporte]]

---

## Tópico 1 — Panorâmica com 3 fotos

**Problema:** Merge de 3 fotos de paisagem (esq + centro + dir) — erro "fotos insuficientes para correspondência".

**Causa:** Overlap insuficiente entre frames (~20–30% necessário).

**Solução alternativa:**
Photoshop → `File > Automate > Photomerge` → opção "Reposition"

---

## Tópico 2 — Masking Models travado em 0%

**Bug amplamente reportado.** Adobe corrigiu na versão **14.3.1**.

**Causa raiz:** Mudança arquitetural na v13.0 — modelos de IA passaram a ser baixados separadamente.

**Soluções em ordem:**
1. Atualizar para v14.3.1+
2. Limpar pasta `ModelZoo`
3. Configurar exceções no firewall/antivírus
4. Clean reinstall

---

## Conversas de referência

https://claude.ai/chat/6b5269fb-b20d-41f0-8749-a826b807fb89
https://claude.ai/chat/ca801757-96ff-4043-a0c8-f2fe4bb77ff5
