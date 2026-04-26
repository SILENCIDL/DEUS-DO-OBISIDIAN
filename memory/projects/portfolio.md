# Project Portfolio

**Also known as:** Portfolio web, website, vinicius-site  
**Status:** Active - MVP Q2 2026  
**Goal:** Showcase visual work (photos, video, 3D) + blog + contact

---

## What It Is

Professional portfolio website combining:
- Photography gallery (esporte, video, produto, retrato)
- Case studies (detailed project breakdowns)
- Blog (técnica fotografia, development, learning)
- Contact + social links
- Clean, fast, SEO-optimized

---

## Critical Decision: Astro vs Next.js

### Astro (Static Site Generation)
- ✅ Fast (minimal JS)
- ✅ SEO out-of-box
- ✅ Perfect for portfolio (content-heavy)
- ✅ Good for blog
- ❌ Less dynamic (no real-time features)

**Best for:** Photo portfolio + blog (Vinicius use case)

### Next.js (React Framework)
- ✅ Fully dynamic
- ✅ Image optimization (next/image)
- ✅ Routing built-in
- ❌ More JS → slower initial load
- ❌ Overkill for static portfolio

**Best for:** E-commerce, dashboards, dynamic apps (not this project)

**DECISION:** Astro (pick this one and move forward)

---

## Sections & Content

### 1. Hero
- Frase catchy (10 seconds storytelling)
- Video or image full-width
- CTA: "View Portfolio" or "Let's Talk"

**Copy example:**
> "Storytelling through light. Photography + cinematography for brands and athletes."

### 2. Gallery (Filterable)
- Grid responsive (masonry desktop, stack mobile)
- Filters: Photography, Video, 3D, All
- Click → lightbox with EXIF data (nerdy)
- Hover → overlay with project title + camera/lens used

### 3. Case Studies
**Project 1: Sports Photography**
- Problem: Capture peak action moments
- Solution: 1/1000+ shutter, burst mode, positioning
- Result: Portfolio of 50+ hero shots

**Project 2: Corporate Video**
- Problem: Monotone corporate → cinematic story
- Solution: LOG grading, color harmony, pacing
- Result: 5-minute video, XYZ views

**Project 3: 3D Web Experience** (future)
- Problem: Static portfolio feels dated
- Solution: Three.js interactive showcase
- Result: Unique, memorable, differentiator

### 4. Blog
- **Post ideas:**
  - "Camera Settings for Sports Photography" (SEO target)
  - "Color Grading in Lightroom: Step-by-Step" (tutorial)
  - "Learning Mandarim While Building a Portfolio" (personal)
  - "Building a Web Portfolio with Astro" (technical)

### 5. Contact
- Email form (Formspree, getform, or contact@vinicius.com)
- Social links (Instagram, LinkedIn, GitHub)
- Availability calendar (Calendly? or "Email for inquiries")

---

## Technical Stack

**Framework:** Astro  
**Styling:** Tailwind CSS  
**Images:** Astro Image optimization  
**Hosting:** Netlify (free tier, auto-deploy from Git)  
**Domain:** vinicius.com or similar  
**Analytics:** Google Analytics 4  

---

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| LCP | < 2.5s | (TBD) |
| CLS | < 0.1 | (TBD) |
| FID | < 100ms | (TBD) |
| Lighthouse | 90+ | (TBD) |

---

## SEO Checklist

- [ ] Meta tags (title, description per page)
- [ ] Open Graph (image preview on social share)
- [ ] Sitemap.xml + robots.txt
- [ ] Canonical tags (avoid duplicates)
- [ ] Schema.org markup (structured data)
- [ ] Alt text on all images
- [ ] Mobile responsive
- [ ] Core Web Vitals optimized

---

## Timeline

**Week 1-2:** Design (Figma wireframes)  
**Week 3-4:** Setup Astro + basic template  
**Week 5-6:** Gallery + case studies  
**Week 7-8:** Blog setup + first 3 posts  
**Week 9:** Optimization + SEO  
**Week 10:** Deploy + launch  

---

## Analytics & Tracking

- [ ] Google Analytics 4 configured
- [ ] Track: page views, scroll depth, clicks (CTA)
- [ ] Conversion: "contact" form submissions
- [ ] Goals: 100 visitors/week → 1000/month by Q4

---

## Future Enhancements (Phase 2)

- [ ] 3D showcase (Three.js integration)
- [ ] Blog RSS feed (content distribution)
- [ ] Newsletter signup
- [ ] Dark mode toggle
- [ ] Multilingual (português, en, 中文?)
- [ ] Client testimonials section
- [ ] Pricing page (if offering services)

---

*Last updated: 2026-05-18*  
*Decision deadline: 2026-05-25 (Astro vs Next.js final call)*  
*MVP launch target: 2026-06-30*
