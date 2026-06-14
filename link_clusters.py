#!/usr/bin/env python3
"""
link_clusters.py — Add internal cluster links (📚 Related Guides) to all blog posts.

Inserts a <section class="related-guides"> before </article> in each blog post,
linking to the category pillar and 2-3 sibling posts in the same cluster.
"""

import re
import random
import os
from pathlib import Path
from collections import defaultdict

BLOG_DIR = Path('/tmp/toolstand-deploy/blog')

# Category → pillar slug mapping (from the task spec)
CATEGORY_PILLAR = {
    'calculator':           'free-online-calculator-tools-complete-guide',
    'converter':            'free-online-converter-tools-complete-guide',
    'developer/formatter':  'free-online-developer-tools-complete-guide',
    'generator':            'free-online-generator-tools-complete-guide',
    'image/design':         'free-online-image-tools-complete-guide',
    'pdf':                  'free-online-pdf-tools-complete-guide',
    'productivity/utility': 'free-online-productivity-tools-complete-guide',
    'security':             'free-online-security-privacy-tools-guide',
    'seo':                  'free-online-seo-webmaster-tools-guide',
    'text/writing':         'free-online-text-writing-tools-complete-guide',
    'health':               'bmi-body-fat-calculator-health-tools',
    'finance':              'compound-interest-vs-loan-calculator',
    'music':                'metronome-music-practice-tool',
    'css/design':           'free-css-visual-generators-guide',
    'schema/markup':        'schema-markup-structured-data-guide',
    'password/auth':        'password-generator-strength-guide',
}

# Ordered keyword → category rules. First match wins.
# Order: most specific/narrow keywords first, broader catch-alls last.
KEYWORD_RULES = [
    # --- Health (very specific) ---
    ('bmi',                                 'health'),
    ('body-fat',                            'health'),
    ('pregnancy',                           'health'),
    ('keto',                                'health'),
    ('macro-calculator',                    'health'),

    # --- Music ---
    ('metronome',                           'music'),
    ('music-practice',                      'music'),

    # --- Finance (specific financial terms) ---
    ('compound-interest',                   'finance'),
    ('loan-calculator',                     'finance'),
    ('dollar-cost',                         'finance'),
    ('dividend',                            'finance'),
    ('savings-calc',                        'finance'),
    ('tip-bill',                            'finance'),
    ('bill-split',                          'finance'),
    ('retirement',                          'finance'),

    # --- CSS/Design ---
    ('css-generator',                       'css/design'),
    ('css-box-shadow',                      'css/design'),
    ('css-border-radius',                   'css/design'),
    ('css-clamp',                           'css/design'),
    ('visual-generator',                    'css/design'),
    ('free-css',                            'css/design'),

    # --- Schema/Markup ---
    ('schema-markup',                       'schema/markup'),
    ('structured-data',                     'schema/markup'),

    # --- Password/Auth ---
    ('password-generator',                  'password/auth'),
    ('password-strength',                   'password/auth'),
    ('ssh-key',                             'password/auth'),

    # --- PDF (pdf-* patterns) ---
    ('pdf-merge',                           'pdf'),
    ('pdf-split',                           'pdf'),
    ('pdf-security',                        'pdf'),
    ('pdf-to-image',                        'pdf'),
    ('image-to-pdf',                        'pdf'),
    ('free-image-to-pdf',                   'pdf'),
    ('-pdf-',                               'pdf'),   # catch remaining pdf-infix

    # --- SEO ---
    ('seo-webmaster',                       'seo'),
    ('-seo-',                               'seo'),
    ('robots-txt',                          'seo'),
    ('utm-builder',                         'seo'),
    ('meta-tag',                            'seo'),
    ('og-preview',                          'seo'),

    # --- Security ---
    ('security-privacy',                    'security'),
    ('encryptor',                           'security'),
    ('whats-my-ip',                         'security'),
    ('-privacy-',                           'security'),

    # --- Productivity ---
    ('productivity-tools',                  'productivity/utility'),
    ('pomodoro',                            'productivity/utility'),

    # --- Developer/Formatter ---
    ('developer-tools',                     'developer/formatter'),
    ('json-toolkit',                        'developer/formatter'),
    ('formatter-minifier',                  'developer/formatter'),
    ('-formatter-',                         'developer/formatter'),
    ('sql-xml-yaml-formatter',             'developer/formatter'),
    ('regex-tools',                         'developer/formatter'),
    ('markdown-previewer',                  'developer/formatter'),
    ('hash-generator',                      'developer/formatter'),
    ('jwt-decoder',                         'developer/formatter'),
    ('base64-url-encode',                   'developer/formatter'),
    ('ai-prompt-dockerfile',                'developer/formatter'),

    # --- Image/Design ---
    ('best-free-image-converter',           'image/design'),
    ('color-palette',                       'image/design'),
    ('color-code-converter',                'image/design'),
    ('svg-optimizer',                       'image/design'),
    ('-designers',                          'image/design'),

    # --- Generator (catch various generator patterns) ---
    ('qr-code-generator',                   'generator'),
    ('youtube-title-generator',             'generator'),
    ('lorem-ipsum',                         'generator'),
    ('-generator-',                         'generator'),
    ('-generator',                          'generator'),

    # --- Converter (catch converter patterns) ---
    ('timestamp-unix-converter',            'converter'),
    ('timezone-converter',                  'converter'),
    ('currency-unit-converter',             'converter'),
    ('csv-json-xml-converter',              'converter'),
    ('-converter-',                         'converter'),

    # --- Text/Writing ---
    ('word-counter',                        'text/writing'),
    ('readability',                         'text/writing'),
    ('case-converter',                      'text/writing'),
    ('text-writing',                        'text/writing'),

    # --- Calculator (broadest, last) ---
    ('-calculator',                         'calculator'),
    ('calculator-',                         'calculator'),

    # --- Fallbacks (broader patterns) ---
    ('security',                            'security'),
    ('encrypt',                             'security'),
    ('privacy',                             'security'),
    ('productivity',                        'productivity/utility'),
    ('timer',                               'productivity/utility'),
    ('developer',                           'developer/formatter'),
    ('formatter',                           'developer/formatter'),
    ('minifier',                            'developer/formatter'),
    ('image',                               'image/design'),
    ('color',                               'image/design'),
    ('design',                              'image/design'),
    ('generator',                           'generator'),
    ('converter',                           'converter'),
    ('text',                                'text/writing'),
    ('writing',                             'text/writing'),
    ('seo',                                 'seo'),
    ('pdf',                                 'pdf'),
    ('css',                                 'css/design'),
    ('schema',                              'schema/markup'),
    ('markup',                              'schema/markup'),
    ('password',                            'password/auth'),
    ('calculator',                          'calculator'),
    ('music',                               'music'),
    ('health',                              'health'),
    ('finance',                             'finance'),
]


