# ◈ Oriz

**Technology Company — Building the Utility Web**

[![Cloudflare Pages](https://img.shields.io/badge/Deployed%20on-Cloudflare%20Pages-F38020?logo=cloudflare&logoColor=white)](https://oriz.in)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-6-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Oriz builds powerful utility websites and services — from financial calculators to developer toolkits and custom business solutions.

🌐 **Live**: [oriz.in](https://oriz.in)

---

## 🚀 Products

| Product | Domain | Description |
|---------|--------|-------------|
| **FinSuit** | [fin.oriz.in](https://fin.oriz.in) | Comprehensive suite of financial calculators — EMI, SIP, tax planning, currency conversion, retirement planning |
| **DevSuit** | [dev.oriz.in](https://dev.oriz.in) | Developer utility toolkit — JSON/XML formatters, regex testers, encoders/decoders, color pickers, code minifiers |

## 🛠️ Services

- **Web Development** — Custom websites and web applications with modern frameworks
- **Utility Platforms** — Purpose-built calculators, converters, and interactive tools
- **Progressive Web Apps** — Offline-capable, installable web experiences
- **API Development** — Scalable RESTful APIs with developer-friendly documentation
- **SEO & Performance** — Core Web Vitals optimization and technical SEO audits
- **Cloud Deployment** — Edge-deployed apps on Cloudflare, AWS, and Vercel

## ⚙️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | TypeScript, React, Vite, Next.js, HTML5, CSS3 |
| **Backend** | Node.js, Python, FastAPI, Express, REST APIs |
| **Infrastructure** | Cloudflare Pages, Cloudflare Workers, GitHub Actions, Docker, Vercel |
| **Tools** | Git, ESLint, Prettier, Vitest, Playwright |

## 📁 Project Structure

```
oriz/
├── index.html            # Main HTML — single-page layout with SEO meta tags
├── src/
│   ├── main.ts           # TypeScript entry — nav, scrolling, animations
│   ├── style.css         # Design system — dark theme, glassmorphism, responsive
│   └── vite-env.d.ts     # Vite type references
├── public/
│   ├── favicon.svg       # Gradient SVG favicon
│   ├── robots.txt        # Crawler rules
│   └── _headers          # Cloudflare Pages headers (caching + security)
├── ops/
│   ├── config.py         # Centralized deployment configuration
│   ├── build.py          # Build utilities (build, clean, validate)
│   ├── deploy_all.py     # Multi-platform deployment orchestrator
│   ├── deploy_cf.py      # Cloudflare Pages deployment
│   ├── deploy_netlify.py # Netlify deployment (CLI + API fallback)
│   ├── deploy_vercel.py  # Vercel deployment
│   ├── deploy_surge.py   # Surge.sh deployment
│   ├── deploy_neocities.py # Neocities deployment (API batch upload)
│   ├── dns_cloudflare.py # Cloudflare DNS management
│   ├── dns_spaceship.py  # Spaceship DNS / nameserver management
│   ├── manage_files.py   # File analysis, integrity checks, backups
│   └── manage_email.py   # Email routing via Cloudflare Email Routing
├── vite.config.ts        # Vite build configuration
├── tsconfig.json         # TypeScript strict config
└── package.json          # Dependencies and scripts
```

## 🏁 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) ≥ 18
- npm ≥ 9

### Development

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000)
npm run dev
```

### Production Build

```bash
# Type-check and build
npm run build

# Preview production build
npm run preview
```

## ☁️ Deployment

### Cloudflare Pages

This project is optimized for **Cloudflare Pages** with:

- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Node.js version**: `18`

Security and caching headers are configured in [`public/_headers`](public/_headers).

### Manual Deploy

1. Push to the connected GitHub repository
2. Cloudflare Pages auto-deploys from the `main` branch
3. Custom domain `oriz.in` is configured via Cloudflare DNS

### Ops Scripts

The `ops/` directory contains Python deployment and management scripts. All scripts load credentials from `.env`.

```bash
# Install Python dependencies
pip install python-dotenv requests

# Deploy to all enabled platforms
python ops/deploy_all.py

# Deploy to individual platforms
python ops/deploy_cf.py           # Cloudflare Pages
python ops/deploy_netlify.py      # Netlify
python ops/deploy_vercel.py       # Vercel
python ops/deploy_surge.py        # Surge.sh
python ops/deploy_neocities.py    # Neocities

# DNS management
python ops/dns_cloudflare.py --list       # List DNS records
python ops/dns_cloudflare.py --setup      # Set up DNS for oriz.in
python ops/dns_cloudflare.py --email      # Set up email DNS records
python ops/dns_spaceship.py --domains     # List Spaceship domains
python ops/dns_spaceship.py --setup-cf-ns # Set Cloudflare nameservers
python ops/dns_spaceship.py --verify-ns   # Verify NS configuration

# File management
python ops/manage_files.py --analyze      # Analyze dist directory
python ops/manage_files.py --verify       # Verify build integrity
python ops/manage_files.py --checksums    # Generate SHA256 checksums
python ops/manage_files.py --clean        # Clean build artifacts
python ops/manage_files.py --backup       # Backup dist directory

# Email management (chiragsinghal127@gmail.com)
python ops/manage_email.py --setup        # Set up Cloudflare Email Routing
python ops/manage_email.py --list-rules   # List routing rules
python ops/manage_email.py --test         # Send test deployment report
```

## ✨ Features

- **Dark Theme** — Premium dark palette with purple-to-cyan gradient accents
- **Glassmorphism Cards** — Frosted-glass UI components with blur effects
- **Scroll Animations** — IntersectionObserver-based fade-in reveals
- **Mobile Responsive** — Hamburger menu and fluid layouts for all screen sizes
- **Smooth Scrolling** — Click-to-scroll navigation with header offset
- **Active Section Tracking** — Nav highlights current section on scroll
- **SEO Optimized** — Open Graph, Twitter Cards, semantic HTML, meta descriptions
- **Performance** — Minimal dependencies, tree-shaken, aggressively cached
- **Accessibility** — ARIA labels, keyboard navigation, reduced-motion support
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, Referrer-Policy

## 📄 License

MIT © [Oriz](https://oriz.in)
