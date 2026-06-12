# ToolStand 🧰

Free online tools. No downloads, no subscriptions, no dark patterns.

**108 tools** — all free, all browser-based, all embeddable.

🌐 **[toolstand.io](https://toolstand.io)**

## Categories

| Category | Tools | Hub |
|----------|-------|-----|
| 🔧 Everyday Tools | 21 | [/hubs/everyday-tools.html](https://toolstand.io/hubs/everyday-tools.html) |
| 🔄 Converters | 21 | [/hubs/converters.html](https://toolstand.io/hubs/converters.html) |
| ⚡ Generators | 18 | [/hubs/generators.html](https://toolstand.io/hubs/generators.html) |
| 💻 Developer Tools | 16 | [/hubs/developer-tools.html](https://toolstand.io/hubs/developer-tools.html) |
| 🧮 Calculators | 15 | [/hubs/calculators.html](https://toolstand.io/hubs/calculators.html) |
| 🎮 Games & Fun | 5 | [/hubs/games-fun.html](https://toolstand.io/hubs/games-fun.html) |
| 💰 Money & Finance | 5 | [/hubs/money-finance.html](https://toolstand.io/hubs/money-finance.html) |
| 🎨 Design & Creative | 4 | [/hubs/design-creative.html](https://toolstand.io/hubs/design-creative.html) |
| 💪 Health & Wellness | 3 | [/hubs/health-wellness.html](https://toolstand.io/hubs/health-wellness.html) |

## Performance

- 🖥️ Desktop: **99/100/96/100** (Performance / Accessibility / Best Practices / SEO)
- 📱 Mobile: **92/100/92/100**
- ⚡ FCP: 0.3s · LCP: 0.5s · CLS: 0.045

## Tech Stack

- **Hosting:** Cloudflare Pages (free, global CDN)
- **Domain:** Cloudflare Registrar
- **All client-side:** HTML + CSS + vanilla JS — no backend, no frameworks
- **Build:** `python3 build.py` — pre-renders tool cards, computes category counts
- **CSP:** Strict Content Security Policy via `_headers`
- **Service Worker:** PWAs-capable, offline support

## Nightly Quality Audit

Every night at 01:00 UTC, an automated audit scans all tools for:

- JavaScript syntax errors (`node --check`)
- HTML integrity (`<<script` typos, `<main>` balance, unwrapped JS)
- URL accessibility (200 OK check)
- **Auto-fix** for common issues, agent repair for complex ones

Script: `scripts/toolstand_audit.py`

## Embed Any Tool

Every tool has an embed page — just copy the iframe:

```html
<iframe src="https://toolstand.io/tools/qr-code/embed" width="100%" height="350"></iframe>
```

No ads on embed pages. No attribution required (but appreciated).

## Tools

- **📱 QR Code Generator & Scanner** → /tools/qr-code/
- **🔐 Hash Generator (SHA-256, SHA-1, SHA-512)** → /tools/hash-generator/
- **📐 Spirit Level** → /tools/spirit-level/
- **🍅 Pomodoro Timer** → /tools/pomodoro/
- **🎵 Metronome** → /tools/metronome/
- **🔊 Decibel Meter** → /tools/decibel-meter/
- **🎡 Decision Wheel** → /tools/decision-wheel/
- **🌙 Sleep Sounds & White Noise** → /tools/sleep-sounds/
- **🖥️ Dead Pixel Test** → /tools/dead-pixel-test/
- **👶 Pregnancy Due Date Calculator** → /tools/due-date-calculator/
- **✍️ Signature Generator** → /tools/signature-generator/
- **⚖️ BMI Calculator** → /tools/bmi-calculator/
- **🎂 Age Calculator** → /tools/age-calculator/
- **🔐 Password Generator** → /tools/password-generator/
- **📝 Word & Character Counter** → /tools/word-counter/
- **🔣 Base64 Encoder & Decoder** → /tools/base64/
- **🎨 Color Code Converter** → /tools/color-converter/
- **⏳ Countdown Timer** → /tools/countdown/
- **📺 DPI & PPI Calculator** → /tools/dpi-calculator/
- **🏛️ Roman Numeral Converter** → /tools/roman-numerals/
- **💵 Tip Calculator** → /tools/tip-calculator/
- **📈 Compound Interest Calculator** → /tools/compound-interest/
- **💎 Dividend Reinvestment Calculator** → /tools/dividend-calculator/
- **💣 Minesweeper** → /tools/minesweeper/
- **🐍 Snake Game** → /tools/snake-game/
- **⚡ Reaction Time Test** → /tools/reaction-time/
- **🔉 Frequency Generator** → /tools/tone-generator/
- **📋 Text Diff Checker** → /tools/diff-checker/
- **🎬 Video Script Timer** → /tools/video-script-timer/
- **📹 YouTube Title Generator** → /tools/youtube-title-generator/
- **🤖 AI Token Counter** → /tools/token-counter/
- **📦 JSON Formatter** → /tools/json-formatter/
- **📊 Trade Risk Calculator** → /tools/trade-risk-calculator/
- **💸 DCA Calculator** → /tools/dca-calculator/
- **🥑 Keto Calculator** → /tools/keto-calculator/
- **🆔 UUID Generator** → /tools/uuid-generator/
- **🎫 JWT Decoder** → /tools/jwt-decoder/
- **🕐 Unix Timestamp Converter** → /tools/timestamp-converter/
- **🔗 URL Encoder & Decoder** → /tools/url-encoder/
- **🏷️ HTML Entity Encoder** → /tools/html-entity-encoder/
- **🔤 Case Converter** → /tools/case-converter/
- **🔢 Number Base Converter** → /tools/base-converter/
- **⏱️ Stopwatch** → /tools/stopwatch/
- **📅 Date Difference Calculator** → /tools/date-difference/
- **📊 UTM Builder** → /tools/utm-builder/
- **🤖 Robots.txt Generator** → /tools/robots-txt-generator/
- **🏷️ Meta Tag Generator** → /tools/meta-tag-generator/
- **🎨 Color Palette Generator** → /tools/color-palette-generator/
- **📝 Lorem Ipsum Generator** → /tools/lorem-ipsum/
- **🕐 Cron Expression Builder** → /tools/cron-builder/
- **🔍 Regex Tester** → /tools/regex-tester/
- **📄 Markdown Previewer** → /tools/markdown-previewer/
- **🔒 Password Strength Checker** → /tools/password-strength-checker/
- **📐 Unit Converter** → /tools/unit-converter/
- **📖 Readability Checker** → /tools/readability-checker/
- **🌍 Time Zone Converter** → /tools/timezone-converter/
- **🔍 JSON Compare** → /tools/json-compare/
- **💧 Water Intake Calculator** → /tools/water-intake/
- **🌈 Gradient Generator** → /tools/gradient-generator/
- **📋 JSON Schema Generator** → /tools/json-schema-generator/
- **✅ YAML Validator** → /tools/yaml-validator/
- **🗄️ SQL Formatter** → /tools/sql-formatter/
- **📊 Barcode Generator** → /tools/barcode-generator/
- **🔢 Scientific Calculator** → /tools/scientific-calculator/
- **🌡️ Temperature Tracker** → /tools/temperature-tracker/
- **🔍 Regex Explainer** → /tools/regex-explainer/
- **📄 XML Formatter** → /tools/xml-formatter/
- **🔄 XML ↔ JSON Converter** → /tools/xml-json-converter/
- **📊 CSV ↔ JSON Converter** → /tools/csv-json-converter/
- **🔎 JSONPath Tester** → /tools/jsonpath-tester/
- **🔍 SERP Preview** → /tools/serp-preview/
- **📈 Inflation Calculator** → /tools/inflation-calculator/
- **🎲 Random Number Generator** → /tools/random-number/
- **📐 Aspect Ratio Calculator** → /tools/aspect-ratio/
- **🔐 Text Encryptor** → /tools/text-encryptor/
- **🔑 SSH Key Generator** → /tools/ssh-key-generator/
- **🎵 BPM Tap Tempo** → /tools/bpm-tap/
- **👁️ Open Graph Preview** → /tools/og-preview/
- **🖼️ Image Resizer** → /tools/image-resizer/
- **🔄 Image Format Converter** → /tools/image-converter/
- **🏦 Loan & Mortgage Calculator** → /tools/loan-calculator/
- **🔥 Calorie & TDEE Calculator** → /tools/calorie-calculator/
- **👁️ Color Blindness Simulator** → /tools/color-blindness/
- **🏃 Pace & Running Calculator** → /tools/pace-calculator/
- **✅ Pomodoro + Task Tracker** → /tools/pomodoro-task/
- **💱 Currency Converter** → /tools/currency-converter/
- **📈 Function Graph Plotter** → /tools/function-plotter/
- **🧾 Invoice Generator** → /tools/invoice-generator/
- **🧩 Wordle Solver** → /tools/wordle-solver/
- **📑 PDF Merge** → /tools/pdf-merge/
- **✂️ PDF Split** → /tools/pdf-split/
- **🖼️ Image to PDF** → /tools/image-to-pdf/
- **📄 PDF to Image** → /tools/pdf-to-image/
- **🏗️ Schema Markup Generator** → /tools/schema-markup-generator/
- **❓ FAQ Schema Generator** → /tools/faq-schema-generator/
- **💰 Savings Calculator** → /tools/savings-calculator/
- **👴 Retirement Calculator** → /tools/retirement-calculator/
- **💪 Body Fat Calculator** → /tools/body-fat-calculator/
- **✂️ SVG Optimizer** → /tools/svg-optimizer/
- **📦 CSS Box Shadow Generator** → /tools/css-box-shadow/
- **🔲 CSS Border Radius Generator** → /tools/css-border-radius/
- **📏 CSS Clamp Generator** → /tools/css-clamp-generator/
- **🗜️ JSON Minifier** → /tools/json-minifier/
- **☕ JSON to Java POJO** → /tools/json-to-java/
- **🤖 AI Prompt Builder** → /tools/ai-prompt-builder/
- **🐳 Dockerfile Generator** → /tools/dockerfile-generator/
- **🔍 Meta Tag & SERP Preview** → /tools/meta-tag-preview/
- **📊 Markdown Table Generator** → /tools/markdown-table/

## Blog

- [SHA-256 Hash Generator: 9 Smart Categories & 108 Free Tools](https://toolstand.io/blog/sha256-hash-generator-9-categories-108-tools/) — June 2026
- [10 New Free PDF, SEO & Finance Tools](https://toolstand.io/blog/10-new-free-pdf-seo-finance-health-tools/) — May 2026

## License

MIT — use them, embed them, build on them. Just don't remove the attribution if you fork.
