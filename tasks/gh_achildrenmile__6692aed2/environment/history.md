> DEVELOPER

Implement the following plan:

# Plan: Krisenkommunikation-Seite mit PDF-Download & Online-Formular

## Context
Das Krisenkommunikation-Aufnahmeformular ist ein zentrales Dokument für den Notfunkbetrieb. Es soll als eigene Seite auf der BOS-ARSA-Website verfügbar sein — sowohl als druckbare PDF als auch als interaktives Online-Formular, das client-seitig ausgefüllt und als PDF heruntergeladen werden kann.

## Neue Dateien (5)

### 1. `src/krisenkommunikation.njk` — Seitentemplate
- Layout: `base.njk`, `pageCSSFile: "/css/krisenkommunikation.css"`
- **Abschnitt 1**: Download-Card mit Link zur statischen PDF
- **Divider**: "oder online ausfüllen"
- **Abschnitt 2**: HTML-Formular mit allen Feldern des Aufnahmeformulars:
  - Lfd. Nr., Entgegennahme (Rufzeichen, QTH, QRG, Telefon), Datum/Uhrzeit
  - Notruf durch, 7 W-Fragen (WER–WARUM) als Textareas
  - Weitergabe-Tabelle (3 feste + 2 freie Organisationen mit Checkboxen)
  - Erledigt (Wann, Durch)
- **Buttons**: "Als PDF herunterladen" + "Formular leeren"
- Scripts am Seitenende: `jspdf.umd.min.js` + `krisenkommunikation-pdf.js`

### 2. `src/css/krisenkommunikation.css` — Seitenstile
- Download-Card, Divider, Formularfelder, Weitergabe-Grid
- Responsive: 4-Spalten → 2 → 1 auf Mobil; Weitergabe-Tabelle stapelt sich

### 3. `js/jspdf.umd.min.js` — jsPDF-Bibliothek (self-hosted)
- Download von cdnjs (~300KB), Root-`js/`-Ordner neben `lucide.min.js`

### 4. `js/krisenkommunikation-pdf.js` — PDF-Generierung
- Liest Formularwerte, erzeugt A4-PDF mit jsPDF
- Logo (bosarsa.jpeg) wird beim Seitenaufruf als Base64 vorgeladen
- Tabellenstruktur mit Linien/Rahmen wie das Original
- Seitenumbruch […]

> AGENT

I'll implement this plan step by step. Let me start by reading the existing files I need to modify, and download jsPDF.

> TOOL

tool_use TaskCreate
id: toolu_01E7FPXx57zvRNDGRidEw7F3
```json
{
  "subject": "Download jsPDF and copy static PDF",
  "description": "Download jsPDF UMD bundle from cdnjs into js/ folder, and handle the static PDF",
  "activeForm": "Downloading jsPDF library"
}
```

> TOOL

tool_result
id: toolu_01E7FPXx57zvRNDGRidEw7F3
```
Task #1 created successfully: Download jsPDF and copy static PDF
```

> TOOL

tool_use TaskCreate
id: toolu_01F8P5eFbshruDbnAJ5LTUod
```json
{
  "subject": "Update .eleventy.js passthrough rules",
  "description": "Add passthrough for js/ folder and *.pdf files",
  "activeForm": "Updating Eleventy config"
}
```

> TOOL

tool_result
id: toolu_01F8P5eFbshruDbnAJ5LTUod
```
Task #2 created successfully: Update .eleventy.js passthrough rules
```

> TOOL

tool_use TaskCreate
id: toolu_01EzneDEaqBQFXTDxqYBLnc5
```json
{
  "subject": "Create CSS, JS, and page template",
  "description": "Create krisenkommunikation.css, krisenkommunikation-pdf.js, and krisenkommunikation.njk",
  "activeForm": "Creating page files"
}
```

> TOOL

tool_result
id: toolu_01EzneDEaqBQFXTDxqYBLnc5
```
Task #3 created successfully: Create CSS, JS, and page template
```

> TOOL

tool_use TaskCreate
id: toolu_013f24uFhipMgggC1BStdSSa
```json
{
  "subject": "Update footer, sitemap, llms.txt",
  "description": "Add navigation link, sitemap entry, and LLMs description",
  "activeForm": "Updating existing files"
}
```

> TOOL

tool_result
id: toolu_013f24uFhipMgggC1BStdSSa
```
Task #4 created successfully: Update footer, sitemap, llms.txt
```

> TOOL

tool_use TaskCreate
id: toolu_0158pYTgMf75NxcS1GrJyQxs
```json
{
  "subject": "Build and verify",
  "description": "Run Eleventy build and verify all output files exist",
  "activeForm": "Building and verifying"
}
```

> TOOL

tool_result
id: toolu_0158pYTgMf75NxcS1GrJyQxs
```
Task #5 created successfully: Build and verify
```

> AGENT

Now let me read all the files I need to understand and modify in parallel.

> TOOL

tool_use Read
id: toolu_01MfH312HXZsP2uQzMJhDgJy
```json
{
  "file_path": "/home/<USER>/bosarsa/.eleventy.js"
}
```

> TOOL

tool_result
id: toolu_01MfH312HXZsP2uQzMJhDgJy
```
     1→module.exports = function(eleventyConfig) {
     2→  // Passthrough copy — static assets stay in root
     3→  eleventyConfig.addPassthroughCopy({ "fonts": "fonts" });
     4→  eleventyConfig.addPassthroughCopy({ "favicon": "/" });
     5→  eleventyConfig.addPassthroughCopy({ "*.mp4": "/" });
     6→  eleventyConfig.addPassthroughCopy({ "*.png": "/" });
     7→  eleventyConfig.addPassthroughCopy({ "*.webp": "/" });
     8→  eleventyConfig.addPassthroughCopy("src/css");
     9→
    10→  return {
    11→    dir: {
    12→      input: "src",
    13→      output: "_site",
    14→      includes: "_includes",
    15→      data: "_data"
    16→    },
    17→    templateFormats: ["njk", "md"],
    18→    htmlTemplateEngine: "njk",
    19→    markdownTemplateEngine: "njk"
    20→  };
    21→};
    22→

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use Read
id: toolu_01RRpDeTw6DTNCSnmfR371Lv
```json
{
  "file_path": "/home/<USER>/bosarsa/src/_includes/footer.njk"
}
```

> TOOL

tool_result
id: toolu_01RRpDeTw6DTNCSnmfR371Lv
```
     1→<footer class="footer" id="kontakt">
     2→  <div class="container">
     3→    <div class="footer__inner">
     4→      <div>
     5→        <div class="footer__brand">
     6→          <img src="/logo.webp?v=2" alt="BOS-ARSA" class="footer__brand-logo" width="160" height="63">
     7→          <span class="footer__brand-name">BOS-ARSA</span>
     8→        </div>
     9→        <p class="footer__org-name">{{ site.fullName }} – {{ site.legalName }}</p>
    10→        <div class="footer__details">
    11→          {{ site.address.care }}<br>
    12→          {{ site.address.zip }} {{ site.address.city }}, {{ site.address.street }}<br><br>
    13→          Zuständige Vereinsbehörde: {{ site.vereinsbehoerde }}<br>
    14→          ZVR-Zahl: {{ site.zvr }}<br><br>
    15→          <a href="mailto:{{ site.email }}">{{ site.email }}</a>
    16→        </div>
    17→      </div>
    18→      <div>
    19→        <div class="footer__links-title">Navigation</div>
    20→        <ul class="footer__link-list">
    21→          <li><a href="/#ueber-uns">Über uns</a></li>
    22→          <li><a href="/#vorstand">Vorstand</a></li>
    23→          <li><a href="/#ziele">Ziele</a></li>
    24→          <li><a href="/#funkbetrieb">Funkbetrieb</a></li>
    25→          <li><a href="/#mitglied">Mitglied werden</a></li>
    26→          <li><a href="/termine/">Termine</a></li>
    27→          <li><a href="/presse/">Presse</a></li>
    28→          <li><a href="mailto:{{ site.email }}">Kontakt</a></li>
    29→        </ul>
    30→      </div>
    31→      <div>
    32→        <div class="footer__links-title">Rechtliches & Links</div>
    33→        <ul class="footer__link-list">
    34→          <li><a href="/impressum/">Impressum</a></li>
    35→          <li><a href="/datenschutz/">Datenschutz</a></li>
    36→          <li><a href="https://oe8.oevsv.at/ortsstellen/adl820/" target="_blank" rel="noopener noreferrer">ADL820 im ÖVSV</a></li>
    37→          <li><a href="https://bosarsalog.oeradio.at" target="_blank" rel="noopener noreferrer">bosarsalog.oeradio.at</a></li>
    38→          <li><a href="https://oeradio.at" target="_blank" rel="noopener noreferrer">oeradio.at</a></li>
    39→        </ul>
    40→      </div>
    41→    </div>
    42→    <div class="footer__bottom">
    43→      <span>&copy; <span id="year"></span> BOS-ARSA. Alle Rechte vorbehalten.</span>
    44→      <span>Amateurfunk im Sinne der Sicherheit</span>
    45→    </div>
    46→  </div>
    47→</footer>

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and […]

> TOOL

tool_use Read
id: toolu_017MXLzCxbAz27c1uiwExZ7q
```json
{
  "file_path": "/home/<USER>/bosarsa/src/sitemap.njk"
}
```

> TOOL

tool_result
id: toolu_017MXLzCxbAz27c1uiwExZ7q
```
     1→---
     2→permalink: /sitemap.xml
     3→eleventyExcludeFromCollections: true
     4→---
     5→<?xml version="1.0" encoding="UTF-8"?>
     6→<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     7→  <url>
     8→    <loc>{{ site.url }}/</loc>
     9→    <lastmod>2026-02-22</lastmod>
    10→    <changefreq>monthly</changefreq>
    11→    <priority>1.0</priority>
    12→  </url>
    13→  <url>
    14→    <loc>{{ site.url }}/presse/</loc>
    15→    <lastmod>2026-02-22</lastmod>
    16→    <changefreq>monthly</changefreq>
    17→    <priority>0.6</priority>
    18→  </url>
    19→  <url>
    20→    <loc>{{ site.url }}/termine/</loc>
    21→    <lastmod>2026-03-06</lastmod>
    22→    <changefreq>weekly</changefreq>
    23→    <priority>0.7</priority>
    24→  </url>
    25→  <url>
    26→    <loc>{{ site.url }}/impressum/</loc>
    27→    <lastmod>2026-02-22</lastmod>
    28→    <changefreq>yearly</changefreq>
    29→    <priority>0.3</priority>
    30→  </url>
    31→  <url>
    32→    <loc>{{ site.url }}/datenschutz/</loc>
    33→    <lastmod>2026-02-22</lastmod>
    34→    <changefreq>yearly</changefreq>
    35→    <priority>0.3</priority>
    36→  </url>
    37→</urlset>

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use Read
id: toolu_01ELGhHvBVNEVr8Hp7jxfcJN
```json
{
  "file_path": "/home/<USER>/bosarsa/src/llms.njk"
}
```

> TOOL

tool_result
id: toolu_01ELGhHvBVNEVr8Hp7jxfcJN
```
     1→---
     2→permalink: /llms.txt
     3→eleventyExcludeFromCollections: true
     4→---
     5→# {{ site.name }} — {{ site.fullName }}
     6→
     7→> {{ site.legalName }} ist ein österreichischer Verein, der den Amateurfunk innerhalb der Behörden und Organisationen mit Sicherheitsaufgaben (BOS) fördert. Der Verein stellt sicher, dass Kommunikation auch dann funktioniert, wenn herkömmliche Infrastruktur ausfällt.
     8→
     9→## Über den Verein
    10→
    11→BOS-ARSA wurde gegründet, um den Amateurfunk als zuverlässige Notfall- und Sicherheitskommunikation in Österreich zu etablieren. Der Verein richtet sich an Mitglieder von Behörden und Organisationen mit Sicherheitsaufgaben (BOS), darunter Polizei, Feuerwehr, Rettungsdienste und Katastrophenschutz.
    12→
    13→## Zweck
    14→
    15→Der Verein bezweckt die Erhaltung, Förderung und Verbreitung des Amateurfunkwesens innerhalb des Wirkungsbereiches der Behörden und Organisationen mit Sicherheitsaufgaben (BOS).
    16→
    17→## Ziele
    18→
    19→- Ausbildung & Lizenzierung: Unterstützung bei der Erlangung von Amateurfunklizenzen für BOS-Angehörige
    20→- Notfallkommunikation: Aufbau redundanter Kommunikationswege für Krisensituationen
    21→- Netzwerkaufbau: Vernetzung von Funkamateurinnen und Funkamateuren im BOS-Bereich in ganz Österreich
    22→- Übungen & Training: Regelmäßige Funkübungen und Weiterbildungen
    23→- Zusammenarbeit: Kooperation mit Behörden, Einsatzorganisationen und verwandten Vereinen
    24→
    25→## Vorstand
    26→
    27→- Präsident: Gabrutsch Wolfgang, BA MBA MBA DBA
    28→- Generalsekretär: Londer Erich, BA
    29→- Kassier: Ing. René Camaur
    30→- Kassier Stellvertreter: Joham Thomas
    31→- Schriftführer: Kugi Jürgen
    32→- […]

> AGENT

Now let me read a few more reference files and check for existing assets.

> TOOL

tool_use Read
id: toolu_01Ur8pY7kq86t3v36RVkKTHe
```json
{
  "file_path": "/home/<USER>/bosarsa/src/css/base.css"
}
```

> TOOL

tool_result
id: toolu_01Ur8pY7kq86t3v36RVkKTHe
```
     1→/* Local Fonts — DSGVO-konform, kein Google-Aufruf */
     2→@font-face {
     3→  font-family: 'Inter';
     4→  font-style: normal;
     5→  font-weight: 300 800;
     6→  font-display: swap;
     7→  src: url(/fonts/inter-latin.woff2) format('woff2');
     8→  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
     9→}
    10→@font-face {
    11→  font-family: 'Inter';
    12→  font-style: normal;
    13→  font-weight: 300 800;
    14→  font-display: swap;
    15→  src: url(/fonts/inter-latin-ext.woff2) format('woff2');
    16→  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
    17→}
    18→@font-face {
    19→  font-family: 'JetBrains Mono';
    20→  font-style: normal;
    21→  font-weight: 400 500;
    22→  font-display: swap;
    23→  src: url(/fonts/jetbrains-mono-latin.woff2) format('woff2');
    24→  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    25→}
    26→@font-face {
    27→  font-family: 'JetBrains Mono';
    28→  font-style: normal;
    29→  font-weight: 400 500;
    30→  font-display: swap;
    31→  src: url(/fonts/jetbrains-mono-latin-ext.woff2) format('woff2');
    32→  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
    33→}
    34→
    35→*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    36→
    37→:root {
    38→  /* Austrian Police Uniform Blues — derived from Bundespolizei dunkelblau […]

> AGENT

Now let me look at an existing page for reference, and check for the logo file and existing JS.

> TOOL

tool_use Read
id: toolu_01JLTWBfEGa8PLYisq9rqJZ6
```json
{
  "file_path": "/home/<USER>/bosarsa/src/presse.njk"
}
```

> TOOL

tool_result
id: toolu_01JLTWBfEGa8PLYisq9rqJZ6
```
     1→---
     2→layout: base.njk
     3→title: "Presse — BOS-ARSA"
     4→description: "Pressespiegel und Medienberichte über BOS-ARSA – Österreichischer Amateurfunkverein der Behörden und Organisationen mit Sicherheitsaufgaben"
     5→canonical: "https://bosarsa.oeradio.at/presse/"
     6→activeNav: presse
     7→permalink: /presse/
     8→---
     9→
    10→<div class="page-content">
    11→  <h1>Presse & Medien</h1>
    12→  <p class="subtitle">Berichte, Artikel und Podcasts über BOS-ARSA in chronologischer Reihenfolge</p>
    13→
    14→  {% for article in presse %}
    15→  <a class="article" href="{{ article.url }}" target="_blank" rel="noopener noreferrer">
    16→    <div class="article__date">{{ article.date }} <span class="article__tag article__tag--{{ article.tag }}">{{ article.tagLabel }}</span></div>
    17→    <h2 class="article__title">{{ article.title }}</h2>
    18→    <div class="article__source">{{ article.source }}</div>
    19→    <p class="article__desc">{{ article.desc }}</p>
    20→  </a>
    21→  {% endfor %}
    22→</div>

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use Glob
id: toolu_015AAB9Mc45ofSj8MVenyXt5
```json
{
  "pattern": "*.jpeg",
  "path": "/home/<USER>/bosarsa"
}
```

> TOOL

tool_result
id: toolu_015AAB9Mc45ofSj8MVenyXt5
```
No files found
```

> TOOL

tool_use Glob
id: toolu_01KTRwGmMjTmMFpNgwB11vMZ
```json
{
  "pattern": "bosarsa.*",
  "path": "/home/<USER>/bosarsa"
}
```

> TOOL

tool_result
id: toolu_01KTRwGmMjTmMFpNgwB11vMZ
```
No files found
```

> TOOL

