# reorganize_vault.py
# Script utilizado para reorganizar a estrutura do vault do Obsidian
# Rodar com: python reorganize_vault.py

import os
import shutil
from pathlib import Path

VAULT = Path("pasta do obsidian/ponto 000")

ESTRUTURA = {
    "000 - NÚCLEO": [],
    "100 - IDENTIDADE E MARCA/VRGS": [],
    "100 - IDENTIDADE E MARCA/Negócios": [],
    "200 - FOTOGRAFIA/Negócio": [],
    "200 - FOTOGRAFIA/Técnica": [],
    "200 - FOTOGRAFIA/Projetos": [],
    "200 - FOTOGRAFIA/História": [],
    "200 - FOTOGRAFIA/Fotos DSC": [],
    "300 - SISTEMAS E IA/MICÉLIO": [],
    "300 - SISTEMAS E IA/ÁGORA": [],
    "400 - CONTEÚDO E SOCIAL/Instagram": [],
    "400 - CONTEÚDO E SOCIAL/YouTube": [],
    "400 - CONTEÚDO E SOCIAL/Produção": [],
    "500 - FINANCEIRO": [],
    "600 - ESTUDOS/ENEM 2026": [],
    "600 - ESTUDOS/ANHANGUERA": [],
    "600 - ESTUDOS/Leitura": [],
    "600 - ESTUDOS/Idiomas": [],
    "700 - PROJETOS/Ativos": [],
    "700 - PROJETOS/Pausados": [],
    "700 - PROJETOS/Futuros": [],
    "800 - DIÁRIO E ROTINA/Diário": [],
    "800 - DIÁRIO E ROTINA/Saúde": [],
    "900 - ARQUIVO": [],
}


def criar_pastas(vault_path):
    for pasta in ESTRUTURA:
        caminho = vault_path / pasta
        caminho.mkdir(parents=True, exist_ok=True)
        print(f"✓ Criada: {caminho}")


def listar_notas(vault_path):
    notas = list(vault_path.rglob("*.md"))
    print(f"\n📋 {len(notas)} notas encontradas:")
    for n in notas:
        print(f"  {n.relative_to(vault_path)}")
    return notas


if __name__ == "__main__":
    vault = VAULT
    print("🔍 Lendo vault atual...")
    notas = listar_notas(vault)
    print("\n📁 Criando estrutura de pastas...")
    criar_pastas(vault)
    print("\n✅ Estrutura criada com sucesso.")
