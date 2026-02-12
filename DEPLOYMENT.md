# Deployment Guide for Oriz Website

This guide provides detailed instructions for deploying the Oriz website to Cloudflare Pages.

## Prerequisites

- A Cloudflare account
- Git repository (GitHub, GitLab, or Bitbucket)
- Node.js 18+ installed locally (for testing)

## Build Configuration

The project is configured with the following build settings:

- **Build Command**: `npm run build`
- **Build Output Directory**: `dist`
- **Node Version**: 18 or higher

## Deployment Methods

### Method 1: Git Integration (Recommended)

This method automatically deploys your site whenever you push to your repository.

#### Step 1: Push to Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Oriz website"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

#### Step 2: Connect to Cloudflare Pages

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **Pages** in the sidebar
3. Click **Create a project**
4. Select **Connect to Git**
5. Choose your Git provider (GitHub, GitLab, or Bitbucket)
6. Authorize Cloudflare to access your repositories
7. Select the `oriz` repository

#### Step 3: Configure Build Settings

On the build configuration page, enter:

- **Project name**: `oriz` (or your preferred name)
- **Production branch**: `main`
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Root directory**: `/` (leave empty or use `/`)

#### Step 4: Environment Variables

No environment variables are required for this static site.

#### Step 5: Deploy

1. Click **Save and Deploy**
2. Cloudflare will build and deploy your site
3. You'll receive a `*.pages.dev` URL

### Method 2: Direct Upload via Wrangler CLI

Use this method for manual deployments or CI/CD pipelines.

#### Step 1: Install Wrangler

```bash
npm install -g wrangler
```

#### Step 2: Authenticate

```bash
wrangler login
```

This will open a browser window for authentication.

#### Step 3: Build the Project

```bash
npm run build
```

#### Step 4: Deploy

```bash
wrangler pages deploy dist --project-name=oriz
```

For subsequent deployments:

```bash
npm run build && wrangler pages deploy dist --project-name=oriz
```

### Method 3: Direct Upload via Dashboard

#### Step 1: Build Locally

```bash
npm run build
```

#### Step 2: Upload to Cloudflare

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **Pages**
3. Click **Create a project**
4. Select **Upload assets**
5. Enter project name: `oriz`
6. Drag and drop the `dist` folder or click to browse
7. Click **Deploy site**

## Custom Domain Configuration

### Adding oriz.in Domain

#### Step 1: Access Custom Domains

1. Go to your Cloudflare Pages project
2. Click on the **Custom domains** tab
3. Click **Set up a custom domain**

#### Step 2: Add Domain

1. Enter `oriz.in`
2. Click **Continue**

#### Step 3: Configure DNS

If your domain is already on Cloudflare:
- DNS records will be automatically configured
- A CNAME record will be created pointing to your Pages project

If your domain is not on Cloudflare:
1. Add a CNAME record in your DNS provider:
   - **Name**: `@` (or leave empty for root domain)
   - **Value**: `<your-project>.pages.dev`
   - **TTL**: Auto or 3600

2. For www subdomain, add another CNAME:
   - **Name**: `www`
   - **Value**: `<your-project>.pages.dev`
   - **TTL**: Auto or 3600

#### Step 4: Verify

- DNS propagation may take up to 24 hours
- Check status in Cloudflare Pages dashboard
- Test your domain once active

## Continuous Deployment

With Git integration, every push to your main branch triggers an automatic deployment:

1. Make changes to your code
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update website"
   git push
   ```
3. Cloudflare automatically builds and deploys

### Preview Deployments

- Every pull request gets a unique preview URL
- Test changes before merging to production
- Preview URLs are automatically generated

## Build Optimization

The project includes several optimizations:

### Performance
- Minified JavaScript and CSS
- Optimized asset loading
- Efficient caching headers

### Security
- Security headers configured in `_headers`
- XSS protection
- Content type sniffing prevention
- Frame options configured

### SEO
- Semantic HTML structure
- Meta tags for social sharing
- Sitemap.xml included
- Robots.txt configured

## Monitoring and Analytics

### Cloudflare Analytics

1. Go to your Pages project
2. Click on **Analytics** tab
3. View:
   - Page views
   - Unique visitors
   - Bandwidth usage
   - Geographic distribution

### Adding Custom Analytics

To add Google Analytics or other services:

1. Edit `index.html`
2. Add tracking script in the `<head>` section
3. Commit and push changes

## Troubleshooting

### Build Fails

**Issue**: Build command fails
**Solution**:
- Check Node.js version (must be 18+)
- Verify all dependencies are in `package.json`
- Review build logs in Cloudflare dashboard

### Assets Not Loading

**Issue**: CSS or JS files return 404
**Solution**:
- Verify `dist` directory contains all files
- Check `_headers` file is in dist directory
- Clear browser cache

### Custom Domain Not Working

**Issue**: Domain shows error or doesn't load
**Solution**:
- Verify DNS records are correct
- Wait for DNS propagation (up to 24 hours)
- Check SSL/TLS settings in Cloudflare

### TypeScript Errors

**Issue**: Build fails with TypeScript errors
**Solution**:
- Run `npm run build` locally to see errors
- Fix type errors in source files
- Ensure `tsconfig.json` is properly configured

## Rollback

To rollback to a previous deployment:

1. Go to Cloudflare Pages dashboard
2. Click on your project
3. Navigate to **Deployments** tab
4. Find the previous successful deployment
5. Click **...** menu → **Rollback to this deployment**

## Performance Tips

1. **Enable Cloudflare CDN**: Automatically enabled with Pages
2. **Use Cloudflare Images**: For optimized image delivery
3. **Enable Brotli Compression**: Automatically enabled
4. **Monitor Core Web Vitals**: Use Cloudflare Analytics

## Security Best Practices

1. **Keep Dependencies Updated**: Run `npm audit` regularly
2. **Review Security Headers**: Check `_headers` file
3. **Enable HTTPS**: Automatically enabled with Cloudflare
4. **Use Cloudflare WAF**: Available with paid plans

## Support

For issues or questions:
- Check [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- Visit [Cloudflare Community](https://community.cloudflare.com/)
- Contact Oriz development team

## Useful Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Deploy with Wrangler
wrangler pages deploy dist --project-name=oriz
```

---

Last Updated: 2024