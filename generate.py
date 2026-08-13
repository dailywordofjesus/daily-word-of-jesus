#!/usr/bin/env python3
"""
DAILY WORD OF JESUS — static site generator (final v2).
New: "## " lines become article subheadings; ad positions adapt to
article length; output folders auto-cleaned (no stale pages).
Run: python generate.py
"""
import json
import os
import re
from datetime import datetime
from urllib.parse import quote

SITE_NAME = "DAILY WORD OF JESUS"
SITE_URL = "https://dailywordofjesus.github.io/daily-word-of-jesus"
SITE_DESCRIPTION = (
    "Daily Word of Jesus, inspiring stories, miracles, faith and Christian reflections."
)
SITE_OG_IMAGE = f"{SITE_URL}/images/og-site.png"
ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLES_JSON = os.path.join(ROOT, "articles.json")
ARTICLES_DIR = os.path.join(ROOT, "articles")
CATEGORY_DIR = os.path.join(ROOT, "category")
SMARTLINK_URL = "https://www.effectivecpmnetwork.com/zwqu9mg8bc?key=2a9312a2f1ef35694cfa32de3c7c1243"

# ---------------------------------------------------------------- helpers
def _clean(obj):
    if isinstance(obj, dict):
        return {k.strip(): _clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean(v) for v in obj]
    if isinstance(obj, str):
        return obj.strip()
    return obj

def load_articles():
    with open(ARTICLES_JSON, "r", encoding="utf-8") as f:
        articles = _clean(json.load(f))
    for a in articles:
        a.setdefault("slug", slugify(a.get("title", "")))
    articles.sort(key=lambda a: a.get("date", ""), reverse=True)
    return articles

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower().strip()).strip("-")

def article_url(article):
    return f"{SITE_URL}/articles/{article['slug']}.html"

def category_url(slug):
    return f"{SITE_URL}/category/{slug}.html"

def format_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%B %d, %Y")
    except ValueError:
        return s

def rel_prefix(depth):
    return "../" * depth

def collect_categories(articles):
    cats, seen = [], set()
    for a in articles:
        if a["category"] not in seen:
            seen.add(a["category"])
            cats.append((a["category"], a["category_name"]))
    return cats

def clean_html(dirpath):
    for name in os.listdir(dirpath):
        if name.endswith(".html"):
            os.remove(os.path.join(dirpath, name))

# ---------------------------------------------------------------- fragments
def render_header(depth, categories):
    p = rel_prefix(depth)
    nav_links = [f'<a href="{p}index.html">Home</a>']
    nav_links += [f'<a href="{p}category/{s}.html">{n}</a>' for s, n in categories]
    nav_html = "\n".join(nav_links)
    return f"""
<header class="site-header">
<div class="site-header-inner">
<a class="site-logo" href="{p}index.html">Daily Word <span>of Jesus</span></a>
<button class="menu-toggle" aria-label="Open menu">&#9776;</button>
<nav class="site-nav">
{nav_html}
</nav>
</div>
<div class="ad-container ad-slot-header" id="ad-header"></div>
</header>
"""

def render_footer():
    return f"""
<footer class="site-footer">
<div class="container">
<p>&copy; {datetime.now().year} {SITE_NAME}. All rights reserved.</p>
<p><a href="index.html">Home</a></p>
</div>
</footer>
"""

def render_promo_box():
    return f"""
<div class="promo-box">
<div class="promo-label">Advertisement / Promotional Link</div>
<div class="promo-title">Recommended for You</div>
<a class="promo-button" href="{SMARTLINK_URL}" target="_blank" rel="noopener sponsored">Discover More</a>
</div>
"""

def render_native_slot():
    return ('<div class="ad-container ad-slot-inline" id="ad-native">'
            '<div class="ad-label">Advertisement</div></div>')

def render_inline_banner_slot():
    return ('<div class="ad-container ad-slot-inline" id="ad-article-300x250">'
            '<div class="ad-label">Advertisement</div></div>')

def render_sidebar(variant):
    return f"""
<aside class="article-sidebar">
<div class="ad-container ad-slot-sidebar" id="ad-sidebar" data-variant="{variant}">
<div class="ad-label">Advertisement</div>
</div>
</aside>
"""

def render_share_buttons(article):
    u = quote(article_url(article), safe="")
    t = quote(article["title"], safe="")
    return f"""
<div class="share-row">
<span class="share-label">Share</span>
<a href="https://wa.me/?text={t}%20{u}" target="_blank" rel="noopener">WhatsApp</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener">Facebook</a>
<a href="https://twitter.com/intent/tweet?text={t}&url={u}" target="_blank" rel="noopener">X</a>
</div>
"""

def render_og_tags(*, og_type, title, description, image, url):
    return f"""
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{image}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">
"""

def page_shell(*, depth, title, description, canonical_url, og_block, body):
    p = rel_prefix(depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_url}">
<link rel="stylesheet" href="{p}style.css">
{og_block}
</head>
<body>
{body}
<script src="{p}script.js"></script>
</body>
</html>
"""

def render_article_card(article, depth):
    p = rel_prefix(depth)
    return f"""
