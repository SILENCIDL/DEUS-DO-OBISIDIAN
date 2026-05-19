# 🏠 SUBTEMAS EXPANDIDOS - Projetos Pessoais
## Engineering meets lifestyle: automation para qualidade de vida

---

## 🌱 HORTA COM IRRIGAÇÃO AUTÔNOMA

### Visão Geral do Projeto
- **Objetivo**
  - Produzir alimentos frescos (self-sufficiency)
  - Automação total (zero manutenção diária)
  - IoT playground (aproveitar pra aprender)
  - ROI: reduzir gastos com supermercado + bem-estar

- **Escopo MVP (Minimum Viable Product)**
  - 1 cama de plantação (1m x 2m)
  - Sensor umidade do solo
  - Válvula solenóide para irrigação
  - Controller (Arduino ou Raspberry Pi)
  - App mobile simples (web ou Telegram bot)

---

### ⚙️ HARDWARE & ELETRÔNICA

#### Controller Options
- **Arduino (Preferred)**
  - Menor curva aprendizado
  - Ecossistema robusto (shields, libraries)
  - Custo: $50-100 kit completo
  - Conectividade: WiFi com módulo ESP8266/ESP32

- **Raspberry Pi**
  - Mais poderoso (Linux, Python nativo)
  - Curva maior
  - Extensível (GPIO, USB, networking built-in)
  - Custo: $35-60 + accessórios

#### Sensores
- **Umidade do Solo**
  - Capacitivo (melhor, menos corrosão) vs resistivo
  - Calibração necessária (dry=0, wet=1023)
  - Quantidade: 3-5 sensores por cama (cobertura)

- **Temperatura & Umidade do Ar**
  - DHT22 (barato, 5V, 1-wire protocol)
  - Opcional: influencia na frequency de irrigação

- **Luz (opcional)**
  - LDR (light dependent resistor)
  - Rastreamento de ciclo dia/noite
  - Trigger automático para lâmpadas grow

#### Atuadores
- **Válvula Solenóide**
  - 12V ou 24V (depende fonte)
  - Tempo abertura: 5-30min (determinar por teste)
  - Qualidade: industrial (evitar vazamentos)

- **Bomba de Água**
  - Submersível ou inline (depende design)
  - Vazão: 500-2000L/hr (calcular)
  - Fonte + relé para controle

- **Luzes (se grow operation)**
  - LED grow lights (blue 6500K, red 3000K)
  - Controladas por relé
  - Timer automático (por Arduino)

#### Fonte de Energia
- **Opção 1: Plug AC**
  - Simples, confiável
  - Consumo: ~5-10W Arduino + sensores
  - Bomba pode demandar 50-100W
  
- **Opção 2: Solar (ambitious)**
  - Painel solar 20W
  - Bateria LiFePO4 ou chumbo-ácido
  - Charge controller
  - Total custo 3-5x mais

---

### 💻 SOFTWARE & LÓGICA

#### Firmware Arduino
```
Pseudocódigo:
Loop cada 5 minutos:
  1. Ler sensor umidade
  2. Se umidade < threshold_min:
     - Abrir válvula por 10min
     - Log evento
  3. Se umidade > threshold_max:
     - Nada (espera evaporação)
  4. Enviar data pra cloud (WiFi)
  5. Sleep 5min (economizar energia)
```

#### Thresholds Iniciais
- **Tomate**: 40-70% umidade (adaptar por tipo plantação)
- **Alface**: 60-80% (mais úmido)
- **Suculentas**: 20-40% (menos é mais)

#### Conectividade Cloud
- **Opção A: Local API** (Obsidian API que você ama!)
  - Arduino envia POST requests
  - Armazena em JSON local
  - Sem internet = sem problema

- **Opção B: Cloud Service**
  - Arduino Cloud (oficial, fácil)
  - Blynk (interface amigável)
  - IFTTT integrations
  - Custo: free tier ou $5-10/mês

- **Opção C: Custom Server**
  - Node.js + Express API
  - Database (PostgreSQL, MongoDB)
  - Own-hosted ou Heroku/Railway
  - Complexidade: média

#### App Mobile/Web
- **Telegram Bot** (simplest MVP)
  - Arduino envia alertas via bot
  - Usuário pode comandar "Water now" via chat
  - ~50 linhas de código Python

