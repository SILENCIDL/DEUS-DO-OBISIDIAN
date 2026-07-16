---
tipo: aula
área: Fotografia
trilha: Fotógrafo Completo
módulo: Técnica / Edição
nível: 3
status: em-estudo
dificuldade: intermediária
pré-requisitos: [[FOTO - Técnica]]
continuações: [[FOTOGRAFIA - Arte, técnica e negócio]]
relacionadas: [[LIGHTRROM]], [[PHOTOSHOP]], [[CPU]]
atualizado: 2026-07-16
---

# 🎨 Gestão de Cor — Do Sensor à Impressão

> [!abstract] Ideia central
> A cor que você vê na tela não é "a cor" — é uma interpretação. Gestão de cor é garantir que a mesma imagem apareça **o mais consistente possível** do sensor ao monitor e à impressão, evitando o clássico "na tela estava lindo, impresso ficou estranho".

---

## 🎯 Objetivo de aprendizagem
- Entender espaço de cor, profundidade de bits e perfil.
- Saber por que a impressão difere da tela e como reduzir isso.
- Calibrar o fluxo para entregar cor previsível.

## ❓ Por que isso importa
Você edita ([[LIGHTRROM]]) e imprime Fine Art ([[FOTOGRAFIA - Arte, técnica e negócio]]). Sem gestão de cor, o cliente recebe uma impressão diferente do que aprovou — retrabalho e prejuízo.

## 🧠 Conhecimentos prévios
- [[FOTO - Técnica]] (Aula 7 — Edição) e [[LIGHTRROM]].
- Ideia de RAW × JPEG.

## 🗺️ Visão geral
```
SENSOR (RAW) → ESPAÇO DE COR → MONITOR (calibrado) → IMPRESSÃO (perfil do papel)
     dados       sRGB/AdobeRGB      o que você vê        gamut menor → soft proof
```

---

## 📚 Conceitos fundamentais

### 1. Espaço de cor (gamut)
- **Definição:** o conjunto de cores que um espaço consegue representar.
- **Principais:** **sRGB** (menor, padrão da web/redes), **Adobe RGB** (maior, cobre mais verdes/ciano, bom para impressão), **ProPhoto RGB** (enorme, usado na edição interna).
- **Função:** define quais cores "cabem" no arquivo.
- **Aplicação:** entregar **sRGB** para Instagram/web; **Adobe RGB** ou perfil do lab para impressão.
- ⚠️ **Erro:** postar Adobe RGB na web → cores lavadas/dessaturadas (a web assume sRGB).

### 2. Profundidade de bits
- **Definição:** quantos tons por canal de cor. **8 bits** (JPEG) × **16 bits** (RAW/TIFF).
- **Função:** mais bits = transições mais suaves, menos "banding" (faixas no céu).
- **Aplicação:** editar em 16 bits, exportar 8 bits para entrega comum.

### 3. Perfil ICC
- **Definição:** um "dicionário" que descreve como um dispositivo (monitor, impressora, papel) reproduz cor.
- **Função:** traduz a cor entre dispositivos para manter consistência.
- **Aplicação:** usar o perfil ICC do **papel + impressora** específicos ao imprimir.

### 4. Calibração de monitor
- **Definição:** ajustar o monitor para exibir cor de forma padronizada (com um **colorímetro**, ex.: Spyder/Calibrite).
- **Função:** sem isso, você edita "às cegas" — cada tela mente de um jeito.
- **Aplicação:** calibrar mensalmente; trabalhar em ambiente com luz neutra e estável.

### 5. Soft proofing (prova virtual)
- **Definição:** simular na tela como a foto ficará **naquele papel/impressora**, usando o perfil ICC.
- **Função:** antecipar diferenças antes de gastar tinta/papel.
- **Aplicação:** no Lightroom/Photoshop, ativar soft proof com o perfil do lab.

---

## 🔎 Explicação aprofundada
A tela **emite luz** (RGB, aditivo) e alcança cores muito vivas. O papel **reflete luz** (CMYK, subtrativo) e tem um **gamut menor** — não consegue reproduzir certos azuis e verdes saturados. Por isso uma foto vibrante na tela pode "apagar" no papel: as cores fora do gamut do papel são **remapeadas**. O soft proofing mostra isso antes; ajustar saturação/contraste na prova evita a surpresa.

Consistência exige a cadeia inteira alinhada: **monitor calibrado** + **espaço de cor correto** + **perfil do papel**. Se um elo falha, o resultado é imprevisível.