<a class="card" href="{p}articles/{article['slug']}.html">
<img src="{p}{article['image']}" alt="{article['title']}" loading="lazy">
<div class="card-body">
<div class="card-category">{article['category_name']}</div>
<h3 class="card-title">{article['title']}</h3>
<p class="card-excerpt">{article['excerpt']}</p>
</div>
</a>
"""

# ---------------------------------------------------------------- homepage
def build_homepage(articles, categories):
    depth = 0
    latest = articles[0]
    cards = "".join(render_article_card(a, depth) for a in articles)
    body = f"""
{render_header(depth, categories)}
<main class="container">
<section class="daily-word">
<div class="eyebrow">Daily Word</div>
<blockquote>&ldquo;{latest['verse_text']}&rdquo;</blockquote>
<cite>{latest['verse_ref']}</cite>
</section>
<h2 class="section-title">Latest Inspiration</h2>
{render_native_slot()}
<h2 class="section-title">Latest Articles</h2>
<div class="article-grid">
{cards}
</div>
{render_promo_box()}
</main>
{render_footer()}
"""
    html = page_shell(
        depth=depth,
        title=f"{SITE_NAME} — Daily Devotion & Inspiring Stories",
        description=SITE_DESCRIPTION,
        canonical_url=f"{SITE_URL}/",
        og_block=render_og_tags(og_type="website", title=SITE_NAME,
                                description=SITE_DESCRIPTION,
                                image=SITE_OG_IMAGE, url=f"{SITE_URL}/"),
        body=body,
    )
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

# ---------------------------------------------------------------- article
def render_related_articles(current, all_articles, depth):
    related = [a for a in all_articles
               if a["slug"] != current["slug"] and a["category"] == current["category"]]
    if len(related) < 3:
        related += [a for a in all_articles
                    if a["slug"] != current["slug"] and a not in related]
    related = related[:3]
    if not related:
        return ""
    p = rel_prefix(depth)
    items = "".join(f"""
<a class="card" href="{p}articles/{a['slug']}.html">
<img src="{p}{a['image']}" alt="{a['title']}" loading="lazy">
<div class="card-body">
<div class="card-category">{a['category_name']}</div>
<h3 class="card-title">{a['title']}</h3>
</div>
</a>
""" for a in related)
    return f"""
<h2 class="section-title">Related Articles</h2>
<div class="related-list">
{items}
</div>
"""

def build_article_page(article, all_articles, categories):
    depth = 1
    p = rel_prefix(depth)
    items_list = article["content"]
    total_paras = sum(1 for x in items_list if not x.startswith("## "))
    parts = []
    para_count = 0
    for item in items_list:
        if item.startswith("## "):
            parts.append(f'<h2 class="article-subheading">{item[3:]}</h2>')
            continue
        parts.append(f"<p>{item}</p>")
        para_count += 1
        if para_count == 4 and total_paras > 6:
            parts.append(render_native_slot())
        if para_count == total_paras // 2 and total_paras > 8:
            parts.append(render_inline_banner_slot())
    article_html = "\n".join(parts)
    canonical = article_url(article)
    body = f"""
{render_header(depth, categories)}
<main class="wide-container">
<div class="article-layout">
<article>
<div class="article-header">
<div class="card-category">{article['category_name']}</div>
<h1 class="article-title">{article['title']}</h1>
<div class="article-meta">{format_date(article['date'])}</div>
</div>
<img class="article-hero-image" src="{p}{article['image']}" alt="{article['title']}">
<div class="verse-box">
&ldquo;{article['verse_text']}&rdquo;<br>
<strong>&mdash; {article['verse_ref']}</strong>
</div>
<div class="article-body">
{article_html}
</div>
{render_share_buttons(article)}
{render_related_articles(article, all_articles, depth)}
{render_promo_box()}
</article>
{render_sidebar("banner_160x600")}
</div>
</main>
{render_footer()}
"""
    html = page_shell(
        depth=depth,
        title=f"{article['title']} — {SITE_NAME}",
        description=article["excerpt"],
        canonical_url=canonical,
        og_block=render_og_tags(og_type="article", title=article["title"],
                                description=article["excerpt"],
                                image=f"{SITE_URL}/{article['image']}",
                                url=canonical),
        body=body,
    )
    with open(os.path.join(ARTICLES_DIR, f"{article['slug']}.html"), "w", encoding="utf-8") as f:
        f.write(html)

# ---------------------------------------------------------------- category
def build_category_pages(articles, categories):
    depth = 1
    grouped = {}
    for a in articles:
        grouped.setdefault(a["category"], []).append(a)
    for cat_slug, name in categories:
        cat_articles = grouped.get(cat_slug, [])
        cards = "".join(render_article_card(a, depth) for a in cat_articles)
        canonical = category_url(cat_slug)
        body = f"""
{render_header(depth, categories)}
<main class="wide-container">
<div class="article-layout">
<div class="layout-main">
<h1 class="section-title">{name}</h1>
<div class="article-grid">
{cards}
</div>
{render_promo_box()}
</div>
{render_sidebar("banner_160x300")}
</div>
</main>
{render_footer()}
"""
        html = page_shell(
            depth=depth,
            title=f"{name} — {SITE_NAME}",
            description=f"{name} articles from {SITE_NAME}.",
            canonical_url=canonical,
            og_block=render_og_tags(og_type="website",
                                    title=f"{name} — {SITE_NAME}",
                                    description=f"{name} articles from {SITE_NAME}.",
                                    image=SITE_OG_IMAGE, url=canonical),
            body=body,
        )
        with open(os.path.join(CATEGORY_DIR, f"{cat_slug}.html"), "w", encoding="utf-8") as f:
            f.write(html)

# ---------------------------------------------------------------- main
def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    os.makedirs(CATEGORY_DIR, exist_ok=True)
    clean_html(ARTICLES_DIR)
    clean_html(CATEGORY_DIR)
    articles = load_articles()
    categories = collect_categories(articles)
    build_homepage(articles, categories)
    for article in articles:
        build_article_page(article, articles, categories)
    build_category_pages(articles, categories)
    print(f"Generated 1 homepage, {len(articles)} article pages, "
          f"{len(categories)} category pages.")

if __name__ == "__main__":
    main()