- **Web Dashboard**
  - Gráfico de umidade vs tempo (Chart.js)
  - Histórico de eventos
  - Manual overrides (forçar irrigação)
  - Status atual (último sync, bateria)

- **Mobile App**
  - React Native ou Flutter
  - Push notifications (slack, email)
  - Biometria para autorizar mudanças
  - Backlog: Modo vacação, learning curve

---

### 🌿 AGRONOMIA & PLANTAÇÃO

#### Culturas Iniciais
- **Tomate** (ROI alto, longo ciclo)
  - 80-90 dias till fruit
  - Precisa de staking/suporte
  - Sensível a cálcio (blossom end rot)

- **Alface** (rápido, fácil)
  - 30-45 dias
  - Cut-and-come-again (colheita contínua)
  - Sombreamento em verão (bolting risk)

- **Ervas** (custo vs benefício excelente)
  - Manjericão (30 dias, basil pesto!)
  - Cilantro (45 dias, sensível a calor)
  - Gengibre (lento, mas perene)

#### Sazonalidade Mantiqueira
- **Primavera (Set-Nov)**
  - Temperatura ótima (18-25°C)
  - Plantação: tomate, berinjela
  
- **Verão (Dez-Fev)**
  - Muito quente (risco bolting em alface)
  - Ótimo: milho, melancia, abóbora
  - Sombreamento necessário (50%)
  
- **Outono (Mar-Mai)**
  - Volta ideal (20-24°C)
  - Replantação de inverno
  
- **Inverno (Jun-Ago)**
  - Frio, menos luz
  - Brassicas (couve, brócolis)
  - Possivelmente iluminação artificial

#### Compostagem (Ciclo Completo)
- **Input**
  - Resíduos da horta (folhas mortas)
  - Resíduos cozinha (cascas, solos)
  - Aparas de grama (nitrogen)

- **Processo**
  - Pile 1m³ (ideal)
  - Brown:Green = 3:1 (carbono:nitrogen)
  - Umidade 50-60% (como esponja espremida)
  - Aeração semanal (garfo ou turner)
  - Tempo: 2-3 meses → preto e terra

- **Output**
  - Compost pronto = input para horta
  - Zero waste, ciclo fechado!

---

### 📈 ESCALABILIDADE & FUTURO

#### Expansão Fase 2 (Meses 6-12)
- [ ] Cama 2 (plantação diferente)
- [ ] Sensores de pH (nutrição)
- [ ] Fertilizante liquido automático (hydroponics?)
- [ ] Lamps grow (estender temporada)

#### Integração com Outras Automações
- **Obsidian API**
  - Registrar colheitas (data + quantidade)
  - Histórico de problemas (praga, deficiência)
  - Receitas pra usar produção

- **Home Assistant**
  - Horta como device no ecossistema
  - Automations (se temperatura > 30°C, aumenta sombreamento)
  - Notificações integradas

#### Viabilidade Econômica
- **Custo inicial: ~$300-500**
  - Arduino: $60
  - Sensores: $100
  - Válvula + bomba: $80
  - Estrutura: $100
  
- **Payback: ~2 anos**
  - Economizar ~$150/mês em alimentos frescos
  - Benefício bem-estar > financeiro

---

## 💕 PLANEJAMENTO CASAL

### Estrutura & Dimensões

#### 1. Viagens (Adventure)
- **Bucket List por Estação**
  - Verão: praia, parques (weather)
  - Inverno: esqui, montanha, city breaks
  - Primavera: natureza (flores, trekkings)
  - Outono: colheita, roadtrips

- **Pesquisa & Planning**
  - Mood: ativo vs relaxante?
  - Budget: luxury vs backpacking?
  - Quando: feriados fixos, flexível?
  - Com quem: just us 2, amigos?

- **Exemplos de Trips**
  - Mantiqueira local (weekend: trilhas, hortênsias)
  - São Paulo (cultural, museus, food)
  - Litoral (praia, sunset, seafood)
  - Interior: Minas, Goiás (estradas, paisagem)

#### 2. Finanças Conjuntas (Stability)
- **Budget Categories**
  - Necessário: moradia, comida, utilidades
  - Investimento: horta, educação, tech
  - Lazer: viagens, hobbies, eventos
  - Buffer: 3 meses emergências