## 🧩 Exemplo concreto
Você edita um pôr do sol saturadíssimo em ProPhoto, exporta e manda pro lab. Impresso, o laranja "queima" e perde detalhe. Com **soft proof** do perfil do papel, você teria visto o alerta de gamut e reduzido a saturação do laranja — a impressão sairia como esperado.

## 🎯 Aplicação na realidade de Vinícius
- **Web/Instagram:** sempre exportar **sRGB** ([[PADDING PRETO e BRANCO]], [[INSTAGRAM - Minha vitrine visual]]).
- **Impressão Fine Art:** pedir o **perfil ICC** do lab, fazer soft proof, entregar no espaço que ele pedir.
- **Edição:** monitor calibrado + [[CPU|máquina]] adequada para trabalhar em 16 bits.

## 🛠️ Procedimento prático — entregar cor previsível
1. **Preparação:** monitor calibrado; luz do ambiente estável.
2. **Edição:** trabalhar em 16 bits; espaço amplo (ProPhoto/Adobe RGB) no editor.
3. **Web:** exportar JPEG **sRGB**, 8 bits.
4. **Impressão:** obter perfil ICC do papel/lab → ativar **soft proof** → ajustar → exportar no espaço pedido.
5. **Verificação:** comparar prova impressa de teste com a tela.
6. **Correção:** ajustar saturação/brilho das cores fora do gamut.

## ⚠️ Erros frequentes
| Erro | Consequência | Correção |
|------|--------------|----------|
| Postar Adobe RGB na web | Cores lavadas | Exportar sRGB |
| Monitor não calibrado | Edita "errado" sem saber | Calibrar com colorímetro |
| Ignorar perfil do papel | Impressão diferente da tela | Usar ICC + soft proof |
| Editar em 8 bits | Banding no céu/gradientes | Editar em 16 bits |
| Brilho do monitor no máximo | Fotos saem escuras impressas | Calibrar luminância (~120 cd/m²) |

## ⚖️ Comparações
| Espaço | Tamanho do gamut | Uso |
|--------|------------------|-----|
| sRGB | Menor | Web, redes, entrega comum |
| Adobe RGB | Médio-grande | Impressão profissional |
| ProPhoto RGB | Enorme | Edição interna (16 bits) |

## ✅ Exercício de compreensão
1. Por que a impressão costuma ter cores menos vivas que a tela?
2. O que é um perfil ICC?
3. Quando exportar em sRGB e quando em Adobe RGB?

## 🏋️ Exercício prático
- [ ] Exporte a mesma foto em sRGB e Adobe RGB, poste ambas e compare no celular.
- [ ] Ative o soft proof com um perfil de papel e observe o aviso de gamut.

## 🏆 Critérios de domínio
- [ ] Escolhe o espaço de cor certo para cada entrega.
- [ ] Entende por que tela ≠ impressão.
- [ ] Sabe o que calibrar e por quê.

## 🔁 Revisão ativa
1. (Básica) O que é gamut?
2. (Compreensão) Por que 16 bits evita banding?
3. (Aplicação) Vai imprimir Fine Art: quais passos garantem cor fiel?
4. (Diagnóstico) Cliente diz que a impressão saiu "sem graça". Causa provável?
5. (Decisão) Entregar foto para o Instagram do cliente: qual espaço de cor?

> [!question]- Respostas
> 1. O conjunto de cores que um espaço/dispositivo consegue representar.
> 2. Mais tons por canal → transições suaves, sem faixas visíveis.
> 3. Monitor calibrado + soft proof com o perfil do papel + exportar no espaço do lab.
> 4. Provável falta de soft proof / cores fora do gamut do papel remapeadas.
> 5. sRGB.

---

## 🔗 Conexões
### Pré-requisitos
- [[FOTO - Técnica]] (Edição) · [[LIGHTRROM]]

### Continuações
- [[FOTOGRAFIA - Arte, técnica e negócio]] — impressão Fine Art e entrega.

### Aprofundamentos
- [[PHOTOSHOP]] · [[CPU]] (hardware para edição em 16 bits)

---

## 📖 Fontes e referências
- Fundamentos de color management (espaços sRGB/Adobe RGB/ProPhoto, perfis ICC, soft proofing) — documentação Adobe e do ICC (International Color Consortium).

## 🧾 Síntese final
- **Aprendido:** cor depende de espaço, bits, perfil e calibração; tela e papel têm gamuts diferentes.
- **Praticar:** exportar no espaço certo; testar soft proof.
- **Depois:** aplicar na impressão Fine Art ([[FOTOGRAFIA - Arte, técnica e negócio]]).