def classify_slug(slug: str) -> str:
    """Return the category for a blog slug using first-match keyword rules."""
    for keyword, category in KEYWORD_RULES:
        if keyword in slug:
            return category
    return 'unknown'


def extract_h1(filepath: Path) -> str | None:
    """Extract the <h1> text from an HTML file."""
    text = filepath.read_text(encoding='utf-8')
    m = re.search(r'<h1>(.*?)</h1>', text, re.DOTALL)
    if m:
        # Strip HTML tags within h1 for safety
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return None


def main():
    random.seed(42)  # deterministic sibling selection

    # --- Collect all blog posts ---
    all_posts = []  # list of dicts: slug, category, title, path
    for d in sorted(BLOG_DIR.iterdir()):
        if not d.is_dir():
            continue
        slug = d.name
        index_path = d / 'index.html'
        if not index_path.is_file():
            continue

        category = classify_slug(slug)
        title = extract_h1(index_path)
        all_posts.append({
            'slug': slug,
            'category': category,
            'title': title or slug.replace('-', ' ').title(),
            'path': index_path,
        })

    # --- Group by category ---
    by_category = defaultdict(list)
    for p in all_posts:
        by_category[p['category']].append(p)

    # --- Report ---
    print(f"Total blog posts: {len(all_posts)}")
    print(f"Categories found: {len(by_category)}")
    for cat in sorted(by_category):
        posts_in_cat = by_category[cat]
        print(f"  {cat}: {len(posts_in_cat)} posts")
        for pp in posts_in_cat:
            print(f"    - {pp['slug']}")
    print()

    # Build a slug→title lookup
    slug_to_title = {p['slug']: p['title'] for p in all_posts}

    # --- Update each post ---
    updated = 0
    skipped = 0
    errors = 0

    for p in all_posts:
        cat = p['category']
        pillar_slug = CATEGORY_PILLAR.get(cat)

        # Siblings: same category, excluding self AND the pillar
        # (pillar is linked separately as "Complete category guide")
        siblings = [s for s in by_category[cat]
                    if s['slug'] != p['slug'] and s['slug'] != pillar_slug]

        # Pick 2-3 random siblings (deterministic via seed)
        num_sibs = min(3, len(siblings))
        chosen = random.sample(siblings, num_sibs) if num_sibs > 0 else []

        # Read current content
        content = p['path'].read_text(encoding='utf-8')

        # Skip if already has related-guides
        if 'class="related-guides"' in content or 'related-guides' in content:
            skipped += 1
            continue

        # Build related-guides HTML
        html_parts = ['<section class="related-guides">']
        html_parts.append('<h2>📚 Related Guides</h2>')
        html_parts.append('<ul>')

        # Pillar link (skip if this IS the pillar)
        if pillar_slug and pillar_slug != p['slug']:
            pillar_title = slug_to_title.get(pillar_slug, pillar_slug.replace('-', ' ').title())
            html_parts.append(
                f'<li><a href="/blog/{pillar_slug}/">📖 {pillar_title}</a> — Complete category guide</li>'
            )

        # Sibling links
        for sib in chosen:
            html_parts.append(
                f'<li><a href="/blog/{sib["slug"]}/">📄 {sib["title"]}</a></li>'
            )

        html_parts.append('</ul>')
        html_parts.append('</section>')
        related_html = '\n'.join(html_parts)

        # Insert before </article>
        if '</article>' not in content:
            print(f"  ERROR: No </article> found in {p['slug']}")
            errors += 1
            continue

        new_content = content.replace('</article>', related_html + '\n</article>', 1)
        p['path'].write_text(new_content, encoding='utf-8')
        updated += 1
        print(f"  ✓ {p['slug']} → {cat}  (pillar={'self' if pillar_slug == p['slug'] else pillar_slug}, siblings={len(chosen)})")

    print(f"\n{'='*60}")
    print(f"Results: {updated} updated, {skipped} skipped, {errors} errors")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
