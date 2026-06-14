#!/usr/bin/env python3
"""Add 'Tools in This Category' sections to pillar blog posts."""
import os, re

TOOLS_DIR = '/tmp/toolstand-deploy/tools'
BLOG_DIR = '/tmp/toolstand-deploy/blog'

# Category → pillar blog slug
CATEGORY_PILLAR = {
    'calculator': 'free-online-calculator-tools-complete-guide',
    'converter': 'free-online-converter-tools-complete-guide',
    'developer': 'free-online-developer-tools-complete-guide',
    'generator': 'free-online-generator-tools-complete-guide',
    'image': 'free-online-image-tools-complete-guide',
    'pdf': 'free-online-pdf-tools-complete-guide',
    'productivity': 'free-online-productivity-tools-complete-guide',
    'utility': 'free-online-productivity-tools-complete-guide',
    'security': 'free-online-security-privacy-tools-guide',
    'seo': 'free-online-seo-webmaster-tools-guide',
    'text': 'free-online-text-writing-tools-complete-guide',
}

# Read tools data
with open(os.path.join(TOOLS_DIR, '..', 'shared', 'tools-data.js')) as f:
    content = f.read()

# Build category → list of (slug, name) 
cat_tools = {}
for line in content.split('\n'):
    m = re.match(r'\s*\{\s*id:"([^"]+)".*name:"([^"]+)".*tags:\[([^\]]+)\]', line)
    if m:
        slug, name, tags_str = m.group(1), m.group(2), m.group(3)
        tags = [t.strip().strip('"') for t in tags_str.split(',')]
        for tag in tags:
            if tag in CATEGORY_PILLAR:
                cat_tools.setdefault(tag, []).append((slug, name))
                break

# Build HTML sections for each pillar blog
sections = {}
for cat, pillar_slug in CATEGORY_PILLAR.items():
    tools = cat_tools.get(cat, [])
    if not tools:
        continue
    links = '\n'.join(f'      <li><a href="/tools/{slug}/">{name}</a></li>' for slug, name in tools[:20])
    section = f'''  <section class="tools-in-category">
    <h2>🛠️ Tools in This Category</h2>
    <ul>
{links}
    </ul>
  </section>
'''
    sections[pillar_slug] = section

# Update blog posts
for pillar_slug, section_html in sections.items():
    blog_path = os.path.join(BLOG_DIR, pillar_slug, 'index.html')
    if not os.path.exists(blog_path):
        print(f"  SKIP: {pillar_slug} — not found")
        continue
    
    with open(blog_path) as f:
        html = f.read()
    
    if 'tools-in-category' in html:
        print(f"  SKIP: {pillar_slug} — already has section")
        continue
    
    # Insert before closing </article> or </main> or </body>
    for tag in ['</article>', '</main>', '</body>']:
        if tag in html:
            html = html.replace(tag, section_html + '\n' + tag, 1)
            break
    
    with open(blog_path, 'w') as f:
        f.write(html)
    print(f"  OK: {pillar_slug} — {len(cat_tools.get([k for k,v in CATEGORY_PILLAR.items() if v==pillar_slug][0], []))} tools")

print("Done!")
