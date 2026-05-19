---
created: 2026-04-26
módulo: TECH
tags: [tech, ferramentas, ferramenta]
status: ativo
---

# Adobe — Erros e Suporte

**Área:** Tecnologia & Ferramentas
**Tags:** #adobe #creative-cloud #erro #windows
**Status:** Resolvido ✅
**Links:** [[Lightroom Classic]]

---

## Erro 1 — Creative Cloud não alcança servidores Adobe

**Soluções em ordem:**
1. Verificar data/hora do sistema
2. Reiniciar serviços Adobe (via services.msc)
3. Configurar exceções no firewall/antivírus
4. Sair e entrar novamente no Creative Cloud Desktop
5. Limpar cache Adobe
6. Verificar VPN ativa

---

## Erro 2 — Desinstalar Creative Cloud completamente (Windows 10)

**Método oficial:**
Adobe Creative Cloud Cleaner Tool

**Método manual:**
1. Painel de Controle → Desinstalar
2. Deletar pastas residuais em `Program Files` e `AppData`
3. Desativar serviços Adobe via `services.msc`
4. Forçar deleção com `rd /s /q [caminho]` se necessário

**Nota:** Remover CC não afeta apps Adobe já instalados.

---

## Conversas de referência

https://claude.ai/chat/e4a7a64d-a523-4d3c-bd88-2b1ebc5281a0
https://claude.ai/chat/d4a87c96-1b37-4e72-ae6a-6596e658c312
---
*Pai: [[_MOC-Tech]]*
