#!/usr/bin/env python3
"""Add 'When to Use' and 'How It Works' sections to tool pages."""
import os, re, json

TOOLS_DIR = '/tmp/toolstand-deploy/tools'

# Category-specific "When to Use" scenarios
WHEN_TO_USE = {
    'calculator': [
        "You need a quick calculation without opening a spreadsheet",
        "You're comparing financial scenarios (loans, investments, savings)",
        "You want instant health/fitness numbers without downloading an app",
        "You're teaching math or finance concepts and need live examples",
        "You need to verify numbers from another source quickly",
    ],
    'converter': [
        "You're working with data in one format but need it in another",
        "You're debugging and need to convert timestamps, encodings, or units",
        "You received a file in the wrong format and need it changed fast",
        "You're building something and need format/code conversion on the fly",
        "You want to avoid installing heavy software for a one-time conversion",
    ],
    'generator': [
        "You need to create something quickly — a password, QR code, UUID, or key",
        "You're setting up a new project and need placeholder data or credentials",
        "You want to automate a repetitive creation task without writing code",
        "You're testing and need sample data (Lorem Ipsum, random numbers, barcodes)",
        "You need a professional-looking output without design skills",
    ],
    'developer': [
        "You're coding and need to format, validate, or test data structures",
        "You're debugging an API response and need to inspect tokens or schemas",
        "You're optimizing your workflow and want to avoid context-switching to desktop apps",
        "You're learning and want to experiment with regex, SQL, or JSON in real-time",
        "You're doing code review and need quick diff/view/preview tools",
    ],
    'productivity': [
        "You're working and need a timer, stopwatch, or focus tool",
        "You're planning and need to count words, check readability, or diff text",
        "You're organizing and need date calculations, timezone conversions",
        "You want to stay focused without app notifications interrupting you",
        "You need a utility that just works — no signup, no download, no fuss",
    ],
    'utility': [
        "You need a quick browser-based tool without installing anything",
        "You're on a shared or public computer and can't install software",
        "You want a privacy-first tool that doesn't send your data anywhere",
        "You're helping someone and need an instant tool they can also use",
        "You need a reliable tool that works offline once loaded",
    ],
    'pdf': [
        "You have PDF files that need merging, splitting, or converting",
        "You're preparing documents and don't want to upload them to a cloud service",
        "You need to extract images or pages from a PDF quickly",
        "You're working with sensitive documents that should stay on your device",
        "You want PDF tools that work offline and don't require Adobe Acrobat",
    ],
    'seo': [
        "You're optimizing a website and need to preview meta tags or SERP appearance",
        "You're launching a new page and want to check robots.txt, sitemaps, or UTM tags",
        "You're doing competitor research and need quick SEO tool access",
        "You want to validate structured data or schema markup before deploying",
        "You're teaching SEO and need live, free tools your students can use",
    ],
    'security': [
        "You need to generate strong passwords or SSH keys securely",
        "You're handling sensitive data and want client-side encryption",
        "You're auditing security and need to hash, encrypt, or inspect tokens",
        "You want security tools that never send your data to a server",
        "You're teaching cybersecurity and need practical, hands-on tools",
    ],
    'game': [
        "You need a quick break and want a simple browser game",
        "You're testing reaction time, decision-making, or puzzle-solving skills",
        "You want to demonstrate probability or randomness concepts",
        "You're looking for classic games without ads, downloads, or signups",
        "You want to challenge friends with fair, transparent game mechanics",
    ],
}

# Default for uncategorized
DEFAULT_WHEN = [
    "You need a quick browser-based tool without installing anything",
    "You're on a shared computer and can't install software",
    "You want a privacy-first tool — your data never leaves your device",
    "You're helping someone and need a tool they can access instantly",
    "You want a reliable, ad-free experience with no signup required",
]

def get_how_it_works(slug, name):
    """Generate privacy/technical explanation."""
    return f"""<p><strong>{name}</strong> runs entirely in your browser using standard web technologies — HTML, CSS, and JavaScript. Your input never leaves your device. There is no server, no backend, and no account needed. Everything is processed locally using your device's computing power. This means: (1) your data stays private, (2) the tool works offline once loaded, and (3) there are no usage limits or subscription paywalls.</p>"""

def get_when_to_use(category, name, slug):
    """Generate 'When to Use' content."""
    scenarios = WHEN_TO_USE.get(category, DEFAULT_WHEN)
    items = '\n'.join(f'        <li>{s}</li>' for s in scenarios[:5])
    return f"""<p><strong>{name}</strong> is useful in many real-world situations. Here are the most common scenarios where it saves time and effort:</p>
      <ul>
{items}
      </ul>"""

# Read tools data for category mapping
with open(os.path.join(TOOLS_DIR, '..', 'shared', 'tools-data.js')) as f:
    tools_js = f.read()

tool_categories = {}
for line in tools_js.split('\n'):
    m = re.match(r'\s*\{\s*id:"([^"]+)".*name:"([^"]+)".*tags:\[([^\]]+)\]', line)
    if m:
        slug, name, tags_str = m.group(1), m.group(2), m.group(3)
        tags = [t.strip().strip('"') for t in tags_str.split(',')]
        tool_categories[slug] = {'name': name, 'tags': tags}

# Process each tool
updated_when = 0
updated_how = 0
for slug, info in tool_categories.items():
    tool_path = os.path.join(TOOLS_DIR, slug, 'index.html')
    if not os.path.exists(tool_path):
        continue
    
    with open(tool_path) as f:
        html = f.read()
    
    name = info['name']
    # Pick primary category
    category = info['tags'][0] if info['tags'] else 'utility'
    
    # --- Add When to Use ---
    if 'when-to-use' not in html.lower() and 'When to Use' not in html:
        when_html = f'''    <section class="when-to-use">
      <h2>🕐 When to Use {name}</h2>
{get_when_to_use(category, name, slug)}
    </section>
'''
        # Insert after FAQ section or before related-tools
        if '<nav class="related-tools">' in html:
            html = html.replace('<nav class="related-tools">', when_html + '\n  <nav class="related-tools">', 1)
        elif '<nav class="related-guides">' in html:
            html = html.replace('<nav class="related-guides">', when_html + '\n  <nav class="related-guides">', 1)
        elif '</main>' in html:
            html = html.replace('</main>', when_html + '\n</main>', 1)
        updated_when += 1
    
    # --- Add How It Works ---
    if 'how-it-works' not in html.lower() and 'How It Works' not in html:
        how_html = f'''    <section class="how-it-works">
      <h2>⚙️ How It Works</h2>
{get_how_it_works(slug, name)}
    </section>
'''
        if '<nav class="related-tools">' in html:
            html = html.replace('<nav class="related-tools">', how_html + '\n  <nav class="related-tools">', 1)
        elif '<nav class="related-guides">' in html:
            html = html.replace('<nav class="related-guides">', how_html + '\n  <nav class="related-guides">', 1)
        elif '</main>' in html:
            html = html.replace('</main>', how_html + '\n</main>', 1)
        updated_how += 1
    
    with open(tool_path, 'w') as f:
        f.write(html)

print(f"Added 'When to Use': {updated_when} tools")
print(f"Added 'How It Works': {updated_how} tools")
