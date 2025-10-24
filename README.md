# Memorial Pages (Ultra-light GitHub Pages)

Super-light, mobile-friendly memorial pages. One tiny static page per person. A semi-hidden index (`map.html`) lists all memorials and locations; only link to it from individual pages so guests discover it after finding a memorial.

## Publish on GitHub Pages
1. Create a new repo (public).
2. Upload this root folder.
3. In **Settings → Pages**, set **Source** = Deploy from a branch; **Branch** = `main`; **Folder** = `/docs`.
4. Site will appear at: `https://<username>.github.io/<repo>/`

### URLs
- Person page: `/people/<slug>/`
- Map page: `/map.html`

## Add a Person
1. Create `docs/people/<slug>/`
2. Copy `docs/people/example-one/index.html` into it.
3. Put 1–3 images into `docs/assets/` (1200px width, WebP or JPEG).
4. Update the `<img>` path + text.
5. Add the person to `docs/map.html`.

## Optional: QR Codes
Use `tools/generate_qr.py` locally to batch-generate PNGs for each person page URL.

**Privacy**: No analytics, no cookies. `noindex` on map & person pages.
