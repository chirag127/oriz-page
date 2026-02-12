# Oriz - Technology Solutions & Digital Services

A modern, professional static website for Oriz, showcasing our suite of utility websites and digital services.

## 🚀 Features

- **Modern Design**: Clean, professional aesthetic with smooth animations
- **Fully Responsive**: Optimized for all devices (desktop, tablet, mobile)
- **TypeScript**: Type-safe code for better maintainability
- **Fast Performance**: Built with Vite for lightning-fast builds
- **SEO Optimized**: Comprehensive meta tags and semantic HTML
- **Cloudflare Pages Ready**: Optimized for deployment on Cloudflare Pages

## 🛠️ Tech Stack

- **TypeScript** - Type-safe JavaScript
- **Vite** - Next-generation frontend tooling
- **CSS3** - Modern styling with CSS variables
- **HTML5** - Semantic markup

## 📦 Products Showcased

1. **Fin Suite** (fin.oriz.in) - Financial tools and calculators
2. **Dev Suite** (dev.oriz.in) - Developer tools and utilities
3. **Velvet** - Adult content platform
4. **Office Suite** - Office file management tools
5. **Pixel** - Image processing and manipulation tools
6. **Utility Tools** (tools.oriz.in) - Collection of web utilities

## 🏃 Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd oriz
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The site will be available at `http://localhost:3000`

## 🔨 Build

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

To preview the production build locally:

```bash
npm run preview
```

## 🌐 Deployment to Cloudflare Pages

### Method 1: Git Integration (Recommended)

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
3. Go to **Pages** → **Create a project**
4. Connect your Git repository
5. Configure build settings:
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `/` (or leave empty)
6. Click **Save and Deploy**

### Method 2: Direct Upload

1. Build the project locally:
```bash
npm run build
```

2. Install Wrangler CLI:
```bash
npm install -g wrangler
```

3. Login to Cloudflare:
```bash
wrangler login
```

4. Deploy to Cloudflare Pages:
```bash
wrangler pages deploy dist --project-name=oriz
```

### Environment Variables

No environment variables are required for this static site.

### Custom Domain

To add a custom domain (oriz.in):

1. Go to your Cloudflare Pages project
2. Navigate to **Custom domains**
3. Click **Set up a custom domain**
4. Enter your domain name
5. Follow the DNS configuration instructions

## 📁 Project Structure

```
oriz/
├── public/              # Static assets
│   └── favicon.svg      # Site favicon
├── src/                 # Source files
│   ├── main.ts          # Main TypeScript file
│   └── style.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
├── _headers             # Cloudflare Pages headers
├── _redirects           # Cloudflare Pages redirects
└── README.md            # This file
```

## 🎨 Customization

### Colors

Edit CSS variables in `src/style.css`:

```css
:root {
  --primary-color: #2563eb;
  --secondary-color: #8b5cf6;
  /* ... more variables */
}
```

### Products

Edit the products array in `src/main.ts`:

```typescript
const products: Product[] = [
  {
    name: 'Your Product',
    description: 'Product description',
    url: 'https://your-url.com',
    category: 'utility',
    icon: '🚀'
  }
]
```

## 🔒 Security Headers

The site includes security headers configured in `_headers`:
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy
- Permissions-Policy

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📄 License

Copyright © 2024 Oriz. All rights reserved.

## 🤝 Contributing

This is a private project for Oriz. For inquiries, please contact the development team.

## 📞 Support

For support or questions, please contact the Oriz team.

---

Built with ❤️ by Oriz
