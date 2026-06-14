#!/usr/bin/env python3
"""Add 'Related Guides' section to tool pages — links to category pillar blog post."""
import os, re, sys

TOOLS_DIR = '/tmp/toolstand-deploy/tools'
BLOG_DIR = '/tmp/toolstand-deploy/blog'

# Tool slug → pillar blog mapping
CATEGORY_PILLARS = {
    'calculator': 'free-online-calculator-tools-complete-guide',
    'converter': 'free-online-converter-tools-complete-guide',
    'developer': 'free-online-developer-tools-complete-guide',
    'generator': 'free-online-generator-tools-complete-guide',
    'utility': 'free-online-productivity-tools-complete-guide',
    'productivity': 'free-online-productivity-tools-complete-guide',
    'pdf': 'free-online-pdf-tools-complete-guide',
    'image': 'free-online-image-tools-complete-guide',
    'health': 'bmi-body-fat-calculator-health-tools',
    'finance': 'compound-interest-vs-loan-calculator',
    'seo': 'free-online-seo-webmaster-tools-guide',
    'security': 'free-online-security-privacy-tools-guide',
    'text': 'free-online-text-writing-tools-complete-guide',
    'game': 'free-online-developer-tools-complete-guide',
    'design': 'free-css-visual-generators-guide',
    'formatter': 'free-online-developer-tools-complete-guide',
    'education': 'free-online-productivity-tools-complete-guide',
    'music': 'metronome-music-practice-tool',
    'accessibility': 'free-online-productivity-tools-complete-guide',
}

# Tool slug → primary category (based on known tool data)
TOOL_CATEGORY = {}
# Read tools-data.js to get category mapping
with open(os.path.join(TOOLS_DIR, '..', 'shared', 'tools-data.js')) as f:
    content = f.read()

# Parse TOOLS array - format: { id:"slug", name:"...", tags:["tag1","tag2"], ... }
lines = content.split('\n')
for line in lines:
    m = re.match(r'\s*\{\s*id:"([^"]+)".*tags:\[([^\]]+)\]', line)
    if m:
        slug = m.group(1)
        tags_str = m.group(2)
        tags = [t.strip().strip('"') for t in tags_str.split(',')]
        for tag in tags:
            if tag in CATEGORY_PILLARS:
                TOOL_CATEGORY[slug] = tag
                break
        if slug not in TOOL_CATEGORY:
            TOOL_CATEGORY[slug] = 'utility'

print(f"Loaded {len(TOOL_CATEGORY)} tool categories")

# Process each tool page
updated = 0
skipped = 0
for slug, category in TOOL_CATEGORY.items():
    tool_path = os.path.join(TOOLS_DIR, slug, 'index.html')
    if not os.path.exists(tool_path):
        continue
    
    with open(tool_path) as f:
        html = f.read()
    
    # Skip if already has related-guides
    if 'related-guides' in html:
        skipped += 1
        continue
    
    pillar = CATEGORY_PILLARS.get(category, 'free-online-productivity-tools-complete-guide')
    pillar_title = pillar.replace('-', ' ').title()
    
    guide_html = f'''  <nav class="related-guides">
    <h2>📚 Related Guides</h2>
    <ul>
      <li><a href="/blog/{pillar}/">{pillar_title}</a> — Free {category.title()} Tools & Tips</li>
    </ul>
  </nav>
'''
    
    # Insert before closing </main> or before <footer>
    if '</main>' in html:
        html = html.replace('</main>', guide_html + '\n</main>', 1)
    elif '<footer' in html:
        html = html.replace('<footer', guide_html + '\n<footer', 1)
    else:
        html += guide_html
    
    with open(tool_path, 'w') as f:
        f.write(html)
    updated += 1

print(f"Updated: {updated}, Skipped (already had): {skipped}")
