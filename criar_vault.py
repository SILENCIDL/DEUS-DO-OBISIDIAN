#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cria estrutura de pastas para vault Obsidian
Caminho base: C:\Users\Usuário\Desktop\DIREÇÃO
"""

from pathlib import Path

def criar_estrutura_obsidian():
    # Caminho base
    base = Path(r"C:\Users\Usuário\Desktop\DIREÇÃO")
    
    # Define a estrutura completa
    estrutura = {
        "01_Fotografia": [
            "Projetos_e_Eventos (ex: II Festival de Vôlei São Bento do Sapucaí)",
            "Fotop_e_Equipe",
            "Pack_Filmic_Mantiqueira",
            "Equipamentos_e_Metas (Inventário Nikon, Lentes e meta do MacBook M4)",
            "Estudos_Optica_e_Sensores"
        ],
        "02_Desenvolvimento": [
            "Portfolio_Site_Vinicius",
            "Automacoes_Obsidian_API",
            "Projeto_Software_3D"
        ],
        "03_Idiomas": [
            "Mandarim",
            "Espanhol",
            "Frances"
        ],
        "04_Projetos_Pessoais": [
            "Horta_Irrigacao_Autonoma",
            "Planejamento_Casal"
        ]
    }
    
    criadas = []
    existentes = []
    
    # Cria diretório base se não existir
    if not base.exists():
        base.mkdir(parents=True)
        print(f"[BASE CRIADA] {base}")
    else:
        print(f"[BASE EXISTE] {base}")
    
    # Cria pastas principais e subpastas
    for pasta_principal, subpastas in estrutura.items():
        caminho_principal = base / pasta_principal
        
        if not caminho_principal.exists():
            caminho_principal.mkdir(parents=True)
            criadas.append(pasta_principal)
            print(f"  [+] {pasta_principal}")
        else:
            existentes.append(pasta_principal)
            print(f"  [=] {pasta_principal} (já existe)")
        
        for subpasta in subpastas:
            caminho_sub = caminho_principal / subpasta
            
            if not caminho_sub.exists():
                caminho_sub.mkdir(parents=True)
                criadas.append(f"{pasta_principal}/{subpasta}")
                print(f"      [+] {subpasta}")
            else:
                existentes.append(f"{pasta_principal}/{subpasta}")
                print(f"      [=] {subpasta} (já existe)")
    
    # Resumo
    print(f"\n{'='*50}")
    print(f"CONCLUÍDO")
    print(f"{'='*50}")
    print(f"Total criado: {len(criadas)} pastas")
    print(f"Total existente: {len(existentes)} pastas")
    print(f"\nVault pronto em: {base}")

if __name__ == "__main__":
    criar_estrutura_obsidian()