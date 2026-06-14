#!/usr/bin/env python3
"""Generate use-case landing pages for top tools."""
import os, json

DEPLOY = '/tmp/toolstand-deploy'
USE_CASES_DIR = os.path.join(DEPLOY, 'use-cases')

# Tool → list of use cases (slug, title_short, description)
USE_CASES = {
    'qr-code': [
        ('qr-code-for-restaurants', 'Restaurant Menus', 'Create QR codes for restaurant menus — contactless dining, digital ordering, instant menu access.'),
        ('qr-code-for-business-cards', 'Business Cards', 'Add QR codes to business cards — link to LinkedIn, portfolio, or website with one scan.'),
        ('qr-code-for-events', 'Events & Tickets', 'Generate QR codes for event tickets, check-ins, and registration. Fast and scannable.'),
        ('qr-code-for-wifi', 'WiFi Sharing', 'Create a QR code that connects guests to your WiFi instantly — no typing needed.'),
    ],
    'password-generator': [
        ('password-generator-for-wifi', 'WiFi Passwords', 'Generate strong WiFi passwords that are easy to share but hard to crack.'),
        ('password-generator-for-enterprise', 'Enterprise', 'Enterprise-grade passwords meeting NIST 2026 guidelines. 20+ characters, all types.'),
        ('password-generator-for-memorable-phrases', 'Memorable Phrases', 'Create passwords you can actually remember — passphrase mode with word combinations.'),
    ],
    'bmi-calculator': [
        ('bmi-calculator-for-weight-loss', 'Weight Loss Tracking', 'Track your BMI changes during your weight loss journey. See progress over time.'),
        ('bmi-calculator-for-athletes', 'Athletes & Fitness', 'Calculate athlete BMI and understand body composition beyond the simple number.'),
        ('bmi-calculator-for-kids', 'Children & Teens', 'Calculate BMI for children with age-percentile charts instead of adult thresholds.'),
    ],
    'age-calculator': [
        ('age-calculator-for-retirement', 'Retirement Planning', 'Calculate exact age for retirement eligibility, pension claims, and planning.'),
        ('age-calculator-for-school', 'School Enrollment', 'Check if a child meets the age cutoff for kindergarten or school enrollment.'),
    ],
    'spirit-level': [
        ('spirit-level-for-picture-hanging', 'Picture Hanging', 'Use your phone as a bubble level. Perfect for hanging pictures, shelves, and artwork.'),
        ('spirit-level-for-woodworking', 'Woodworking & DIY', 'Precise leveling for woodworking projects. Check surfaces and alignments quickly.'),
    ],
    'sleep-sounds': [
        ('sleep-sounds-for-insomnia', 'Insomnia Relief', 'White noise and nature sounds to help you fall asleep faster and stay asleep longer.'),
        ('sleep-sounds-for-babies', 'Baby Sleep', 'Gentle white noise and lullabies to help babies fall asleep and sleep through the night.'),
        ('sleep-sounds-for-focus', 'Focus & Study', 'Ambient sounds to block distractions and improve concentration during work or study.'),
    ],
    'metronome': [
        ('metronome-for-guitar', 'Guitar Practice', 'Keep perfect time while practicing guitar. Adjustable BPM with visual beat indicator.'),
        ('metronome-for-piano', 'Piano Practice', 'Precise metronome for piano practice. Simple interface, no distractions.'),
        ('metronome-for-drums', 'Drum Practice', 'Visual and audio beats for drum practice. Tap tempo to match any song.'),
    ],
    'pomodoro': [
        ('pomodoro-for-students', 'Students & Study', '25-minute focus sessions with 5-minute breaks. Proven to improve study efficiency.'),
        ('pomodoro-for-developers', 'Developers & Coding', 'Deep work sessions for coding. Block distractions and ship more code.'),
        ('pomodoro-for-writers', 'Writers & Creatives', 'Focus sprints for writing, designing, and creative work. Beat procrastination.'),
    ],
    'dead-pixel-test': [
        ('dead-pixel-test-for-new-monitor', 'New Monitor Check', 'Full-screen color test for new monitors, TVs, and phones. Find dead pixels before return window closes.'),
        ('dead-pixel-test-for-used-devices', 'Used Device Inspection', 'Check used phones and laptops for screen damage before buying. Complete color sweep.'),
    ],
    'currency-converter': [
        ('currency-converter-for-travel', 'Travel Planning', 'Convert currencies while traveling. 170+ currencies, live rates, offline capable.'),
        ('currency-converter-for-freelancers', 'Freelancers', 'Convert international client payments instantly. Accurate rates for invoicing.'),
        ('currency-converter-for-ecommerce', 'E-Commerce', 'Price products in multiple currencies. Keep listings accurate with live conversion.'),
    ],
    'json-formatter': [
        ('json-formatter-for-api-debugging', 'API Debugging', 'Format and validate JSON API responses. Find syntax errors instantly.'),
        ('json-formatter-for-log-files', 'Log File Analysis', 'Pretty-print JSON log files. Make dense data readable in seconds.'),
    ],
    'regex-tester': [
        ('regex-tester-for-email-validation', 'Email Validation', 'Test regex patterns for email validation. Real-time matching with explanation.'),
        ('regex-tester-for-url-parsing', 'URL Parsing', 'Build and test regex patterns for URL extraction and validation.'),
    ],
    'word-counter': [
        ('word-counter-for-essays', 'Essays & Assignments', 'Count words, characters, and reading time for essays and school assignments.'),
        ('word-counter-for-seo', 'SEO Content', 'Check word count for SEO-optimized content. Target your ideal article length.'),
    ],
    'csv-json-converter': [
        ('csv-json-converter-for-data-science', 'Data Science', 'Convert between CSV and JSON for data analysis. Clean, validate, export.'),
        ('csv-json-converter-for-api-migration', 'API Migration', 'Transform API data formats. CSV to JSON and back — no scripting needed.'),
    ],
}

