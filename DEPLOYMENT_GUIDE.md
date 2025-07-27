# NBA Stats Analysis - Deployment Guide

This guide covers deploying the NBA Stats Analysis React application to various platforms and environments.

## 🚀 Quick Deployment Options

### 1. Netlify (Recommended for Beginners)

**Steps:**
1. Push your code to GitHub
2. Go to [netlify.com](https://netlify.com) and sign up
3. Click "New site from Git"
4. Connect your GitHub repository
5. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `build`
6. Click "Deploy site"

**Environment Variables (Optional):**
```
REACT_APP_API_URL=https://your-backend-api.com
REACT_APP_ENVIRONMENT=production
```

### 2. Vercel (Fastest)

**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`

**Or use Vercel Dashboard:**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure build settings
4. Deploy automatically

### 3. GitHub Pages (Free)

**Steps:**
1. Install gh-pages: `npm install --save-dev gh-pages`
2. Add to package.json:
   ```json
   {
     "homepage": "https://yourusername.github.io/repo-name",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```
3. Deploy: `npm run deploy`

## 🔧 Production Build

### Local Build Testing
```bash
# Install dependencies
npm install

# Build for production
npm run build

# Test build locally
npx serve -s build
```

### Build Optimization
```bash
# Analyze bundle size
npm install --save-dev source-map-explorer
npm run build
npx source-map-explorer 'build/static/js/*.js'
```

## 🌐 Domain Configuration

### Custom Domain Setup

#### Netlify
1. Go to Site settings > Domain management
2. Add custom domain
3. Update DNS records as instructed

#### Vercel
1. Go to Project settings > Domains
2. Add your domain
3. Update DNS records

#### GitHub Pages
1. Go to repository Settings > Pages
2. Add custom domain
3. Create CNAME file in public folder

## 🔒 Environment Configuration

### Environment Variables

Create `.env.production` for production:
```env
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_ENVIRONMENT=production
REACT_APP_VERSION=1.0.0
REACT_APP_GA_TRACKING_ID=GA-XXXXXXXXX
```

### API Configuration

Update `package.json` proxy for development:
```json
{
  "proxy": "http://localhost:8000"
}
```

For production, ensure your API is deployed and accessible.

## 📊 Performance Optimization

### Build Optimization
```bash
# Generate production build
npm run build

# Analyze bundle
npm install --save-dev webpack-bundle-analyzer
npm run build
npx webpack-bundle-analyzer build/static/js/*.js
```

### Image Optimization
```bash
# Install image optimization
npm install --save-dev imagemin imagemin-webp

# Optimize images in public folder
npx imagemin public/images/* --out-dir=public/images/optimized
```

### Code Splitting
```javascript
// Lazy load components
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const PlayerAnalysis = React.lazy(() => import('./pages/PlayerAnalysis'));
```

## 🔍 Monitoring & Analytics

### Google Analytics
```javascript
// Add to index.html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

### Error Tracking (Sentry)
```bash
npm install @sentry/react @sentry/tracing
```

```javascript
// In index.js
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 1.0,
});
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
# Build stage
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Compose
```yaml
version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "80:80"
    depends_on:
      - backend
  backend:
    build: ./backend
    ports:
      - "8000:8000"
```

## ☁️ Cloud Platform Deployment

### AWS S3 + CloudFront
```bash
# Install AWS CLI
aws configure

# Create S3 bucket
aws s3 mb s3://your-app-bucket

# Upload build files
aws s3 sync build/ s3://your-app-bucket --delete

# Create CloudFront distribution
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

### Google Cloud Platform
```bash
# Install gcloud CLI
gcloud auth login

# Deploy to App Engine
gcloud app deploy app.yaml
```

### Microsoft Azure
```bash
# Install Azure CLI
az login

# Deploy to Static Web Apps
az staticwebapp create --name your-app --source https://github.com/username/repo
```

## 🔧 CI/CD Pipeline

### GitHub Actions
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v1.2
        with:
          publish-dir: './build'
          production-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from GitHub Actions"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

### GitLab CI
```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - npm ci
    - npm test

build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - build/

deploy:
  stage: deploy
  script:
    - npm install -g netlify-cli
    - netlify deploy --dir=build --prod
  only:
    - main
```

## 🔒 Security Considerations

### HTTPS Configuration
- Enable HTTPS on all platforms
- Configure HSTS headers
- Use secure cookies

### Content Security Policy
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'unsafe-inline' https://www.googletagmanager.com;
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
               font-src 'self' https://fonts.gstatic.com;">
```

### Environment Variables
- Never commit `.env` files
- Use platform-specific secret management
- Rotate API keys regularly

## 📊 Performance Monitoring

### Web Vitals
```javascript
// Add to index.js
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  // Send to your analytics service
  console.log(metric);
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

### Lighthouse CI
```bash
npm install -g @lhci/cli

# Add to package.json scripts
"lhci": "lhci autorun"
```

## 🚨 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check for missing dependencies
npm audit fix
```

#### Deployment Issues
- Check build logs for errors
- Verify environment variables
- Ensure API endpoints are accessible
- Check CORS configuration

#### Performance Issues
- Optimize images
- Enable gzip compression
- Use CDN for static assets
- Implement lazy loading

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review build logs
3. Test locally first
4. Contact platform support

---

**Happy Deploying! 🚀**