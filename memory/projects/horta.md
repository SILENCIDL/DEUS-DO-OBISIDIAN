# Project Horta (Garden Automation)

**Also known as:** Smart garden, irrigation automation, IoT project  
**Status:** Research → Build (Q2 2026)  
**Goal:** Fully automated vegetable garden with zero daily maintenance

---

## Why Horta?

- **Self-sufficiency:** Grow fresh food, reduce grocery bills
- **IoT learning:** Apply programming + hardware skills
- **Sustainability:** Compostagem (zero waste cycle)
- **Mental health:** Hobby that produces food
- **ROI:** ~2 years payback on $300-500 investment

---

## MVP Scope (First 3 Months)

### Hardware Target
- 1 raised garden bed (1m x 2m)
- 1 Arduino (microcontroller brain)
- 3-5 soil moisture sensors
- 1 solenoid valve (water control)
- 1 water pump (source → garden)
- 1 simple power supply (plug AC)

### Software Target
- Arduino firmware (threshold-based irrigation)
- Telegram bot (monitor + manual override)
- Simple logging (timestamp + sensor readings)

### Result
- Garden waters itself (threshold: 40-60% moisture)
- You check Telegram 1x/week for status
- Can manually trigger water if needed

---

## Phase 1: Hardware (Weeks 1-4)

### Decision: Arduino vs Raspberry Pi

| Aspect | Arduino | Raspberry Pi |
|--------|---------|--------------|
| **Learning curve** | Easy | Medium (Linux) |
| **Cost** | $20-50 | $35-60 |
| **Setup time** | 2 days | 1 week |
| **Expandability** | Shields + modules | GPIO + USB |
| **Overkill?** | No, perfect | Yes, too powerful |

**DECISION:** Arduino (pick this, proven)

### Bill of Materials (BOM) - MVP

| Item | Part | Cost | Notes |
|------|------|------|-------|
| **Controller** | Arduino Uno + WiFi shield (ESP8266) | $50 | Brain of system |
| **Sensors** | Capacitive soil moisture (x3) | $30 | Better than resistive (lasts longer) |
| **Actuators** | Solenoid 12V + pump kit | $80 | Water control |
| **Power** | 12V power supply + relay | $40 | Safe switching |
| **Misc** | Wires, breadboard, USB cable | $20 | Prototyping |
| **Structure** | Raised bed kit or wood | $100 | Physical garden |
| **Soil** | Compost + soil mix | $50 | Growing medium |

**Total MVP: ~$370-450**

### Suppliers (Brazil context)
- Mercado Livre (Arduino, sensors, relés)
- Eletrônicos (local electronics shop)
- Shopee (cheapest often)
- Amazon Brasil (if available)

### Assembly Checklist
- [ ] Arduino + ESP8266 connected
- [ ] Upload test sketch (blink LED)
- [ ] Sensor calibration (dry=0, wet=1023)
- [ ] Relay testing (pump triggers on signal)
- [ ] Power supply safe (no shorts, proper grounding)

---

## Phase 2: Software (Weeks 5-8)

### Arduino Firmware

```pseudocode
Setup:
  - Initialize sensors (pins)
  - Connect to WiFi
  - Initialize relay (output)

Loop (every 5 minutes):
  1. Read soil moisture (3 sensors, average)
  2. If average < threshold_min (40%):
     - Open valve for 10 minutes
     - Log event: [timestamp, moisture before, action]
  3. If moisture > threshold_max (70%):
     - Wait for evaporation (do nothing)
  4. Send status to cloud (if connected)
  5. Sleep 5 min (save power)
```

### Connectivity Options

**Option A: Telegram Bot (Simplest)**
- Arduino sends POST to Telegram API
- You get daily report: "Moisture 65%, all ok"
- Can reply "Water now!" for manual override
- No backend needed, free

**Option B: Local API (Obsidian Integration)**
- Arduino → home server (local network)
- Obsidian API receives + logs data
- Visible in Obsidian vault history
- Works offline

**Option C: Cloud Service (Blynk/Arduino Cloud)**
- Arduino Cloud native integration
- Web dashboard + phone app
- Real-time graphs
- Cost: free tier or $5-10/month

**DECISION:** Telegram Bot MVP (pick this, simplest) → upgrade to Obsidian integration Q3

### Thresholds (Tuning Required)

**Tomate:** 40-70% (needs consistent moisture)  
**Alface:** 60-80% (more water-loving)  
**Suculentas:** 20-40% (drought tolerant)  

Start with 50% threshold, adjust after 2 weeks of observation.

---

## Phase 3: Agronomia (Planting)

### Sazonalidade Mantiqueira

**Primavera (Sep-Nov): IDEAL**
- Temp 18-25°C (optimal)
- Plant: Tomate, berinjela, pimenta
- Harvest: 8-10 weeks in

