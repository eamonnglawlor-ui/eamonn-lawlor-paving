# Eamonn Lawlor Paving & Groundworks

Static website for Eamonn Lawlor Paving & Groundworks in Limerick. Plain HTML and CSS. The gallery lightbox is the only JavaScript. There is no build step.

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
- The accent orange is `#B6703F`, sampled from the orange diamond on the business-card logo. The card photographs are not in the published site.
- Job photographs are the optimised JPEG and WebP files in `images/full` (long edge at most 1600px) and `images/thumbs` (long edge 600px).

## Content

Details used are the ones supplied for the business: name, phone, email, the card tagline, Facebook, Limerick, 25 years of experience, and the service list, including resin bound interiors and microcement floors. There is no review section, no prices, and no contact or quote form. The gallery has no interior or microcement photographs, because none of the supplied photos show those floors.
