# Pack Filmic Mantiqueira: Perfil de Cor, LOG e Estética

## Navegação
- [[📋 ÍNDICE - 01 Fotografia|← Fotografia]]
- [[🏠 ÍNDICE|🏠 Início]]

---

## 1. RESUMO EXECUTIVO

O desenvolvimento de presets cinematográficos ou Packs Filmic exige a distinção técnica entre curvas logarítmicas (LOG) e perfis padrão de câmera. A construção visual focada em regiões úmidas e serranas como a Serra da Mantiqueira apoia-se em correção primária metódica para acomodar os extremos de iluminação, visando traduzir uma estética orgânica, etérea e rica em profundidade textural.

---

## 2. MAPA DE CONHECIMENTO

A manipulação da ciência das cores em âmbito profissional distancia-se fundamentalmente dos filtros genéricos de aplicativos devido à captação na fonte. Diferente dos perfis Standard — que aplicam um processamento interno severo de contraste e saturação de forma irreversível nos pixels capturados —, os perfis LOG aplicam uma função de transferência matemática (geralmente uma curva de gama baseada em cálculos logarítmicos) para comprimir a imensa faixa dinâmica do sensor, achatando o sinal e protegendo os limites críticos das altas-luzes e sombras densas. Este aspecto visual desbotado e de baixo contraste, característico das imagens saindo diretamente da câmera, é o preço temporário a ser pago pela retenção exponencial de dados. A conversão de LOG requer hardware robusto, visto que manipulações extremas em arquivos capturados sob as limitações do espaço de cor de 8-bits resultam invariavelmente em banding de cor e artefatos de ruído destrutivos; portanto, arquivos de 10-bits ou a captação RAW em fotografia tornam-se imperativos absolutos.

Aplicar esta engenharia à região da Serra da Mantiqueira significa traduzir os fenômenos atmosféricos em valores de Look Up Tables (LUTs) ou perfis (Presets). A estética local caracteriza-se pela exuberância densa das matas nativas, águas cristalinas das cachoeiras e neblinas espessas em altitude. A criação de um Pack Filmic para este bioma foca em uma paleta onde os verdes não são fluorescentes, mas assumem matrizes de esmeralda profunda ou tons ocre/musgo, enquanto a "hora mágica" em picos como a Pedra do Baú demanda a preservação luxuosa dos canais quentes sem a clipagem do canal vermelho (red channel clipping). O fluxo de trabalho (captura → correção → aplicação) exige que a correção primária estabeleça o balanço de branco e a expansão de contraste corretos antes de se aplicar o Look de forma não-destrutiva.

| Atributo Técnico | Captação Standard / JPEG | Captação LOG / RAW |
|---|---|---|
| Latitude Dinâmica | Baixa. Altas-luzes facilmente "estouradas" (clipped) e irrecuperáveis. | Altíssima. Retém detalhes sutis nas sombras e texturas em nuvens claras. |
| Aparência Bruta | Pronta para uso, com contraste e saturação acentuados (processamento in-camera). | Lavada, acinzentada, exigindo manipulação técnica e calibração de perfil em software. |
| Flexibilidade Criativa | Limitada. Edições agressivas destroem rapidamente o arquivo (artefatos/banding). | Máxima. Permite aplicação de color grading complexo para criar estéticas cinematográficas (Filmic). |

---

## 3. NOTAS DE AÇÃO

- [ ] Mapear as curvas nativas (ex: N-Log ou Z-Log da Nikon) e realizar capturas de teste de alto contraste para dominar o processo de transformação de espaço de cor (Color Space Transform) no software de edição, visando a expansão correta da curva de Gama.
- [ ] Criar três vertentes de Presets/LUTs baseados no estudo da paleta da Mantiqueira: "Neblina Matinal" (sombras frias, levantamento do ponto preto), "Verde Atlântico" (saturação seletiva para folhagens escuras) e "Golden Hour Baú" (preservação de highlights quentes).
- [ ] Padronizar o workflow de pós-produção: Nível 1 - Correção Primária de Exposição/Balanço de Branco; Nível 2 - Conversão para Rec.709; Nível 3 - Aplicação do Look Filmic no topo da hierarquia de nós/camadas de edição.

---

## 4. RECURSOS

- **Fundamentos Científicos do LOG:** [URL](https://www.cinematools.co/blog/why-you-should-be-filming-in-log-and-not-standard-profiles)
- **Estudo Estético da Mantiqueira:** [URL](https://www.renatomachadophoto.com/mantiqueira2026)

---

## 5. TAGS SUGERIDAS

#color_grading #log_profiles #pack_filmic #serra_da_mantiqueira #pos_producao
---
*Pai: [[_MOC-Fotografia]]*
