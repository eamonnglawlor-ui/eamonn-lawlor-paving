# Eamonn Lawlor Paving & Groundworks

Static website for Eamonn Lawlor Paving & Groundworks, Dooradoyle, Co. Limerick. Plain HTML and CSS. The gallery lightbox is the only JavaScript. There is no build step.

## Preview

From the repository root:

```bash
python3 -m http.server 8080
```

Open http://localhost:8080/

## Deploy

Publish the repository root as-is.

- **Netlify:** build command empty (no build command), publish directory = repository root.
- **Cloudflare Pages:** build command empty, build output / publish directory = repository root.
- **GitHub Pages:** serve from the repository root (main branch, root folder).

## Domain placeholder

Canonical URLs, Open Graph tags, JSON-LD, `sitemap.xml` and `robots.txt` use `https://www.eamonnlawlorpaving.ie`.

That domain has not been bought for this project. Replace it in those files before the site goes live. Each page also has an HTML comment marking the placeholder.

## Other placeholders

- Service area copy says “Limerick and surrounding areas”, with the HTML comment `<!-- PLACEHOLDER: confirm service area with Eamonn -->` beside it.
- Job photographs were not in this workspace (`uploads/site-assets.tar.gz` was missing), so none are published. Do not fill the gallery with stock photos. When the real photos are available, resize the long edge to about 1600px and make about 600px thumbnails, as JPEG and WebP, and add `width`, `height` and `loading="lazy"` (the hero can stay eager).
- The accent orange is `#D9822B`, the approximate card colour supplied with the brief. The business-card photographs were not in the workspace, so the colour was not sampled from those files, and the card photos are not in the repo.

## Content

Only details supplied for the business are used: name, phone, email, the card tagline, Facebook, Dooradoyle, and the service list. There is no review section, no prices, and no contact or quote form.
