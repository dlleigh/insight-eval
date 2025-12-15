# Insight Evaluation Website

High-fidelity reproduction of the Insight Evaluation consulting website, rebuilt as a modern, mobile-responsive static site for self-hosting on GitHub Pages.

## Overview

This is a complete reproduction of insighteval.com, originally built with HostGator's Gator website builder. The site has been rebuilt using clean HTML5, CSS3, and vanilla JavaScript to be:

- **Pixel-perfect** - Matches the original design exactly
- **Mobile-responsive** - Fully functional on all device sizes
- **Self-hosted** - Free hosting on GitHub Pages
- **Easy to maintain** - Simple, clean code with no frameworks

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

## Features

- **3 pages**: Home, About Us, Services
- **Responsive design**: Works on desktop, tablet, and mobile
- **Testimonials carousel**: 5 testimonials with prev/next navigation and touch swipe support
- **Mobile menu**: Hamburger menu for small screens
- **Smooth scrolling**: Anchor links smoothly scroll to sections
- **Optimized images**: All images compressed for fast loading

## Design Specifications

### Colors
- Dark Blue: `#015B90`
- Light Blue: `#80ADCC`
- Orange: `#E27939`
- Dark Gray: `#474747`
- Text Gray: `#787878`

### Typography
- **Open Sans**: Navigation, headings
- **Questrial**: Hero titles, service names
- **Raleway**: Body text, testimonials
- **Nixie One**: Services section title

All fonts loaded via Google Fonts CDN.

### Layout
- Desktop content width: 814px
- Header height: 143px (fixed)
- Mobile-first responsive design
- Breakpoints: 768px (mobile), 1024px (tablet)

## How to Update the Site

### Editing Content

1. **Text changes**: Edit the HTML files directly
   - `index.html` - Home page content
   - `about-us.html` - About page, team bios, values
   - `services.html` - Service descriptions

2. **Style changes**: Edit `css/style.css`
   - Colors are defined as CSS variables at the top
   - Responsive breakpoints at bottom of file

3. **Images**: Replace files in `images/` folder with same filenames

### Adding a Testimonial

In `index.html`, find the testimonials section and add:

```html
<div class="testimonial">
  <p class="testimonial-quote">"Your testimonial text here."</p>
  <p class="testimonial-author">Name</p>
  <p class="testimonial-org">Organization</p>
</div>
```

### Deployment

Changes are automatically deployed when you push to the `main` branch:

```bash
git add .
git commit -m "Update content"
git push origin main
```

Site will update at https://insighteval.com within 1-2 minutes.

## Local Development

To test changes locally before deploying:

1. Simply open `index.html` in your browser
2. Or use a local server:
   ```bash
   python3 -m http.server 8000
   ```
   Then visit http://localhost:8000

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

## Browser Support

- Chrome/Edge (modern versions)
- Firefox (modern versions)
- Safari (desktop and iOS)
- Mobile browsers (iOS Safari, Chrome Android)

## Cost Savings

- **Previous hosting (HostGator)**: ~$200-300/year
- **GitHub Pages hosting**: **FREE**
- **Annual savings**: $200-300

## Technical Details

- Pure HTML5/CSS3/JavaScript (no frameworks)
- No build process required
- CSS Grid and Flexbox for layouts
- Font Awesome 6 for icons
- Touch-optimized for mobile devices
- Semantic HTML for accessibility
- Optimized images (~32MB total)

## Support

For questions or issues:
- Check the code comments in HTML/CSS/JS files
- Open an issue in this GitHub repository
- Email: info@insighteval.com

---

**Last updated**: December 2025
**Built with**: High-fidelity reproduction from original site
