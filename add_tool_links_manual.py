#!/usr/bin/env python3
"""Add tool links to remaining pillar blogs based on tool name/slug matching."""
import os, re

BLOG_DIR = '/tmp/toolstand-deploy/blog'
TOOLS_DIR = '/tmp/toolstand-deploy/tools'

# Manual mapping: pillar_slug → list of (tool_slug, tool_name)
PILLAR_TOOLS = {
    'free-online-image-tools-complete-guide': [
        ('image-resizer', 'Image Resizer & Compressor'),
        ('image-converter', 'Image Format Converter'),
        ('image-to-pdf', 'Image to PDF'),
        ('pdf-to-image', 'PDF to Image'),
        ('svg-optimizer', 'SVG Optimizer'),
        ('color-converter', 'Color Code Converter'),
        ('color-palette-generator', 'Color Palette Generator'),
        ('color-blindness', 'Color Blindness Simulator'),
        ('og-preview', 'OG Image Preview'),
    ],
    'free-online-text-writing-tools-complete-guide': [
        ('word-counter', 'Word & Character Counter'),
        ('case-converter', 'Case Converter'),
        ('lorem-ipsum', 'Lorem Ipsum Generator'),
        ('readability-checker', 'Readability Checker'),
        ('diff-checker', 'Text Diff Checker'),
        ('text-encryptor', 'Text Encryptor / Decryptor'),
        ('markdown-previewer', 'Markdown Previewer'),
        ('html-entity-encoder', 'HTML Entity Encoder'),
        ('number-to-words', 'Number to Words Converter'),
    ],
    'free-css-visual-generators-guide': [
        ('css-border-radius', 'CSS Border Radius Previewer'),
        ('css-box-shadow', 'CSS Box Shadow Generator'),
        ('css-clamp-generator', 'CSS Clamp Calculator'),
        ('gradient-generator', 'CSS Gradient Generator'),
        ('color-palette-generator', 'Color Palette Generator'),
    ],
    'metronome-music-practice-tool': [
        ('metronome', 'Metronome'),
        ('bpm-tap', 'BPM Tap Tempo'),
        ('tone-generator', 'Frequency Generator'),
    ],
    'bmi-body-fat-calculator-health-tools': [
        ('bmi-calculator', 'BMI Calculator'),
        ('body-fat-calculator', 'Body Fat Calculator'),
        ('calorie-calculator', 'Calorie Calculator'),
        ('keto-calculator', 'Keto Macro Calculator'),
        ('water-intake', 'Water Intake Calculator'),
        ('pace-calculator', 'Pace Calculator'),
        ('due-date-calculator', 'Pregnancy Due Date Calculator'),
    ],
    'compound-interest-vs-loan-calculator': [
        ('compound-interest', 'Compound Interest Calculator'),
        ('loan-calculator', 'Loan Calculator'),
        ('tip-calculator', 'Tip Calculator'),
        ('dca-calculator', 'DCA Calculator'),
        ('dividend-calculator', 'Dividend Calculator'),
        ('savings-calculator', 'Savings Calculator'),
        ('retirement-calculator', 'Retirement Calculator'),
        ('inflation-calculator', 'Inflation Calculator'),
        ('trade-risk-calculator', 'Trade Risk Calculator'),
        ('currency-converter', 'Currency Converter'),
    ],
    'schema-markup-structured-data-guide': [
        ('schema-markup-generator', 'Schema Markup Generator'),
        ('faq-schema-generator', 'FAQ Schema Generator'),
        ('json-schema-generator', 'JSON Schema Generator'),
        ('meta-tag-generator', 'Meta Tag Generator'),
        ('meta-tag-preview', 'Meta Tag & SERP Preview'),
        ('serp-preview', 'SERP Preview'),
    ],
}

for pillar, tools in PILLAR_TOOLS.items():
    blog_path = os.path.join(BLOG_DIR, pillar, 'index.html')
    if not os.path.exists(blog_path):
        print(f"  SKIP: {pillar} — not found")
        continue
    
    with open(blog_path) as f:
        html = f.read()
    
    if 'tools-in-category' in html:
        print(f"  SKIP: {pillar} — already has section")
        continue
    
    links = '\n'.join(f'      <li><a href="/tools/{slug}/">{name}</a></li>' for slug, name in tools)
    section = f'''  <section class="tools-in-category">
    <h2>🛠️ Tools in This Category</h2>
    <ul>
{links}
    </ul>
  </section>
'''
    
    for tag in ['</article>', '</main>', '</body>']:
        if tag in html:
            html = html.replace(tag, section + '\n' + tag, 1)
            break
    
    with open(blog_path, 'w') as f:
        f.write(html)
    print(f"  OK: {pillar} — {len(tools)} tools")

print("Done!")