tool_use Glob
id: toolu_019ZKx749JsMbuxACQbgygjZ
```json
{
  "pattern": "*.{jpeg,jpg,webp,png}",
  "path": "/home/<USER>/bosarsa"
}
```

> TOOL

tool_result
id: toolu_019ZKx749JsMbuxACQbgygjZ
```
/home/<USER>/bosarsa/favicon/web-app-manifest-512x512.png
/home/<USER>/bosarsa/favicon/web-app-manifest-192x192.png
/home/<USER>/bosarsa/favicon/favicon-96x96.png
/home/<USER>/bosarsa/favicon/apple-touch-icon.png
/home/<USER>/bosarsa/_site/web-app-manifest-512x512.png
/home/<USER>/bosarsa/_site/web-app-manifest-192x192.png
/home/<USER>/bosarsa/_site/favicon-96x96.png
/home/<USER>/bosarsa/_site/apple-touch-icon.png
/home/<USER>/bosarsa/_site/logo-web.png
/home/<USER>/bosarsa/logo-web.png
/home/<USER>/bosarsa/logo.webp
/home/<USER>/bosarsa/_site/logo.webp
/home/<USER>/bosarsa/_site/og-image.png
/home/<USER>/bosarsa/og-image.png
/home/<USER>/bosarsa/ueber-uns.webp
/home/<USER>/bosarsa/_site/ueber-uns.webp
/home/<USER>/bosarsa/notfunk-header.webp
/home/<USER>/bosarsa/_site/notfunk-header.webp
/home/<USER>/bosarsa/sicherheitstage-2026.webp
/home/<USER>/bosarsa/_site/sicherheitstage-2026.webp
```

> TOOL

tool_use Glob
id: toolu_018knFpdZP9BQjVTE9JdUpSF
```json
{
  "pattern": "js/**",
  "path": "/home/<USER>/bosarsa"
}
```

> TOOL

tool_result
id: toolu_018knFpdZP9BQjVTE9JdUpSF
```
/home/<USER>/bosarsa/js/lucide.min.js
```

> TOOL

tool_use Glob
id: toolu_01ACz1MYZTY9SpjjVcmJG6U5
```json
{
  "pattern": "*.pdf",
  "path": "/home/<USER>/bosarsa"
}
```

> TOOL

tool_result
id: toolu_01ACz1MYZTY9SpjjVcmJG6U5
```
No files found
```

> AGENT

Let me also check the plan transcript to get the PDF content details and the form fields.

> TOOL

tool_use Read
id: toolu_01JXy7J3v6KB4JgKqL9EjSuH
```json
{
  "file_path": "/home/<USER>/bosarsa/src/_includes/base.njk"
}
```

> TOOL

