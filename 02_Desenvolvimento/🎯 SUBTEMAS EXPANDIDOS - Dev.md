# 💻 SUBTEMAS EXPANDIDOS - Desenvolvimento
## Full-stack thinking: web + 3D + automation

---

## 🌐 PORTFÓLIO WEB

### Decisões Arquiteturais
- **Astro** (Static Site Generation)
  - ✅ Pros: fast, minimal JS, SEO out-of-box
  - ❌ Cons: menos dinâmico, learning curve
  - Use case: portfolio fotografo (content-heavy)
  
- **Next.js** (React framework)
  - ✅ Pros: full dynamic, image optimization, routing
  - ❌ Cons: mais JS no cliente, mais complex
  - Use case: blog com backend, e-commerce

### Estrutura Esperada
- **Home/Hero**
  - Frase catchy (storytelling em 10 segundos)
  - Video/imagem full-width (autoplay, muted)
  - CTA principal (portfolio, contact, blog)

- **Galeria Filtrada**
  - Grid responsivo (masonry em desktop, stack mobile)
  - Filtros por categoria (fotografia, video, 3D)
  - Lightbox ou modal com EXIF (nerd flex)

- **Case Studies**
  - Projeto 1: evento esportivo (problema → solução → resultado)
  - Projeto 2: video corporativo (brief → processo → deliverable)
  - Projeto 3: 3D web experience (conceito → técnica → interação)

- **Blog**
  - Post sobre fotografia técnica
  - Post sobre development deep-dive
  - Post sobre learning idiomas

- **Contact**
  - Email form (Formspree, getform)
  - Social links (Instagram, LinkedIn, Github)
  - Availability calendar? (Calendly embed)

### Performance & SEO
- **Core Web Vitals**
  - LCP (Largest Contentful Paint) < 2.5s
    - Lazy load images below fold
    - Minimize CSS/JS
    - Compress media
  
  - CLS (Cumulative Layout Shift) < 0.1
    - Reservar espaço para imagens (aspect ratio)
    - Evitar inserts dinâmicos acima do fold
  
  - FID (First Input Delay) < 100ms
    - Minimizar JavaScript bloqueante
    - Code splitting

- **SEO Checklist**
  - Meta tags (title, description)
  - Open Graph (Twitter card, LinkedIn preview)
  - Sitemap.xml + robots.txt
  - Canonical tags (evitar duplicatas)
  - Schema.org (structured data para GoogleBot)

### Analytics & Tracking
- **Google Analytics 4**
  - Track page views
  - Scroll depth (engagement)
  - Click events (CTA tracking)
  - Conversion funnel (visit → contact)

---

## 🔧 AUTOMAÇÕES & INTEGRAÇÕES

### Obsidian API REST Local
- **Setup**
  - Instalação de plugin (JSON API ou similar)
  - Permitir conexões localhost
  - Autenticação token ou aberta?

- **Endpoints CRUD**
  - GET /vault (listar todas notas)
  - POST /create (nova nota)
  - PUT /note/{id} (editar)
  - DELETE /note/{id} (arquivar/remover)

- **Use cases**
  - Auto-backup para Git
  - Sync com Anki (flashcard generation)
  - Publicar notas no blog (Obsidian → static site)
  - Webhooks para eventos (nova nota → Slack notification)

### Scripts Automation
- **Shell (Bash/Zsh)**
  - Batch processing (resize images, convert formats)
  - Backup automation (rsync, git commits)
  - Daily tasks (check emails, pull data)
  
- **Python**
  - Data manipulation (CSV → structured data)
  - Image processing (pillow, opencv)
  - Web scraping (beautifulsoup, selenium)
  - ML basics (classification, recommendation)
  
- **Node.js/JavaScript**
  - API integrations (fetch from multiple sources)
  - File system tasks
  - Scheduled jobs (node-cron)