**Verão (Dec-Feb): HOT**
- Temp 25-35°C (risky)
- Issues: Bolting (lettuce flowers), sunburn
- Solution: 50% shade cloth
- Plant: Milho, melancia, abóbora

**Outono (Mar-May): GOOD**
- Temp 18-24°C (cooling)
- Plant: Alface, brócolis, repolho
- Ideal replanting season

**Inverno (Jun-Aug): COLD**
- Temp 10-18°C (too cold for many)
- Plant: Brassicas (couve, brócolis)
- Optional: Grow lights for heat

### Initial Crops (Choose 2-3)

**Tomate (Long-cycle, High ROI)**
- Sementes: 80-90 dias till fruit
- Precisa: Stake/suporte (crescimento vertical)
- Issue: Blossom end rot (calcium deficiency)
- Yield: 5-10kg per plant per season
- Profit: ~$20/plant (vs $3 grocery)

**Alface (Quick, Easy, Repeatable)**
- Sementes: 30-45 dias
- Vantagem: Cut-and-come-again (harvest leaves continuously)
- Risco: Bolts in summer (goes to seed)
- Solution: Shade cloth or succession planting (new seeds every 2 weeks)
- Yield: 1-2kg per cycle per cama
- Profit: ~$5/cycle

**Ervas (Fast, High Market Value)**
- Manjericão: 30 dias, pesto heaven
- Cilantro: 45 dias, bold flavor
- Gengibre: 9-12 meses, perennial cash crop
- Profit: $10-20 per plant (retail herb = expensive)

### Compostagem (Cycle Closure)

**Input:** Kitchen scraps + garden waste  
**Output:** Rich soil amendment  

**Process:**
1. Pile 1m³ (ideal size)
2. Brown:Green ratio = 3:1 (carbono:nitrogen)
   - Browns: Dead leaves, straw, cardboard
   - Greens: Grass clippings, veggie scraps, coffee grounds
3. Moisture: 50-60% (like wrung-out sponge)
4. Aeration: Turn weekly (with fork or tumbler)
5. Timeline: 2-3 months → black gold

**Closed Loop:**
- Horta waste → Compost pile
- Compost ready → Back to horta soil
- Zero external input needed (after 1 cycle)

---

## Phase 4: Maintenance & Iteration

### Weekly Tasks (5 min)
- Check Telegram status (moisture, pump works?)
- Visual inspection (plants look healthy?)
- Remove weeds (if any)

### Monthly Tasks (30 min)
- Adjust threshold (if over/under watering)
- Add compost to soil (replace nutrients)
- Check for pests (inspect leaves)

### Seasonal Tasks
- Harvest (yay!)
- Replant (new season = new crops)
- Soil amendment (compost, nutrients)

---

## Phase 2 (6 months in): Expansion Ideas

### Escalabilidade Options

**Option A: Multi-zone Garden**
- 2 raised beds (different crops)
- Separate sensors per bed
- One Arduino controls both

**Option B: Hydroponic Upgrade**
- Water recirculation (use less water)
- Nutrient dosing (automated fertilizer)
- Higher yields per square foot

**Option C: Advanced Sensors**
- pH sensor (nutrient availability)
- Temperature (trigger shade cloth)
- Light sensor (detect day/night)

**Option D: Home Assistant Integration**
- Horta as device in smart home
- Automations: "If temp > 30°C, activate shade"
- Notifications: "Harvest ready!"

---

## Budget Breakdown

| Phase | Item | Cost |
|-------|------|------|
| **Phase 1** | Hardware + setup | $370-450 |
| **Phase 2** | Software (time only) | Free |
| **Phase 3** | Seeds + soil | $50 |
| **Ongoing** | Maintenance supplies | ~$5-10/month |
| **Phase 2 (6mo)** | Expansion hardware | $200-300 |

**Year 1 Total: ~$500-600**  
**Payback: ~2 years** (saving $200-300/year on groceries + emotional ROI)

---

## Success Metrics

### By End Q2 2026 (August)
- [ ] System assembled and tested
- [ ] First harvest (alface or ervas)
- [ ] Zero manual irrigation (fully automated)
- [ ] Telegram reporting working

### By End Q4 2026 (December)
- [ ] 50+ kg vegetables harvested
- [ ] $200+ saved on groceries
- [ ] System refined (thresholds dialed in)
- [ ] Compost cycle started

### By Mid 2027
- [ ] Scaled to 2+ beds
- [ ] Writing blog post about system
- [ ] Considering hydroponics upgrade

---

## Questions to Clarify

- [ ] Shed/gazebo space for equipment? (pump, controller placement)
- [ ] Water source? (hose, well, rain tank?)
- [ ] Sunlight hours? (6+ hours needed)
- [ ] Budget confirm? ($400-500 ok?)
- [ ] Start date? (Which season best?)

---

*Last updated: 2026-05-18*  
*Hardware research deadline: 2026-05-25*  
*Build start target: 2026-06-01*  
*First harvest target: 2026-07-15*