tool_result
id: toolu_01JXy7J3v6KB4JgKqL9EjSuH
```
     1→<!DOCTYPE html>
     2→<html lang="de">
     3→<head>
     4→  <meta charset="UTF-8">
     5→  <meta name="viewport" content="width=device-width, initial-scale=1.0">
     6→  <title>{{ title }}</title>
     7→  <meta name="description" content="{{ description }}">
     8→  {% if keywords %}<meta name="keywords" content="{{ keywords }}">{% endif %}
     9→  <meta name="author" content="BOS-ARSA">
    10→  <meta name="robots" content="index, follow">
    11→  <link rel="canonical" href="{{ canonical }}">
    12→  <!-- Open Graph -->
    13→  <meta property="og:title" content="{{ title }}">
    14→  <meta property="og:description" content="{{ ogDescription | default(description) }}">
    15→  <meta property="og:type" content="website">
    16→  <meta property="og:url" content="{{ canonical }}">
    17→  <meta property="og:locale" content="de_AT">
    18→  <meta property="og:site_name" content="BOS-ARSA">
    19→  <meta property="og:image" content="{{ site.url }}/og-image.png">
    20→  <meta property="og:image:width" content="1200">
    21→  <meta property="og:image:height" content="630">
    22→  <meta property="og:image:alt" content="BOS-ARSA — Amateurfunk im Sinne der Sicherheit">
    23→  <!-- Twitter Card -->
    24→  <meta name="twitter:card" content="summary_large_image">
    25→  <meta name="twitter:title" content="{{ title }}">
    26→  <meta name="twitter:description" content="{{ ogDescription | default(description) }}">
    27→  <meta name="twitter:image" content="{{ site.url }}/og-image.png">
    28→  {% if structuredData %}
    29→  <!-- Structured Data -->
    30→  <script type="application/ld+json">
    31→  {{ structuredData | dump | safe }}
    32→  </script>
    33→  {% endif %}
    34→  <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
    35→  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    36→  <link rel="shortcut icon" href="/favicon.ico">
    37→  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    38→  <link rel="manifest" href="/site.webmanifest">
    39→  <script src="/js/lucide.min.js"></script>
    40→  <link […]

> AGENT

Now let me check the plan transcript for more details about the form structure.

> TOOL

tool_use Task
id: toolu_01RMynmPteDYWU969JemnFeF
```json
{
  "description": "Read plan transcript for details",
  "prompt": "Read the file /home/<USER>/.REDACTED.jsonl and extract the detailed information about:\n1. The Krisenkommunikation form fields and structure (the 7 W-Fragen, the Weitergabe table organizations, etc.)\n2. Any specific details about how the PDF generation should work\n3. Any details about the static PDF that needs to be created\n4. Any specific CSS design details\n\nReturn ALL the details you find about the form structure, field names, organizations for the Weitergabe table, and PDF layout.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: toolu_01RMynmPteDYWU969JemnFeF
```
Good. I have the main information. Now let me compile a comprehensive report. Based on my search, I found the complete specification from line 1527 of the JSONL file. Let me create a final summary:

## COMPREHENSIVE EXTRACTION: Krisenkommunikation Form Structure and PDF Generation Details

Based on my analysis of `/home/<USER>/.REDACTED.jsonl`, here are ALL the detailed specifications for the Krisenkommunikation form:

### 1. FORM FIELDS STRUCTURE (7 W-Fragen and other fields)

The form contains the following fields organized in sections:

**Section 1: Header/Meta Information**
- `Lfd. Nr.` — Running number (sequential)

**Section 2: Entgegennahme durch (Reception Information)**
- `Mein Rufzeichen` — Operator's call sign
- `Mein QTH` — Operator's location
- `QRG` — Frequency
- `Telefon` — Phone number

**Section 3: Time Information**
- `Aufnahmedatum` — Reception date
- `Aufnahmeuhrzeit (MEZ)` — Reception time (Central European Time)

**Section 4: Emergency Call Information**
- `Notruf durch` — Emergency call received from (free text)

**Section 5: The 7 W-Questions (7 W-Fragen)**
- `WER` — Who (free text field)
- `WAS` — What (free text field)
- `WANN` — When (free text field)
- `WO` — Where (free text field)
- `WIE` — How (free text field)
- `WOMIT` […]

> AGENT

Now I have all the details. Let me start implementing. First, let me handle Task #1 — download jsPDF and check for the static PDF.

> TOOL

tool_use TaskUpdate
id: toolu_01GJgf7SYkbtV7vVMwTHPmK9
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01GJgf7SYkbtV7vVMwTHPmK9
```
Updated task #1 status
```

> TOOL

tool_use Bash
id: toolu_01Scb7ifiysnmvTP5jVyJnYK
```json
{
  "command": "ls -la /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular.pdf 2>/dev/null || echo \"PDF not found in Downloads\"",
  "description": "Check for static PDF in Downloads"
}
```

> TOOL

tool_result
id: toolu_01Scb7ifiysnmvTP5jVyJnYK
```
-rw-r--r-- 1 achildrenmile users 586213 Mar  8 00:11 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular.pdf
```

> TOOL

tool_use Bash
id: toolu_01KKaSLE9R3pAn5QyqJCHuXZ
```json
{
  "command": "cp /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular.pdf /home/<USER>/bosarsa/Krisenkommunikation-Aufnahmeformular.pdf",
  "description": "Copy static PDF to project root"
}
```

> TOOL

tool_result
id: toolu_01KKaSLE9R3pAn5QyqJCHuXZ
```

```

> AGENT

Now download jsPDF from cdnjs.

> TOOL

tool_use Bash
id: toolu_0188uiVKD83bKrn8HebUTddd
```json
{
  "command": "curl -sL \"https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.2/jspdf.umd.min.js\" -o /home/<USER>/bosarsa/js/jspdf.umd.min.js && wc -c /home/<USER>/bosarsa/js/jspdf.umd.min.js",
  "description": "Download jsPDF UMD bundle from cdnjs",
  "timeout": 30000
}
```

> TOOL

tool_result
id: toolu_0188uiVKD83bKrn8HebUTddd
```
548 /home/<USER>/bosarsa/js/jspdf.umd.min.js
```

> AGENT

That's way too small — likely a redirect or error page. Let me try a different version/URL.

> TOOL

tool_use Bash
id: toolu_014GF5hkQkDzqYY5SvGkxFv6
```json
{
  "command": "head -c 200 /home/<USER>/bosarsa/js/jspdf.umd.min.js",
  "description": "Check what was downloaded"
}
```

> TOOL

tool_result
id: toolu_014GF5hkQkDzqYY5SvGkxFv6
```
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
<!-- a padding to disable MSIE and Chrome friendly err
```

> AGENT

Not found. Let me find the correct URL.

> TOOL

tool_use WebSearch
id: toolu_013uFxHSCDfRhKpybMhuyLSy
```json
{
  "query": "cdnjs jspdf umd min js latest version URL 2025"
}
```

> TOOL

tool_result
id: toolu_013uFxHSCDfRhKpybMhuyLSy
```
Web search results for query: "cdnjs jspdf umd min js latest version URL 2025"

Links: [{"title":"jspdf - Libraries - cdnjs - The #1 free and open source CDN built to make life easier for developers","url":"https://cdnjs.com/libraries/jspdf"},{"title":"jsPDF","url":"https://artskydj.github.io/jsPDF/docs/index.html"},{"title":"jspdf - npm","url":"https://www.npmjs.com/package/jspdf"},{"title":"JSPDF.UMD.MIN.JS: DOWNLOAD - CDNPKG","url":"https://www.cdnpkg.com/jspdf/file/jspdf.umd.min.js/"},{"title":"jspdf CDN by jsDelivr - A CDN for npm and GitHub","url":"https://www.jsdelivr.com/package/npm/jspdf"},{"title":"JSPDF.MIN.JS: DOWNLOAD - CDNPKG","url":"https://www.cdnpkg.com/jspdf/file/jspdf.min.js/"},{"title":"jspdf","url":"https://app.unpkg.com/jspdf@2.0.0/files/dist/jspdf.umd.min.js.map"},{"title":"jspdf.umd.min.js.map","url":"https://unpkg.com/browse/jspdf@2.0.0/dist/jspdf.umd.min.js.map"},{"title":"jspdf/README.md","url":"https://unpkg.com/browse/jspdf@2.0.0/README.md"},{"title":"Link to CDN in README is 404 · Issue #3947 · parallax/jsPDF","url":"https://github.com/parallax/jsPDF/issues/3947"}]

Based on the search results, here's what I found about the jsPDF UMD minified file on CDN:

## CDNJS Latest Version URL

The latest version available on cdnjs is: `https://cdnjs.cloudflare.com/ajax/libs/jspdf/3.0.3/jspdf.umd.min.js`

## Alternative CDN Options

If you want the very latest version available, the latest version is 4.2.0, but note that version 3.0.3 is the latest available on cdnjs, though newer versions like 4.0.0 have been released.

For the latest version, you can use:
- **unpkg**: `https://unpkg.com/jspdf@latest/dist/jspdf.umd.min.js` (always gets the latest)
- **CDNJS**: `https://cdnjs.cloudflare.com/ajax/libs/jspdf/3.0.3/jspdf.umd.min.js` (most recent on this CDN)


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
```

> TOOL

tool_use Bash
id: toolu_01C8GSpRGGaP9ojQuzHEGtiR
```json
{
  "command": "curl -sL \"https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js\" -o /home/<USER>/bosarsa/js/jspdf.umd.min.js && wc -c /home/<USER>/bosarsa/js/jspdf.umd.min.js",
  "description": "Download jsPDF 2.5.1 from cdnjs",
  "timeout": 30000
}
```

> TOOL

tool_result
id: toolu_01C8GSpRGGaP9ojQuzHEGtiR
```
364463 /home/<USER>/bosarsa/js/jspdf.umd.min.js
```

> AGENT

That's the right size (~356KB). Let me verify it's valid JS.

> TOOL

tool_use Bash
id: toolu_01HAq2aNGG2rceDBHLobEQJy
```json
{
  "command": "head -c 100 /home/<USER>/bosarsa/js/jspdf.umd.min.js",
  "description": "Verify jsPDF is valid JS"
}
```

> TOOL

tool_result
id: toolu_01HAq2aNGG2rceDBHLobEQJy
```
/** @license
 *
 * jsPDF - PDF Document creation from JavaScript
 * Version 2.5.1 Built on 2022-01-2
```

> AGENT

jsPDF is downloaded. Task 1 done.

> TOOL

tool_use TaskUpdate
id: toolu_01AjooYYwHtekFThijtu25Qk
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01AjooYYwHtekFThijtu25Qk
```
Updated task #1 status
```

> AGENT

Now Task #2 — update `.eleventy.js` passthrough rules.

> TOOL

tool_use TaskUpdate
id: toolu_012hewwyrUN6AeVRgahgk8M1
```json
{
  "taskId": "2",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_012hewwyrUN6AeVRgahgk8M1
```
Updated task #2 status
```

> TOOL

tool_use Edit
id: toolu_016QKDdJpLzZzESJTQrM3bds
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/.eleventy.js",
  "old_string": "  eleventyConfig.addPassthroughCopy({ \"*.webp\": \"/\" });\n  eleventyConfig.addPassthroughCopy(\"src/css\");",
  "new_string": "  eleventyConfig.addPassthroughCopy({ \"*.webp\": \"/\" });\n  eleventyConfig.addPassthroughCopy({ \"*.pdf\": \"/\" });\n  eleventyConfig.addPassthroughCopy({ \"js\": \"js\" });\n  eleventyConfig.addPassthroughCopy(\"src/css\");"
}
```

> TOOL

tool_result
id: toolu_016QKDdJpLzZzESJTQrM3bds
```
The file /home/<USER>/bosarsa/.eleventy.js has been updated successfully.
```

> TOOL

tool_use TaskUpdate
id: toolu_013kQcQwCfLR3rqUh87gtJvD
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_013kQcQwCfLR3rqUh87gtJvD
```
Updated task #2 status
```

> AGENT

Now Task #3 — create the CSS, JS, and page template. Let me start with all three files.

> TOOL

tool_use TaskUpdate
id: toolu_01XEE4KSwr5APiCSY94StYJ3
```json
{
  "taskId": "3",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01XEE4KSwr5APiCSY94StYJ3
```
Updated task #3 status
```

> TOOL

tool_use Write
id: toolu_01DjkaqZKyFB77z3FygycKHB
```json
{
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "content": "/* ===== Krisenkommunikation Page ===== */\n\n.krisen-page {\n  max-width: 860px;\n  margin: 0 auto;\n  padding: calc(var(--nav-h) + 48px) 24px 80px;\n}\n\n.krisen-page h1 {\n  font-size: 1.6rem;\n  font-weight: 800;\n  color: var(--gray-900);\n  margin-bottom: 8px;\n}\n\n.krisen-page .subtitle {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 40px;\n}\n\n/* ===== Download Card ===== */\n.download-card {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  gap: 24px;\n  padding: 28px 32px;\n  background: var(--white);\n  border: 1px solid var(--gray-100);\n  border-radius: var(--radius);\n  transition: border-color .2s, box-shadow .2s;\n}\n\n.download-card:hover {\n  border-color: var(--polizei-mid);\n  box-shadow: 0 2px 12px rgba(59,90,140,.08);\n}\n\n.download-card__info h2 {\n  font-size: 1.05rem;\n  font-weight: 700;\n  color: var(--gray-900);\n  margin-bottom: 4px;\n}\n\n.download-card__info p {\n  font-size: .85rem;\n  color: var(--gray-500);\n}\n\n.download-card .btn i {\n  width: 18px;\n  height: 18px;\n}\n\n/* ===== Divider ===== */\n.form-divider {\n  display: flex;\n  align-items: center;\n  gap: 16px;\n  margin: 40px 0;\n  color: var(--gray-300);\n  font-size: .82rem;\n  font-weight: 600;\n  letter-spacing: .5px;\n  text-transform: uppercase;\n}\n\n.form-divider::before,\n.form-divider::after {\n  content: '';\n  flex: 1;\n  height: 1px;\n  background: var(--gray-200);\n}\n\n/* ===== Form ===== */\n.krisen-form {\n  background: var(--white);\n  border: 1px solid var(--gray-100);\n  border-radius: var(--radius);\n  padding: 32px;\n}\n\n.krisen-form__section {\n  margin-bottom: 32px;\n}\n\n.krisen-form__section-title {\n  font-size: .72rem;\n  font-family: var(--font-mono);\n  letter-spacing: 3px;\n  text-transform: uppercase;\n  color: var(--bos-gold);\n  margin-bottom: 16px;\n  padding-bottom: 8px;\n  border-bottom: 1px solid var(--gray-100);\n}\n\n.krisen-form__row {\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  gap: 16px;\n  margin-bottom: 16px;\n}\n\n.krisen-form__row--2 {\n  grid-template-columns: repeat(2, 1fr);\n}\n\n.krisen-form__row--3 {\n  grid-template-columns: repeat(3, 1fr);\n}\n\n.krisen-form__group {\n  display: flex;\n  flex-direction: column;\n  gap: […]

> TOOL

tool_result
id: toolu_01DjkaqZKyFB77z3FygycKHB
```
File created successfully at: /home/<USER>/bosarsa/src/css/krisenkommunikation.css
```

> AGENT

Now create the PDF generator JS.

> TOOL

tool_use Write
id: toolu_01G5eFfv8LvjEEVxQLS3T5BX
```json
{
  "file_path": "/home/<USER>/bosarsa/js/krisenkommunikation-pdf.js",
  "content": "/* Krisenkommunikation — PDF-Generator (jsPDF) */\n(function () {\n  'use strict';\n\n  var logoBase64 = null;\n\n  // Preload logo as Base64\n  function preloadLogo() {\n    var img = new Image();\n    img.crossOrigin = 'anonymous';\n    img.onload = function () {\n      var canvas = document.createElement('canvas');\n      canvas.width = img.naturalWidth;\n      canvas.height = img.naturalHeight;\n      canvas.getContext('2d').drawImage(img, 0, 0);\n      logoBase64 = canvas.toDataURL('image/png');\n    };\n    img.src = '/logo-web.png';\n  }\n\n  function val(id) {\n    var el = document.getElementById(id);\n    return el ? el.value.trim() : '';\n  }\n\n  function checked(id) {\n    var el = document.getElementById(id);\n    return el ? el.checked : false;\n  }\n\n  function generatePDF() {\n    var jsPDF = window.jspdf.jsPDF;\n    var doc = new jsPDF({ unit: 'mm', format: 'a4' });\n    var pw = 210;\n    var ml = 15;          // margin left\n    var mr = 15;          // margin right\n    var cw = pw - ml - mr; // content width\n    var y = 15;\n\n    // Colors\n    var navy = [15, 26, 46];\n    var gold = [212, 168, 67];\n    var gray = [100, 110, 130];\n    var lightGray = [200, 207, 215];\n    var black = [17, 24, 39];\n\n    // ===== Header =====\n    if (logoBase64) {\n      doc.addImage(logoBase64, 'PNG', ml, y, 18, 18);\n    }\n    doc.setFont('helvetica', 'bold');\n    doc.setFontSize(16);\n    doc.setTextColor.apply(doc, navy);\n    doc.text('Krisenkommunikation', ml + 22, y + […]

> TOOL

tool_result
id: toolu_01G5eFfv8LvjEEVxQLS3T5BX
```
File created successfully at: /home/<USER>/bosarsa/js/krisenkommunikation-pdf.js
```

> AGENT

Now create the main page template.

> TOOL

tool_use Write
id: toolu_019yp1rBRuyopq7ZAQF7cg6D
```json
{
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "content": "---\nlayout: base.njk\ntitle: \"Krisenkommunikation — BOS-ARSA\"\ndescription: \"Krisenkommunikation-Aufnahmeformular zum Download und Online-Ausfüllen. Strukturierte Erfassung von Notrufen für den BOS-Funkbetrieb.\"\ncanonical: \"https://bosarsa.oeradio.at/krisenkommunikation/\"\nactiveNav: krisenkommunikation\npageCSSFile: \"/css/krisenkommunikation.css\"\npermalink: /krisenkommunikation/\n---\n\n<div class=\"krisen-page\">\n  <h1>Krisenkommunikation</h1>\n  <p class=\"subtitle\">Aufnahmeformular für strukturierte Notfallmeldungen im BOS-Funkbetrieb</p>\n\n  {# ===== Download Card ===== #}\n  <div class=\"download-card\">\n    <div class=\"download-card__info\">\n      <h2>Aufnahmeformular als PDF</h2>\n      <p>Druckfertige Version zum Ausfüllen per Hand — ideal für den Einsatz im Feld.</p>\n    </div>\n    <a href=\"/Krisenkommunikation-Aufnahmeformular.pdf\" download class=\"btn btn--gold\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>\n\n  {# ===== Divider ===== #}\n  <div class=\"form-divider\">oder online ausfüllen</div>\n\n  {# ===== Online Form ===== #}\n  <form id=\"krisenForm\" class=\"krisen-form\" autocomplete=\"off\">\n\n    {# --- Lfd. Nr. --- #}\n    <div class=\"krisen-form__section\">\n      <div class=\"krisen-form__row--2\">\n        <div class=\"krisen-form__group\">\n          <label for=\"lfdnr\">Lfd. Nr.</label>\n          <input type=\"text\" id=\"lfdnr\" placeholder=\"z.B. 001\">\n        </div>\n      </div>\n    </div>\n\n    {# --- Entgegennahme --- #}\n    <div class=\"krisen-form__section\">\n      <div class=\"krisen-form__section-title\">Entgegennahme durch</div>\n      <div class=\"krisen-form__row\">\n        <div class=\"krisen-form__group\">\n          <label for=\"rufzeichen\">Mein Rufzeichen</label>\n          <input type=\"text\" id=\"rufzeichen\" placeholder=\"z.B. OE8ABC\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"qth\">Mein QTH</label>\n          <input type=\"text\" id=\"qth\" placeholder=\"z.B. Klagenfurt\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"qrg\">QRG</label>\n          <input type=\"text\" id=\"qrg\" placeholder=\"z.B. 145.7625 MHz\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"telefon\">Telefon</label>\n          <input type=\"tel\" id=\"telefon\" placeholder=\"z.B. +43 664 ...\">\n        </div>\n      </div>\n    </div>\n\n    {# --- Datum / Uhrzeit --- #}\n    <div class=\"krisen-form__section\">\n      <div class=\"krisen-form__row--2\">\n        <div class=\"krisen-form__group\">\n          <label for=\"datum\">Aufnahmedatum</label>\n          <input type=\"date\" id=\"datum\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label […]

> TOOL

tool_result
id: toolu_019yp1rBRuyopq7ZAQF7cg6D
```
File created successfully at: /home/<USER>/bosarsa/src/krisenkommunikation.njk
```

> TOOL

tool_use TaskUpdate
id: toolu_01WjnwLMU2ENU31u8iEXPY5N
```json
{
  "taskId": "3",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01WjnwLMU2ENU31u8iEXPY5N
```
Updated task #3 status
```

> AGENT

Now Task #4 — update footer, sitemap, and llms.txt.

> TOOL

tool_use TaskUpdate
id: toolu_015L4TcAwtujfp5LqdtVMeZJ
```json
{
  "taskId": "4",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_015L4TcAwtujfp5LqdtVMeZJ
```
Updated task #4 status
```

> TOOL

tool_use Edit
id: toolu_01GUy5FRg96NSUkAG66Y7CCs
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/_includes/footer.njk",
  "old_string": "          <li><a href=\"/presse/\">Presse</a></li>\n          <li><a href=\"mailto:{{ site.email }}\">Kontakt</a></li>",
  "new_string": "          <li><a href=\"/presse/\">Presse</a></li>\n          <li><a href=\"/krisenkommunikation/\">Krisenkommunikation</a></li>\n          <li><a href=\"mailto:{{ site.email }}\">Kontakt</a></li>"
}
```

> TOOL

tool_result
id: toolu_01GUy5FRg96NSUkAG66Y7CCs
```
The file /home/<USER>/bosarsa/src/_includes/footer.njk has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01555Qzzegj8XFypXqPDXYWA
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/sitemap.njk",
  "old_string": "  <url>\n    <loc>{{ site.url }}/impressum/</loc>",
  "new_string": "  <url>\n    <loc>{{ site.url }}/krisenkommunikation/</loc>\n    <lastmod>2026-03-08</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.6</priority>\n  </url>\n  <url>\n    <loc>{{ site.url }}/impressum/</loc>"
}
```

> TOOL

tool_result
id: toolu_01555Qzzegj8XFypXqPDXYWA
```
The file /home/<USER>/bosarsa/src/sitemap.njk has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_018ZhAJydHK82oFD2fvzCtHq
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/llms.njk",
  "old_string": "## Kontakt",
  "new_string": "## Krisenkommunikation\n\nBOS-ARSA stellt ein Krisenkommunikation-Aufnahmeformular bereit, das im Notfunkbetrieb zur strukturierten Erfassung von Notrufen verwendet wird. Das Formular enthält Felder für die Entgegennahme (Rufzeichen, QTH, QRG), Datum/Uhrzeit, die 7 W-Fragen (WER, WAS, WANN, WO, WIE, WOMIT, WARUM) sowie eine Weitergabe-Tabelle für Organisationen wie ÖRK-LZ, LAWZ und Polizei-LLZ. Es ist als druckbare PDF und als interaktives Online-Formular verfügbar unter: {{ site.url }}/krisenkommunikation/\n\n## Kontakt"
}
```

> TOOL

tool_result
id: toolu_018ZhAJydHK82oFD2fvzCtHq
```
The file /home/<USER>/bosarsa/src/llms.njk has been updated successfully.
```

> TOOL

tool_use TaskUpdate
id: toolu_013eesQmhMHtDNDr2gzEPDdg
```json
{
  "taskId": "4",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_013eesQmhMHtDNDr2gzEPDdg
```
Updated task #4 status
```

> AGENT

Now Task #5 — build and verify.

> TOOL

tool_use TaskUpdate
id: toolu_0196fHjdhskPF4Ury4BXqhoZ
```json
{
  "taskId": "5",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_0196fHjdhskPF4Ury4BXqhoZ
```
Updated task #5 status
```

> TOOL

tool_use Bash
id: toolu_01SjXd5rxYfnhnqxfwHXP4KK
```json
{
  "command": "nix-shell -p nodejs_20 --run \"npx @11ty/eleventy\" 2>&1",
  "description": "Build the site with Eleventy",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_01SjXd5rxYfnhnqxfwHXP4KK
```
[11ty] Writing ./_site/llms.txt from ./src/llms.njk
[11ty] Writing ./_site/robots.txt from ./src/robots.njk
[11ty] Writing ./_site/sitemap.xml from ./src/sitemap.njk
[11ty] Writing ./_site/datenschutz/index.html from ./src/datenschutz.njk
[11ty] Writing ./_site/impressum/index.html from ./src/impressum.njk
[11ty] Writing ./_site/index.html from ./src/index.njk
[11ty] Writing ./_site/krisenkommunikation/index.html from ./src/krisenkommunikation.njk
[11ty] Writing ./_site/presse/index.html from ./src/presse.njk
[11ty] Writing ./_site/termine/index.html from ./src/termine.njk
[11ty] Copied 27 Wrote 9 files in 0.25 seconds (v3.1.2)
```

> AGENT

Build succeeded. Let me verify the key output files exist.

> TOOL

tool_use Bash
id: toolu_01AwxE9BdCuQobXTnRSJCAjy
```json
{
  "command": "ls -la /home/<USER>/bosarsa/_site/krisenkommunikation/index.html /home/<USER>/bosarsa/_site/js/jspdf.umd.min.js /home/<USER>/bosarsa/_site/js/krisenkommunikation-pdf.js /home/<USER>/bosarsa/_site/Krisenkommunikation-Aufnahmeformular.pdf /home/<USER>/bosarsa/_site/css/krisenkommunikation.css /home/<USER>/bosarsa/_site/js/lucide.min.js",
  "description": "Verify all output files exist"
}
```

> TOOL

tool_result
id: toolu_01AwxE9BdCuQobXTnRSJCAjy
```
-rw-r--r-- 1 achildrenmile users   5468 Mar  8 00:32 /home/<USER>/bosarsa/_site/css/krisenkommunikation.css
-rw-r--r-- 1 achildrenmile users 364463 Mar  8 00:31 /home/<USER>/bosarsa/_site/js/jspdf.umd.min.js
-rw-r--r-- 1 achildrenmile users   8024 Mar  8 00:33 /home/<USER>/bosarsa/_site/js/krisenkommunikation-pdf.js
-rw-r--r-- 1 achildrenmile users 392129 Feb 22 14:35 /home/<USER>/bosarsa/_site/js/lucide.min.js
-rw-r--r-- 1 achildrenmile users 586213 Mar  8 00:31 /home/<USER>/bosarsa/_site/Krisenkommunikation-Aufnahmeformular.pdf
-rw-r--r-- 1 achildrenmile users  14497 Mar  8 00:34 /home/<USER>/bosarsa/_site/krisenkommunikation/index.html
```

> AGENT

All files present and correct.

> TOOL

tool_use TaskUpdate
id: toolu_01HHTw4ehfHaRnq48rwY38DK
```json
{
  "taskId": "5",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01HHTw4ehfHaRnq48rwY38DK
```
Updated task #5 status
```

> AGENT

All done. Here's a summary of what was implemented:

**New files (5):**
- `src/krisenkommunikation.njk` — Page template with download card + full interactive form
- `src/css/krisenkommunikation.css` — Responsive styles (4-col → 2 → 1 on mobile, stacking Weitergabe table)
- `js/jspdf.umd.min.js` — Self-hosted jsPDF 2.5.1 library (364KB)
- `js/krisenkommunikation-pdf.js` — Client-side PDF generator (logo preload, A4 layout with sections, page breaks)
- `Krisenkommunikation-Aufnahmeformular.pdf` — Static PDF from Downloads (586KB)

**Modified files (4):**
- `.eleventy.js` — Added passthrough for `js/` and `*.pdf`
- `src/_includes/footer.njk` — Added "Krisenkommunikation" link after "Presse"
- `src/sitemap.njk` — New entry `/krisenkommunikation/` with lastmod 2026-03-08
- `src/llms.njk` — Added Krisenkommunikation section describing the form

**Build:** Successful — all 9 templates written, 27 files copied. Ready for `bash deploy-production.sh`.

> DEVELOPER

deploy

> TOOL

tool_use Bash
id: toolu_01XzXez5ZkDDx7VZ3t9WjiUx
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy to production via rsync + docker",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01XzXez5ZkDDx7VZ3t9WjiUx
```
[0;32m=== Deploying BOS-ARSA to achildrenmile@host-node-01 ===[0m
Host: achildrenmile@host-node-01
Remote dir: /home/<USER>/apps/bosarsa
Container: bosarsa
Port: 3417:80

[0;32mStep 1: Syncing files...[0m
sending incremental file list
./
.eleventy.js
Krisenkommunikation-Aufnahmeformular.pdf
.entire/logs/entire.log
.entire/metadata/
.entire/metadata/8a03439b-e8b5-46d7-8cf2-f3d9c3ed625e/full.jsonl
.entire/metadata/8a03439b-e8b5-46d7-8cf2-f3d9c3ed625e/prompt.txt
.entire/metadata/8a03439b-e8b5-46d7-8cf2-f3d9c3ed625e/summary.txt
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/context.md
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/full.jsonl
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/prompt.txt
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/summary.txt
.entire/tmp/
.entire/tmp/pre-prompt-8a03439b-e8b5-46d7-8cf2-f3d9c3ed625e.json
.entire/tmp/pre-prompt-af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6.json
_site/
_site/Krisenkommunikation-Aufnahmeformular.pdf
_site/index.html
_site/llms.txt
_site/robots.txt
_site/sitemap.xml
_site/css/
_site/css/krisenkommunikation.css
_site/datenschutz/index.html
_site/fonts/
_site/impressum/index.html
_site/js/
_site/js/jspdf.umd.min.js
_site/js/krisenkommunikation-pdf.js
_site/js/lucide.min.js
_site/krisenkommunikation/
_site/krisenkommunikation/index.html
_site/presse/index.html
_site/termine/index.html
js/
js/jspdf.umd.min.js
js/krisenkommunikation-pdf.js
src/
src/krisenkommunikation.njk
src/llms.njk
src/sitemap.njk
src/_includes/
src/_includes/footer.njk
src/css/
src/css/krisenkommunikation.css

sent 4,375,418 bytes  received 30,474 bytes  2,937,261.33 bytes/sec
total size is 103,841,556  speedup is 23.57
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 2.0s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [stage-1 1/4] FROM docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#5 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba 0.0s done
#5 DONE 0.0s

#6 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#6 resolve docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa 0.0s done
#6 DONE 0.2s

#7 [internal] load build context
#7 transferring context: 34.40MB 0.3s done
#7 DONE 0.3s

#6 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#6 sha256:9d10d4687fae6e13c052431ea3221ccda835c3262df3564310345ffe173146d9 0B / 445B 0.3s
#6 sha256:7ad115895a6aadccf7f98a05c33873c04df2933ba557c5bcdbedd3de612803da […]

> AGENT

Deployment successful. Die Krisenkommunikation-Seite ist jetzt live unter **https://bosarsa.oeradio.at/krisenkommunikation/**.

> DEVELOPER

telefon field does not fit on the formular space it is overlapping into grey area.

> TOOL

tool_use Read
id: toolu_01QGv7NaVhs9BgTygg99XfVt
```json
{
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "offset": 78,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01QGv7NaVhs9BgTygg99XfVt
```
    78→/* ===== Form ===== */
    79→.krisen-form {
    80→  background: var(--white);
    81→  border: 1px solid var(--gray-100);
    82→  border-radius: var(--radius);
    83→  padding: 32px;
    84→}
    85→
    86→.krisen-form__section {
    87→  margin-bottom: 32px;
    88→}
    89→
    90→.krisen-form__section-title {
    91→  font-size: .72rem;
    92→  font-family: var(--font-mono);
    93→  letter-spacing: 3px;
    94→  text-transform: uppercase;
    95→  color: var(--bos-gold);
    96→  margin-bottom: 16px;
    97→  padding-bottom: 8px;
    98→  border-bottom: 1px solid var(--gray-100);
    99→}
   100→
   101→.krisen-form__row {
   102→  display: grid;
   103→  grid-template-columns: repeat(4, 1fr);
   104→  gap: 16px;
   105→  margin-bottom: 16px;
   106→}
   107→

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> AGENT

The issue is that grid items with `<input>` elements have a default `min-width` that prevents them from shrinking below their intrinsic size. I need to add `min-width: 0` to the form group, and also add a medium breakpoint so the 4-column row wraps to 2 columns on tablets.

> TOOL

tool_use Edit
id: toolu_011X72dXA71RKLJdtpwijMY1
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-form__group {\n  display: flex;\n  flex-direction: column;\n  gap: 4px;\n}",
  "new_string": ".krisen-form__group {\n  display: flex;\n  flex-direction: column;\n  gap: 4px;\n  min-width: 0;\n}"
}
```

> TOOL

tool_result
id: toolu_011X72dXA71RKLJdtpwijMY1
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> AGENT

Also ensure inputs respect their container width:

> TOOL

tool_use Edit
id: toolu_01PEULbUFHBimQJdzmqwadN7
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-form__group input,\n.krisen-form__group textarea {\n  font-family: var(--font-main);\n  font-size: .88rem;\n  padding: 10px 12px;\n  border: 1px solid var(--gray-200);\n  border-radius: var(--radius);\n  background: var(--off-white);\n  color: var(--gray-900);\n  transition: border-color .2s, box-shadow .2s;\n}",
  "new_string": ".krisen-form__group input,\n.krisen-form__group textarea {\n  font-family: var(--font-main);\n  font-size: .88rem;\n  padding: 10px 12px;\n  border: 1px solid var(--gray-200);\n  border-radius: var(--radius);\n  background: var(--off-white);\n  color: var(--gray-900);\n  transition: border-color .2s, box-shadow .2s;\n  width: 100%;\n  min-width: 0;\n}"
}
```

> TOOL

tool_result
id: toolu_01PEULbUFHBimQJdzmqwadN7
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> AGENT

Now add a medium breakpoint so 4 columns become 2 on tablets:

> TOOL

tool_use Edit
id: toolu_012TNU2oG5etw4P4EXCjcPt7
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": "/* ===== Responsive ===== */\n@media (max-width: 768px) {",
  "new_string": "/* ===== Responsive ===== */\n@media (max-width: 900px) {\n  .krisen-form__row {\n    grid-template-columns: repeat(2, 1fr);\n  }\n}\n\n@media (max-width: 768px) {"
}
```

> TOOL

tool_result
id: toolu_012TNU2oG5etw4P4EXCjcPt7
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_012zPs7pV2HdS2e5kg6y7qgw
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy fix to production",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_012zPs7pV2HdS2e5kg6y7qgw
```
[0;32m=== Deploying BOS-ARSA to achildrenmile@host-node-01 ===[0m
Host: achildrenmile@host-node-01
Remote dir: /home/<USER>/apps/bosarsa
Container: bosarsa
Port: 3417:80

[0;32mStep 1: Syncing files...[0m
sending incremental file list
.entire/logs/entire.log
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/full.jsonl
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/prompt.txt
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/summary.txt
.entire/tmp/
.entire/tmp/pre-prompt-af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6.json
src/css/
src/css/krisenkommunikation.css

sent 63,006 bytes  received 5,968 bytes  45,982.67 bytes/sec
total size is 104,002,012  speedup is 1,507.84
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 1.0s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#5 resolve docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa 0.0s done
#5 DONE 0.0s

#6 [stage-1 1/4] FROM docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#6 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba 0.0s done
#6 DONE 0.0s

#7 [internal] load build context
#7 transferring context: 926.40kB 0.1s done
#7 DONE 0.1s

#8 [build 3/6] COPY package*.json ./
#8 CACHED

#9 [build 2/6] WORKDIR /app
#9 CACHED

#10 [build 4/6] RUN npm ci --production
#10 CACHED

#11 [build 5/6] COPY . .
#11 DONE 0.8s

#12 [build 6/6] RUN npx @11ty/eleventy
#12 2.052 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 2.108 [11ty] Writing ./_site/robots.txt […]

> AGENT

Fix deployed. The changes:

- Added `min-width: 0` to `.krisen-form__group` and inputs so they shrink properly within the grid
- Added `width: 100%` to inputs to fill their container
- Added a medium breakpoint at 900px where the 4-column row becomes 2 columns, giving each field more space before collapsing to 1 column on mobile

> DEVELOPER

not visible. see latest screenshot

> TOOL

tool_use Glob
id: toolu_011fsbvGz1i2Hqub5f1piXYB
```json
{
  "pattern": "**/*.png",
  "path": "/home/<USER>/Downloads"
}
```

> TOOL

tool_result
id: toolu_011fsbvGz1i2Hqub5f1piXYB
```
/home/<USER>/Downloads/ChatGPT Image Jan 7, 2026, 10_54_22 AM.png
REDACTED.png
/home/<USER>/Downloads/AFU_Spittal_-_Logo_final-min.png
/home/<USER>/Downloads/oeradio.png
/home/<USER>/Downloads/OERadio_1200x675.png
REDACTED (1).png
/home/<USER>/Downloads/ChatGPT Image Jan 7, 2026, 08_21_48 PM.png
/home/<USER>/Downloads/ChatGPT Image Jan 7, 2026, 08_21_56 PM.png
/home/<USER>/Downloads/OE8HAM.png
/home/<USER>/Downloads/OE8DSQ.png
/home/<USER>/Downloads/OE8WAL.png
/home/<USER>/Downloads/OE8LUA.png
/home/<USER>/Downloads/OE8URQ.png
/home/<USER>/Downloads/OE8ASR.png
/home/<USER>/Downloads/OE8ASR_M.png
/home/<USER>/Downloads/OE8CNI.png
/home/<USER>/Downloads/OE8RMJ.png
/home/<USER>/Downloads/OE8CKK.png
/home/<USER>/Downloads/OE8KSM.png
/home/<USER>/Downloads/OE8YYY.png
/home/<USER>/Downloads/Telegram Desktop/OE8LUA (1).png
/home/<USER>/Downloads/vellach_vorm_grundstück_files/logo.png
/home/<USER>/Downloads/Ferienhaus Bela - Urlaub mit Hund in Kärnten, Österreich_files/logo.png
/home/<USER>/Downloads/DEMO_OE0TEST_DEMO.png
/home/<USER>/Downloads/internalnewsletter.png
/home/<USER>/Downloads/qsl-card-generator-linux/data/flutter_assets/assets/icon/app_icon.png
/home/<USER>/Downloads/qsl-card-generator-linux/data/flutter_assets/assets/icon/app_icon_foreground.png
REDACTED.png
/home/<USER>/Downloads/antennenblick_Halbwellen-Dipol_20m_10m.png
/home/<USER>/Downloads/antennenblick_Halbwellen-Dipol_20m_10m (1).png
/home/<USER>/Downloads/antennenblick_Halbwellen-Dipol_20m_10m (2).png
/home/<USER>/Downloads/favicon/web-app-manifest-512x512.png
/home/<USER>/Downloads/favicon/web-app-manifest-192x192.png
/home/<USER>/Downloads/favicon/favicon-96x96.png
/home/<USER>/Downloads/favicon/apple-touch-icon.png
/home/<USER>/Downloads/ChatGPT Image Jan 22, 2026, 02_50_30 PM.png
/home/<USER>/Downloads/hamsip.png
/home/<USER>/Downloads/hamnetsip.png
/home/<USER>/Downloads/oeradiologoicon.png
REDACTED.png
/home/<USER>/Downloads/ChatGPT Image Jan 28, 2026, 11_55_44 AM.png
/home/<USER>/Downloads/oeradiologo-300x200.png
/home/<USER>/Downloads/ChatGPT Image Feb 2, 2026, 08_19_40 AM.png
REDACTED.png
/home/<USER>/Downloads/ChatGPT Image Feb 10, 2026, 01_37_14 PM.png
/home/<USER>/Downloads/ChatGPT Image Feb 10, 2026, 01_38_20 PM.png
/home/<USER>/Downloads/oeradiokl.png
/home/<USER>/Downloads/ChatGPT Image Feb 14, 2026, 02_17_03 PM.png
/home/<USER>/Downloads/ChatGPT Image Feb 14, 2026, 02_31_01 PM.png
REDACTED.png
REDACTED.png
REDACTED (1).png
REDACTED (2).png
REDACTED.png
REDACTED (3).png
REDACTED (1).png
REDACTED (4).png
REDACTED (2).png
REDACTED (3).png
REDACTED.png
REDACTED.png
REDACTED (1).png
REDACTED.png
/home/<USER>/Downloads/bosarsa.png
/home/<USER>/Downloads/ChatGPT Image Feb 19, 2026, 05_11_23 PM.png
/home/<USER>/Downloads/ChatGPT Image Feb 21, 2026, 11_07_33 PM.png
REDACTED.png
REDACTED (5).png
/home/<USER>/Downloads/noschnitzel.png
/home/<USER>/Downloads/noschnitzel (1).png
REDACTED.png
REDACTED (1).png
REDACTED.png
/home/<USER>/Downloads/oeradioaprshund.png
/home/<USER>/Downloads/ChatGPT Image Feb 26, 2026, 08_45_04 PM.png
/home/<USER>/Downloads/oe8hfs/Screenshot From 2026-03-01 13-20-05.png
/home/<USER>/Downloads/oe8hfs/Screenshot From 2026-03-01 13-20-15.png
/home/<USER>/Downloads/oe8hfs/Screenshot From 2026-03-01 13-20-24.png
/home/<USER>/Downloads/ChatGPT Image Mar 2, 2026, 05_19_34 PM.png […]

> TOOL

tool_use Bash
id: toolu_01JgLsQiYaahbJHsXJ4epUeE
```json
{
  "command": "ls -lt /home/<USER>/Downloads/*.png 2>/dev/null | head -5",
  "description": "Find most recent screenshot"
}
```

> TOOL

tool_result
id: toolu_01JgLsQiYaahbJHsXJ4epUeE
```
-rw-r--r-- 1 achildrenmile users 2576060 Mar  8 00:21 /home/<USER>/Downloads/ChatGPT Image Mar 8, 2026, 12_21_31 AM.png
-rw-r--r-- 1 achildrenmile users 2397574 Mar  8 00:13 /home/<USER>/Downloads/ChatGPT Image Mar 8, 2026, 12_13_16 AM.png
-rw-r--r-- 1 achildrenmile users 2784143 Mar  7 17:06 /home/<USER>/Downloads/ChatGPT Image Mar 7, 2026, 05_06_10 PM.png
-rw-r--r-- 1 achildrenmile users 1510755 Mar  7 15:37 /home/<USER>/Downloads/ChatGPT Image Mar 7, 2026, 03_37_39 PM.png
-rw-r--r-- 1 achildrenmile users 2753583 Mar  7 14:12 /home/<USER>/Downloads/ChatGPT Image Mar 7, 2026, 02_12_47 PM.png
```

> AGENT

Those are ChatGPT images, not screenshots. Let me check for actual screenshots elsewhere.

> TOOL

tool_use Bash
id: toolu_01A1sZpmu77rVhFYCeK7m7RL
```json
{
  "command": "ls -lt /home/<USER>/Pictures/*.png /home/<USER>/Pictures/Screenshots/*.png /tmp/*.png ~/Desktop/*.png 2>/dev/null | head -10",
  "description": "Find screenshots in common locations"
}
```

> TOOL

tool_result
id: toolu_01A1sZpmu77rVhFYCeK7m7RL
```
-rw-r--r-- 1 achildrenmile users   71082 Mar  8 08:17 /home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-17-04.png
-rw-r--r-- 1 achildrenmile users  134750 Mar  8 00:02 /tmp/logo-clean2.png
-rw-r--r-- 1 achildrenmile users  142904 Mar  8 00:01 /tmp/logo-clean.png
-rw-r--r-- 1 achildrenmile users  148294 Mar  8 00:00 /tmp/logo-crop-240.png
-rw-r--r-- 1 achildrenmile users  141648 Mar  8 00:00 /tmp/logo-crop-230.png
-rw-r--r-- 1 achildrenmile users  278353 Mar  7 23:59 /tmp/logo-v2-check.png
-rw-r--r-- 1 achildrenmile users  738166 Mar  7 23:59 /tmp/form-v2-1.png
-rw-r--r-- 1 achildrenmile users   67785 Mar  7 23:57 /tmp/logo-lower-left-zoom.png
-rw-r--r-- 1 achildrenmile users   59853 Mar  7 23:57 /tmp/logo-area.png
-rw-r--r-- 1 achildrenmile users  695106 Mar  7 23:57 /tmp/form-check-1.png
```

> TOOL

tool_use Read
id: toolu_01RWEBYRL4uCCM7vDu77oJCU
```json
{
  "file_path": "/home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-17-04.png"
}
```

> TOOL

tool_result
id: toolu_01RWEBYRL4uCCM7vDu77oJCU
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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yMUuKibgDeDYpbjdLkqLCjEsE8O2cWw/hunCwc2Fp7m5oFcik2Zs4YsZ27GNEMDGdMAxLTBNwMR0LAyjFL83G5fLwhUSSWTtFkSHW+Smp1KQkUlA04iKiIiIiIiIiIiInLQUFIqIVAKGYWC53VSJT8ATX4387Gzydm4Bvx8bE5fhBiwcA8DAMsqmIrUDvj1lLgwcbNOFiYMfD5GRHqLr1iIyxEXW9u0UZOXiOA6Oo18rIiIiIiIiIiIiIv8ECgpFRCobw8DlcuHyePBERhIWFYXX6ycrPZ1AQR4YBqbtlK1daJSNOLRNC09CAtGx8Zi+YgpycwmUlhDw+bADWmNQRERERERERERE5J9IQaGIiGC5XHjCwnCHhOC4LBzTwu+3CQ9zY/ttAl4vvqJiSouLcGz7RHdXRERERERERERERI4DBYUiIiIiIiIiIiIiIiIilZB5ojsgIiIiIiIiIiIiIiIiIn8/BYUiIiIiIiIiIiIiIiIilZCCQhEREREREREREREREZFKSEGhiIiIiIiIiIiIiIiISCWkoFBERERERERERERERESkElJQKCIiIiIiIiIiIiIiIlIJKSgUEREREREREQG+gRAAACAASURBVBERERERqYQUFIqIiIiIiIiIiIiIiIhUQgoKRURERERERERERERERCohBYUiIiIiIiIiIiIiIiIilZCCQhEREREREREREREREZFKSEGhiIiIiIiIiIiIiIiISCXkCgsLPdF9EBEREREREREREREREZG/mVFQVOqc6E6IiIiIiIiIiIiIiIiIyN9LU4+KiIiIiIiIiIiIiIiIVEIKCkVEREREREREREREREQqIQWFIiIiIiIiIiIiIiIiIpWQgkIRERERERERERERERGRSkhBoYiIiIiIiIiIiIiIiEglpKBQREREREREREREREREpBJSUCgiIiIiIiIiIiIiIiJSCSkoFBEREREREREREREREamEFBSKiIiIiIiIiIiIiIiIVEIKCkVEREREREREREREREQqIQWFIiIiIiIiIiIiIiIiIpWQgkIRERERERERERERERGRSkhBoYiIiIiIiIiIiIiIiEglpKBQREREREREREREREREpBJSUCgiIiIiIiIiIiIiIiJSCSkoFBEREREREREREREREamEFBSKiIiIiIiIiIiIiIiIVEIKCkVEREREREREREREREQqIQWFIiIiIiIiIiIiIiIiIpWQgkIRERERERERERERERGRSkhBoYiIiIiIiIiIiIiIiEglpKBQREREREREREREREREpBJSUCgiIiIiIiIiIiIiIiJSCSkoFBEREREREREREREREamEFBSKiIiIiIiIiIiIiIiIVEIKCkVEREREREREREREREQqIQWFIiIiIiIiIiIiIiIiIpWQgkIRERERERERERERERGRSkhBoYiIiIiIiIiIiIiIiEglpKBQREREREREREREREREpBJSUCgiIiIiIiIiIiIiIiJSCSkoFBEREREREREREREREamEFBSKiIiIiIiIiIiIiIiIVEIKCkVEREREREREREREREQqIQWFIiIiIiIiIiIiIiIiIpWQgkIRERERERERERERERGRSkhBoYiIiIiIiIiIiIiIiEglpKBQREREREREREREREREpBJSUCgiIiIiIiIiIiIiIiJSCSkoFBEREREREREREREREamEFBSKiIiIiIiIiIiIiIiIVEIKCkVEREREREREREREREQqIQWFIiIiIiIiIiIiIiIiIpWQgkIRERERERERERERERGRSkhBoYiIiIiIiIiIiIiIiEglpKBQREREREREREREREREpBJSUCgiIiIiIiIiIiIiIiJSCSkoFBEREREREREREREREamEFBSKiIiIiIiIiIiIiIiIVEIKCkVEREREREREREREREQqIQWFIiIiIiIiIiIiIiIiIpWQgkIRERERERERERERERGRSkhBoYiIiIiIiIiIiIiIiEglpKBQREREREREREREREREpBJSUCgiIiIiIiIiIiIiIiJSCSkoFBEREREREREREREREamEFBSKiIiIiIiIiIiIiIiIVEIKCkVERKTSGvXsGE49qzf9L7iUHyZPPdHdkUrun3w/fjtxMn0GXMLp3fvw4stvnujuiIiIiIiIiMgRMgqKSp0T3QkRERGRv9vM2fP412XXlW9HhIezbNFvhISEnMBeSWX1T74fi4qKadvpLEpKSsvLvv7yA7p07nACeyUiIiIiIiIiR8J1ojsgIiIilVthUREtkk4JKntlzNNcMLBvhbrLlicz9F9XU1xcUl6WEB/HhPEf0aB+vf96X/8J+g26lGXLk8u3b7rhKh64984T2CM5Vnl5+SS2Oz2o7IOxr3F2j7P+66+dlZ3Dx598GVR2yUUXUr161fJt06w4SYnj6LuIIiIiIiIiIv8EmnpURERE/hF27NzFNTfcHhQShoaGMPadV/5SSHjGaV0ZOmQgACEhIYx84sF/xOgt+d90st6PWVnZPD/m9aD/dqelBdUJDQ3hycfux+12A3DFZRfTtUvHE9FdERERERERETlKGlEoIiIiJ72SklJuuPnf7N6dHlT+2kvP0qF9m7/c7ovPPcmtN19HbEw0MTHRx9pNkWPyT74fL7noQs49pyf5+fnUr1f3RHdHRERERERERI6QgkIRERE5qTmOw+3/vp+ly5KDyu+7+3bOO7fnMbffsIGmLJWTxz/5foyLjSEuNuZEd0NEREREREREjoKCQhERETnpGIZR/u+XX32byVN+Cdp/6SWDueWmayocd6C13H6Z8g0+n58XX36DmbPm0rhRA378/ium/jyda264PajumuS5RISHl29nZGbx9TcTWblqLVu2prB+/Sbi4mNp2rgRTZs2ove5Z9OxQ9uD/hwbN21h7PufsHDRUrZtS6V69ao0a9qEjh3aMGTwQOLjYg/b/3Ur5+P3+xnz8pv89sdsUlN30rx5E87t1YPhV/4rqL9H4q57H+XLcRPKt03T5MOxr9O925+vm5OTyyefj2Pa9D/YmrKdosIi6tatTYf2bbhm+DCaNm1cod39z2fP7mfy4X9eZ/OWFMa+/wkzfptFwA7Q57xe3HPXreXTai5bnsyX475lwcIlZGXn0L5dawb2603/fr2D2n/yqed5Z+xH5dv33X07t9x0DTNnz+PTz8Yxa858qlVN4MrLL+HyYRcBZSHzD5OnMvnHn5k7byExMdG0aZ3I1cMvpW2bpKD2j2Rtx0FDLmfR4mXl29dcNYzHHr73gP275cZruO+e25k9Zz6vvTmW5JWrCQ0JoXPn9lx1xaV06tjukOcPKt6PB1NcXMIFQ69g5ao15WVVE+L54bvPqVWzBgA+n49JP/7MnLkL2LBxM6vXrMPlclGzRnXq1KnFgL69GTjg/KB26zY68GjdvgP/BUCvnt14/71Xj2oNxVlz5vP5F1+zcvVaUlN3EB8XR8MG9ehz/jkMHTygwnSrf8czISIiIiIiIlKZKSgUERGRk45lWQB8N/FHXnjpjaB9PbqfwagnHz7ittat38i9DzxOfn7BUfVh9Zp1DLnkKvLy8oPKCwoLSUnZzq/Tf+etdz7g8mEX8dQTDwaFm35/gBfGvM5rb74XfOymQjZu2sKPP/3Cq2+8x5jRIzmnV/dD9mPnrt3ccPO/WbN2fXnZ4iXLWbxkORN/mMLnn7x7xKO4vhw3ISgkBLjr3yOCQsIfJk/lwYdHkpWdU+F8rF6zjk8/H8+Vl1/Cww/83yHX0MvPL2Dqz9MZcce9QetKvjP2I9IzMnllzNN88dU33H3fY0HH/TR1Gj9NnUZuXj6XXTr0kO2PfvE1XnntnfKy7OwcHnh4JIZhcNmlQ/n33Q8x/pvvy/dnZGaxYeNmfvzpF77+8gNaJ7U6aPvHyuv18vGnX/HAwyODyid+P4WJ30/hqScf4oo9geaxuveBx4NCQpfLxdtvvFgeEhYXl3DlNbcwZ+6CCsdmZ+ewavVapv48ndVr1nHfPbdXqHM8ZGXncM/9j/HT1GlB5dtTd7A9dQd/zJrLW+98wJjnR9K5U/tDtnU8nwkRERERERGRys480R0QERER2Z/LZbF23QbufeDxoPKWLZrx1msvYFlH/ifMiy+/edQhod/v5+bb7qkQEh7Ix59+xcefjQsqu+f+RyuEhPvLzc3j+pvuZOGipYes9+RTzwcFIvtatXotjzz29GH7uLfuo48/G1TWr8+53HrzteXb47/5nptG3FUhJNzfhx9/wXU33Ylt2wetk5aewcOPPR0UEu414btJfD3hex569OB9HznqhUNet/kLFweFhPsa/cKrfPLZuKCQcF/FxSU8OeqFg7Z9PGzctIWHHh110P0PPzrqoNf1aHz2xddM+G5SUNmjD90dFLY9PvK5A4aE+3v9rbF8/OlXx9yn/RUWFXHxpddUCAn3tzVlGxddeg3z5i86ZL3j9UyIiIiIiIiIiIJCEREROQlZpsU99z9GYVFReVmd2rX48D+vEx4edlRtbdiwCbfbzbnn9OCuO2+h19ndD3vM0mXJbNiwKajs5RdHsWrZbBbM/oX777mjvNw0TX77fVb59pSffmXc1xODjr3lxmt4/71XGfP8U5x5xqnl5f5AgGeff+WQffll2m90aN+GG64bztk9zsLtdgftnzR56mGDvYLCQm4acVfQ+WzRvCljnn+qfDstLZ37H3oi6Lg6tWtxz1238dILT3FK105B+6bPmMmnn48/6GtuTdlGXl4+gy/oz0VDBhEZERG0/657HyUQCNC/73lcPuwiEuLjgvYXFhUxY5/zur8FC5dQr14drrv6cnr17IZp/vlnbVZ2Dg8/9jRV90xF2q/PuRVGP86Zu4DMrOyDtn+sps34g4iIcIYOHsDVw4dVWHvQtm2+GvftMb3GqtVreeTxZ4LKLhzUj+FX/Kt8e8vWlKDrFBoawmMP38vyRb/zy5Rv6Nn9zKDj3373w/J/f/XZWF564Sn29+yoR/nqs7Hcc9etR9TPF158vUKw1/f8c3jztee56YariIqqUl7u9/u54/8exO8PHLS94/FMiIiIiIiIiEgZTT0qIiIiJ513xn7E4iXLg8p27NzF7t3p1KxR/ajaatSwPm++9jytWjY/4mMKCgorlNWvV5cqVSKpUiWSm264iipVImnRoimJLVsEhZfjJwSPYtu7Vt1efXr3osc5A9mxcxcAc+ctJCVlO/Xq1TlgX84/rxdvvDoal6tsOtYJ303itjvvL9/vDwRYv34jXbt0BGCfGVD3bBvcdc8jbNq8tbwsLjaGsW+/TGjon+HZd9//SElJafm2aZp8/MGbNGncEIBBA/py4UVXBF2XbydOLl8P8EBeGP0kfXr3AuDCC/pxybA/Ry/6/X4evO/f3Hj9cABuuuFqup3dH5/PV15ny9ZtB207JCSEb778kOrVqwJlI0fHvPxmUPtj336Z9u1al/18E39kxB33BrWxcePmCutEHk+ffPAWHdqXrfP3yIN307vf0KDAbO36jUfUjrH/RQWKCou4acRdlJb+ec3at2vN6GceC6pXv15d5s/+me3bd7BteyoR4eGcd25PAGJjY7j8souYNuOP8vpbU7aRmZVNfFwsp57SmQ0bN1d47aTEFrRpnXhEfff7/RVGPA65sH95SN2vz7l06tAuaH3G7ak7mDV7Ht3OOu2AbR7tMyEiIiIiIiIiB6egUERERE46B5p60LZt7vi/B/jx+68ICws94rauv/bKowoJAZo2bVShbNCQy+nSuQNJiS1p2aIp7du1ISmxRYV6CxcuCdrOyMzi5VffDiqLjo4qDwoBFi9dftCgsH+/88oDEaDCyD6ArOw/R8Y5TvC+cV9PJD09o3zbNE3eeO35Cq+3/xSoXTp3KA8JASzLZGD/84OCwoWLluL3B4L6t6/TT+1S/u9Tu3bCNM2g6Ur3DXLq1qlF0yaNWLV6bXlZ8T4jIPfXvFmT8pBw/7YAIsLDy0NCgNNP71qhjQNNi3q8tGzRrDwkhLLz16lju6CgMDv7yEY0OvtfVODRJ58Luq41a1TnvbdewuPxBNUzDIOaNapTs0Z1OndqT2lpKXPnLWRryjZ2p2UwafLUCm17vd4j6teRWLN2AxmZWUFlFw7qF7R97jk9iI2NIXufUYALFi05aFB4tM+EiIiIiIiIiBycgkIRERE5aXXp3IH5CxaXb2/ctIWnn3uJJx6974jbqFGj2lG/bu1aNbn37tt4dnTwtKDzFywO6k+1alW58vJLuPG6K/F4PBQXl1SYzvLLcRMO+3o7duw66L79p1rdd5rGvQ6QI5XbN0wCaFC/Ll32Wb9ur7QK9epVqNOwQf2gbdu22blzF3Xr1j7ga7vcf/6paZpmhaBw/7Um959C8lDc7uA/Yz37HWvu1/b++//bDjRFbpUqkUHbBwoAj9T+1/WM07tSrVrVA9bdtSuNJ0Y9z9SfpweNQPw7pKWnVyhrsN99BNCkUUMWLPozZN+1K+2gbR7rMyEiIiIiIiIif9IahSIiInJSOuO0rnz+8Tv86+ILg8rf//Azfv9j9n/99UfcdC0Txn1Er57dDlonLS2d0S+8ynU33nlMoU9xyX9vZNv+Nm3eykv7jXA8Fsfyc8vxM+7rifwxc06F8ozMLPpfeCnf/zClQkjo+n/27ju+xvON4/g3OdmJFUJCEDViE6P23rNWVam2dGhV6fy16NBNdWu1VM3am9h7bzETEcQIsWNkr/P7Ixw5ksgk9Hzer1decp5x39czzpM4V677NhjUsH7KSsvHAfcVAAAAAACPBhWFAADgsVO5Unn9PS5pGMVPh32gjZu2KfTiJdP69/73qdatXKh8+fI+1Dhq1ayuSRPG6FzIBW3bvlOHDvtrz14/s+EjJWn9xi066h+oypXKq6BrAbOqwrkzJ6Y6NOKjdH9Mv4+doFYtmqp6tcqmZYXdCpntc/rM2RTtBJ8+Y/ba2tpaRYt65HC0ueP+aQBv3bqdYpvbt8MfUTQZc/91/fiTr7TKd45cXO5VLv4z8V+z6jzXAvk14LWX1ahhXVWpXFGHDh9Vh2eef2gxFnZLWeV4+vQZFfcsarbsxCnzuRCzUgkMAAAAAAAyj4pCAADw2Bn4xitycXaWlDRc4/1DjV66dEXDP/vmofUfcOy4Zs5eoB9/Gat3Pxiu7Tt2qVfPbvr2q0+0ZsV8bV7vm2KfkJDzkqSaNaubLV/iuzLFtqtWr9f8hUu1e89+hV689FCrpxo3qq/lS2eroGsB07LExER9+PHnZhVmte6Le/ee/Tp56rTpdUJCohYvXWG2Tc0a1dKcn/BJc3/Sec26TWbDe27ctE3Hg04+6rDS9O6QNzXml5Fmy86eDdFX3/5otuz4CfOY339vkAa+0V9VKleUJJ0LuZDpvuPjEzK8rXe50mb3niQtXLLc7PXqNRvM5ieUpNo1Uw6PCwAAAAAAch4VhQAA4LETHx9v9rptmxbq1KGNli5bZVq2eOkKtWzRRF06t8/x/rdt360vvv7e9Hrl6vWKiYlVi+aNVdTDXevWb06xT6lSSfOu9ejWSavXbDAtnzZ9jgwGg9q2aSFrKyvt3X9QP/0y1nSMDg722rJ+2UOroKpU0VtFPdw19KN39MFHn5uWHwsM0k+//qmh/3tHktSlc3uN+mGMKXmYmJiovv3eVN/ePeXuXliz5izUfr9DZm13fabDQ4k5N5QrU1qbNt8b0vby5Stq07GnOnVoIzs7W82YNT8Xo0upWtVKatSwnp7t8YzmzltsWj5j1ny1bd1CzZo2lCTZ2pj/ur93r596P9dNNjY22rZjt0Z+/+sD+3ErVDDFsgWLfHX+QqjyuLioaZMGD9zf1tZW3bp01N8Tp5mWzZ23WHGxcWrXtqWOHPHXlH9nm+1T1MNdDRvUfWC7AAAAAAAgZ1BRCAAAnghffv6xXAvkN1v22RcjdfnylRzvq1fPLipZorjpdXh4hIZ/9o3qNmyjEqWrmSURpaQkm3e5MpKkdm1aqknj+mbrJ0+dqV59XlXP3q/o+x9+M0uE9nup9yMZZvG5Z7uq0X3Jl7/GT9bBQ0ckSW5uhTR40Otm68+dO69vR/2swe8O1fYdu83WVa1SSc8/1/3hBv0I9ejeWdbW5r8aX7lyVRMnT9df4yfLYDDo2e6dcym6tH069H253Tds7P+GjVB4eNIwqZUrVzBbt3DxMtWu11JNWnRSrz6vpjrEbHL58uWV533DhE6ZNksD3/5Q02fNy1CMgwe9nuIeX7RkuQYMfE9jxk5IMczr118M+89UqgIAAAAA8LgjUQgAAJ4IhQoV1CdD3zdbFhZ2Q+988EmO9+Xi4qKZ//6dYjjO1LRs3kSjR35htuzn0V+rfr2nM7TvO2+/keU4M2vUdyNMQ7pKSVWD73zwiamKcNCbr6jfS73Tbada1cr6c8zo/1Qyp2IFb4349H9prh/17WcqUKBAmutzS4EC+fXFfXFfvHhZn474TpLUt3dPlS1b2mz91WvXdSo4ab7JgW/0l43NgwcZGfrhO6kuD7xvrs605M+fT+P++ElFPdwfuJ2NwaDhH7+nVi2bZqhdAAAAAACQfSQKAQDAE+PZHs+kqIrbsnWHJk2ZkeN9FfcsqgVzpmjUt5+nmC/N1tZWzZs20p+//6BJE8bIwcHebL2bWyHNnDZeP4z6QlWSVXQVLuymhvXr6LX+fTVj2nhNmjBGTk6OOR57Wop7FtX7775ltuzEiVMaNfo3SZK1tbW+/Pxjzfz3bzVv2ijF/l4lS+jLzz/WgjmTVaKE5yOJ+VHq91JvLZ7/rzp3aisP9yIqUCC/GjWsp9nTJ6hdm5YphvF8XHTq2DbF9Zq3YKk2btqmfPnyasn8afr4wyFq1rShab7AenVra9zYn0xDzz5I505tNWfGP2rWtKGKFy9mqry8cfOW4uLiMhRjDZ+qWr18nt4b8maK4UxtbGzUo1sn+S6eqTdefzlD7QEAAAAAgJxhFR4ZY8ztIAAAAAAAAAAAAAA8WlQUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggUgUAgAAAAAAAAAAABaIRCEAAAAAAAAAAABggQzDhn86IreDAAAAkKRfxs3Q1LnL1LRBTdnZ2mZqX6NRmjJ7qSbNXKIzIaGqVb1itmJZuX67Fi7foAZPV8tWO5lx/NRZ/TFxjmYuXCWfKt7Km8f5kfWdlpXrt2vRio2qXzvnzkNqx7lk1SYtX7tN9WpV1Zh/Zut86GVVKFcqx/rMCb9NmKWLl66qfFmvh9bHklWbNc93rRrXrfHQ+kjPlz/+rSWrNqtRXR/Z2tqYlp88HaJh3/yulk3qyMbGkKW2M3uPDxk+Wl4lisqtYAGNeYjnP737POTCZf3vy1/Vplk9GQxP3t9a/vjnvzofelmVvJ/KdlszF67SHxPnyHfNFvmu2aLdfkd149ZtlXuqpKytrUzbRUfHaMmqzZqxcKUWr9ik4LPnVdjNVfnz5jFr73ZEpBb4rtOM+Su0acd+hd24pdJexWVjePA9tv/QMX3xw3hTHHe/zl24pNrZfP5L0uBh9+69+z2qnw+ZeR4En72goV+PUcfWjR5qTAAAAAD+e2zS3wQAAODhi4iMUlDwWbm7FdT+Q8fUqK5PpvY/ePS4DhwJVK+ubVSmVPGHFOXDNXfxGhUu5KruHVuoqHvh3A7noUntOIu4FVR8fIIkqUQxdxUulPLD+awKCArWuKkL9MtX7+dYm6l548NvNWxIf5XwdM9yG+5uroqI9MxWHKP/mKpqlcqpddO6WW4jIjJKC5dvUJ/u7bLcRmrn3VLu8ceNV3EPFXErmKPtPdOuqaSkJOr6rXsUERmlF3q0lyRFRcdo1JgpMhoTVbdGFRV0zaeDR4/r+9+n6LUXuqp6ZW/TdiN/naSi7m7q2qG5rl2/qe17Diro1Dl99PbLsrJKK4IkNjYGvdW/p9myvC65/wcWGZGR50VOPA8AAAAAID0kCgEAwGPB73CgirkXVpWKZbTvUECmE4VhN2+psJur6tWq+pAifPjCbt5WpzaNc6Tq53GW2nHWqVHZ9P0zbZvkRliPhadrVNbTyc5FbqlQrpS27PRTo7o+KlEs64nP+1nKPf646d6xRY625+TkqAplkyp+K5QtpYIF8mnGgpWmROGCZetlbW2lYe+8ZqoMrFuzilas26apc5apfNlScrC3k9/hQCUmJpol+xrWqaZxUxfo0pVrci/84OSmtZW1KY7/osfleQAAAADgv41EIQAAeCzsP3xMVSqWUbVK5bRi3XZFREbJ2cnRtH7wsNF6s18P04fCJ0+H6Mc/p2nsqKEa+s3vCrtxS1JSlUa75vX1TLumGjxstPr0aCe/w4EKOB4s98IF9WqfLnK7U60WcuGyfNdsVsDx04pPSFCLRrXVtX1zUxVLfHyCxk2dr8ATZ2QwGNSoro86t2ksKWmYt5//mq6Xe3XSohUbZZRR3Ts0V3x8gpav3aZrYTdUrnRJDXipu+mD8kP+QVq3ebdOnwuVR5FCat6otp72qaStuw7o33nLJUljJ82VJP01epiiY2K1dNVmHQoIUmxsnCp5P6Vn2jZVvrwukpKGwixaxE2nzoTo9LkL+mHEu9q8Y7+OnzqrEkWLaMuuA3IvXFB9n22vHXsPa9f+I4qPT1CjOtVN1UAr12/X4YAT+vCtF03n+pdxM1S6lKc6tW6c4jr5HQ7U2s27dPrcBTk5OqpHpxamJN/K9dt1/NRZuTg7ye/wMfXr1Vk1qpY37ZvWcaYXQ3rtSlJCQqKmz1+ugOPBioqOUWkvT/Xv/Yz8Dgea+nzjw2/VqU1jdWjZUIOHjdYzbZto8879MhgM+uz91/TbhFkqWczddG4k6a2PR2nI68+r3FMlUpyLCdMX6cLFK3q1Txd9+ePfkqRvf52o8mW89M6A3g+8Zx90/ZKfi4uXr2rp6i06FnRaLs5Oql29otq1aCCDwTrV8zJ36VqF3bilk6dDtHjlJv0x8iMZjUat3bxbe/yO6tKV6yr7VHF1bN1IXsWLpjimu6pUKKPrYbc0c8FKffT2y6luYzRK67bs0h4/f125FqbSXp5q27y+Snt5ml3rNz78VtUqldXBo0Eprn14RKQWr9ykwwEndOPmbVWvXE59erRXHmenNGOT7t1rGb3PpbTff6k5d/6Slq7erOOnzqpwoQJq1qC22fr0rm16RbMD0gAAIABJREFUz56IyCgtWLZeh/xPyMHeTh1bNdSilZvUu1tbValQJt14f5swSyU9PRQZGaW9BwPk5Oig7h1bqHrlcqkeT/J7OyvnLiMSExPv/GvU7v1H9VyXVimGD23R+GmtWLddh44e19M1KisxMVHxCYlmz/s8Ls76YGDfTPWdmuxeo+Sio2M0cswUlfB0V//nO5uWL1m1WZt37JeLs6N8KnurQ+tGpmOOjIrW0lWbdeTYSUVFx6hqxTLq3Lap4uPi9cnIsZLMnxfZfR7cdfDocS1cvlG3wyNUpUIZdWnXVPnzmQ/3CgAAAADJPXkTbAAAgP+cqOgYBZ44rcrepVWimLvyuDhp/6FjGd7/u+GD9FyX1irp6aG/Rg8z+4B747a96tS6kYa900/2dram5EVcfLx+mzBTTo4OeuPl7hrwYjft2HtYew8cNe17JiRU1lbW6tOjnSqWK6Xla7fqRPA50/r4hHgFnTqrDwb2Vb2aVTV5tq82bt+ngf2f1asvdNWJ4HPa45fU3vnQy/pz0lwV8yisfs93VkXvpzRltq+OBZ1WwzrV9dfoYXJxdtJb/Xvqr9HDJEnT561QwPFgtWteXz06ttDlq2H6c/Jcs2Pfue+wWjetq7df7SUHeztJ0sngEBV0za9P3ntVefM464ex/yoyKlrD331FbZvX04r123Ut7GbmLpKkcxcu6e9/F6hGlfIa9Mpz6tymsabM9tWNm7dN2wSdPKuSnu4a2O9ZlS1tnlxL6zgz4kHtSknX+eDRIHXv1EJDh/RTfHyC5ixeo4Z1qmvI68/LwcFef40epg4tG5r22XcoQL26tFHfZztk+lzMWbxGZ0JC9d4bfVTU3c10LMOG9Nc7A3pnuJ3Urt9d8QkJ+mX8TMXExOqFHu3UpF4Nbd19QL5rtpi2uf+8fDd8kEp7eapbh+b6Y+RHSedm+z75rt6sWtUr6uVeHeXs7Khfxs1QZFR0mnHFxyclzoPPXtCOvYdS3WbrLj8tXbVFtapX1Is9OyiPi5N++3umwiMiU5z3N19+NtVr/++85Tp3/qJe7NlRQ15/XrfDI7V4xcYMnbvM3OcPev+lOPaEBI35Z5Yk6aWeHVWnRmUtXL4+QzEll9azR5KmzV2m4DMX1LV9M3Vq01jrt+5VVHSMaX1G4t2y00/VKntrxP8GqHL50po8a4niExJy/NylJ+zmba1Yv001q1WQJN28Ha6Y2FiVT6XSz87WVl4liurilWuSpBpVy8vW1kaffz9O2/ccVHSyc/AoPOga3RWfkKBfJ8xSETdX9evVybT87PmLOnU6RH26t1XjujW0eaefVqzbZlo/be5yBQQFq12L+urRqYUuXbmuCf8uVKGC+dN8XmT3eSBJS1ZuUsvGT6tXl9a6ePmqJs5YnCPnCgAAAMB/FxWFAAAg1x04clzOTo7yKlFMklS9Ujn5Hc78PIWpadawtop5JM2F1qppXf0zfZEkydbGRp+8+6ryuDibKgjLl/FS8NkLqn2naidfXhe90qeLrK2tVLNqBZ07f0mnzpw3zYGYmGhUh1YN5eLspPYtG2jdlt1q8HQ1FXLNr0Ku+VWlYlmdOnNe9WpV1ZadfmpQp7p6PtMq6Rgrl9ONm7e0c99hlS/rlSLuiMgo7TsUoKFD+ql40SKSpErlS+ujL3/T2fMXTcNBVq9czjTf110F8uc1nbuOrRrpq58mqF2LBsrj7KSWjeto/ZY9Cj5zXgUL5MvUuSxetIhGfjJYefPcmQOsrLRs7VadCQk1Vay4FsinFo2ezlS7GZFeuzdvh6t40SKqVa2iJOn1F7vJaDQ+sM1mDWqpQrmMD1toJUlWVlq3Zbf2HvTX0CH95ZJO5Vt6Urt+dx32D5Kjg70G9uspa+ukm9TZyUFLV28xDc+akfO9daefXujR3nRf+1Qpr09H/qmDR4+nOlSvlZIShY2b1tDeA/6at3SdfFKJcfOO/erUppFaNq5z51i8dT70inbsPaxWTepk6PhffaGrYmJiTdVkV6/d0Oad+zO0b2bu88y8/w4dDVJiolEDXuxuqtRKTDRqvu+6DMV1V1rPnvCISB08GqRhQ/qreLGk93Yxdzd99dME074Zibd6pXKqeOf+7dqhmTZs26vzoZdV0tMjR89davwDT+mND781vS7iVlDtWjSQJEVGRkmSnBwdUt3X2clRkVExpm0+e/81rduyWwuWbdD0+StVoayX2rVooNJeSXPzffPLPzp3/pJp/+YNa5vOS2xcnFkckvThWy+a9k1PWtdIUtLPBaP01+R5Mlhba8CL3WSVbNJEK1lpwEvd5ehgL0lydHTQohUb1Kl1Y0VERumQf5C+GfaW8t+pAPcu46WhX49R2I1bKpA/b6rxZPd5IEndO7U03RdPeXlq+Ld/6Oq1GypUMH+GzgkAAAAAy0OiEAAA5Lr9hwJUuXwZU8LOp0p5/TZhpqKjY+Rw50PYrMrjci+R4+TooNi4ONNrg8Fay9ZsUdCps4qKidHZkItmyclCrvlNH8hKUt48zoqJjTVrP3miyMbGIEeHex+O29vZKi4uXtKd6pMz57V11wGz/cumMqSlJJ05FypbGxtTkvBu/B5FCin47AVTojC1IRqdne7FYGNjY9r3Ljs7W8XFx6fab3oio6K1fO1WhYRe1s3b4bpx87bpGCXJxdnxAXtnXXrtNqrjox/2T9N3v06Se+GC8i7jpbo1qzy4TZfMJfmMkg4eOa4Ll66of+9nVCAHhvN70BCbZ86FKvTSVQ386Duz5dbWVrqbA03vvCQmJurCxSv6Z8Zi/XNfZdGVazdS3ccoyaikDnp3b6uvfpqgxSs3qVb1iqZtEhISFXLhkl54tr3ZvmVKFdeZc6EPjMnsWKyste9ggA76Byk6OkZnQkJVyDVjCY3M3OeZef+dCQmVV3EPs+Ec03qfPkhaz56zIRdlZ2trShJKUjGPwmbPuozEm7x9O1tbGQwGxcTGKSOy+4zwKu5hqty+HR6prTv99Mu4Gfrsg9dMz8SoqOgUVXFS0h9BFHN3M712sLdTh5YN1bZZfe32O6J9BwP001/TNfKTQcrj4qzXX+hm9ty+/5mbfH5DSSqarO30POjng9EozV26VqGXruq74YNkbW0+GE8xDzdTklCSypUuoZu3wnU7IlLnzl9SQkKCPv7qtxR9XrkWlmaiMLvPA0nyLl3S9H3BAvnkWiCfTp+7QKIQAAAAQJpIFAIAgFwVGxcn/+PBSkhI0PY9B83W7T0YoIZ1qj+Ufq9cDdOo36fIu3RJVatUTh7uhbRpe8YqmbLCaDSqSf2aKeYQS6vqJtFoVLLiFfN1d+YCe9T2HzqmSTOXqGGd6mpYp7pc8+fVlNm+uRLL/dwKFdA3w96Sf+ApbdqxX1Pn+OpwQJAGvNg9R/u5ceu2vEuX1KIVG1WlQhmzREFOSzQaVdrLUx1bN8pyG0ZjUuLvhR7tVdDVvDosIwk598KF1KxBba3fukfeZe4lIIx3UolWqdykCRm8PxMTjRo1ZrKsrKxUuUJplS7pqZNnQrT3gH+G9s+MzLz/jEZjKsf14OrUzHjQezt5DJl5XjxqTk6Oprn/pKQ5Lf/3xa86fuKMKno/pTwuzjoaeCrF8zsmNk7BZ86rRaPa9zcpg8Fa9WpVVb1aVfXJd2N14MhxNarrk+qcgXdZW1mbxZHTrKysVMg1v2YsWKmB/Z69f2Wq+yQkJCoxMVEODvYa8GK3FOvvVjBmVkafB9l5TwIAAACwTCQKAQBArjp45LhsDAYNesW8KmTT9n3yO3zM9EGznZ2twsMjTetv3Lqt7Ag8eUaOjvZ6rW9X07I1m3Zlq80HKeruptjYOLMPtQOCglUgX+qVJcU8CismJlYhFy7Ls2jSB8uRUdEKvXTVrMowu+zt7RQeEWm27NbtiFS3PXAkUE/XqKTnurSWlJSwjLgzzOCjiiEtEZFRiotPUNWKZVW1YlntOxigybOWZi4OOzvdThZHRGSUEu6b861xXR+1a9FAX//8jybNXJIyeZBMdu9ZT4/C8jscqPJlSplyEudDL0tKM0eRgsFgrcKFXGVjYzC79/wOB5qGi01PpzaNtdvviBat2GRaZmMwyK1QAQWdPGuqbpWkoOCzqlaxXGrNpHA97KbOhIRq1KeDle/O8IxnQjJejZgZmXn/uRUsoB17DyshIdFUVXjsxBmzbbJzbd0LF1R0TKzOXbhkei+fPX/RbH6+zD4vcpujg72cnBwUfud54FPFW0tXb5ZPFW/TsLKSNG/pWtna2qh8GS9J0qSZS3TzVrjZPH1Go1Fx8fFmFZ1ZkRM/M7p3bKG8Ls767rdJWrdlt9kwvxdCrygqOsb0xwLHT56Vg4O98uVxltHdTTHRMXJ3K2iqHoyOjlFQ8Dmz85EZGX0eBJ48bbpvroXd1PWwm3IvXDBLfQIAAACwDNn73xcAAEA27Tt0TBW9n1KFsqXMvho8XV3HTpwxfXhe0tNdS1Zt1pFjJ7Xb76g2Z7P6r0D+vLp2/aZ27TussJu35btmi04Gh+TEIaWqQ6tGOuQfpEXLN+jGzdvadzBAf02epyPHTqQeX748atG4jibNXKzDASfkH3hK46bMV4VypUxzJOaEUiWK6dKV61q8cpMCgoK1cPmGND9Qz58vj44GnlLwmfMKuXBZU+b4KiEh+5UqmYkhLUtXb9Gv42fo+MkzunDxirbtPqD8+ZMSYc6OjoqJjlHYzdu6FnYzzTZKFvfQrn1HtGvfYR05dlIzF66SrY3539VZWVnJ3t5Ob7zUXf7HT2n9lj2mdQ4O9rp4+aquXk8a0jO792yt6pXk5Oig8dMW6HzoZZ0+d0Hjpi7Q6o07H7ifk6ODLl25ZoqjW4fmmrd0nbbs9FN4RKSWrNqsCdMX6dr1tM9FcvZ2turesYUuXr5qtrxHx5byXbNFu/YfUUBQsGYtXKXw8EhTtVh6593FxUkGg0GrN+7U7YhIbdnppx17D2copszKzPvPp4q34uPj9c+MRQoICtau/Ue098BRs22yc20LueaXd+mSmjhjsU6dOa/T50L179zlZomxzD4vHrXIyCgFBAUrIChY2/cc1Jh/ZishIdE052fX9s3k6OCgkWMma8W67drtd1R/TZmv7XsO6sWeHWR/Z0jS5o1q6+SZEP09baGOBp7SgSOB+md60hC5ac3Vl1E58TPDykryLFpYPTu31IJlG3Q25KJpnbOTg/7+d6H8jwdr38EAzfddp7o1q8jKykoF8udVs4a1NXbyXB05dlLXb9zSPzMWa87iNaZn5v3Pi/Rk5HlgMFhr+dptOnj0uI4GntKEfxfKs2jhDM1bCQAAAMBykSgEAAC5Jj4hQUePnUwxvJ4kVfIuLRuDQfsPB0qSnu/aVlZWVvpz8jzt3n9EjevVyFbflbyfUrMGtTRt3nIN//YPRUZGq0bV7H0w/SCu+fNqYL9ntcvvqD7+eoymzVuuFo3rqH7tamnu071jc5UsXlR/TJyj3ybMksHGoFd6P5OjcXkV91CHVg21euMOTZ+3Qk6ODmnOx9auRQMV8yisUb9P0c/jpqtC2VKmZNyjiiEt3To0UzGPwvpl/Ex9+ePfioyKVv9enSVJxYsVUY2qFTT06zFau3l3mm20aFRb5ct6adKspVq2Zovq1KgsOzvbVLct5lFYz3ZupfnL1puqejq3bqxJM5do3JT5krJ/z1pbW+mt/j1163a4vvppgr7/fapKeLqrd/d2D9yvTbN62n/omD4b9aeiomNUvXI5dWrTWHOWrNEHI37R7v1H9NoLXTJVZVSnRmWVKlnMbFm1SmXVpX0zTZ2zTL+On6mjx09p0KvPmebaS++8O9jb6aWeHbTnwFF9OOIXHTgSqMbJ5gjNSZl5/7k4O+ndAX0UFxevsZPmynfNFnVq3cRsm+xe2wEvdddTJYtp7KS5+u3vmWrZpI7Z/KZZeV48SqfPherX8TP16/iZmjpnmc6HXtbg13qZ5thzdLDXx2+/JJ/K3tq+96Cmz1uhxMRE/W/QS2YJwJKeHnrzpR46cfqcxkyYpYXLN8jZ2VHD33kl28Os5uTPjCb1a6pqxTL6a8o80zyQ7kUKqbSXp/6YOEcLl29QozrV1bNzS9M+PTq1VPGi7vr9n9ka9s3vioyK1pv9epgSwvc/L9KTkeeBwdqg1k3ratrc5Zo4Y7EKF3LV26/0yvJxAwAAALAMVuGRMTk34QYAAAAA4IGio2Nkb29nmk/OaDRq8PDRGvLa8zlaMQwAAAAAQHqYoxAAAAAAHqFfxs9UIdf86t29rSIiorRqww452NszRCQAAAAA4JGjohAAAAAAHqGQC5e1eOVGHTl2UkajUSU83fXyc51U1N0tt0MDAAAAAFgYEoUAAAAAAAAAAACABbLO7QAAAAAAAAAAAAAAPHokCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEAkCgEAAAAAAAAAAAALRKIQAAAAAAAAAAAAsEA2uR0AAACwbHHxCYqNi5fRaMztUAAAAABAkmRlZSU7WxvZ2hhyOxQAAB4qEoUAACBXxcbFq0BeJ/4DDgAAAOCxERefoLBbkfw/BQDwn8fQowAAIFcZjUb+8w0AAADgsWJrY2DUEwCARSBRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABSJRCAAAAAAAAAAAAFggEoUAAAAAAAAAAACABbLJ7QAAAAAAAAAeVzeCV+niwfFKiLmZ26EAFsNgn0/u1V5X/lJtcjsUAAD+86goBAAAAAAASANJQuDRS4i5qYsHx+d2GAAAWAQShQAAAAAAAGkgSQjkDt57AAA8GiQKAQAAAAAAAAAAAAtEohAAAAAAAAAAAACwQCQKAQAAAAAAAAAAAAtkk9sBAAAAWILQi5e0YdN2XQi9qAL58+mVl3vndkiPzIZN2+QfcFxR0dHq1L6VvMuVye2QAAAAAAAAIBKFAAAAZi5evKyKPo1Nrz96f5A++mBQtto8eeqMOnTto8uXr0qSqlau+FAShX37D9KyFWvVoV1LTZv4e463nxXDP/9Of46fYnrtXbb0E5Uo/HP8ZA3/fKQk6XrosVyN5cX+b8t3xRo1bVxfC2ZPzHI7bw35WDPnLDJb5laooKpXq6wmjerqlX59ZG9nJ0nyqdNSZ86GmLazs7VV6dJequFTVc/37KL6dWun23ZyY376Rn2e757l2AEAAAAAQM5i6FEAAIBkFvuuMns9b6Fvttsc/89UXb58Vc7OTnr9lRf0wXtvZrvNJ8Hly1dNScLatarrow8GqWGDOrkcFVJz5eo1rVm3SZ+MGKV33v80ze1i4+IUcCxI02fOV8euffXHX5MeYZQAAAAAACCnkSgEAABIZvHSlZKkXs92kSSdPHVau/bsz1ab50IuSJKeruWjkV9/oo7tWmUvyCfEuZDzpu8/H/6+Pnp/kArkz5eLESG5cmVL63roMV0976+t65eoTaumkqTZ8xYr6MQps21f7vucroce0+nAPZo+eaw6tU+6hz/9YpSmz5yfZtv3f1FNCAAAAADA44VEIQAAwB2nz5zTzt37JEnP9eiskiU8JUkLFy9Psa2Xd225epTX6J/HmpbdvHVLrh7l5epRXlP+naOFi5fL1aO8Vq7eIClprj5Xj/J6a8jHkpKGCnX1KK+33xsu3xVr1LVnP5WtVE99+w8yxXHXqjUb9Wzv1+RTp6VKlK2pjl376s+/pyg2Li7VY3lQe34Hj5jiPBZ4Qq8NfF9lKtZV+2f6aNWajbp167befm+4fOq0VNlK9dTn5YG6cfOWWfvrN25V/wHvyqdOSz1V/ml16tZXs+beG3KyYfPOatXhOdPrjl37ytWjvE4Fn5EkRURE6qvvflbHrn1VslwtNWvdTUM++FTHg06mGueOXXs1+P1PVLxMDa3fuDXbx5CR65eWW7du6+NPvlaz1t1Uslwt1azXWm8N+VgHD/tnKPbUZPb63nUq+IxeeuVt1arfWkVLVdfTDdvp5deG6Kh/4AP3S87a2loVK5TTsI+GmJZt27En1W3z5s2jdm2aa8o/Y9SyedIQvT+PGSej0Zjh/gAAAAAAwOODOQoBAADuuJsQdHR0UN26tdSsSQNNnjZbCxev0Feffyxb28z96lSwoKuaNK4vf/9AXbl6TYUKuqpSpfIqU7qU2XYnTgRr9txFio9PkCQtW7FWa9dv0bKF01TDp6rWrNuk5198Q5Lk4uKsp7xKavvOPdq+c48OHfLXn2NGmbV38tRp9X/9nTTbS27QO0MVERml2+Hh2rl7n4LeOaU6T9fQnr0HZGNjo2vXw7Ri1XqNHP2bRn79iSRpzbpNeu6FAZKkkiU85elZVNt27NG2HXvkXqSwmjauL59qleXo6Kh9+w9Kkmr4VFWePC5ydHRQQkKCnnthgLbvvJeMOnjYXwcP+2vFynVav2q+PIt5mMU55P1PdeJkcKrnOSvHkB3PvTDAVGVauVJ5nT13XjPnLNKSZau1cslMVaroneHYJWX6+t4VduOm2j3TW1euXJODg4MqV/LWUf9AnTgZrJ2792n3lhXKmzdPto83LX37PKu16zfrVPBZHQs8oQrlyz60vgAAAAAAwMNBRSEAAMAds+ctkSTVfbqm7O3s1KxpQ0lJ87et27Al0+01blhXC2dPVA2fKpKkalUraeHsiXp38ACz7fwOHNb2jb4KOemn779Nmh8uJiZGi+4MgxoTG6s+vbrp1X59dGD3Om1cs0CjvvnkTsyLde16mFl7p06d0R+/jlTQ0R2ptpdcDZ+q2rHJVzs3L5eLi7OuXQ/TxYuXdWjfBu3fudpUNbZw8QpJUkJCgoZ++o0kaej/Bstv11ptXrvI1M+bgz9SVFS0xvz8rb77cpipn69HfKSFsyfKw72IZs1ZZEoSfv/tpzobtE/LF0+Xa4H8unrtur745ocUceZxcdbGNQt07UKAmt+5Llk9huwID4+QT7XK6tyxjaZPHqvNaxfJb9dalStbWhERkZo5e2GmYpcyf33v2rZjt65cuSZJWuU7U6t9Z+vI/k3q2b2z3hv8hhISEzN8XFeuXNO3o341vW7UoG66+5QqWdz0/fkLoWbrjgedNFVU3v1q2LxzhuMBAAAAAACPBhWFAAAAkvwDjpuGvbybzGnWuL7sbG0VGxenRUtWqG3rZg+l75o1qpmqDF/t10eTps5SwLEgXb58VZLUsV0rdWzXSrdvh+vQkQAdOuKvvfsOmva/EHpRBV0LmLX3bLdOabaXXPu2LSRJpbxKqHLF8tq5e598qleRvZ2dJKlp43pau36zrly9pvj4BO33O6RTwWeT9ilZQlu375YkeXgUkSRdunRFBw4dUb06tdI83iXLVkuSKlYop1f79ZGUlJx9oXcP/fbHBC31Xa24X+PN9hn0Zn9VrVwx1fYyeww2NoY0Y0uPi4uzvv1qmIxGo06eOq3FS1cq6GSwwm7ckCSF3JcwSy92KfPX966yySpTR/84VrVqVpN3uTIa9tEQlSheLN1juZvMu99H7w9S6adKprs/AAAAAAB48pEoBAAAkPk8hJ9+MUqffmE+3OOylWsVEREpZ2enHO/bzt7O7LWjg4PZ6zNnQzTi6x+0OFlFYJ48LlluLzkbm3u/DlpZWZn9K0kGg/mvi1evXTd9//pbH6Ta5t0qt7Rcu9NG2TJPmS0vXSopORUbF6ewsBtm69zcCqXZXmaPIbsmT5utX8aM19lz503LXFyc09z+QbFLmb++d3mXK6O/x/6oEV//IN8Va+S7Yo1p3euvvJDpYVaLFHHTB++8qVde7p2h7YPPnDN9X6yo+VCx5cqW1s7NyzLVPwAAAAAAePRIFAIAAEhakCxRmJqIiEgtWbZaz/fsIuleIio6Osa0TVRk9EP7Hww/AAAgAElEQVSJ7f2PRmj9xq2qWaOaPhv2nmrXrKY9+w7qmR4vPZT+HsTVNb/p+z/HjEqRIJIk77Kl02kjqTru7NkQs+V3E292trZydS2g86EXsxtumrJ6/Xbs2qv3/ve5JGnUN5+occO68i5XRl2f669Nm7dnKZbsXN/uXTuoc8c22rp9l44FBmnVmo3avHWnxv/zr5o3bajWLZumuW92k3n/zpgnSXqqVAmV9y6T5XYAAAAAAEDuYY5CAABg8fbsPaDg00nDaX427D1dDz1m+roQfMBULZa86rDwnSqxRUtWaMu2XYqOjtYPv/z5UOILOBYkSerQtoUaNagjOzs7rVi57qH0lZ6aPtVMw2Ae9Q9Uw/pPq2H9p2VvZ6eZsxfoeNDJdKsun+nYRpLkd/CIpk2fK0k6FnhCk6bOkiR17tQmW8ODZkRWr1/g8aThaR0dHdT/peflXa6Mgk6ckn9AYJZjyer1Xb12o7o9119NWnVR7ZrV9ebrL+v3X74zrT8WeCLLMaXl9u1wrduwRS+98rbWrNskSXr9lRfNKjgBAAAAAMCTg4pCAABg8ZIP+dipQxuzdQ4ODmrbupnmLfDV+o1bdeXqNbkVKqhOHVrpp1/HKfj0WVPlV8UK5eTo6KCoqJytLGxQv7bmLfDVn39P0aatO3Xp0uUc7yOjbG1tNPitV/X5V6P1+58TtWHTNhmNRvkHHJckHfU/rpde6PnANnr17KJZcxdp2449GvLBpxo7foqCTpxSYmKiChV01YhPUh/SNCdl9frVqlFNtrY2ioqKVrtnesvZ2Vk7d+2TexG3LMeS1etbsoSnDh321/WwG2rU4hl5eZXQiRPBkpKGQu3UoXWWY7rf5GmzNXna7BTLez3bRa/175Nj/QAAsubVn8MkSRPeTTmnLQAAAPAgVBQCAACLZjQatehOorB61Uoq/VTJFNvcTR4mJiZq3kJfSdJ7g9/Qp0PfVe1a1SVJVStX1NR/xmRobrnM+vn7L9WjW0eFhd3Qtu27VKN6Ff05ZlT6Oz4kg97sr3F/jFbVyhV11D9Q/gHHVaSIm/q92EsL5kyUwfDgakCDwaBZ08ap/0vPy97eXoHHTygxMVHNmjSQ78JpKurh/tCPIavXr3Kl8pr6z+8qUbyY9u47qJCQCxrz0zeqX7dWlmPJ6vX1LldGq5fNVptWTXUh9KI2bd6uq9euq0WzRlq1dJZKeZXIckxpsbe3V8UK5dSnVzctmT9VY38bSTUhADwGAs7FK+BcfG6HAQAAgCeQVXhkjDG3gwAAAJYrPDJaRQrmze0wAAAAUnV0dsvcDiFdDd67Ikna9lPWK9yBx1Gl59bmav+Xrt2Si5NDrsYAAMDDRkUhAAAAAAAAAAAAYIGYoxAAAAAAAABmjp6J0+u/3jC9tjFIFUvYqkElO/Vq4iSbOyON/2/CTW3zjzVt51nIoOqlbfV8Uyd5Fbk3HPn09ZEa6xuRal9rvyskR3vzoazDo4xqM/yqmlWz19cvWcboE1uPxuqjf27qrU7O6t3MKcvtNPnwisoXt9W4wflzMDoAAPBfRaIQAAAAAAAAqarsZau65e0UGWPUvqBY/ekboeu3EjW4i/m8vj6lbWVjsNKlGwlasSdaa/bH6JuX86peBTuz7Vr62MuriPnHUTZP8KdTA3+/oYOn4hj2FQAAPLGe4F/FAAAAAAAA8DB5e9qoX+uk6raYOCd1/OyaluyK1sBOLqaqQkn64sW8KpgnaYab0OsJGvj7DY3495bmDHNVPud7M980rmKvFtXtH+kxAAAAIG0kCgEAAAAAAJ4Qg8YmDQc6vFceebgaUt0m9HqCvpl1Wx4FDBr+fJ4c69ve1kpVn7LVzoBYXb6RoKIFU+/fw9WgXk2c9NvicG05EquOdRyy3KfRKM3aFKWVe6N19WaiWtew19vPuMjqzkil564k6N/1kdodGCtrKyv5lLbV2884m5KTr/4SpsthierT3EnT1kWqU10HDWjvrFd/CVPwxQStG1nI1FfXL6/J3tZKs4a6moY+7VjHQaXcbe71X9Neb3dO6r/PqOs6fSlBktTgvSsa0MFZL7ZwUkS0UVPXRmrP8VhduJagSl62er2ds7w9kz6G23IkRh9PvKV+rZ3kdzJOh4PjtDZZHMntDIjV9A2RCgyJV4nCBtXxttOzjRyV3yXp+MLCE/XPykhtPRqjAi7WGtDeOUUb6cUzZkm4Zm2M0k+v55Pv7mjtCYxVicI2+rCHi8oW46NDAAD+66zT3wQAAAAAAACPg4vXE+V3Ik5vj72p0OsJKdbfTRL6nYiT38m4HO//dqRRkuTsYPXA7Sp7JSWYgi/FZ6u/rUdjtM4vWpVK2iomzqjZm6O01i9GkhQbb9TgP29oy5FYNahoL58ytlp/MCkJF5/s1NyKTNT8rVFqXdNelUraZqr/3YGx5v1vutd/twaOpmTtq22dVdUrqe2Rs29rxoZIubsa1K62g06Fxuu98Td1Mcz8es3eFCVnByv1buZkSnwm5382Xh9PvKmbkUY939RJJQvbaPKaSE3fEGXaZtikW1q4PUplitrIp7Stxi2PUGKieTsZjefnheHK62ilEoVtdPRMnEb8eytT5woAADyZ+LMgAAAAAACAJ8SYgflMScK3x97UmIH5TOuSJwk9XA2a94lrjva95UiMAs7GqUIJG7PhRFPj4pi0PjzKaLb8s6m39NnUe6+7N3TUe93M5ztMLp+ztca+nV+2Bis97W2rYZNuKeBcnFrVsNfGgzG6fCNRX/TNq5Y+ScOZVixhox/nh2vP8VjT/IhxCdKIvnlVsUTmPwZzsrfSuMEFZG0t1S1vq48n3uu/e0NHrTsQo9DrCabhWS/fSNT6gzHq1sBR73dPOq5OdR3U9/swLdwWrTc73qv4q1HGVqNeyZdqv5JU2sOgr1/Op1LuBhUraFCiUdp0OEYHTsZKclZgSLwOBcepZllb/fBaUjsHTsbprT9umNrITDwvt3JS21pJ1Z+v/BymY+fidSvSqLxOD04KAwCAJxuJQgAAAAAAgCeEh6shRbLwroeRJJy/NUrzt96rYHPNY613u6ad2LsrPCqprC3/fQnFlj728ipy7+Oou8NfpqVcMRvZGpISVSULJ20bEZ2UfAw4l1St+Pm0W/p8mvl+F67dq5azs7HKUpJQkooVNMj6ziEUdzPvPzX+Z5OqOBdsi9KCbVFm6+6vAK1S6sHVjfa2VnLLZ605m6N05lKCrtxMUFSMUTF3CkXPXUlqr16Fe3M+Vn3KVva29xJ7mYmnuNu9oWRLFDbo2Ll4RUQnKq9T6kPMAgCA/wYShQAAAAAAAE+Q+5OFdz2MSsLKXraqW95OBoNU3tNG1e5LRKXlyOmkJN79c9w1rmKvFtXtU9slVdbJurp/eM6EO0Nsfv5CXrnlNU9IFit0L7llncGJd4xp5/9S7T81d4f9fKG5k+qWtzNbl9fZvIH0mluyM1qj596Wp5tBzavZy8PVXmN9I9KNKzHRmOz7jMdjHhtVhAAAWArmKAQAAAAAAHhMDRp7Qz2+vp5i+d1k4d058u4uSytJmFY76fH2tFG/1k56sYWTnva2y1CS8Py1BM3aFCkXRyvVuS85lZNK3KmAS0gwyqeMrXzK2MrGRgoNS5CD3YPjdHGwVnSsUZdvJGXSgs7H6/rtxAfukxrr+7opUTgpphsRiaaYPN0MOn05XnY2mUu+bfePUaJRmvJBAb3WzlmNKtspKuZeEvBuMnTr0RjTsp0BsYpLViiYk/EAAID/JioKAQAAAAAAHlN+J+LSXHc3Wfj8yOuyNVg9sJLwQe3khM+n3pKNwUrxiUYdPR0vKyvpq5fyKo/jw0tGtfCx16Q1kfpxQbiCLsTL2cFKczdHyd7WSs2rPbhqsWJJG+05HquBv99QSx97bTwUo/wumf97+sL5DZLi9NuicDWrbq8qXraqVdZWvruiFRefNJznxkMxOnEhXhPfK5CptgvlTUryjVseobrl7TRlbaQMyUYBLe9po0olbeV3Ik5fTr+tYoWstetYnFmStExRmxyLBwAA/DeRKAQAAAAAAHhCebgatPF7t9wOQ34nkxKRJQob1P5pBz3byFFeRR7u3HYFXKw1bnB+zdgQqV3HYnX6UoKql7bVgPbO6VYUvtDcSUHn47XdP1bzt0bpw2fzaM7mSIVHpTP+6H16N3OU38lYzd4cJVsbK1XxstV3/fNpxoZI7Q6M05r90fJ0M2joc3nSnY/xfi+1clJoWIJmbYzS+gMx6trAUWHJqh6trKSR/fNqwsoIbT0Sq0PBVhr6XB59OvWWWTs5FQ8AAPhvsgqPjMncb0AAAAA5KDwyWkUK5s3tMAAAAFJ1dHbLXO2/wXtXJEnbfspeMjCn2gEepUrPrc3V/i9duyUXJ4dcjQEAgIeNOQoBAAAAAAAAAAAAC0SiEAAAAAAA4DG3fE90lvd92PMTAgAA4MnFYOQAAAAAAACPKZ8ytvI7EadvZt7WNzNvZ6ut9rUZQhEAAADmqCgEAAAWb7efv/oOGmH6envYjxo7eb7Oh15+6H1//8e/mrt0XZrrw27e1re/TtbLg7/Uyg07c6TP2+ERGjz8R+32O5oj7SUXGxun/u9+rR17D6dYF5+QoNfe/1abdvjleL/f/DJJ0+evzPF2HyfHT51V30EjNG3uihxv+1jQaQ39Zqz6Dhqhc+cvSZLm+a7Xd79NkST9MHa6Zi1aY9p+6eot+urniZKkk6dD1HfQiByP6VEa+s1YLV29JcXyLTsPaODHox9av2fPX1TfQSMUG/fwKn3mL9ugT0aOeyQxpHcvpPY8u/s8OnLspI6dOKO3h/2fvfsO06us88f/nkxm0iZt0jskIQkJhJBQAogBVBCxARZAsaHYlR/u+tXV/S76XXfVXXUVO66oIFhoFhSkQ+ihphHSe+89k5n5/REyZJKZZBKSDHper+vKJc859znnc+7nnGec5z33fb6V1WtfWRByqPt1572y+78XZ81L8vfxeXSwfw401ifzFi7Z57a7fp405HDcJ692X7qo/SsO+HpVlub4wWX50sXtD1JVAAD8ozCiEAAgScuWpfmnj78nSTJ/0bI8O+nF/N//uiZXfvTijBg6sNnq+vNd47N+w6Z8+sPvytDBAw5oH5Onzcp3r/ltfvrfX0yStG3TOv369Ej3rpUHs9QkSXl5WUaNGJIJz03NKSccW2/dxKkzs62qKicdP/ygH3fggD7p2b3LQd/vq8njT09O317d8+SzU3LpO889qPu+/uY70rN7l1x8/tnp27t7kqRXj67Zvr06SXJEv17p0e3gXy8cer26d8mGI/s2dxlJGv482/l51LWyU1q0aJF+fbqnQ0XbZq5038adMjqnnHBMvWV9e+24dw7X59Hv/3RP5i1Yms99/JL93vZQ/BxoqE8Oxc+ZIupVWZovXdxeyAcAwCEhKAQASNKiRYu6QHDE0IF545lj84Nrb8qPf3lrvvvv/19atGieiRhWr1mfY44elDEjhx20fZaWluafP/Heg7a/3Z10/PD89Prbsr26Oi1LS+uWP/Xc1AwfMjBtWrc66Me8+PyzD/o+X20mPDs177nwnPzoF7dkxuz5GXxkv4O271Vr1ufC887MyOGD65adduLI5MQd//2Ot5x10I7F4XXqiSNz6okjm7uMJA1/nu3+efT5T17aHKXttx7dOjf6RyR/D59Hh+LnwN76BAAAePUSFAIANOKDF705n/g/38zkabNy7NGD880fXJ++vbpl+uwFmTV3QX749c/n3vET8uyk6fnXKz9Ut93Xr/5VhgzslwvOOzNJ8tyU6fnrPY9m5pwFOaJfr4w94di87jUnNHjMH1x7UxYsWpZPfugd+eLXfli3/I57H80XPv2+DB9yZP5676N5dMLELFm2MkMHD8j5bzojgwb0SZI9arzk/HNy/UtT4F36qaty4Xln5u3njstlV36tbrRkTU1N/vS38Xn4yeezYeOmnHrCyKzbsDGdOlTkkgvOSZIsWrI8t/zl/kx6YVY6tG+bsWOOzdvOOT2luwSBO40+duiO8548vS4QqK2tzbOTpuf8885IkmzavCU3//m+PDv5xWzesjXHHzM073jLWencccdoicuu/Fre+eazcs/4CWlZWpr//NInsnzl6lz7mz9nxpwFKS8ry5iRw/KBd5+XkpKSfPMH1+fI/r3yzre8ru7Yf7330cyauzB9e3fPGaeOzmvHHp9kx/SI//G9X+Yzl70rt93xYBYsWppjhg3Kxz9wQcrLyvY4nxtuuTN/vffRPZb/73e+lPKysnp9meyYIvRr/3Ntfvm9f6t7T47o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k9eOPT7HjThq3xscRI8/PTm1tclnvvztestXrFyT91z4xibto6l994odgms02RHQ7a6mpuagHq9Ht857jG5atXpdveNd9d8/S4uSkhw34qgcNbBfps+an0f3Me3mTrW1tXucR20jbZPkP7748SbXvlO7dnsPsPdVw77uzaXLV+Ur3/pZjj7qyIweOTR9e3XP3Q8+ud91Hkz77NdDdE02dL0c2H4q8+2vXpGJU2bknocm5Jrr/5BnJr2Yz3743XnimSn58a9uyZmnjsmZp45Jl8qO+en1t+1zn7/87V/SsrQ073rb619xffujsT6pra3N608/MSeMqv8HHA39rNvf+wQAAHjlBIUAAI34+Y1/SvuKdnsdtdWqVXnWbdhYb9madRvq/rtvr+55cea8umk9k+TJZ6ekZ7cudaHY604/IW8957X50n/+KD/+1a258qMXN3is0tLS9OxWmbKWLet9GTvh2anp3LHxkYh707K0NJWdOmTq9Dl1gWhV1fbMmLMgPbt3SZL079MjTz47JcOHHFkXwM1ftDTZRwh60ugRueX2+9KpY/scNbBf3aigvr26Z8vWrenZvUvd6MHNW7Zm2oy5ex2pt2LlmlRUtM24U47PuFOOz7W/+XOemfjiHmFX317dMm23Pp82Y2769e5+AD20w3W//2uqq2vyngvP2WNdq/LyrFv/8jWwZu36Az5OQyY8OyVnveaEnPTS8x2TZMvWbfmfn/4mM+cuzKABfdK6VXnWb9hUt37Dps3ZXl1d97qpfVd3Tvu4rhtzKK7RJHlhxtwce/TgJDuChBlzFuTM08YcsuM1ZMWqtZk9b1Gu/trn0umlaTlnz1vU5O27d+2chx5/NtXV1XWjpaZMm91o+72F5gdqXzXs69588pkpadumdT592Tvrtrn97kfS/hXU9Ervn32d0+G8Rg7Ehk2bU1W1PccfOzTHHzs0jz89OT+57tYkyVPPTc2pJ4zMpe88N8mOP3bYsMt93pCnnn8hj0x4Pl/7wsdS+viag3gAACAASURBVNJU0c2tb6/u2VpVVa//J0+b1eAI+v29TwAAgFfu1fGbAwBAM6upqcnkabMyedqsTJw6M9/72e/y7KQX84kPXrjXMGzwEX2zZNnK3PSnezN52qz89g931/ui+/w3jcuU6bNz218fyORpszL+8efyw2tvzqo1L49UKikpSetW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",
    "media_type": "image/png"
  }
}
```

> AGENT

I can see the issue — the Telefon field overflows past the white form card's right edge. The CSS fix with `min-width: 0` isn't enough; the grid tracks themselves need `minmax(0, 1fr)` to allow shrinking properly.

> TOOL

tool_use Read
id: toolu_01BBjPy7S994hXWK8WwMmJCL
```json
{
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "offset": 78,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01BBjPy7S994hXWK8WwMmJCL
```
    78→/* ===== Form ===== */
    79→.krisen-form {
    80→  background: var(--white);
    81→  border: 1px solid var(--gray-100);
    82→  border-radius: var(--radius);
    83→  padding: 32px;
    84→}
    85→
    86→.krisen-form__section {
    87→  margin-bottom: 32px;
    88→}
    89→
    90→.krisen-form__section-title {
    91→  font-size: .72rem;
    92→  font-family: var(--font-mono);
    93→  letter-spacing: 3px;
    94→  text-transform: uppercase;
    95→  color: var(--bos-gold);
    96→  margin-bottom: 16px;
    97→  padding-bottom: 8px;
    98→  border-bottom: 1px solid var(--gray-100);
    99→}
   100→
   101→.krisen-form__row {
   102→  display: grid;
   103→  grid-template-columns: repeat(4, 1fr);
   104→  gap: 16px;
   105→  margin-bottom: 16px;
   106→}
   107→
   108→.krisen-form__row--2 {
   109→  grid-template-columns: repeat(2, 1fr);
   110→}
   111→
   112→.krisen-form__row--3 {
   113→  grid-template-columns: repeat(3, 1fr);
   114→}
   115→
   116→.krisen-form__group {
   117→  display: flex;

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use Edit
id: toolu_01QpoDaiZWSUuNKWz8EmAKRy
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-form {\n  background: var(--white);\n  border: 1px solid var(--gray-100);\n  border-radius: var(--radius);\n  padding: 32px;\n}",
  "new_string": ".krisen-form {\n  background: var(--white);\n  border: 1px solid var(--gray-100);\n  border-radius: var(--radius);\n  padding: 32px;\n  overflow: hidden;\n}"
}
```

> TOOL

tool_result
id: toolu_01QpoDaiZWSUuNKWz8EmAKRy
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_012KbF4L6uJp3T5cPDKzJzVt
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": "  grid-template-columns: repeat(4, 1fr);\n  gap: 16px;\n  margin-bottom: 16px;\n}\n\n.krisen-form__row--2 {\n  grid-template-columns: repeat(2, 1fr);\n}\n\n.krisen-form__row--3 {\n  grid-template-columns: repeat(3, 1fr);\n}",
  "new_string": "  grid-template-columns: repeat(4, minmax(0, 1fr));\n  gap: 16px;\n  margin-bottom: 16px;\n}\n\n.krisen-form__row--2 {\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n}\n\n.krisen-form__row--3 {\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n}"
}
```

> TOOL

tool_result
id: toolu_012KbF4L6uJp3T5cPDKzJzVt
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> AGENT

Also fix the `display: grid` on `--2` and `--3` rows — they were missing `display: grid` since they only override `grid-template-columns` but the template uses them as standalone classes (not combined with `krisen-form__row`).

> TOOL

tool_use Read
id: toolu_01J1eybZRTSDXvoqSu7iTq6f
```json
{
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "offset": 26,
  "limit": 20
}
```

> TOOL

tool_result
id: toolu_01J1eybZRTSDXvoqSu7iTq6f
```
    26→  {# ===== Divider ===== #}
    27→  <div class="form-divider">oder online ausfüllen</div>
    28→
    29→  {# ===== Online Form ===== #}
    30→  <form id="krisenForm" class="krisen-form" autocomplete="off">
    31→
    32→    {# --- Lfd. Nr. --- #}
    33→    <div class="krisen-form__section">
    34→      <div class="krisen-form__row--2">
    35→        <div class="krisen-form__group">
    36→          <label for="lfdnr">Lfd. Nr.</label>
    37→          <input type="text" id="lfdnr" placeholder="z.B. 001">
    38→        </div>
    39→      </div>
    40→    </div>
    41→
    42→    {# --- Entgegennahme --- #}
    43→    <div class="krisen-form__section">
    44→      <div class="krisen-form__section-title">Entgegennahme durch</div>
    45→      <div class="krisen-form__row">

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> AGENT

The `--2` and `--3` classes are used standalone. They need their own `display: grid` and gap:

> TOOL

tool_use Edit
id: toolu_01SNzcswuS2ACRrDczsaPxqm
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-form__row--2 {\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n}\n\n.krisen-form__row--3 {\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n}",
  "new_string": ".krisen-form__row--2 {\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  gap: 16px;\n  margin-bottom: 16px;\n}\n\n.krisen-form__row--3 {\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  gap: 16px;\n  margin-bottom: 16px;\n}"
}
```

> TOOL

tool_result
id: toolu_01SNzcswuS2ACRrDczsaPxqm
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01WBHyPJtQLKCJY5mGwfGf1N
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy overflow fix",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01WBHyPJtQLKCJY5mGwfGf1N
```
[0;32m=== Deploying BOS-ARSA to achildrenmile@host-node-01 ===[0m
Host: achildrenmile@host-node-01
Remote dir: /home/<USER>/apps/bosarsa
Container: bosarsa
Port: 3417:80

[0;32mStep 1: Syncing files...[0m
sending incremental file list
.entire/logs/entire.log
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/context.md
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/full.jsonl
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/prompt.txt
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/summary.txt
.entire/tmp/
.entire/tmp/pre-prompt-af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6.json
src/css/
src/css/krisenkommunikation.css

sent 67,334 bytes  received 7,025 bytes  148,718.00 bytes/sec
total size is 104,110,414  speedup is 1,400.11
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 0.9s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#5 resolve docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa 0.0s done
#5 DONE 0.0s

#6 [stage-1 1/4] FROM docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#6 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba 0.0s done
#6 DONE 0.0s

#7 [internal] load build context
#7 transferring context: 1.04MB 0.1s done
#7 DONE 0.1s

#8 [build 2/6] WORKDIR /app
#8 CACHED

#9 [build 3/6] COPY package*.json ./
#9 CACHED

#10 [build 4/6] RUN npm ci --production
#10 CACHED

#11 [build 5/6] COPY . .
#11 DONE 0.6s

#12 [build 6/6] RUN npx @11ty/eleventy
#12 1.388 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 1.394 [11ty] Writing […]

> AGENT

Deployed. The fixes:

- Changed all grid columns from `1fr` to `minmax(0, 1fr)` — this allows grid tracks to shrink below their content's intrinsic minimum width
- Added `overflow: hidden` on `.krisen-form` as a safety net
- Fixed `--2` and `--3` row variants to include `display: grid` (they were used standalone without the base `krisen-form__row` class)

Do a hard refresh (Ctrl+Shift+R) to bypass the CSS cache and check again.