- **Metas Financeiras**
  - 2026: fundo de reserva (3-6 meses)
  - 2027: investimento inicial (???)
  - 2028: house goal / grandes projetos?

- **Transparência & Comunicação**
  - Shared Google Sheets (budget tracking)
  - Monthly money date (30min review)
  - Decisões > $500 consenso

#### 3. Projetos do Lar (Nesting)
- **Pequenas Melhorias**
  - Pintura, decoração, rearranjo
  - Espaço home office (melhor)
  - Iluminação otimizada
  - Prateleiras, organização

- **Reformas Maiores**
  - Renovação cozinha? (future)
  - Novo piso/acabamento?
  - Parede de vidro? (kitchen?)
  - Garden shed para ferramentas?

- **Priority Matrix**
  - Urgente: reparos (vazamento, elétrica)
  - Importante: conforto (móvel novo, aquecimento)
  - Desejo: estético (arte, plantas, décor)

#### 4. Desenvolvimento Pessoal (Growth)
- **Seu Desenvolvimento (Vinicius)**
  - Fotografia: cursos (lighting, pós-produção)
  - Programação: new language ou deepdive?
  - Idiomas: mandarim commitment
  - Fitness: treino, esportes

- **Desenvolvimento Dela**
  - Carreira: cursos, certificações
  - Hobbies: dança, pintura, música?
  - Saúde: yoga, running, climbing?
  - Learning: idiomas, leitura?

- **Desenvolvimento Juntos**
  - Casal: comunicação, intimidade
  - Amizades: social life
  - Comunidade: voluntariado?
  - Espiritualidade: meditação, valores compartilhados?

---

### 🗓️ RITMO & CADÊNCIA

#### Semanal (15 min)
- [ ] Segunda: semana overview (o que vem?)
- [ ] Quarta: mid-week check (tudo ok?)
- [ ] Domingo: week review + próxima semana plan

#### Mensal (1 hora)
- [ ] 1o domingo: money date + finanças
- [ ] 2o domingo: projects review (lar, viagens)
- [ ] 3o domingo: growth & desenvolvimento pessoal
- [ ] 4o domingo: quality time + planejamento próximo mês

#### Trimestral (2-3 horas)
- [ ] Review: goals vs reality (acertamos?)
- [ ] Ajustes: pivotar ou continuar?
- [ ] Novo: novos goals pro trimestre?
- [ ] Celebração: wins do trimestre

---

### 📋 FERRAMENTAS RECOMENDADAS

- **Shared Calendar**
  - Google Calendar (eventos, compromissos)
  - Marca datas: viagens, aniversários, eventos

- **Budget Tracking**
  - Google Sheets (simples, compartilhado)
  - Notion (mais visual, database)
  - YNAB (app, mais sofisticado)

- **Board de Ideias**
  - Pinterest (viagens, decoração)
  - Miro (brainstorming visual)
  - Notion database (ideias, projetos)

- **Communication**
  - WhatsApp / Telegram (daily)
  - Notion shared space (projects, planning)
  - Calendar comments (context em eventos)

---

### 🎯 VALORES FUNDAMENTAIS

- **Partnership**
  - Decisões juntos (consenso, não comando)
  - Respeito mútuo (espaço pessoal também)
  - Suporte (goals dele/dela = priority)

- **Transparência**
  - Honestidade financeira
  - Comunicação proativa (não acumular ressentimento)
  - Feedback construtivo (não crítica)

- **Diversão**
  - Aventura regularmente
  - Risadas, leveza
  - Surpresas (romanticismo não morre)

---

## 🔗 CONEXÕES ENTRE PROJETOS

### Sinergia Possível
- **Horta → Planejamento Casal**
  - Colheita = meal planning juntos
  - Compost = ciclo de vida (life lessons?)
  - Projeto comum = teamwork

- **Desenvolvimento → Fotografia**
  - Portfolio web = showcase de fotos
  - 3D visualizations = produto showcase
  - Blog = documentar processos

- **Idiomas → Viagens**
  - Espanhol = viagens Latam
  - Mandarim = conversa com chineses
  - Francês = europeu charm

---

*Última atualização: 2026-05-18*
*Próxima revisão: 2026-06-15 (check-in trimestral)*
---
*Pai: [[_MOC-Pessoal]]*
