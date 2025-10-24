#!/usr/bin/env python3
import csv, sys, re, unicodedata
from pathlib import Path
from html import escape

# ---------- Site Text ----------
FOOTER_LINE = "Family memorials for Clarissa and Robert’s wedding on 10/25/2025 at Camp Pinnacle in Flat Rock, NC."
MAP_TITLE = "Memorials & Locations"
MAP_INTRO = (
    "These are family memorials created for Clarissa and Robert’s wedding at Camp Pinnacle. "
    "Walk the camp to find each memorial. Every page includes a few images and a short reflection."
)

# ---------- Paths ----------
REPO_ROOT = Path(__file__).resolve().parent
DOCS = REPO_ROOT / "docs"
CSV_DEFAULT = DOCS / "memorials_completed_with_images.csv"
PEOPLE = DOCS / "people"
ASSETS = DOCS / "assets"

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s

def read_rows(csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            name = (row.get("name") or "").strip()
            if not name:
                continue
            # Collect up to 4 non-blank images; no auto-extension
            imgs = []
            for i in range(1,5):
                p = (row.get(f"image{i}") or "").strip()
                a = (row.get(f"image{i}_alt") or "").strip()
                if p:
                    imgs.append((p, a))
            yield {
                "name": name,
                "slug": (row.get("slug(optional)") or "").strip() or slugify(name),
                "years": (row.get("years") or "").strip(),
                "location": (row.get("location") or "").strip(),
                "story": (row.get("story") or "").strip(),
                "images": imgs,
            }

def ensure_dirs():
    DOCS.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    PEOPLE.mkdir(exist_ok=True)

PAGE_TMPL = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>In Memory of {title}</title>
  <meta name="description" content="A short remembrance of {desc}.">
  <link rel="stylesheet" href="../../assets/style.css">
  <meta name="robots" content="noindex,follow">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header>
    <h1>In Memory of {title}</h1>
  </header>
  <main id="content">
    {years_html}
    {images_html}
    {story_html}
    <p class="small"><a href="../../map.html">Back to memorials &amp; locations</a></p>
  </main>
  <footer>
    <p class="small">{footer_line}</p>
  </footer>
</body>
</html>
"""

def build_images_html(images):
    # Only render provided images (skip blanks)
    tags = []
    for path, alt in images:
        alt_attr = escape(alt) if alt else "Memorial photo"
        tags.append(f'<figure><img src="../../{escape(path)}" alt="{alt_attr}" loading="lazy" decoding="async"></figure>')
    return "\n    ".join(tags)

def build_story_html(story):
    if not story:
        return ""
    parts = [escape(p.strip()) for p in story.splitlines() if p.strip()]
    if not parts:
        return ""
    return "\n    ".join(f"<p>{p}</p>" for p in parts)

def write_page(row):
    slug = row["slug"]
    out_dir = PEOPLE / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    years_html = f'<p class="small">{escape(row["years"])}</p>' if row["years"] else ""
    images_html = build_images_html(row["images"])
    story_html = build_story_html(row["story"]) or ""

    html = PAGE_TMPL.format(
        title=escape(row["name"]),
        desc=escape(row["name"]),
        years_html=years_html,
        images_html=images_html,
        story_html=story_html,
        footer_line=escape(FOOTER_LINE)
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    return slug

def write_map(rows):
    items = []
    for row in rows:
        name = escape(row["name"])
        slug = row["slug"]
        loc = escape(row["location"]) if row["location"] else ""
        loc_div = f'<div class="small">Location: {loc}</div>' if loc else ""
        items.append(f"""<li>
        <strong><a href="./people/{slug}/">{name}</a></strong>
        {loc_div}
      </li>""")

    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>{MAP_TITLE}</title>
  <meta name="description" content="Family memorials for Clarissa and Robert’s wedding at Camp Pinnacle.">
  <link rel="stylesheet" href="./assets/style.css">
  <meta name="robots" content="noindex,follow">
</head>
<body>
  <header>
    <h1>{MAP_TITLE}</h1>
    <p class="small">{MAP_INTRO}</p>
  </header>
  <main>
    <ul class="list">
      {''.join(items)}
    </ul>
  </main>
  <footer>
    <p class="small">{FOOTER_LINE}</p>
  </footer>
</body>
</html>"""
    (DOCS / "map.html").write_text(page, encoding="utf-8")

def main():
    # Optional: allow overriding CSV path via CLI
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else CSV_DEFAULT
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        sys.exit(1)

    ensure_dirs()
    data = list(read_rows(csv_path))
    for row in data:
        write_page(row)
    write_map(data)
    print(f"Created {len(data)} pages and rebuilt docs/map.html from {csv_path.name}")

if __name__ == "__main__":
    main()