def make_page(slug, tool_name, uc_slug, uc_title, description):
    tool_url = f'/tools/{slug}/'
    page_title = f'Free Online {tool_name} for {uc_title} | ToolStand'
    canonical = f'https://toolstand.io/use-cases/{uc_slug}/'
    
    faqs = [
        ('Is this tool really free?', 'Yes, completely free with no usage limits, no watermarks, and no premium tiers.'),
        ('Do I need to create an account?', 'No. No signup, no email, no account required. Just open the page and start using the tool immediately.'),
        ('Is my data safe when using this tool?', 'Yes. All processing happens locally in your browser. No data is ever uploaded to any server.'),
        ('Can I embed this tool on my own website?', 'Yes! Every ToolStand tool includes a free embed code. Copy the code and paste it on your site.'),
    ]
    
    faq_json = json.dumps([{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs])
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/shared/styles.css">
<meta name="theme-color" content="#2563eb">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="ToolStand">
<meta property="og:image" content="https://toolstand.io/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://toolstand.io/assets/og-image.png">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": ["WebApplication", "SoftwareApplication"],
  "name": "{tool_name}",
  "url": "https://toolstand.io{tool_url}",
  "description": "{description}",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "All",
  "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
  "author": {{"@type": "Organization", "name": "ToolStand", "url": "https://toolstand.io"}}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": {faq_json}
}}
</script>
</head>
<body>
<header class="header">
  <div class="container">
    <a href="/" class="logo">🧰 ToolStand</a>
    <nav class="nav">
      <a href="/blog/">Blog</a>
      <a href="/about/">About</a>
    </nav>
  </div>
</header>
<main class="container">
  <section class="hero" style="padding:40px 0 20px">
    <p style="color:var(--text-secondary);margin-bottom:8px">Use Case</p>
    <h1>Free Online {tool_name} for {uc_title}</h1>
    <p style="color:var(--text-secondary);font-size:1.1rem;max-width:600px">{description}</p>
  </section>

  <section style="margin:32px 0;padding:24px;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);text-align:center">
    <p style="font-size:1.1rem;margin-bottom:16px">Use the <strong>{tool_name}</strong> below — no signup, no download, instant.</p>
    <a href="{tool_url}" style="display:inline-block;background:var(--primary);color:#fff;padding:12px 32px;border-radius:8px;text-decoration:none;font-weight:600;font-size:1.05rem">Open {tool_name} →</a>
  </section>

  <section>
    <h2>Why Use {tool_name} for {uc_title}?</h2>
    <p>{description} This tool is specifically designed to handle this use case — no configuration needed, just open and use.</p>
    <p>Here's what makes it the best choice for {uc_title.lower()}:</p>
    <ul style="margin-left:1.5rem;line-height:1.8">
      <li><strong>Free forever</strong> — no trial periods, no credit card, no premium tier</li>
      <li><strong>Privacy-first</strong> — everything runs in your browser, no data leaves your device</li>
      <li><strong>Instant access</strong> — no downloads, no signup, no account creation</li>
      <li><strong>Works offline</strong> — once loaded, the tool works without internet</li>
      <li><strong>Embeddable</strong> — add it to your own website with a single line of code</li>
    </ul>
  </section>

  <section>
    <h2>How to Use {tool_name} for {uc_title}</h2>
    <ol style="margin-left:1.5rem;line-height:2">
      <li>Open the <a href="{tool_url}">{tool_name}</a> page</li>
      <li>The tool loads instantly — no waiting, no loading screens</li>
      <li>Use it directly for your {uc_title.lower()} needs</li>
      <li>Results appear immediately — copy, download, or share as needed</li>
      <li>Bookmark the page for next time</li>
    </ol>
  </section>

  <section>
    <h2>Frequently Asked Questions</h2>
    {''.join(f'<details style="margin-bottom:12px"><summary style="cursor:pointer;font-weight:600;padding:8px 0">{q}</summary><p style="padding:8px 0 16px;color:var(--text-secondary)">{a}</p></details>' for q,a in faqs)}
  </section>

  <nav style="margin-top:40px;padding:24px;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius)">
    <h2 style="margin-top:0">🔗 More from ToolStand</h2>
    <ul style="list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px">
      <li><a href="{tool_url}" style="color:var(--primary);text-decoration:none;font-weight:500">{tool_name} — Main Tool</a></li>
      <li><a href="/" style="color:var(--primary);text-decoration:none;font-weight:500">All 110 Free Tools</a></li>
    </ul>
  </nav>
</main>
<footer class="footer">
  <div class="container">
    <p>🧰 <strong>ToolStand</strong> — Free tools, always.</p>
    <p class="small"><a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/about/">About</a></p>
  </div>
</footer>
<script src="/shared/bot-detect.js" defer></script>
<script src="/shared/analytics.js" defer></script>
</body>
</html>'''

# Generate pages
count = 0
for slug, cases in USE_CASES.items():
    # Get tool name from tools-data
    tool_name = slug.replace('-', ' ').title()
    
    for uc_slug, uc_title, desc in cases:
        out_dir = os.path.join(USE_CASES_DIR, uc_slug)
        os.makedirs(out_dir, exist_ok=True)
        
        html = make_page(slug, tool_name, uc_slug, uc_title, desc)
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)
        count += 1
        print(f"  {uc_slug}")

print(f"\nGenerated {count} use-case pages")
