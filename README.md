# Insight Evaluation Website

## Site Structure

```
├── index.html          # Home page
├── about-us.html       # About Us page
├── services.html       # Services page
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   └── script.js       # JavaScript (carousel, mobile menu)
└── images/             # All images (optimized)
```

## GitHub Pages Setup

Already configured! But if you need to set up again:

1. Go to repository Settings → Pages
2. Source: Deploy from `main` branch, `/ (root)` folder
3. Custom domain: `insighteval.com`
4. Enforce HTTPS: Enabled

### DNS Configuration

Point your domain to GitHub Pages with these records:

**A Records** (for apex domain `insighteval.com`):
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**CNAME Record** (for www subdomain):
```
www → [your-github-username].github.io
```