### Fluxos Específicos
- **Import de Dados**
  - CSV de cliente → parsed → CRM
  - API dados meteorológicos → horta automação
  - Feed RSS → agregador pessoal

- **Processamento de Fotos**
  - Batch rename (por date/event)
  - Redimensionar para web
  - Gerar thumbs e WebP
  - Upload para cloud com retry logic

---

## 🎮 SOFTWARE 3D

### Blender Fundamentals
- **Modeling**
  - Low-poly vs high-poly (performance vs detail)
  - Modifiers (array, mirror, bevel, boolean)
  - Sculpting (organic shapes)
  
- **Materials & Texturing**
  - PBR workflow (diffuse, normal, roughness, metallic)
  - Shader nodes (principled BSDF, mix)
  - UV mapping e unwrapping
  
- **Lighting**
  - Three-point lighting (key, fill, back)
  - HDRI (environment lighting)
  - Shadows (sharp vs soft)
  
- **Rendering**
  - Cycles (foto-realista, lento)
  - Eevee (tempo-real, fast)
  - Passes (beauty, normal, ID, AO)

### WebGL/Three.js Pipeline
- **Conversão Blender → Web**
  - Export .glb/.gltf (formato web-friendly)
  - Otimizar geometria (reduce polys)
  - Texture baking (se necessário)
  
- **Three.js Implementation**
  - Scene setup (camera, renderer, lights)
  - Load model (GLTFLoader)
  - Material override (customizar aparência no web)
  - Interação (mouse, touch, keyboard)
  
- **Performance Optimization**
  - LOD (Level of Detail) para modelos complexos
  - Frustum culling (não renderizar fora de câmera)
  - Instancing (repetir geometria)
  - Lazy loading (carregar modelo on-demand)

### Portfolio 3D Showcase
- **Exemplos de projeto**
  - Visualização de produto (rotação, zoom)
  - Ambiente explorable (first-person, third-person)
  - Data visualization 3D (grafo de conhecimento?)
  - Generative art (algorítmico, variação por seed)

---

## 📚 STACK TÉCNICO PROFUNDO

### JavaScript/TypeScript
- **Async Patterns**
  - Promises (then/catch)
  - Async/await (mais legível)
  - Promise.all (paralelismo)
  
- **ES6+ Features**
  - Arrow functions, destructuring
  - Spread operator
  - Template literals
  - Class vs function components
  
- **Testing**
  - Jest (unit tests)
  - Testing Library (component tests)
  - E2E (Playwright, Cypress)

### Python Deep Dives
- **Data Science Stack**
  - Pandas (dataframes, manipulation)
  - NumPy (arrays, math)
  - Matplotlib/Seaborn (visualization)
  - Scikit-learn (basic ML)
  
- **Automation**
  - Requests (HTTP calls)
  - BeautifulSoup (parsing HTML)
  - Selenium (browser automation)
  - Schedule (recurring tasks)

### CSS & Design
- **Tailwind Mastery**
  - Utility-first mindset
  - Custom config (colors, spacing)
  - Responsive classes (sm:, md:, lg:)
  - Dark mode support
  
- **Responsive Design**
  - Mobile-first approach
  - Breakpoints e media queries
  - Flexbox vs Grid
  - Container queries (novo!)
  
- **Animations**
  - CSS transitions
  - Keyframes
  - GSAP library (complex animations)
  - Lottie (JSON animations)

---

## 🎯 ROADMAP DESENVOLVIMENTO

### Q2 2026
- [ ] Finalizar design portfólio (Figma)
- [ ] Setup Astro project
- [ ] Galeria base + filtering

### Q3 2026
- [ ] Blog posts (3x)
- [ ] Case studies escritos
- [ ] Deploy e otimização SEO

### Q4 2026
- [ ] Explorar Blender + Three.js
- [ ] Prototype 3D showcase
- [ ] Obsidian API automation POC

---

*Última atualização: 2026-05-18*
---
*Pai: [[_MOC-Tech]]*
