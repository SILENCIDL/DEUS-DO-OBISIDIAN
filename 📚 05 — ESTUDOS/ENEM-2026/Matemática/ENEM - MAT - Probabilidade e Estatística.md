---
tags: [estudos, enem, matematica, cor/ciano-50-200-220]
tipo: conteúdo-enem
updated: 2026-02-04
---

# 📕 Probabilidade e Estatística

Categoria: [[ENEM - Matemática]]

---

## Estatística

### Medidas de Tendência Central

#### Média Aritmética
> **x̄ = (x₁ + x₂ + ... + xₙ) / n**

Exemplo: Notas 7, 8, 5, 10
x̄ = (7 + 8 + 5 + 10) / 4 = 30/4 = **7,5**

#### Média Ponderada
> **x̄ = (x₁·p₁ + x₂·p₂ + ...) / (p₁ + p₂ + ...)**

Exemplo: Prova (peso 3) = 8, Trabalho (peso 1) = 6
x̄ = (8×3 + 6×1) / (3+1) = 30/4 = **7,5**

#### Mediana
Valor central dos dados **ordenados**.

Exemplo: 3, 5, 7, 8, 12 → Mediana = **7**
Exemplo: 3, 5, 7, 8 → Mediana = (5+7)/2 = **6**

#### Moda
Valor que **mais aparece**.

Exemplo: 2, 3, 3, 5, 7, 3 → Moda = **3**

---

### Medidas de Dispersão

#### Amplitude
> **A = maior valor - menor valor**

#### Variância
> **σ² = Σ(xᵢ - x̄)² / n**

#### Desvio Padrão
> **σ = √σ²**

**Interpretação**: Quanto maior o desvio padrão, mais **espalhados** estão os dados.

Exemplo: Turma A: notas 7, 7, 7, 7 (σ = 0)
Turma B: notas 2, 5, 9, 12 (σ alto) → mais desigual

---

## Análise Combinatória

### Princípio Fundamental da Contagem
Se evento 1 tem **m** possibilidades e evento 2 tem **n** possibilidades:
> **Total = m × n**

Exemplo: 3 camisas × 4 calças = **12 combinações**

### Fatorial
> **n! = n × (n-1) × (n-2) × ... × 1**

| n | n! |
|---|-----|
| 0 | 1 |
| 1 | 1 |
| 2 | 2 |
| 3 | 6 |
| 4 | 24 |
| 5 | 120 |
| 6 | 720 |
| 10 | 3.628.800 |

### Permutação
**Ordem importa, usa todos os elementos.**

> **Pₙ = n!**

Exemplo: De quantas formas 5 pessoas sentam em 5 cadeiras?
P₅ = 5! = **120**

### Arranjo
**Ordem importa, usa parte dos elementos.**

> **Aₙ,ₚ = n! / (n-p)!**

Exemplo: De quantas formas escolher presidente e vice entre 10 pessoas?
A₁₀,₂ = 10!/8! = 10 × 9 = **90**

### Combinação
**Ordem NÃO importa.**

> **Cₙ,ₚ = n! / [p! × (n-p)!]**

Exemplo: Escolher 3 pessoas de um grupo de 10:
C₁₀,₃ = 10! / (3! × 7!) = 720/6 = **120**

### Quando usar qual?

| Situação | Fórmula | Exemplo |
|----------|---------|---------|
| Todos, com ordem | Permutação | Fila de espera |
| Parte, com ordem | Arranjo | Presidente e vice |
| Parte, sem ordem | Combinação | Comissão, grupo |

---

## Probabilidade

### Probabilidade simples
> **P(A) = casos favoráveis / casos possíveis**

Exemplo: Dado de 6 faces, P(sair 3) = 1/6

### Propriedades
- 0 ≤ P(A) ≤ 1
- P(certeza) = 1
- P(impossível) = 0
- P(A) + P(não A) = 1

### Eventos independentes (E)
> **P(A e B) = P(A) × P(B)**

Exemplo: Moeda (cara) e dado (6):
P = 1/2 × 1/6 = **1/12**

### Eventos mutuamente exclusivos (OU)
> **P(A ou B) = P(A) + P(B)**

Exemplo: Dado, sair 2 ou 5:
P = 1/6 + 1/6 = **2/6 = 1/3**

### Probabilidade condicional
> **P(A|B) = P(A e B) / P(B)**

---

## Dica ENEM

O ENEM cobra:
1. **Média, mediana e moda** — cálculo e interpretação
2. **Probabilidade simples** — moeda, dado, urna
3. **Combinação** — grupos, comissões
4. **Princípio da contagem** — senhas, placas

**Estratégia**:
- Identifique se a ordem importa (arranjo) ou não (combinação)
- Em probabilidade, liste os casos possíveis quando forem poucos
- Use o complementar: P(pelo menos 1) = 1 - P(nenhum)

---

## 🔗 Conexões
- [[ENEM - Matemática]]
- [[ENEM - MAT - Perguntas.canvas]]
- [[ENEM - Área de Ação.canvas]]

