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

> DEVELOPER

Bitte auch dieses Dokument auf die BOS-ARSA-Seite hochladen. downloads folder

> TOOL

tool_use Bash
id: toolu_016nkGioxkLmjyJGxkUjFLrp
```json
{
  "command": "ls -lt /home/<USER>/Downloads/*.pdf 2>/dev/null | head -10",
  "description": "Find PDF files in Downloads"
}
```

> TOOL

tool_result
id: toolu_016nkGioxkLmjyJGxkUjFLrp
```
-rw-r--r-- 1 achildrenmile users   359938 Mar  8 08:21 REDACTED.3.3 (1).pdf
-rw-r--r-- 1 achildrenmile users   359938 Mar  8 08:19 REDACTED.3.3.pdf
-rw-r--r-- 1 achildrenmile users  1024352 Mar  8 08:13 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular (6).pdf
-rw-r--r-- 1 achildrenmile users   586213 Mar  8 00:11 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular.pdf
-rw-r--r-- 1 achildrenmile users   378333 Mar  7 23:40 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular (5).pdf
-rw-r--r-- 1 achildrenmile users   378333 Mar  7 22:02 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular (4).pdf
-rw-r--r-- 1 achildrenmile users   378333 Mar  7 21:24 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular (3).pdf
-rw-r--r-- 1 achildrenmile users   378333 Mar  7 21:21 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular (2).pdf
-rw-r--r-- 1 achildrenmile users   378333 Mar  7 20:18 /home/<USER>/Downloads/Krisenkommunikation-Aufnahmeformular (1).pdf
-rw-r--r-- 1 achildrenmile users   163601 Mar  6 14:49 /home/<USER>/Downloads/Angebot_WoGa-MCT_Strali.pdf
```

> AGENT

Das neueste Dokument ist `Notfunk-Konzept_T1V1.3.3.pdf`. Soll das auf die Krisenkommunikation-Seite als zusätzlicher Download, oder soll es woanders eingebunden werden?

> TOOL

tool_use AskUserQuestion
id: toolu_01F7LasBfYN7BAjAETugJign
```json
{
  "questions": [
    {
      "question": "Wie soll das Notfunk-Konzept auf der Seite eingebunden werden?",
      "header": "Einbindung",
      "options": [
        {
          "label": "Auf Krisenkommunikation-Seite",
          "description": "Als zweite Download-Card neben dem Aufnahmeformular"
        },
        {
          "label": "Eigene Seite",
          "description": "Neue Seite /notfunk-konzept/ mit eigenem Download"
        },
        {
          "label": "Nur als Download",
          "description": "Nur als PDF-Datei verfügbar machen, ohne spezielle Seiteneinbindung"
        }
      ],
      "multiSelect": false
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01F7LasBfYN7BAjAETugJign
```
User has answered your questions: "Wie soll das Notfunk-Konzept auf der Seite eingebunden werden?"="Auf Krisenkommunikation-Seite". You can now continue with the user's answers in mind.
```

> TOOL

tool_use Bash
id: toolu_0132oCf3s5k1zwPxs4HuZsBS
```json
{
  "command": "cp \"REDACTED.3.3.pdf\" /home/<USER>/bosarsa/Notfunk-Konzept.pdf",
  "description": "Copy Notfunk-Konzept PDF to project root"
}
```

> TOOL

tool_result
id: toolu_0132oCf3s5k1zwPxs4HuZsBS
```

```

> AGENT

Now add a second download card on the Krisenkommunikation page.

> TOOL

tool_use Read
id: toolu_01LBqX56sTYNNSc8eK2wGJ9k
```json
{
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "offset": 13,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01LBqX56sTYNNSc8eK2wGJ9k
```
    13→  <p class="subtitle">Aufnahmeformular für strukturierte Notfallmeldungen im BOS-Funkbetrieb</p>
    14→
    15→  {# ===== Download Card ===== #}
    16→  <div class="download-card">
    17→    <div class="download-card__info">
    18→      <h2>Aufnahmeformular als PDF</h2>
    19→      <p>Druckfertige Version zum Ausfüllen per Hand — ideal für den Einsatz im Feld.</p>
    20→    </div>
    21→    <a href="/Krisenkommunikation-Aufnahmeformular.pdf" download class="btn btn--gold">
    22→      <i data-lucide="download"></i> PDF herunterladen
    23→    </a>
    24→  </div>
    25→
    26→  {# ===== Divider ===== #}
    27→  <div class="form-divider">oder online ausfüllen</div>

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use Edit
id: toolu_01QTgCncKTgCPKTHVHWNFTny
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "old_string": "  {# ===== Divider ===== #}\n  <div class=\"form-divider\">oder online ausfüllen</div>",
  "new_string": "  {# ===== Download Card 2 ===== #}\n  <div class=\"download-card\" style=\"margin-top: 16px\">\n    <div class=\"download-card__info\">\n      <h2>Notfunk-Konzept</h2>\n      <p>Konzeptdokument für den Notfunkbetrieb — Grundlagen, Abläufe und Organisation.</p>\n    </div>\n    <a href=\"/Notfunk-Konzept.pdf\" download class=\"btn btn--polizei\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>\n\n  {# ===== Divider ===== #}\n  <div class=\"form-divider\">oder online ausfüllen</div>"
}
```

> TOOL

tool_result
id: toolu_01QTgCncKTgCPKTHVHWNFTny
```
The file /home/<USER>/bosarsa/src/krisenkommunikation.njk has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01LD5RNwsHDH9Tt2vZJ8CFwV
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy with Notfunk-Konzept PDF",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01LD5RNwsHDH9Tt2vZJ8CFwV
```
[0;32m=== Deploying BOS-ARSA to achildrenmile@host-node-01 ===[0m
Host: achildrenmile@host-node-01
Remote dir: /home/<USER>/apps/bosarsa
Container: bosarsa
Port: 3417:80

[0;32mStep 1: Syncing files...[0m
sending incremental file list
./
Notfunk-Konzept.pdf
.entire/logs/entire.log
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/context.md
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/full.jsonl
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/prompt.txt
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/summary.txt
.entire/tmp/
.entire/tmp/pre-prompt-af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6.json
src/
src/krisenkommunikation.njk

sent 446,916 bytes  received 7,449 bytes  302,910.00 bytes/sec
total size is 104,803,866  speedup is 230.66
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 0.5s

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
#7 transferring context: 1.74MB 0.1s done
#7 DONE 0.1s

#8 [build 3/6] COPY package*.json ./
#8 CACHED

#9 [build 2/6] WORKDIR /app
#9 CACHED

#10 [build 4/6] RUN npm ci --production
#10 CACHED

#11 [build 5/6] COPY . .
#11 DONE 1.0s

#12 [build 6/6] RUN npx @11ty/eleventy
#12 2.062 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 2.120 […]

> AGENT

Deployed. Jetzt kümmere ich mich um deine Folgewünsche: Seitenstruktur mit Überschriften/Einleitung verbessern und ein Nav-Menüitem für Krisenkommunikation hinzufügen.

> TOOL

tool_use Read
id: toolu_01CD2M1CyVhoGjJxQUNoAtLH
```json
{
  "file_path": "/home/<USER>/bosarsa/src/_includes/nav.njk"
}
```

> TOOL

tool_result
id: toolu_01CD2M1CyVhoGjJxQUNoAtLH
```
     1→<nav class="nav" id="nav" role="navigation" aria-label="Hauptnavigation">
     2→  <div class="container nav__inner">
     3→    <a href="/" class="nav__brand" aria-label="BOS-ARSA Startseite">
     4→      <img src="/logo.webp?v=2" alt="BOS-ARSA Logo" class="nav__brand-logo" width="176" height="70">
     5→      <span class="nav__brand-text">
     6→        <span class="nav__brand-name">BOS-ARSA</span>
     7→        <span class="nav__brand-sub">Amateur-Radio-Society-Austria</span>
     8→      </span>
     9→    </a>
    10→    <button class="nav__hamburger" id="navToggle" aria-label="Menü öffnen" aria-expanded="false" aria-controls="navLinks">
    11→      <span></span><span></span><span></span>
    12→    </button>
    13→    <ul class="nav__links" id="navLinks">
    14→      {% set prefix = "#" if activeNav == "home" else "/#" %}
    15→      <li><a href="{{ prefix }}ueber-uns">Über uns</a></li>
    16→      <li><a href="{{ prefix }}video">Videos</a></li>
    17→      <li><a href="{{ prefix }}vorstand">Vorstand</a></li>
    18→      <li><a href="{{ prefix }}ziele">Ziele</a></li>
    19→      <li><a href="{{ prefix }}funkbetrieb">Funkbetrieb</a></li>
    20→      <li><a href="{{ prefix }}mitglied">Mitglied werden</a></li>
    21→      <li><a href="/termine/"{% if activeNav == "termine" %} class="active"{% endif %}>Termine</a></li>
    22→      <li><a href="/presse/"{% if activeNav == "presse" %} class="active"{% endif %}>Presse</a></li>
    23→      <li><a href="{{ prefix }}kontakt">Kontakt</a></li>
    24→    </ul>
    25→  </div>
    26→</nav>

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>

```

> TOOL

tool_use Read
id: toolu_01Lto4RYPfjBjUGDd2h1DugY
```json
{
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk"
}
```

> TOOL

tool_result
id: toolu_01Lto4RYPfjBjUGDd2h1DugY
```
     1→---
     2→layout: base.njk
     3→title: "Krisenkommunikation — BOS-ARSA"
     4→description: "Krisenkommunikation-Aufnahmeformular zum Download und Online-Ausfüllen. Strukturierte Erfassung von Notrufen für den BOS-Funkbetrieb."
     5→canonical: "https://bosarsa.oeradio.at/krisenkommunikation/"
     6→activeNav: krisenkommunikation
     7→pageCSSFile: "/css/krisenkommunikation.css"
     8→permalink: /krisenkommunikation/
     9→---
    10→
    11→<div class="krisen-page">
    12→  <h1>Krisenkommunikation</h1>
    13→  <p class="subtitle">Aufnahmeformular für strukturierte Notfallmeldungen im BOS-Funkbetrieb</p>
    14→
    15→  {# ===== Download Card ===== #}
    16→  <div class="download-card">
    17→    <div class="download-card__info">
    18→      <h2>Aufnahmeformular als PDF</h2>
    19→      <p>Druckfertige Version zum Ausfüllen per Hand — ideal für den Einsatz im Feld.</p>
    20→    </div>
    21→    <a href="/Krisenkommunikation-Aufnahmeformular.pdf" download class="btn btn--gold">
    22→      <i data-lucide="download"></i> PDF herunterladen
    23→    </a>
    24→  </div>
    25→
    26→  {# ===== Download Card 2 ===== #}
    27→  <div class="download-card" style="margin-top: 16px">
    28→    <div class="download-card__info">
    29→      <h2>Notfunk-Konzept</h2>
    30→      <p>Konzeptdokument für den Notfunkbetrieb — Grundlagen, Abläufe und Organisation.</p>
    31→    </div>
    32→    <a href="/Notfunk-Konzept.pdf" download class="btn btn--polizei">
    33→      <i data-lucide="download"></i> PDF herunterladen
    34→    </a>
    35→  </div>
    36→
    37→  {# ===== Divider ===== #}
    38→  <div class="form-divider">oder online ausfüllen</div>
    39→
    40→  {# ===== Online Form ===== #}
    41→  <form id="krisenForm" class="krisen-form" autocomplete="off">
    42→
    43→    {# --- Lfd. Nr. --- #}
    44→    <div class="krisen-form__section">
    45→      <div class="krisen-form__row--2">
    46→        <div class="krisen-form__group">
    47→          <label for="lfdnr">Lfd. Nr.</label>
    48→          <input type="text" id="lfdnr" placeholder="z.B. 001">
    49→        </div>
    50→      </div>
    51→    </div>
    52→ […]

> AGENT

Now I'll restructure the page with sections and headings, and add the nav item.

> TOOL

tool_use Edit
id: toolu_01GBnfrowT4sz2FvUSgZBQtY
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "old_string": "<div class=\"krisen-page\">\n  <h1>Krisenkommunikation</h1>\n  <p class=\"subtitle\">Aufnahmeformular für strukturierte Notfallmeldungen im BOS-Funkbetrieb</p>\n\n  {# ===== Download Card ===== #}\n  <div class=\"download-card\">\n    <div class=\"download-card__info\">\n      <h2>Aufnahmeformular als PDF</h2>\n      <p>Druckfertige Version zum Ausfüllen per Hand — ideal für den Einsatz im Feld.</p>\n    </div>\n    <a href=\"/Krisenkommunikation-Aufnahmeformular.pdf\" download class=\"btn btn--gold\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>\n\n  {# ===== Download Card 2 ===== #}\n  <div class=\"download-card\" style=\"margin-top: 16px\">\n    <div class=\"download-card__info\">\n      <h2>Notfunk-Konzept</h2>\n      <p>Konzeptdokument für den Notfunkbetrieb — Grundlagen, Abläufe und Organisation.</p>\n    </div>\n    <a href=\"/Notfunk-Konzept.pdf\" download class=\"btn btn--polizei\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>\n\n  {# ===== Divider ===== #}\n  <div class=\"form-divider\">oder online ausfüllen</div>\n\n  {# ===== Online Form ===== #}\n  <form id=\"krisenForm\" class=\"krisen-form\" autocomplete=\"off\">",
  "new_string": "<div class=\"krisen-page\">\n  <h1>Krisenkommunikation</h1>\n  <p class=\"subtitle\">Strukturierte Erfassung und Weitergabe von Notfallmeldungen im BOS-Funkbetrieb</p>\n\n  <p class=\"krisen-intro\">\n    Im Notfunkbetrieb ist eine klare und strukturierte Kommunikation entscheidend.\n    Das Krisenkommunikation-Aufnahmeformular unterstützt Funkoperatoren bei der\n    systematischen Erfassung von Notrufen nach dem bewährten 7-W-Fragen-Schema und\n    stellt sicher, dass alle relevanten Informationen vollständig weitergegeben werden.\n  </p>\n\n  {# ===== Downloads ===== #}\n  <h2 class=\"krisen-section-title\"><i data-lucide=\"folder-down\"></i> Dokumente & Downloads</h2>\n\n  <div class=\"download-card\">\n    <div class=\"download-card__info\">\n      <h3>Aufnahmeformular</h3>\n      <p>Druckfertige Version zum Ausfüllen per Hand — ideal für den Einsatz im Feld.</p>\n    </div>\n    <a href=\"/Krisenkommunikation-Aufnahmeformular.pdf\" download class=\"btn btn--gold\">\n      <i data-lucide=\"download\"></i> PDF […]

> TOOL

tool_result
id: toolu_01GBnfrowT4sz2FvUSgZBQtY
```
The file /home/<USER>/bosarsa/src/krisenkommunikation.njk has been updated successfully.
```

> AGENT

Now add CSS for the new elements and the nav item.

> TOOL

tool_use Edit
id: toolu_01BNTiTkdHQtfgeuY49cNDLL
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-page .subtitle {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 40px;\n}",
  "new_string": ".krisen-page .subtitle {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 20px;\n}\n\n.krisen-intro {\n  font-size: .92rem;\n  color: var(--gray-700);\n  line-height: 1.7;\n  margin-bottom: 40px;\n}\n\n.krisen-section-title {\n  display: flex;\n  align-items: center;\n  gap: 10px;\n  font-size: 1.1rem;\n  font-weight: 700;\n  color: var(--polizei-navy);\n  margin-bottom: 16px;\n  margin-top: 40px;\n}\n\n.krisen-section-title:first-of-type {\n  margin-top: 0;\n}\n\n.krisen-section-title i {\n  width: 20px;\n  height: 20px;\n  color: var(--bos-gold);\n}\n\n.krisen-form-intro {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 16px;\n}"
}
```

> TOOL

tool_result
id: toolu_01BNTiTkdHQtfgeuY49cNDLL
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> AGENT

Notfunk-Konzept als erstes setzen und Nav-Item hinzufügen.

> TOOL

tool_use Edit
id: toolu_0113CmAPAM4mGeHCQMB6rJY2
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "old_string": "  <div class=\"download-card\">\n    <div class=\"download-card__info\">\n      <h3>Aufnahmeformular</h3>\n      <p>Druckfertige Version zum Ausfüllen per Hand — ideal für den Einsatz im Feld.</p>\n    </div>\n    <a href=\"/Krisenkommunikation-Aufnahmeformular.pdf\" download class=\"btn btn--gold\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>\n\n  <div class=\"download-card\" style=\"margin-top: 12px\">\n    <div class=\"download-card__info\">\n      <h3>Notfunk-Konzept</h3>\n      <p>Konzeptdokument für den Notfunkbetrieb — Grundlagen, Abläufe und Organisation.</p>\n    </div>\n    <a href=\"/Notfunk-Konzept.pdf\" download class=\"btn btn--polizei\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>",
  "new_string": "  <div class=\"download-card\">\n    <div class=\"download-card__info\">\n      <h3>Notfunk-Konzept</h3>\n      <p>Konzeptdokument für den Notfunkbetrieb — Grundlagen, Abläufe und Organisation.</p>\n    </div>\n    <a href=\"/Notfunk-Konzept.pdf\" download class=\"btn btn--polizei\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>\n\n  <div class=\"download-card\" style=\"margin-top: 12px\">\n    <div class=\"download-card__info\">\n      <h3>Aufnahmeformular</h3>\n      <p>Druckfertige Version zum Ausfüllen per Hand — ideal für den Einsatz im Feld.</p>\n    </div>\n    <a href=\"/Krisenkommunikation-Aufnahmeformular.pdf\" download class=\"btn btn--gold\">\n      <i data-lucide=\"download\"></i> PDF herunterladen\n    </a>\n  </div>"
}
```

> TOOL

tool_result
id: toolu_0113CmAPAM4mGeHCQMB6rJY2
```
The file /home/<USER>/bosarsa/src/krisenkommunikation.njk has been updated successfully.
```

> AGENT

Now add the nav menu item.

> TOOL

tool_use Edit
id: toolu_01NXony8ge9Nu3MT8Sj7Xiky
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/_includes/nav.njk",
  "old_string": "      <li><a href=\"/presse/\"{% if activeNav == \"presse\" %} class=\"active\"{% endif %}>Presse</a></li>\n      <li><a href=\"{{ prefix }}kontakt\">Kontakt</a></li>",
  "new_string": "      <li><a href=\"/presse/\"{% if activeNav == \"presse\" %} class=\"active\"{% endif %}>Presse</a></li>\n      <li><a href=\"/krisenkommunikation/\"{% if activeNav == \"krisenkommunikation\" %} class=\"active\"{% endif %}>Krisenkommunikation</a></li>\n      <li><a href=\"{{ prefix }}kontakt\">Kontakt</a></li>"
}
```

> TOOL

tool_result
id: toolu_01NXony8ge9Nu3MT8Sj7Xiky
```
The file /home/<USER>/bosarsa/src/_includes/nav.njk has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01LhSRZmsPVBoUMkwraHyfjd
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy page restructure + nav item",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01LhSRZmsPVBoUMkwraHyfjd
```
[0;32m=== Deploying BOS-ARSA to achildrenmile@host-node-01 ===[0m
Host: achildrenmile@host-node-01
Remote dir: /home/<USER>/apps/bosarsa
Container: bosarsa
Port: 3417:80

[0;32mStep 1: Syncing files...[0m
sending incremental file list
src/
src/krisenkommunikation.njk
src/_includes/
src/_includes/nav.njk
src/css/
src/css/krisenkommunikation.css

sent 56,791 bytes  received 588 bytes  114,758.00 bytes/sec
total size is 104,805,089  speedup is 1,826.54
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 0.5s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [stage-1 1/4] FROM docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#5 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba 0.0s done
#5 DONE 0.0s

#6 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#6 resolve docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa 0.0s done
#6 DONE 0.0s

#7 [internal] load build context
#7 transferring context: 146.57kB 0.1s done
#7 DONE 0.1s

#8 [build 3/6] COPY package*.json ./
#8 CACHED

#9 [build 2/6] WORKDIR /app
#9 CACHED

#10 [build 4/6] RUN npm ci --production
#10 CACHED

#11 [build 5/6] COPY . .
#11 DONE 0.6s

#12 [build 6/6] RUN npx @11ty/eleventy
#12 1.394 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 1.400 [11ty] Writing ./_site/robots.txt from ./src/robots.njk […]

> AGENT

Deployed. Zusammenfassung der Änderungen:

1. **Seitenstruktur** — Einleitungstext mit Beschreibung des 7-W-Fragen-Schemas hinzugefügt
2. **Abschnitte mit Überschriften** — "Dokumente & Downloads" und "Online-Aufnahmeformular" als h2-Sektionen mit Icons
3. **Notfunk-Konzept zuerst** — steht jetzt vor dem Aufnahmeformular-Download
4. **Nav-Menüitem** — "Krisenkommunikation" in der Hauptnavigation zwischen "Presse" und "Kontakt"

> DEVELOPER

besser formatieren. text pickt zu sehr zusammen

> TOOL

tool_use Read
id: toolu_01CA7evqkffkHou2CmdQXR8q
```json
{
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css"
}
```

> TOOL

tool_result
id: toolu_01CA7evqkffkHou2CmdQXR8q
```
     1→/* ===== Krisenkommunikation Page ===== */
     2→
     3→.krisen-page {
     4→  max-width: 860px;
     5→  margin: 0 auto;
     6→  padding: calc(var(--nav-h) + 48px) 24px 80px;
     7→}
     8→
     9→.krisen-page h1 {
    10→  font-size: 1.6rem;
    11→  font-weight: 800;
    12→  color: var(--gray-900);
    13→  margin-bottom: 8px;
    14→}
    15→
    16→.krisen-page .subtitle {
    17→  font-size: .85rem;
    18→  color: var(--gray-500);
    19→  margin-bottom: 20px;
    20→}
    21→
    22→.krisen-intro {
    23→  font-size: .92rem;
    24→  color: var(--gray-700);
    25→  line-height: 1.7;
    26→  margin-bottom: 40px;
    27→}
    28→
    29→.krisen-section-title {
    30→  display: flex;
    31→  align-items: center;
    32→  gap: 10px;
    33→  font-size: 1.1rem;
    34→  font-weight: 700;
    35→  color: var(--polizei-navy);
    36→  margin-bottom: 16px;
    37→  margin-top: 40px;
    38→}
    39→
    40→.krisen-section-title:first-of-type {
    41→  margin-top: 0;
    42→}
    43→
    44→.krisen-section-title i {
    45→  width: 20px;
    46→  height: 20px;
    47→  color: var(--bos-gold);
    48→}
    49→
    50→.krisen-form-intro {
    51→  font-size: .85rem;
    52→  color: var(--gray-500);
    53→  margin-bottom: 16px;
    54→}
    55→
    56→/* ===== Download Card ===== */
    57→.download-card {
    58→  display: flex;
    59→  align-items: center;
    60→  justify-content: space-between;
    61→  gap: 24px;
    62→  padding: 28px 32px;
    63→  background: var(--white);
    64→  border: 1px solid var(--gray-100);
    65→  border-radius: var(--radius);
    66→  transition: border-color .2s, box-shadow .2s;
    67→}
    68→
    69→.download-card:hover {
    70→  border-color: var(--polizei-mid);
    71→  box-shadow: 0 2px 12px rgba(59,90,140,.08);
    72→}
    73→
    74→.download-card__info h2 {
    75→  font-size: 1.05rem; […]

> AGENT

Ich erhöhe die Abstände durchgehend — mehr Luft zwischen Überschrift, Einleitung, Sektionen und Formular-Elementen.

> TOOL

tool_use Edit
id: toolu_01LPDrhHqRHYTrGqqjrxHY9v
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-page h1 {\n  font-size: 1.6rem;\n  font-weight: 800;\n  color: var(--gray-900);\n  margin-bottom: 8px;\n}\n\n.krisen-page .subtitle {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 20px;\n}\n\n.krisen-intro {\n  font-size: .92rem;\n  color: var(--gray-700);\n  line-height: 1.7;\n  margin-bottom: 40px;\n}\n\n.krisen-section-title {\n  display: flex;\n  align-items: center;\n  gap: 10px;\n  font-size: 1.1rem;\n  font-weight: 700;\n  color: var(--polizei-navy);\n  margin-bottom: 16px;\n  margin-top: 40px;\n}\n\n.krisen-section-title:first-of-type {\n  margin-top: 0;\n}\n\n.krisen-section-title i {\n  width: 20px;\n  height: 20px;\n  color: var(--bos-gold);\n}\n\n.krisen-form-intro {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 16px;\n}",
  "new_string": ".krisen-page h1 {\n  font-size: 1.6rem;\n  font-weight: 800;\n  color: var(--gray-900);\n  margin-bottom: 12px;\n}\n\n.krisen-page .subtitle {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 28px;\n}\n\n.krisen-intro {\n  font-size: .92rem;\n  color: var(--gray-700);\n  line-height: 1.75;\n  margin-bottom: 48px;\n}\n\n.krisen-section-title {\n  display: flex;\n  align-items: center;\n  gap: 10px;\n  font-size: 1.1rem;\n  font-weight: 700;\n  color: var(--polizei-navy);\n  margin-bottom: 20px;\n  margin-top: 56px;\n}\n\n.krisen-section-title:first-of-type {\n  margin-top: 0;\n}\n\n.krisen-section-title i {\n  width: 20px;\n  height: 20px;\n  color: var(--bos-gold);\n}\n\n.krisen-form-intro {\n  font-size: .85rem;\n  color: var(--gray-500);\n  margin-bottom: 20px;\n}"
}
```

> TOOL

tool_result
id: toolu_01LPDrhHqRHYTrGqqjrxHY9v
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01QSXBAGoMQntZGPm6yUJ7iw
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".download-card__info h2 {\n  font-size: 1.05rem;\n  font-weight: 700;\n  color: var(--gray-900);\n  margin-bottom: 4px;\n}\n\n.download-card__info p {\n  font-size: .85rem;\n  color: var(--gray-500);\n}",
  "new_string": ".download-card__info h2,\n.download-card__info h3 {\n  font-size: 1.05rem;\n  font-weight: 700;\n  color: var(--gray-900);\n  margin-bottom: 6px;\n}\n\n.download-card__info p {\n  font-size: .85rem;\n  color: var(--gray-500);\n  line-height: 1.5;\n}"
}
```

> TOOL

tool_result
id: toolu_01QSXBAGoMQntZGPm6yUJ7iw
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> AGENT

Now increase spacing inside the form sections:

> TOOL

tool_use Edit
id: toolu_016Bph8UitTcYNopEv1tMKSx
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-form__section {\n  margin-bottom: 32px;\n}\n\n.krisen-form__section-title {\n  font-size: .72rem;\n  font-family: var(--font-mono);\n  letter-spacing: 3px;\n  text-transform: uppercase;\n  color: var(--bos-gold);\n  margin-bottom: 16px;\n  padding-bottom: 8px;\n  border-bottom: 1px solid var(--gray-100);\n}",
  "new_string": ".krisen-form__section {\n  margin-bottom: 36px;\n}\n\n.krisen-form__section:last-child {\n  margin-bottom: 0;\n}\n\n.krisen-form__section-title {\n  font-size: .72rem;\n  font-family: var(--font-mono);\n  letter-spacing: 3px;\n  text-transform: uppercase;\n  color: var(--bos-gold);\n  margin-bottom: 20px;\n  padding-bottom: 10px;\n  border-bottom: 1px solid var(--gray-100);\n}"
}
```

> TOOL

tool_result
id: toolu_016Bph8UitTcYNopEv1tMKSx
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01Ju1MRD3WbBGDCpwzv5J4Ta
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-form__group {\n  display: flex;\n  flex-direction: column;\n  gap: 4px;\n  min-width: 0;\n}",
  "new_string": ".krisen-form__group {\n  display: flex;\n  flex-direction: column;\n  gap: 6px;\n  min-width: 0;\n}"
}
```

> TOOL

tool_result
id: toolu_01Ju1MRD3WbBGDCpwzv5J4Ta
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> AGENT

Now also increase the W-Fragen spacing in the template (replace inline styles with proper margin):

> TOOL

tool_use Edit
id: toolu_01Wh8KMS5xj6SMDcagMeFsbV
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "old_string": "style=\"margin-bottom:12px\"",
  "new_string": "style=\"margin-bottom:16px\""
}
```

> TOOL

tool_result
id: toolu_01Wh8KMS5xj6SMDcagMeFsbV
```
The file /home/<USER>/bosarsa/src/krisenkommunikation.njk has been updated. All occurrences of 'style="margin-bottom:12px"' were successfully replaced with 'style="margin-bottom:16px"'.
```

> AGENT

Also increase the form actions spacing:

> TOOL

tool_use Edit
id: toolu_01XQNLRYpaYgVWFb9WA2KjLf
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".krisen-form__actions {\n  display: flex;\n  gap: 12px;\n  margin-top: 32px;\n  padding-top: 24px;\n  border-top: 1px solid var(--gray-100);\n}",
  "new_string": ".krisen-form__actions {\n  display: flex;\n  gap: 16px;\n  margin-top: 40px;\n  padding-top: 28px;\n  border-top: 1px solid var(--gray-100);\n}"
}
```

> TOOL

tool_result
id: toolu_01XQNLRYpaYgVWFb9WA2KjLf
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_018FvsSFo72TujvMUx9xCZDi
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy spacing improvements",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_018FvsSFo72TujvMUx9xCZDi
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
src/
src/krisenkommunikation.njk
src/css/
src/css/krisenkommunikation.css

sent 74,781 bytes  received 8,613 bytes  166,788.00 bytes/sec
total size is 105,054,469  speedup is 1,259.74
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 1.1s

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
#7 transferring context: 1.63MB 0.1s done
#7 DONE 0.1s

#8 [build 2/6] WORKDIR /app
#8 CACHED

#9 [build 3/6] COPY package*.json ./
#9 CACHED

#10 [build 4/6] RUN npm ci --production
#10 CACHED

#11 [build 5/6] COPY . .
#11 DONE 0.8s

#12 [build 6/6] RUN npx @11ty/eleventy
#12 1.962 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 2.037 […]

> AGENT

Deployed. Abstände sind jetzt deutlich großzügiger:

- **h1 → Subtitle**: 12px statt 8px
- **Subtitle → Intro**: 28px statt 20px
- **Intro → erste Sektion**: 48px statt 40px
- **Sektionsüberschriften**: 56px Abstand nach oben, 20px nach unten
- **Formular-Sektionen**: 36px Abstand untereinander
- **Sektion-Titel im Formular**: 20px Abstand nach unten, 10px Padding
- **W-Fragen**: 16px Abstand zwischen den Feldern
- **Label → Input**: 6px statt 4px
- **Aktions-Buttons**: 40px/28px Abstand

Ctrl+Shift+R zum Cache leeren.

> DEVELOPER

see latest screenshot. still the same!

> TOOL

tool_use Bash
id: toolu_01BcvfxoctRXhRhrE1PSAstJ
```json
{
  "command": "ls -lt /home/<USER>/Pictures/Screenshots/*.png | head -3",
  "description": "Find latest screenshot"
}
```

> TOOL

tool_result
id: toolu_01BcvfxoctRXhRhrE1PSAstJ
```
-rw-r--r-- 1 achildrenmile users  125851 Mar  8 08:26 /home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-26-44.png
-rw-r--r-- 1 achildrenmile users   71082 Mar  8 08:17 /home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-17-04.png
-rw-r--r-- 1 achildrenmile users  104976 Mar  7 14:38 /home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-07 14-38-57.png
```

> TOOL

tool_use Read
id: toolu_01ANo5h3NsdRizMYUPhjBLjd
```json
{
  "file_path": "/home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-26-44.png"
}
```

> TOOL

tool_result
id: toolu_01ANo5h3NsdRizMYUPhjBLjd
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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iIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERERERERKQGPIFA1KGug4iIiIiIiIiIiIiIyN+GUVwadA91JURERERERERERERERP4u1C2YiIiIiIiIiIiIiIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERERERERKQGFK6IiIiIiIiIiIiIiIjUgMIVERERERERERERERGRGlC4IiIiIiIiIiIiIiIiUgMKV0RERERERERERERERGpA4YqIiIiIiIiIiIiIiEgNKFwRERERERERERERERGpAYUrIiIiIiIiIiIiIiIiNaBwRUREREREREREREREpAYUroiIiIiIiIiIiIiIiNSAwhUREREREREREREREZEaULgiIiIiIiIiIiIiIiJSAwpXREREREREREREREREakDhioiIiIiIiIiIiIiISA0oXBEREREREREREREREakBhSsiIiIiIiIiIiIiIiI1oHBFRERERERERERERESkBhSuiIiIiIiIiIiIiIiI1IDCFRERERERERERERERkRpQuCIiIiIiIiIiIiIiIlIDCldERERERERERERERERqQOGKiIiIiIiIiIiIiIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERERERERKQGFK6IiIiIiIiIiIiIiIjUgMIVERERERERERERERGRGlC4IiIiIiIiIiIiIiIiUgMKV0RERERERERERERERGpA4YqIiIiIiIiIiIiIiEgNKFwRERERERERERERERGpAYUrIiIiIiIiIiIiIiIiNaBwRUREREREREREREREpAYUroiIiIiIiIiIiIiIiNSAwhUREREREREREREREZEaULgiIiIiIiIiIiIiIiJSAwpXREREREREREREREREakDhioiIiIiIiIiIiIiISA0oXBEREREREREREREREakBhSsiIiIiIiIiIiIiIiI1oHBFRERERERERERERESkBhSuiIiIiIiIiIiIiIiI1IDCFRERERERERERERERkRpQuCIiIiIiIiIiIiIiIlIDCldERERERERERERERERqQOGKiIiIiIiIiIiIiIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERE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IiIiBTC4QkREREREREREREREpAAGV4iIiIiIiIiIiIiIiBTA4AoREREREREREREREZECGFwhIiIiIiIiIiIiIiJSAIMrRERERERERERERERECmBwhYiIiIiIiIiIiIiISAEMrhARERERERERERERESmAwRUiIiIiIiIiIiIiIiIFMLhCRERERERERERERESkAAZXiIiIiIiIiIiIiIiIFMDgChERERERERERERERkQIYXCEiIiIiIiIiIiIiIlIAgytEREREREREREREREQKUPnSGSAiov8NSSmp8D19Gfcfh0JFVQXuLo7o1KYp1NVUy+0Y4ZHRWLxqC9YumVFuaUpKSknFb8s3oHeX1qhTs3qFHac4qWnpmDRnudRyZWVl/L3op2L3Pe9/Cyf8riIvLw9L506ESFRRufz6rdmyH0YG+ujp4y22PD0jE5PmLMMPw/vB2cFGWL5xxxHcuf8Yy3+dDA11NWH5rIWr0aJxXXg3rV/ksf4L5UrSqfPX8CD4GaaOHfils6KwgjriWM0Kk0Z/I7bu+LkruPcgBDMnDit1+orUI8l2afzMJfhucE9Ud7At9fGLsmrDblhVNUWX9s1lrve7HICAu48wffyQcj92RSvvOvLrsn8QHfMWACASiWBjaQavBrXRqF4tse3S0zNwwu8q7j4MQWJiCpzsrdGxdRNYW5iJbRcZFYOT56/haVgEjA31Ud/DFS0a1y0xH7sOncala3eklvfy6AM+XQAAIABJREFUaVVsmyGvH2Ysweghssvb56rjy9Zsh1VVU/Tq3KrEbb/mdoeIiIiISBKDK0REVGZp6RlYtHIzzE2N0K1jS7z/kIBrt4IQ+vwlfvp+MEQi4MjJi4h6HYuxQ3tXWD7K4xiVNDRgYWYMIwP9UqcRHBqOdf8exIp5k0udBgD07doGJsYGwmelEiIlKalpOHDcD22aN4S7qyMDK6Wkoa4GS3NTPAt/KRZcCYuIgkgkQtiLKLg4VQMAJCQm492HeDjZ28hO7CPJcvU56sP/B0+fR+J20GPUrVWj1GlI3gvWoy+jPNpeSY3r10Jd9xrIy83Dk2cvsOvQaaiqqKBebRcA+d9di1dtRV5eLhp4uMGgii6CHj3F739txYhvusHd1QkAEB7xCivW70TDerUwoEd7hEVE4eipS/gQl4AenbyLywIAwMbSTCogZmpkIHvj/5jv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egbU1dWEN5Xz8vLww8wlGD+in9CjgEqWmpYuNi/LSb+rePIsAhNH9f+CuaL/FaynREREREREReOwYERERPTZrVi/Cxt3HEFqWjrevovDjv0noaGuLva2OBXv4ZMwzFq4Go9CniMrOxt3H4Tg0vVAuDrbfems0f8I1lMiIiIiIqKisecKERERfXZR0bE4cuoiHj4JQ15eHqwsTDG4jw/MTY2+dNa+Grm5uTh3OQB+/gFISEyGupoaWnrVQ+e2zUo9GTVRYaynRERERERERWNwhYiIiIiIiIiIiIiISAEcFoyIiIiIiIiIiIiIiEgBDK4QEREREREREREREREpgMEVIiIiIiIiIiIiIiIiBTC4QkREREREREREREREpAAGV4iIiIiIiIiIiIiIiBTA4AoREREREREREREREZECGFwhIiIiIiIiIiIiIiJSAIMrRERERERERERERERECmBwhYiIiIiIiIiIiIiISAEMrhARERERERERERERESmAwRUiIiIiIiIiIiIiIiIFMLhCRERERERERERERESkAAZXiIiIiIiIiIiIiIiIFMDgChERERERERERERERkQIYXCEiIiIiIiIiIiIiIlIAgytEREREREREREREREQKYHCFiIiIiIiIiIiIiIhIAQyuEBERERERERERERERKYDBFSIiIiIiIiIiIiIiIgUwuEJERERERERERERERKQABleIiIiIiIiIiIiIiIgUwOAKERERERERERERERGRAhhcISIiIiIiIiIiIiIiUgCDK0RERERERERERERERApgcIWIiIiIiIiIiIiIiEgBDK4QEREREREREREREREpgMEVIiIiIiIiIiIiIiIiBTC4QkREREREREREREREpAAGV4iIiIiIiIiIiIiIiBTA4AoREREREREREREREZECGFwhIiIiIiIiIiIiIiJSAIMrRERERERERERERERECmBwhYiIiIiIiIiIiIiISAEMrhARERERERERERERESmAwRUiIiIiIiIiIiIiIiIFMLhCRERERERERERERESkAAZXiIiIiIiIiIiIiIiIFMDgChERERERERERERERkQIYXCEiIiIiIiIiIiIiIlIAgytEREREREREREREREQKYHCFiIiIiIiIiIiIiIhIAQyuEBERERERERERERERKYDBFSIiIiIiIiIiIiIiIgUwuEJERERE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VS0u604F+FWlUCEnKlc0BVTAlGOnVs0A1m7YTN1g8/N6N/V5/NEOAPw8ex5btoVS3NODMSPfZ9S4iQW2jxzSIR0lYRERERERERERy1hdSbyuNwoiIvJ/KzHJlEi9kFNmnpe9+w/xRr8PmPDZh1SvWum+lCUiIiIiIiIiIv9e6rkiIiL/1/oOGIaDvT2NGoRQqqQP+w8eYemKtXh7eVK1coX7VpaIiIiIiIiIiPx7qeeKiIj8Xztz9hw//fI7GzdtIzEpCVtbW0JqB9K3z8t4FHO/b2WJiIiIiIiIiMi/l4IrIiIiIiIiIiIiIiIiFrC+3xUQERERERERERERERH5L1FwRURERERERERERERExAIKroiIiIiIiIiIiIiIiFhAwRURERERERERERERERELKLgiIiIiIiIiIiIiIiJiAQVXRERERERERERERERELKDgioiIiIiIiIiIiIiIiAUUXBEREREREREREREREbGAgisiIiIiIiIiIiIiIiIWsL3fFRARkQfD2ZhYxo7/hphzsZyNiTVbFhhQncCA6jz/TJf7VDsREREREREREZGCo+CKiIgUiJ9++Y3wyL25LguP3GssU4BFRERERERERET+6xRcERGRArFs5ToAPh8zlMCA6jmW/fTLb/z0y2/UrFE9x3IREREREREREZH/EqsridfT73clRETkv69lh6cAWPXn7FyX/zjTFFzJr8CA6rz7dm+8vTwLpH4iIiIiIiIiIiIFRQntRUTkH/H8M1147uku+Q6WhEfutSgYIyIiIiIiIiIi8k9RzxURESkQt+u5YollK9cxdvw3ty3v6LEoer7+bq7LHB0dKOZeFB/v4jRuEEKLZg0p5OR013XLKnTXbgYM/siYHvPhQIJrBRboPuTeSEtP57f5f7J95y4OHz2BrY0NlSqUI6ROTTo91AobGxuLyuv8VA8SEq7kmG9ra0PRom4U9yhGcO2atG/TDI9i7gXVjH+lt98bQcTufQD4VavMV+NG3uca3VrX7r25cPESAK2aN2Zg/z73uUYiIiIiIiLyX6CcKyIi8q/TtlVTI7hyp65du86p02c5dfosO0IjmDp9Fu/360O9kFoFVEspCO8PHc32neEAlCtbmqmTxt7zfaampvLByHFs3RFmNn/rjjC27gjj2ImTvP16jwLZV0pKKrGxF4iNvcCefQf56ZffeOHZ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B5fVlcTr6bdfTUREREREREREREREREDDgomIiIiIiIiIiIiIiFhEwRURERERERERERERERELKLgiIiIiIiIiIiIiIiJiAQVXRERERERERERERERELKDgioiIiIiIiIiIiIiIiAUUXBEREREREREREREREbGAgisiIiIiIiIiIiIiIiIWUHBFRERERERERERERETEAgquiIiIiIiIiIiIiIiIWEDBFREREREREREREREREQsouCIiIiIiIiIiIiIiImIB2/tdARER+e9LTknlRnIK6enp97sqIiIiIiIiAFhZWWFvZ4udrc39roqIiDyAFFwREZG7diM5haIuhfRHi4iIiIiI/Gskp6RyKT5Rf6eIiMg9oWHBRETkrqWnp+sPFhERERER+Vexs7VR73oREblnFFwRERERERERERERERGxgIIrIiIiIiIiIiIiIiIiFlBwRURERERERERERERExAIKroiIiIiIiIiIiIiIiFhAwRURERERERERERERERELKLgiIiIiIiIiIiIiIiJiAQVXRERERERERERERERELKDgioiIiIiIiIiIiIiIiAUUXBEREREREREREREREbGAgisiIiIiIiIiIiIiIiIWUHBFRERERERERERERETEAgquiIiIiIiIiIiIiIiIWEDBFREREREREREREREREQsouCIiIiIiIiIiIiIiImIBBVdEREREREREREREREQsoOCKiIiIiIiIiIiIiIiIBRRcERERERERERERERERsYCCKyIiIiIiIiIiIiIiIhZQcEVERERERERERERERMQCCq6IiIiIiIiIiIiIiIhYQMEVERERERERERERERERCyi4IiIiIiIiIiIiIiIiYgEFV0RERERERERERERERCyg4IqIiIiIiIiIiIiIiIgFFFwRERERERERERERERGxgIIrIiIiIiIiIiIiIiIiFrC93xUQERERERERud/+XLebr2etJy4h6X5XReSB4ObsxGvdmtChqf/9roqIiMg9oZ4rIiIiIiIi8n9PgRWRghWXkMTXs9bf72qIiIjcMwquiIiIiIiIyP89BVZECp7uKxEReZApuCIiIiIiIiIiIiIiImIBBVdEREREREREREREREQsoOCKiIiIiIiIiIiIiIiIBRRcERERERERERERERERsYDt/a6AiIjIgyQ1NZWNm3dw7EQ016/foIZ/VeqHBN3vaomIiIiIiIiISAFScEVERB4IW7bv4q33RgJgY2PDT1PGUaF8GbN1Vq75myEffgbAc90e47Wez1q8n7i4eH6d9ycAftUq0qh+sLEs6do1Xu83nD37DhrzHuvU9p4HV8aOn8K8RcsAmPXDl5QrU+qOyklNTaVh6ycACKhehe8mjjZbvm1nOG+//xGpqak4OTky5YuPqVyp3N1V/j9g5Zq/OXIsCoDnnn4UJ0fH+1wjEREREREREbnfNCyYiIg8cFJTUxkx5ivS09MLvOxLly/zw4y5/DBjLpu2hJotW7F6oxFYsbe3I8CvKo0bhhR4He6H/QeP8N4HY0hNTcXO1pYvxnzwfxFYAVi9fpNxzq9fu3G/qyMiIiIiIiIi/wLquSIiIg+kg4ePMfv3xXTr0ukf2+eZs7HG509Gvkf9kFr/2L7vpbMxsbw5YARJ165jbW3Nx8P6ExhQ7X5XS0RERERERETkvlFwRUREHjjFPYtxLvYC30ydQfMm9fEu7nHbbS5eiuOXOX+waVso0afOUKpkCRrWq83TXR/GzdUFgM++msrcBX8Z28xbtIx5i5bRsllDVq3926y8t9//CIARg96ibasmPPXimxw/EU1RN1eWzPvBWC/rcGY9nn+SHs8/aTZ82YRPh3M1KYmffpnHsRMn8a9emYfaNKd966a3bE9aWhp9+g0jLHwPAIMH9KFT+5a3PQ4ZrKytALgcn8Dr/YcTn3AFgIH9etMkl944h44cZ8avCwiP2Mvl+AQqVihHu1ZNeLRTG6ytMzvKZhyHwIBqjP3wfSZ9+zPr/96Gs3NhQmoH8lL3rhRzdwNge2gEb/QfnmcdCxcqxKrFM4zp5ORkfv9jGctXrefw0RO4ujhToXwZ3ur9ImXL+OaoQ0kfL74cO5RPxk9h7/7DFC3qSg2/KvR66Wm8inuQkHCF1o88Z7bPdo+9gLW1NZtW/pbvYykiIiIiIiIiDx4FV0RE5IHTqX1LFixezoWLcYz6dBJffTrslusfPHSM1/sPMwIIAEeOneDIsRP8tXwNE8eNMHs5/09avX4T8xctN6a374xg+84IrK2taduycZ7bjRr3tRFYeeHZLhYFVgBsrK1JTk7m/WFjiT51BoA3Xn0+13L+XLaGjz+dRFpamjEvcs9+IvfsZ+nK9Uz6bAT29nZm2yQnp/DGgOEcPHQMgLjL8ZyMPsOOsEj+x959x9d0/3Ecf2fvJYQQK7bYe9RWVKlVLTVardWBlq5flerQoWaLqtmBKoLae1N7bxISQkIikURk398f4coVkVyjaeP1fDzycO453/M9n/M95wbnc77f79wZ42VlZZVljDa2d/8ZczMuTm++O0xnzp03rrsWfl3Xwq+rx8FjGvvNUNWsVslk/4TERA366EuFXA411nEp5Ir27D+iP2aOz/L4AAAAAADg6cWcKwCAXCcxMUk9u3aUlDYJ+5oN2zItm2ow6JMvRis6JlaWFhYa9OZrWr5ght7u21MWFhYKj4jUJ59/L0kaMrC3/pg1wbhvx7YttWvjIo0cPkS7Ni4yHlOSpv34tXZtXKSWzRs+0rls/3ufJo39Qmv/+k0vtn/OuH7hklV3C1lY3F2Uhf5YsFTLV2+UJLV6tpH6v/6K2ce1srLSsK/GGRM0LZs1ULeX2mUoF3zpsr4ZM1mpqalyd3fVNyM+0OK5U4yJn6PHT2nCT7My7Hfq9DlV9iunVYtmacqEr4y9VYKCQ7Tv4FFJUtlSvvpx9AiTn/TDkb339hvG5TE/TNeZc+dlb2en0SM/0cblc/Trz6NVulRxJSUl6atRE5WUnGwSQ3hEpBzs7TRlwlf67ecxqlSh7O311zX9t/lycXHWro2L1LRRXeM+qxf9Qq8VAAAAAABAcgUAkPskJCaq4wstVdjHW5I0ftJMRcfEps9BGO3ee8jYM6N925bq2vkF5fX0UI8u7dW6ZWNJUuCFizpy7NQ/Fb6JNq2aqXqVCnJ1cdZ7b78uD3e3tJjOB98tZDAYF//ee1A/TPlVklSremUN/2iAcVtUVLSuXovI8HMzLi7DcU+fO6/N23YZP2/duVdXQq9mKLds1QYlJ6dIkj4Y2EdNGtaVdwEvffa/Qcb2X7l2c4bEhpW1tQb0f1Ue7m6qUrG8Xn2lk3FbQGDaubm4OKtmtUrGn9Cwazp89KQk6eVObYwJnJtxcVq3cbskqWmjunqmbg05OjqoTClfdX3xBUlS2NVwHTh0LEP8X4/4QFUqllfpUsX17ecfGocw27J9d4ayAAAAAAAAd5BcAQDkOslJybKxsdHIYe/L0sJCkVE3NH7STNnZ2WYoey7ggnG5ehU/k23Vq1Q0Lp8+F/jE4n2QOz06pLTeJD4FC0iSEpOS7lt+wuRZMhgMsrCw0Dt9e5rMdzJ85Di98HKfDD8LFq/KUE/M7SHS6tSqKkm6dStew74aq9R0iRwpba6VO6pXvdtelpaWqlyhnHHfi5eumOzn7ORoMlRYkcKFjMuJiYkZ4jl1JkDfjZsiSapcsZwGvfmacVtQcIgxebNy7WbVadrR+PP5N3d7Gl2+Ypocypc3j4r4FDR+zuPhLt9ihSVJV69FyHDPuQIAAAAAANxBcgUAkGuVLlVc3bq0l5T20D00LDxDmZR084Tct2vLbXd6Zzwqg0wf2D+pB/gGg0HfjJ2slJSHj/utPt01/tthqlW9siTp2IkzmjZrnkmZ1JS77WfxwPZLznRbViKjbmjIJyOVnJyivJ4eGvXlxyZJo9TUu23oXcBLVSqWv++Pi7OTSb0PileGe68UAAAAAADAXUxoDwDI1fq+1kVbtu1W8KXLmj1vcYbt3gW8jMsHDh1Ts0b1jJ/3HzpqXL7TY+Rh3emlEX0jRjExsXJxcZYknb9w8ZHqvdf7A/to87Zd2nfwqE6eDtDPM//QW326S5J++P6zbNdTtnQJ4xwyn/1vkLr2GqjomFj9Mmeh6tSsYpz7JH377Tt41Nh+qampOnwsbQgvCwsLFfTO/1Dnk5ycosH/+0oR16NkbW2l77/6RG6uLiZl0sdQs1olffL+W9mq++q1CF0KuSKfQmnDl12PjFLg7evhlc9Tlg9KvgAAAAAAgKcaPVcAALmajY2NPv3wHUlS6NWMPVca1K0hB3s7SdLipWs0f/FKRUVF64+Fy7RyzWZJkquLs+rWqiZJcnJ0NO4bciVM0TGxCo+4nmUcxQr7SJJSDQaNHD1Zew8c0dKV6zXz9/mPdH6STHrc1KhaUSM+edeYgPh93mIdPXHa7CptrO++f+GZx11DP3hbUlqPmGFfjTXO09KqeUNjue8nTNX2v/cq9Gq4Pv/2B+NQYHVqVpWzk6Mexnfjpujk6QBJUsvmDRV786b2Hjhi/ElKSpJnHndVq1JBkrR2wzZt3r5bBoNBScnJ+vTLMXr2hR7q0mugoqKiM9T/4fDvdOTYKZ0LDNLHn41S6u2eTI0a1DGWcXRwMC6HXAlVQPr5bgAAAAAAwFOJ5AoAINerVKGsOrVrdd9tjo4O+njIW7KwsFCqwaCxP05Xq46vGecusbSw0CfvvyVraytJaT0aCnjllSTt3ndILdr11J+LVmQZQ+cOzxmXN2/bpQHvj9DXoyer1bONHv0E0w0tZpBBeT099PnQ925vMmjo56PvO2m9ORo9U1utWzaRlNbj44tvf5QkVa3spw5tW0iSoqKi9f7Qb9S+S1+tWb9VkuTm6qL3B/V5qGNu3r5by1ZtMH5esXqTBrw/wuTneuQNSdJH7/WTk6Oj4hMS9PHw71S3WSc1aPGS1m/aoZjYm6pRtaLc3V1N6ndxdlJiYpL6DvxE3Xu/pyPHTkmSPNzd1Kv7i8Zyd3rpSNIbb3+s7r3fU0JCxnlhAAAAAADA04PkCgDgqTCw/2vK65nnvttaNmugH0Z9pvJlS5msr1i+jCaN+1KN0/VikKQfR3+uJg3ryvX20F4xMTezPH5Fv7KaMGq46tWuJmcnf/AZmwAAIABJREFUR5UoXlQfD+6vHl06POQZPVidmlXUuX1rSabJkEfxwcA+8srnKUnasn23lq5cL0n66L3+Gjygt/LfTjpJkpWVlZo1qqffp41VoYccEiw8POseQXcULVxIv00drcYN6pjMx1LYx1sfD+6v9wdmTPBYW1trwqjhqlqpvHFdlYrlNXPyd3J3u5uIaftcMw1+5w2VLllcVlZWsrezVWjYtYc6JwAAAAAAkDtYxMYlMF8rAOCRxMbFK7+na9YFgX+BLr0G6kLQJXm4u2nVolk5HQ4A4F+ifrcxOR3CP67/yw3U44Vaxs8Jick6fT5Mq7ad0NJNR4zrN//6rmxu9+JNNRh0KTRSe48Fa/ayPboaEWMsN3n4y6pcxifDcQIvhavHR78+wTPBv9mOOUNy9PhhEdFydrTP0RgAALkTE9oDAAAAAPAU23X4goIuR8jDzVG1KxbTR72fVarBoOWbjxrLJCYl61xwuKysLFTA01Wdnq2iJrVK671vF+pcsGmPzqWbjuhWfJLxc0RU1r18AQAA/mtIrgAAAAAA8BTbtv+clmw4LEl6ploJfTekvZ5v5GeSXImIuqk+w+cYP7d6pryGvfmc/tenpd4YNtukvtnL9iokLOqfCR4AACCHMOcKAAAAAACQJP19+LySU1JVyMv9geVWbz+h/ceDVdY3v8oUe7j51QAAAP7L6LkCAACeKvNm/ZDTIQAA8K/l6mQvaytLxcUnZln2RECoqvsVUYkieXX6Qtg/EB0AAMC/B8kVAAAAAAAgBzsb9X6xviTpyOmQLMvfvJUgSXJxMp0sfP7YN0w+fz9zvXHYMQAAgNyC5AoAAAAAAE+xD15vrg9eb278HHzluqYu2JHlfk4OdpKkyOg4k/X3TmgfcNF0wnsAAIDcgOQKAAAAAAD/cj753VWlnI+Wbz722OvedfiCgi5HKC4+SUfPhGjf8WClpKRmuV/5EgUkSScDQk3WM6E9AAB4GpBcAQAAAADgX673i/X1bL2yCrp8XUfPXH6sdW/bf87sYbtaPVNe1f2K6FRgmC6GRj7WeAAAAP4LSK4AAAAAAIAH8nR30rQvukmSHO1tVaxQHkVGx+mbaWtyODIAAICcQXIFAAAAAAA8kK2NtcqXKKDUVIMuhkZqwZoDmrNsr65FxuZ0aAAAADmC5AoAAAAAAE+hKX9u05Q/t2VZrvGr47NV31tf/PmoIQEAAPxnWOZ0AAAAAAAAAAAAAP8lJFcAAAAAAAAAAADMQHIFAAAAAIB/Ee98rhrar5VaN/R7YLmh/VrpjU71/qGoAAAAkB7JFQBArrDn4Am9MXikybqkpGR9+u3P+vTbn5WYmJRDkT1e46bO09xFa7JVdtnabfpy7MwnHNE/a83mXXrr4+/15kejZDAYJElfjZulxau2KD4+QYM+Hav9R0498nHMaWdz/frnCvV4Z4ROnQvKsK3XoC8fKX6DwaCff1+s3oNHavzUeY8SptEbg0fq+OnA+277p+4x/xWb9Om3P2erbE7e9waDQWu37Nan307R6+99pU+++UnL123PkVhWb/xbw0dNlSQFXLikHu+MyJE4HsWSVVvU450R2nf4ZIZtoybN1oJlGzLdd9nabfpy3N374LcFKzVhWtpcEJ+PmaG/1mw1K5ZTZy/ofyMnq8c7I3QxJMysfZ+U/h9+p4PHzuR0GHhCCuR1U9VyhR+YYJn46Utq3dBPzzV4cAIGAAAATwbJFQBArjVx1kJFx8RqyJuvyNbWJqfDyVKPd0bofPDlnA4jx3w5dqZWrN+R6fbYm3H6Y/FaNa1fXR++3V0WFhaSJN+iBeXt5Sk7O1sV9SmgfJ7u/1TIj+TXP1coNTX1keq49545cPS09h06qVdfel6vdGzxqCH+I7Jz33t7eapUcZ9/KKKH98P0+VqyaovKlS6u/j07qJiPt+YvXa95S9bldGj/SfsOn5SPt5f2HDzxyHUVKpBPRX0KSJJKFC0kb6+8Zu0/23+1Cnh56oO3usunoNcjxwNk5eDJi1q17biuXIu+b4Jl4qcvqWq5wrpyLVovvjsth6IEAAB4ulnndAAAADwJf/61XsdOBWj44Nfl4eaS0+HgMbgRHauUlFS90LKBSbLslY4tjcuD+7+SE6GZrVypYjodEKS1W/aoVZM6j63eiMgb8s6fVw3qVHlsdf4b1KtZSfVqVsrpMB5ox94jOnTsjEYNf0f5PD0kSbWq+sm3aCHN9l+lVk3qyJ3fRdkWHhGli5fDNLjfK5o4c4GSU1JkbWX10PU1a1DTuNz9xVZm7389Kkadnm+iSuVLPnQMgLlm+O+UJD3XwE9D+7XS8XNXJEmDX22m0sW8SKwAAADkMJIrAIBcw+L2nzv3HtGK9ds1sPfLKurjbdweH58g/xWbdPDYGSUkJKlS+ZLq3Lap8YHnqEmz5VukoGLjbmn3geNydLDTKx1bqnqlspKk4aOmZnjDvniRgvriw76SpINHT2v1pl0KDApRoQL51KJJHdWrUVFS2hA1J88GqUSxQtqwba+cnRxVs0o5dWjdWNcjozVkxATjMfzK+OrjAT2VmpqqZeu2a9e+Y7oRE6t6NSpJt4fCuuPw8bNatfFvBQaFyKeglxrXq6aGdaret3227Tqk3/1XacT7fVQwf169MXikBvfrKr8yvpKkM4HBGjl+ln794TNJacNB9XjxOW35+6CuhIWrRaNaqlaprOb4r1Zg8GUV9vZSv54d5J0/7Q3wuFvx8l++SYeOn9Gt+ARVrVBGL7ZtakxuvTF4pF7v2lb7Dp3UsVMB8s6fV2/3elH58+XRu8PGKSLyhs4EBmvhso2aNWGYSew//eKvnfuOGusp7VtEwwa/rlGTZqt4EW91btvMWLbXoC/10Ts9VLZUMY2aNFs+3vl09vwlBQZd0uRvP5STo4NJ3dlp5+xc2wplfbVx+z7dik9Q02dqqNPzTe57HSTJ2clRDWpX1cJlG1SvRkW5ujjdt1xm1/dqeGSGeyb0aoQiIm9ISusN8kLLBurctlm2rnNm1+Vet+ITNGL0NBUrXFBvvtrRuN5/xaYM9/WdB+GXQ69p0crNOnYqUK4ujqpTvaLatWygiEzu+/tds43b9+nQsbMaNvj1B9Zple7h+4NiehK27Tqk2tX8jImVO5o8U137Dp9U0KVQubu5ZOv8JOnbH39Tad/C6vh8k2zdY3sOntDazbsVHBKqMiWKqngRb2UmOCRUi1Zs1vHTgUpOTlHLJnX0crvmxt5gQZeuyH/FZp06e0EFvDzV5tln9OOM+ZoxbqhsbWwe6bueXX/vP6rSJYqqYrkSsrS01OHjZ42/i+9ITEzSjzMW6MiJs/Ip6KUm9atn+vtv36GTWrlxpwKDQuTk6KBXOrZU/dsJu2Vrt2Xa/h7urpr5xzJJ0tif/5Ak/T5xRJZtkF7AhUsaMXq6fp84wrhuyaotOn7mvIYOek0BFy7p6x9+1cA3XtKS1Vt16XKYKpQtoTdf6yhbm7REcmzcLS1YukH7j5ySna2NOj7g9wv+u7zzuerKtWiTdekTLH4l077XD0qs3K8OAAAAPBkMCwYAyDUsLCwUei1CM/5Yps5tm6tG5XIm22fOW66jpwLVtkUDvdKxhcKuXde4e+al2Lhjn6pXKqtRw95WFb/SmvLrIiWnpEiSXnv5eX08oKc+HtBTg/q8LFsba9W9/YD94uUwjZv6hwoXzK/+r3ZUxfIlNe33JSZzVZwNDFbAhRANH/yGXm7XXBu379fS1VvlldfD+NDtiw/76uMBPSVJa7fs0fK129WgThX16tJGVyMidexUgLG+K2HhGjNlror6FFC/nh1UuXwpzfpjuQ6fOJuhbQ4eO6PfFqzUh2/1UMH82R8O5+99R/XWax3Vp3s7rdiwU5NmLtDL7Zrriw/6KDklRUvXbjOWnT5nqY6eCtALLRvqlQ4tdeVquCbOXGBS37ote9SxdWN98WFf2dnZGh9ajv/yPZX2LaIu7Z/NkFiRpDdf66Rvh74lSZoxbqjJQ9CsbN9zRM83r6cP3+4he3u7DNuzaufsXNuTZ8/L2tpKIz7oo5fbNdfSNVt1JiA405gSk5LUqkkdJaek6I8la+9b5kHX9373zPgv31OPzs+peJGC+n3iCJOEU1Yyuy7pJaekaNSk31XAK6/69+xgXH/h4mWdDbyoXl3aqFmDGsb7+s4+3078XfEJiXrjlbZq1qCmNu88oMUrt2R630sPvmYPqjM7MT0pV8OvGxNY6VlZWurjAT1V2a+UcV1W9+T9POgeCw4J1Y8z5qtEsULq17ODChbIm+kQe0lJyRo1cbacHB30bt8uGtj7JW3bfUi79h+TlNa+30+eI0nq27296taoqPlL15vU8Sjf9ezad/iUKpZNS6xU9iul3QeOZyizcfs+OTs5qP+rHVWhbAlNn/OXTp29kKFc0KVQ/ThzvmpVKa8P3uquTs830bTflygyKusH0E3qV9fvE0fIxdlJg/u/Yrxns9MG5khMTNL+I6f0bp+X9W7fLgoMCtGKdXev4fTZf+l0QLBeeqGZOjzXWKs27FR8fMJDHw//TgvH99HQfhl7Vs3w36lV247rVkLa/HERUTcz7bGSWR0AAAB4/Oi5AgDIVab8ulhWlpY6cPS02rZ4xrg+Nu6W9hw4rs8/7Gscd79S+ZIaMHSMLly8omKF094GrV6prCqWKyFJerldc63dslsXQ8JUvEhB+RYtZKxv3NR5Kla4oJ5rWleStHH7fjWuV9043Ez1SmV1PTJa2/ccNj5wTTUY9M7rL8rRwV4FvDwVdyte8//akOkbyFt2HlCH1o3Vulk9SVIVv9IaNGyscfv6bXtVtUJpde3QwnjMuFvx2rB1ryqXLyXJQrKQzp2/qEkzF+i9fl1V0sx5K5o8U135PD2Uz9NDFcuWkIODnUoWLyxJat6wllZu2Gls34NHT2vsF+8a39wuX6a4Bn06VhGRN+Tp4SZJatG4tgoXyi9Jat2snibPWmhWPA+jRuWyGRJt6WXVztm5tnnzuKtFo9qSpIZ1qmr91r06e/6iSpcokvGAFhZKTk6RT0EvvdCyoRav3Kxmz9TMcG2yvr6Pz4Oui4XSJmofP3WeLC0tNbD3S8YeDnfOZ2Dvl+ToYC9JcnSwN97XB4+elqO9nQb36ypLy7R3epwdHeS/YpNebNs003gedM2yVecDYnpS4hMS5ehon62yWd2T9/Oge2zT9v2qWrGMyb1yJSxcUdGxGeqxsbHWyP/1l6uLk/E6+pXxVcCFENWtUVEHjpxWamqqBvV+ydgTyMLCQnP8V0v6Z77rkTdiFBgUor7d2xnba9rsvzIMDVbEx1u9urQxnnPE9RvauGO/ypYqZlJfUZ8C+uGrIXJzdTae75LVWxUYfFnV3V2zHdcd2W0Dc3V6voncXJ3l5uqs2tX8FBAUIkmKiY3TgaOn9eVHfY29MX0KemnYdz8/1HHw7+Sdz9Xkz3vN8N+pAnldVatiUXX9YNZD1QEAAIDHi+QKACDXiE9IVN48bnq9axsNHzVVG7btNY6zfz4oRDY21sbEiiQ5OTqoUIF8CrhwyZhcST88k62tjaytrJSQkGhynE079uvU2QvGnhSSdOHiFZ07f1Gbduw3KVu2ZFHjcuGC+Y0PeyWpXMliioqOUUzsTbk4mw4LlZKSopDQqyqX7iGhjY21fIvcTfAEBoVkeEBbpmRR7dx79PYng8IjojRq0mzVrVHxvm/VZ8XFydHk+Onjt7ezVXJysiTpfNBlJaekaODQMRnquBoeaXzY6JaufZ0c7ZWYlGR2TOZycXbMdFt22jk719b1nuvn6GCf4b4xSjfkWLuWDbR99yH98ucKfflRX5NiWV/fx+dB18UgaY7/GoWEXtOEL9+TlaVpx+cH3dfngy8rJPSaXh34hck+lpYWMhgMpkmadB50zbKqM6uY0n/Xjp8O1Lc//pbpsTLz5qsdM8wB4+hgr7hb8ZnW3aJxbfV48bkszy8zD7rHLly6kuFeKV2iSKYTwVtZW2nxqi06fS5It+ITdD74sprUry4prX19ixYyGWKtXKm79/o/8V3/e99R5c+XR4W80yaOr+JXWimpqTpy4pyqVSxjLFfmnuRlmZJFM+2xc/NWvJas3qrgkFDdiI5VZFS0kpKSsx1TetltA3PdSf5It69vYlqbXbh4WXa2NibDXBYr7C27dHNP4ekw8ufVOR0CAAAA0iG5AgDINTw93PTmqx1lZWWl1s3q6c+l61WtUll5uLko9Z45NNJLSU3N9jGuhl/XbP/VevPVjvJI98azwWBQ8wY1VaOK6QPO9A94M3mOrOSUjMc3KO0Z/L0Pnw26ex732y6Zns/1qGjVqFJO23cfVpP61U163zxOqYZUOdjbaVCflzNsu/P2+r9R9to562v7sKysrNSzc2uNmTJXuw8cl6XV3cRFdq7vP8XC0kL5PN31y58r9F6/rqbbHnBfp6YaVNq3iDo+3/ixxZKdOrP7XStZ3Edf/+9Ns2PwzJPx4bmPt5eOnQxQg9pVJKU9/L4z1Nmv81fK6THcL5m57z2cya+8sGvX9fmY6SpXqriqVSojH28vrd+6N91+Blk+oK5/4ru+99AJhV27rh7vjDBZv/vAcZPkyv2+H6n3+X7sOXhCU35bpCb1qqtJveryzOOmqbOXPHR8//Tvuwf9/QUAAAAg5zDnCgAg14i5GWd827pTm6ZycXLUb/NXSkp7kz0hMVHBIaHG8jfjbikk9JqK+WQ+8XN6KampGj/tT9WolHFIHx9vLyUkJcmvjK/xR5LypEvAXLp81eTN9pPnLsjB3k7u6d5WvsPaykoe7q4m8wckJSUrMOhyumPm0+l75vU4fS5IhQt6GT+XLF5Yg3q/rGqVyurHGQt0K90Y/Xa2toqOuWn8HHUjJlvtcD8+3l6KT0hQAS9P4/n7Fi2kpKRkOd8zgfzjZG9nq5jYOOPn2LhbxjlysiN77Zz1tX0UVSqUVhW/0prtv9pkyKPsXN/seBzXuWv7FhrU52UdOXFOqzftMtn2oPu6SKH8ioqOUfnSxY1t5+riJFdnp0x7rWQlO3Vm97tmZ2urwoXym/1zv8RarWp++nv/MeM8KE6ODvIr46u8edx1Nfy6ihUpmOk52dnZKjr2psm6+w3plRmvvB4Z7pVT5y7ct+yJM+fl6GCvAW90VsvGdeRXxtfYQ0KS8ufLo4CgEJNeHSfOnDcuP+nveuSNGJ07f0m9urQxznH18YCe6tC6sQ4eO22SPLl3XqPT54JUwMszQ537D59UvRqV1KPzc3qmdmWVLlFEsel+b5jb/ua2gb2drSSZfg/NuL4F8+dVfILp318BQSEm1w1Iz5wJ7T/p21I75gxRlbLmDRv6X/a/2+dcq2Kxh66jXlVf7ZgzRB/1fvbxBQYAAP5z6LkCAMiVrCwt1b9nR305boYOHz+ryn6l1KpJXU35dbFeeqGZrKwstXzdDlUoW+L+82Lcx7zFa3UlNFwdWzc2TmZuZWWlsiWLqkPrRhr6zRTNX7pezzaspTOBFzVt9hL16NxajepWlZT2AG/izIV6rmldxd2K1x+L1+mZ2pWND4Qd7O10JSxczk4OyufpoWdqVdailZvl6uIkN1dnrduyR44Odye/7tC6sf739WQtWbVFpXwLK/RqhNZv26tPBr1mLHPnDfS+Pdrpk69/0k+/LtLg2z0Pihfx1sLlG+XoaK+bcfHasvPAQ7e3p4ebWjSqo3E/z1PnF5rKx9tLv8xbocth11SxXAmTIYYy4+hgrythEboWEal8nh7ZOm7xIgW1eNVmlSlRRM5Ojtq+57BsbMz7503W7Zz1tX1UPTo/p4++nGiSGMrO9b33nrmfx3GdLS0tVKRQAXXr1Epz/FerTIkiKn47WeDk6JDpfV2negWt3rRLP85YoA6tGykxKVlTfvFXiWI+6v9qx2yfQ3rZqfNBMT0p9WpU1P7DJzVmylw1rFtVfqWL62bcLf3513oV8/E2mdD+XiWL+ej3Bau0cNlGlStdTMdOBZqVBGtUt6q+/fE3/bV6q0oW99GZgGCFXo2Q030e9Ht6uCk8Iko79hxWudLFtWXnAZ0NDFbePBUlSbWqlteCZRs0+Rd/devYUoHBIca5le7s/6jf9QfZc/C43Fyc1aR+dZPr5Vu0kJat2abDJ86paoXSkqTIG9Gat2SdKpYroYshYdq+55AG9s7Ym8TD3VU79x3VufOXZGtrrZUb/jbpAWZu+5vbBgW8POXoYK/pc/5SyyZ1dCUsXEdPnlOebA4fls/TQ6V8Cxv//jJIWrFuhxzs7bLcF/8dV65F6+DJiyqQ101D+7VSaHj2EyR3VC2XliA5ePLi4w4vRzk52Grt9AE6ERCqPsPn5HQ4AAAARiRXAAC5VinfwmrWoJZmzF2q0Z8NVNcOLTRj7lKNmTJXklSxXEm99VqnbNe3Y+9RJaekaMK0P43rnBwdNGXUR/L0cNPg/l01eZa/lq3dLgd7Oz3XrJ7Jw/f8efOotG9hjZ0yV3k8XNWkfjWTCbY7tWmiKb8tUpFCBfTVx/31YpsmsrG20pLVW3X12nW1bFLHZIx9Tw83vf9mN/0wbb78V2ySg72d+vXooBL3GfrLztZW7/btouGjpmrtlt1q0ai2Xn3peX0/6XeN/3me/Mr6qukzNTJ92z07XunYQjP/WKbRk9MefJTyLazB/bpm+2Frmxb1NWbKXG3bfVA/ffdRtobdatWkjs4EBGvKb4tVopiP2rVqqKMnA8yKOzvtnNW1fVReeT3Uunk9LV2zzeS4WV3fe++Z+3mc17l5w5o6fiZQE6b9qe+GvS1JKlggX6b3taWlpYb0f0UTpv+pT77+SVaWlqpZtbx6dW1j1jmkl506HxTTk/TO6521Yds+bfn7gDZu36cihfKrcf3qer55vQxz1aTnW7SQOjzXSEvXbtPf+4+qSf3qKpNuTp+s+JXx1duvv6g1m3bJf8Um+ZXx1bMNa2nnvozz81QqX1LPNqql6XOXypBqUPOGtVSzSnnjdidHB308oKcWLt+kj76aKA93V3Xr2FKTf/E3lnnU7/pPv/gr7laChrz5SoZtew+eVJUKpTIkwhzs7VSudDHtPnDcmFx5pnYVXbwcppUTd6h4kULq0719hl6FkvRCywa6dPmqPh8zXU6ODureqZXOnb/78Plh2t+cNrCyslL/nh005bfFOh0QrFpVy6tB7So6nq5HUFbe69tV85as09TZS5SSkqpeXdto3uJ12d4f/w0rtx7X0H6t5J3P76HruJOkAQAAwJNnERuXwCC+AIBHEhsXr/yej2eIpNxq2dptOnTsrIYNfj2nQwGAB4q7FW+S3Dx3/qK+Gj9Ls8YPeyy9f4aPmqra1fz0fPP6j1wX8DjV7zYmp0OQdz5XVS1X+KH2PXjyollDgklpw4I936iCvp+5Xo1qllSl0oUUGh6tMb9s0IETd5M0z9Yrq7aNK6p8CW9FxdzSzoMBmjB7s1JSUuXp7qSlk/pr95ELSk5OUa2KxfTVz6t18ORFLZ3UX4dPX9JbX6S9mFK+RAFN+6KbNu85q6ETlqp1Qz8N7ddK0xfuUOECeVSnSjElJCbrjxX7NH/1ARUtmEdzv+9lEvMHoxdr58FAlSmWX6+2r60qZX1kMEjHzl3WmF826GpEWs+zud/3kqe7kxasOaiXWlXT2h0nNXrWev2vb0u1aVRB733rrz1HL8jV2V7v92quSmUKycnBVgdPXtK2/ee0bNPdBHUNvyLq0a62yvkW0IWQCG3YdVoDuzfW0k1H9N30tERnduJxcrDVpD+26uVW1VXcx1MnAkL12cTliogyHZowt9kxZ0iOHj8sIlrOjk9u7jMAwNOLnisAAAAAJEkxsXEa/Nl4tX+ukVo1rauAC5f051/rVal8xt4kDyv0aoSqPGCYNOBpduVatK5cO/6PH3dg98bacSBAoeHRKlbIU0P7tVKnQdMkSVXK+mjE28/rWmSsNu4+rcIFPNSpRVXZ2Vrrm2lrjXVULeejsPAYLd18VOGR2Z9XSJI6t6ymc8HXdCowTLUrFdOA7o2152iQbsTc0sK1B/Vii6oKj4zVhl2ndfnqDTk52Grcx51ka2OtHQcDZGdrrbpVfDX6/Q7q89lcJSSmzRvlaG+rF5pU1Ja9Z3X83JX7HvurgW1V3a+I1u44qcjoOLWsX161KxXTniNBCouIVqH87hr1fgdZWVlq696zsrS0VI8XapnUke14HGz1ZpcG2n88WPnzuqhqOR8N7N5Yn01cYVZ7AQCAfweSKwAAAAAkSS7OjurXs4OWrNqqeUvWydLSQtUqlVWfbu0eS/03427J0cFehby9Hkt9AB6Pucv3arp/2vxK80a/rsLeHsrn4axrkbHq9GwVpRoMGvT1AgVdvi5JGvNhJ7VuVEE//Xl3OMvEpBS9MWy2bt5KlCR5ujtl+/j7T1zUsB+WSbrbm6ZCSW8t33JMU+dv14stqurq9Vj9MHuzJKlTi6pyc3HQ6FnrtXj9YUnSa+3rqE/n+mpUs5TW7jgpKW3OsC+nrNLeo0GZHvvn+dtVonA+Ld10RJKUlJyi7m1rqVr5wlq17biea+AnO1trLVhzQON/2yRJGtCtsbq0rm6so1UDv2zF42hvqz7D5+pCSITye7pq4YTeKlMsf7bbCQAA/LuQXAEA4B/QtkUDtW3RIKfDAIAs1ahc7r5zlzwOTo4OGv/le0+kbgAP71i6Xh0XQyNV2NtDLk72uhYZq1LFvGRpYZFheC5JKlIgj0KuRkmSAi+GGxMr5goJizIuXwpNW3ZysMu0fDnfApKk93s11/u9mptsK+TlZlxOSUl9YGJFki6ERKhWpWL64ZPOcnKwU6mi+SRJdrZpj0t88rtLknYcCDTus+94kElyJbvxJCWn6EJIhKS0oapibsbLwd5GAADgv4nkCgAAAAAATzGD4e5UrPdOymplaant9uaqAAAgAElEQVSYm/H6euqaDPsFh16XlaXl7f2yMZ1rNoYXzE49VpZp9Yz9ZYOu3TMEWfCV68blVMOD63JzdtCMr7rLO5+rtu0/p7NB1xR0+bpaPpMxwWx4QF3ZjSdjpQ8MDwAA/MtZ5nQAAAAAAADg3ykkLEouTva6ci1aW/ed09Z95+Th6qg8bo6KjonPdL+YmwlKNRjklcdVlreTKrUrFjX7+KmpGTMQF0MjJUnWVlbGmBKTUuSdz00347Lfe6Z0MS9553PV4vWH9fHYv/TjnM1KSkkxKXP56g1JUoMaJY3rGqZbfpzxAACA/xZ6rgAAAAAAgPtavP6walYsqrEfddKm3afl7Givls+U04ETF7Vkw5FM90tMSlZA8DWVKuql3797TYdPX1K9qr5mH/9WQpJuxNxS8UKeeu/Vplq45qBWbTuuLq1r6M0uDVSyaD7FxSeqTaMKSkxK0cqtx7Nd99XrMZKkWhWLqlOLqnJysNWzdcualFm17bi6Pl9dHZpVlr2ttWRhoerli2Qo8zjiAQAA/y30XAEAAAAAAPe1Zd9ZDfthmQKCr6lVAz81r1tGe45e0LfT12a576iZ6xUaHq1ihfKoflVfjf1lw0PFMMN/p2xtrPRii6oqX9JbV65F652v/tS2/edU3a+wXmxRVRdDI/XFTysVczPz3jT3Crp8XT/P3y5XZ3sNfrWpGtUoJf+1B03KXAyN1IdjlujQqUtqWb+8yhbPr+kLd5iUeVzxAACA/xaL2LgERvkEADyS2Lh45fd0zekwAAAAHlr9bmNyOgQgV9oxZ0iOHj8sIlrOjvY5GgMAIHei5woAAAAAAAAAAIAZSK4AAAAAAAAAAACYgQntAQC5yvHTgVq2drvOnr+ofHncVb9WJbVuVk9WVlY5FtPhE2c1bfZfGjGkt/J6uj/WukeOn6Vihb3VrVOrx1ovAAAAAAAAMkfPFQBArrFh2159P2m23Fyd1adbO1WvXFYbtu3TyAm/KDklJcfiyuvhJh9vL7m6Oj1yXV+OnakV6+9OoupbtJAKFsj3yPUCAAAAAAAg++i5AgDIFSIib2i2/2r17dlB9WpUlCTVqV5Bzzevrw+++FEr1u1Qu1YNcyS2Qt5e+nhAzydSd9cOLZ5IvQAAAAAAAMgcyRUAQK6wc+9Rubu6qG71CibrHR3s1fSZGtq++5AxufLG4JHq3KapNmzfJ2srK30z9C0FXboi/xWbdersBRXw8lSbZ5/RjzPma8a4obK1sVFwSKgWrdis46cDlZycopZN6ujlds1lYWGhgAuX9PUPv2rgGy9pyeqtunQ5TBXKltCbr3WUrY2NAi5c0ojR0/X7xBGSpKMnz8l/+SZdvBymPB5uat2snprUry5JiomN08LlG3Xw2BlFRkWreqWyeuOVtnJxdtK7w8YpIvKGzgQGa+GyjZo1YZhGTZqt4kW81bltM0lS6LUI+S/fpOOnA+Xq4qyaVcqpfauGsrKyyjJOAAAAAAAAZA/DggEAcoUrV8NVtlRRWVhYZNjmV8ZXVyMiZTAYjOt2HzyhV19qrd7dXlBySoq+nzxHktS3e3vVrVFR85euN5ZNSkrWqImz5eTooHf7dtHA3i9p2+5D2rX/mLFMYmKS9h85pXf7vKx3+3ZRYFCIVqy7O3zXHQaDQZNm+csrXx599+k7atW0rub4r1bYteuSpBlzl+rCxSvq062dPh7QU9GxN7Vg2UZJ0vgv31Np3yLq0v5ZzZowLEPdqamp+u7H35WQmKReXdro2YY1tW3XIeP+5sQJAAAAAACAzNFzBQCQK9y6laA8Hq733ebi5KDUVINuxSfI0cFektSiUS1VKFtCkrTn4AmlpqZqUO+XjBPfW1hYaI7/akmSjY21Rv6vv1xdnIzJG78yvgq4EKK6t4cgk6ROzzeRm6uz3FydVbuanwKCQjLEkpKaqrhbt9S8YU3l9XRXs2dqyK90ceW7PdH9O290VnxCopwdHSRJYdeua+P2/dlqg4PHzighMVEDe78k69vnkTePu376dZFeeqGZWXECAAAAAAAgcyRXAAC5gpOjg27dSrjvtpibt2RlaSkHezvjOleXu5PLnw++LN+ihYyJFUkqV6qoSR1W1lZavGqLTp8L0q34BJ0PvmwcyusON1dn47Kjg70SEpMyxGJtZaXnmz+j8VPnqUihAipRrJDq1agoS8u0zqSWFhbafeC4Dh45rbj4eJ0Pvqx8nh7ZaoNz5y/Jt2ghY2JFksqWKqqbcbd0NTzSrDgBAAAAAACQOZIrAIBcoahPAa3csFMGgyHD0GDHTgXIp2D++w4ZJqUN1WV5z7Z0I4gp7Np1fT5musqVKq5qlcrIx9tL67fufehYX27XXE3qV9f2PYe1cfs+rVy/U8MGv65ihb01YvR0WVpYqLJfKZXyLayzgRf1d7rhxx7kfudxR0pKykPHCwAAAAAAAFPMuQIAyBWqVSqjqOgYLVu73WR92LXrWrVhp2pWLZfpvvnz5VFAUIiSkpKN606cOW+y7OhgrwFvdFbLxnXkV8b3oXt7GAwGhVy5Kq+8HurYurEmfv2+vPJ56OipAIVfv6HzwZf1bt8u6tC6sSqULSFra6usK72tcKH8CggKMUmknDxzQfZ2tvLKm+eh4gUAAAAAAEBGJFcAALmCp4ebundqpYXLN2rKr4u068Ax+a/YpJHjZ6loYW8937x+pvvWqlpeBoNBk3/xV3hElPYcPK6VG3aa1B0eEaUdew7relS0Fq/crLOBwQ8VZ9SNGA0bNVULl29U1I0YbdqxX+ERUcrr4SZXZ0dZW1lpxfodiom9qY3b92nb7kMm+zs62OtKWISuRURmqLtejYrK5+mhyb/46/jpQO07dFK/zl+pTs83kY1N1p1V4+MT9Nn307Tn4PGHOjcAAAAAAICnBcOCAQByjWYNaqqAl6eWrd2uabP/Ur487nq2US0916yeyTwk93JydNDHA3pq4fJN+uirifJwd1W3ji01+Rd/SVKl8iX1bKNamj53qQypBjVvWEs1q5R/qBg93F31dq8XNcd/tf5avVUODnZqUr+G6tWsJAsLC/Xp3k5zF63V6k27VKl8STWtX0Mbd9yd0L5Ni/oaM2Wutu0+qJ+++8ikbgsLCw3p/4rG/DRH3/74mywsLPR88/pq1bRutmJLNRh0OfSarkdGP9S5AQAAAAAAPC0sYuMSDFkXAwAgc7Fx8crv6ZrTYTySuFvxcnSwN34+d/6ivho/S7PGD8t0rhYAAJB71O82JqdDAHKlHXOG5OjxwyKi5exon3VBAADMxLBgAICnXkxsnAZ9OlYr1u9QSmqqzgQG648l61SpfCkSKwAAAAAAAMiAYcEAAE89F2dH9evZQUtWbdW8JetkaWmhapXKqk+3djkdGgAAAAAAAP6FSK4AACCpRuVyqlG5XE6HAQAAAAAAgP8AhgUDAAAAAAAAAAAwA8kVAAAAAMBTz93FIadDAHIdvlcAgNyM5AoAAAAA4Kn3VteGPAgGHiN3Fwe91bVhTocBAMATYxEbl2DI6SAAAP9tsXHxyu/pmtNhAAAAAICJsIhoOTva53QYAIBciJ4rAAAAAAAAAAAAZiC5AgAAAAAAAAAAYAaSKwAAAAAAAAAAAGYguQIAAAAAAAAAAGAGkisAAAAAAAAAAABmILkCAAAAAAAAAABgBpIrAAAAAAAAAAAAZiC5AgAAAAAAAAAAYAaSKwAAAAAAAAAAAGYguQIAAAAAAAAAAGAGkisAAAAAAAAAAABmILkCAAAAAAAAAABgBpIrAAAAAAAAAAAAZiC5AgAAAAAAAAAAYAaSKwAAAAAAAAAAAGYguQIAAAAAAAAAAGAGkisAAAAAAAAAAABmILkCAAAAAAAAAABgBpIrAAAAAAAAAAAAZiC5AgAAAAAAAAAAYAaSKwAAAAAAAAAAAGYguQIAAAAAAAAAAGAGkisAAAAAAAAAAABmILkCAAAAAAAAAABgBpIrAAAAAAAAAAAAZiC5AgAAAAAAAAAAYAaSKwCAR2ZhYaGk5JScDgMAAAAAjJKSU2RhYZHTYQAAcinrnA4AAPDfZ2tjrcjoOBkMhpwOBQAAAAAkpb0EZmvDoy8AwJPB3zAAgEdmY20lG2urnA4DAAAAAAAA+EcwLBgAAAAAAAAAAIAZSK4AAAAAAAAAAACYgeQKAAAAAAAAAACAGUiuAAAAAAAAAAAAmIHkCgAAAAAAAAAAgBlIrgAAAAAAAAAAAJiB5AoAAAAAAAAAAIAZSK4AAAAAAAAAAACYgeQKAAAAAAAAAACAGUiuAAAAAAAAAAAAmIHkCgAAAAAAAAAAgBmsczoAAMB/X1JyihKTkmUwGHI6FAAAAACQJFlYWMjWxlo21lY5HQoAIBciuQIAeGSJScnycHXkPy0AAAAA/jWSklMUGR3H/1MAAE8Ew4IBAB6ZwWDgPywAAAAA/lVsrK3oXQ8AeGJIrgAAAAAAAAAAAJiB5AoAAAAAAAAAAIAZSK4AAAAAAAAAAACYgeQKAAAAAAAAAACAGUiuAAAAAAAAAAAAmIHkCgAAAAAAAAAAgBlIrgAAAAAAAAAAAJiB5AoAAAAAAAAAAIAZSK4AAAAAAAAAAACYgeQKAAAAAAAAAACAGUiuAAAAAAAAAAAAmIHkCgAAAAAAAAAAgBlIrgAAAAAAAAAAAJiB5AoAAAAAAAAAAIAZSK4AAAAAAAAAAACYgeQKAAAAAAAAAACAGUiuAAAAAAAAAAAAmIHkCgAAAAAAAAAAgBlIrgAAAAAAAAAAAJiB5AoAAAAAAAAAAIAZSK4AAAAAAAAAAACYgeQKAAAAAAAAAACAGUiuAAAAAAAAAAAAmIHkCgAAAAAAAAAAgBlIrgAAAAAAAAAAAJiB5AoAAAAAAAAAAIAZrHM6AAAAAAAAnqSo82sUeniqUhJu5HQowFPDys5NBSr3lXvxljkdCgAATwQ9VwAAAAAAuRqJFeCfl5JwQ6GHp+Z0GAAAPDEkVwAAAAAAuRqJFSBn8N0DAORmJFcAAAAAAAAAAADMQHIFAAAAAAAAAADADCRXAAAAAAAAAAAAzEByBQAAAAAAAAAAwAzWOR0AAAD/RUHBITp45LiuXouQvb2d2rdpIVcX55wOK8fRLgAAAAAA4GlAcgUAkCt9N26KFi9ba/w86K1e6vpi28dS9/pNO/TZ1+OVkpJiXNf2uWaPpe7MdOk1UBeCLqmQd375z/npiR7rYeVEu/wTuvYapPNBF5XHw10r/WfmdDgAAAAAAOBfgGHBAAC5TmpqqtZv2mGybtW6zY+t/ok//2pMIBQtXEjNm9SXh7vbY6v/v4p2AQAAAAAATwt6rgAAcp2du/crJvamJMm7gJeuhF7VmbPndT7ooooXLfxIdacaDAq7FiFJ8itXWjMmffvI8eYGtAsAAAAAAHiakFwBAOQ6q9ZtlSTZWFvr/YF9NOSTkZKkFas36Z1+PU3Krt+0Q59+OUaS9P7APnqx/XPGbX3e+Z+OnjgtS0tL7Vy/UN3eeE8B54OM24+fPKM6TTuqsI+3Fvw2yaSuH78foZu3bum3uYt0PuiiKpQvrdYtmui5ZxuZHP9SyBVNnPq7Tp8NVHhEpPLlzSO/cqXUvk0LVa9S4b7ndyM6RpOm/q6tO/bIxcVJtapX1us9XpJnHndJUlRUtFp1fE2S1LdXV3nl89Sf/st1KeSKypctpb69uqp0yeL6ccqv2nPgiK5HRqlG1Yp6vUdnlS1dwuRY4RGRmj1vsXbtO6SQy2HyyuepapX9NLD/q3K5PZdKVu0iScnJKVq0bI3WbtiqcwFB8vBwU9VK5dXt5fYqUbzIfa/HyOFDdDYwSCvXbFJeTw/NnDxKo8b9rEXL1sja2kpL/5ymUeOn6tCRE3JwsFej+rU08K1e2rXngH6bu1hnAs7LO7+Xmjepp55dO8rKykqSjHVI0h+zJhgTbikpKar/bGdJUvUqFTRp7Bf3bf879u4/opmzFyj4YohiYm/Kp5C3alStqM7tW6uwj3eGa9G5fWuVK1tSf/ov1+mzgdq6+k/Z2to88BgAAAAAAODfieQKACBXiYu7pW0790hK60FRt3Y1ubg4KyYmVqvXb9XbfXvIwsLiicexcetOkzlf9u4/or37j8jS0lItmzWQJAUEBqn3Ox/rVnyCsdzlK2G6fCVM6zZu1xefvqcWTRuY1GuQNOCDETpz9rwkKepGtC5euqJ9B45qzozxsra2Mim/ZftunT4baPy8/9AxffL59ypXpqS2/73PuH7rjj3ave+Qpv3wjUqXKi5JOnk6QO9+9IVuRMcYy4VcDlXI5VDt3X9Yv/w8Wu5urlm2xc24OL313nCTOK6EXtWV0Ktat3G7Rgx9V80a1cuw35z5S3Xi1FlJUl5PD5NtyckpGvy/kTp1JsDYDvP8lyv2ZpxWrt2s1NRUSVLA+aDbP8H6atiQLGPNrqUr1+vr0ZNN1gWeD1bg+WCtXLNJMyZ/p6KFC5lsP37qrBYsWfnYYgAAAAAAADmHOVcAALnKpq1/KzExSZJUvWoFWVpYqEbVipKk8Ijr2rP/8EPXPWfGOO1Yt8D4uVb1ytq1cZGxd0Z62//ep0ljv9Dav34z6Q2zcMkq4/LKtZvl7OwkzzzuGvbRAK376zd9/dkHcnZylCT9/sfiDPVeCb0qezs7ffnpYL3Vp7vyeKT1Vgm6GKI9+w9lKH/23Hl9+8VHWjZ/ulq3bCJJirgepT37D2vCqOFaMm+qmjSsK0lKSEjU8jUbJaXNWzP0i9G6ER2jEsWLaubk77Rp5VxNGDVcTo6OCr0aru8nTMtWu4ydOMOYWGnTqqmWzJuqkcOHyNXFWUnJyfri2x8UdjU8Q+ynTp9Tt5faafTIT/TBoH4Ztru7uWj5gukaPfITubm6SJKWr96opo3qatWiWfpmxAdycLCXlNYj5s5QcY8q1WDQqnVb5O7uqnJlSmjct8O09q/f9GbvbpKk2Jtx8v9rdYb9Tpw6q6aN6mrk8CH6cfQIWdvwjsv/2bvzsKiqNw7g32FA9kWRTRAQURBUxBU1d3PNcs1dU3PJslLLtMXMMs1KS0szTXNfcsnUXAEXXHABVBYREEFAFpF9Z5jfHxMXBoZlYAaU3/fzPDzP3HvPPeedy7mD3nfOOUREREREREQvK/6vnoiIGpSznleE1716dAEA9H2lG7wvXwcAnD5/Cd06d1B7HK8NGSBM67Xw3ZnwvHgNKalpeBQZLZRZMG86FsybLndety5u0NZuhMysbMQnJJWrVwRgzVdLhKSKibGRMIIiIvIJenTrJFe+k3s79H2lGwDg3dlT8e9ZbwBA964dhesw/+0pwvVJTk4BAPjevou4pwkAgInjRsDFuZUsvs4d0L9Pd5w47YlLPjeQl5cPbe1GFV6HrOxsnPP0AQA42DfH50veAwBYmjdFbl4+vv5uI/Ly8vHvOW/MmDJO/hoOHVDu+pQ2Y8o4NDVtgle6N0HfXh44fuo8AOCtyWPR2MQY/Xp3h/flGzjndUV4b4YG+hXWV10aIhE2r/+63P6unTpg87a9AGRJsLJsbZph1fKP6mTkFBERERERERGpF5MrRETUYDxPScVt//sAAAvzpsL6If16d8eqH35Ffn4BvC5dw6eL56t9rYvi9U8AQCwWw6aZJVJS05BfUCBXLjTsEc57+eBheCQio54g6dlz4VhRkbRcvUbGhkJiBQDMmpoKr/Py8sqVNzQsSSbo6mgLrw0M9Er2/ze6AwCkkLUZHvFY2PfN2l/wzdpfytVdWChBQtIz2No0K3esWFR0LAr+e88d2rvKHevSsb3w+mH4Y5TVytG+wnoBwMjIoOQ9lHpvpRMoOqX2F783VZBKpfC5fhs3bvkj/FEUwiOikJWdLXe8rJYOdkysEBERERERETUQTK4QEVGDceb8ZWGtjYTEZ/DoP7pcmfz8Apz3uoLhQ/qXO1b24bsqH8Yr8ueew/ht+z4AgJ6eLpxbt8Twwf1w4eI1xMQ+VXiOCPIP59X1sL5IWiS8btXSHvp6epWUrpikqKSeykItLCwst6/se1WH0jkQBfkQhQoKCvDxF2tw46Y/AMDSwgxu7ZzR3tVZ+H0qwrwKERERERERUcPB5AoRETUYZzwvVavc6fOXhORK6REssbHxwuuCwkI8iVGc4FCFjMws4UG8u5srNqxdDi0tWSwXfXzV1m51WVmaC6+njB+JwQN716wei5J6/O8Fyx275XdPeG3TzLJG9ddE6d95TOxTONg3BwBEREZV6/yrvn5CYmXK+JF4b+40AEBqanqlyRUiIqLKvL1eNjXntoWN6zkSIiIiIqoOJleIiKhBiIl9iodhkQBkU4IdP/C73PHCQgmGjn4LGZlZuBMQiMSkZJibmaKFXXOhzPFT5+HSphVMjI1w5PgZpKVnqC3e0tNGmTYxERIr12/643FUjNrara5XPDpDV0cbObl52LH3MBxa2KJVS3skPXuODz/5Gs9TUtHGqSXWrf680nqamjZGxw5t4RcQiEeR0Vj1/a+Y/dYEhISG4+dNO4Ryr/bvpe63JLC3sxFe//r7bmhpaaGgoKDaiZEiSclonGZWFsLrvX8dV12QRET0fyfkSflRnERERET04mJyhYiIGoSTZ7yE1wP79ix3XFNTjL69PHDitCekUin+PXcRb00eg+Y2VujayQ0379xFTm4eln+zHoAsQfNK987wuX5bLfEaGRrAxbkVgh+E4YL3Vdz2u49mVhYIfhAGS/OmiE98ppZ2q0tPTxdLF8/Him9/wuOoGEydvUjuuEgkwvDB/apV1ycL52LmO58gKzsbJ0574sRpT7njE8eOgIuzo8pir8qAPj2wZft+pKSmIepJLBYulS1O371rR2RnZVd57Tt2cBUST2t/2oL9h/+BhkgDz1PThP1ERERERERE1LBp1HcAREREqnDqrLfwemC/VxSWGTSgZHTE6XMXhderv/oYU8aPhL2dDfT19DCwX09s+XkVjI0N1RYvAPz47ad4pXsXaGhoIDUtHYAUP6z6FC5tWqm13eoaPKAXNqz9Eu1cnIR9GiIR2rk4YfNPX2OAgiSWInbNrbH3j/Xo28sDGhol//SwsjTHkg/n4IP5M1Qee2UMDQ3w+4ZvMfTVPmhq2gQW5k0x+c03sOarJRCLxVWeb2JshF/XfY3Wji0AyKaTs7O1xm8/fQMdHR11h09ERERERERELwBRZnaeelfrJSKiBi8zOxcWpkb1HQYRERGRQkEHB9Z3CFXquSgJAHB1nZnK6gyKKsCcn1OFbU0x4GKrhZ6ujTChjx40//tOwZJtabganC+Us2kqRoeWWpjYVw/2FiVfPNjrlY1NJ7MUtnVhdVPoaovk9mXmSDH4s2fo56aNb6b/f/xb0ScoH5/8kYZ3R+hjUj+9GtfT5+MkODfXwpb3TVQYXf1wHX+hXttPSE6HgR6/AENERKrHacGIiIiIiIiIGrC29lrwcG6E7Dwp7oTlY/PJLDxPL8L7Iw3kyrm31IKmWISEVAlO38rFeb88rHrLCN3bNJIrN9BdG/YW8o8TNF/ipwvzf0nF3UcFKk1sERERUcP3Ev/zh4iIiIiIiIiq4mSjiRmDZKMo8gr08NryZPzjm4v5IwyE0SsA8NU0I5gayqbwfPpcgvm/pGLFnnQc+rQJjPVLpvbs3U4bAzpo1+l7ICIiInrRMLlCREREREREVIfe2ySbquuzCYawaqJ4va+nzyVYdSADVo3F+Gyi6taB09YSob2DFm6E5CMxVYJmporbt2oixoQ+ethwPBNXAvPxWreaT6sklQIHLuXgzO1cPEsrwqCO2ljwhgFE/80i9iRJgj1e2bgZmg8NkQjuLbWw4A19IaHz9k8pSEwpwuT+etjtmY0RHjqYO0wfb/+Ugsh4CTzXNBXaGrUyGdpaIhxY1kSYluy1bjpoYalZ0n4nbSx4Xdb+5O+e43GCBIBsara5w/UxbYAesnKl2HUhG7ce5iMuWQJXey3MGaoPJxvZY5QrgXlYuj0dMwbpwT+iAPcjC3ChVByl3QjJx17vbITGFMLWXIxuTo0wrpcuTAxk7y8lswh/nMmGT1AeGhtoYO4w/XJ1VBXPxn8yceBiDtbNMcbJm7m4FZoPW3NNfDzWAK2s+eiHiIhIHbigPREREREREVEdin9eBP/wAizYlIanzyXljhcnVvzDC+AfUaDy9jOyZUuv6uuIKi3X1l72UD4yobBW7fkE5cHTPxeudlrIK5Di4OUcXPDPAwDkF0rx/uZUXAnMR08Xbbg7asHrrixxUVjq0qRnF+GITw4GddKGq52WUu3fDM2Xb/9SSfuje+oKCa63h+ijvb2s7jUHM7DPOxuWTcQY2kUHj54WYtHvaYhPkf99HbyUA30dESb10xOSRaUFRxdi6fY0pGVLMbGvHuzMNfHn+Wzs9c4Ryny6Ix3HruXAsZkm3FtqYcu/WSgqkq+nuvGsP5YJI10RbM01ERRVgBV70pW6VkRERFR9/PoCERERERERUR3aON9YSKws2JSGjfONhWOlEytWTcQ4/HkTlbZ9JTAPIdEFaGOrKTfVlyIGurLjmTlSuf3Ld6Vj+a6S7TGv6GLRaPn1W0oz1tfApgUm0BKL0NVJC5/uSEfIkwK82lEbF+/mITG1CF9NNcJAd9lUYy62mvjxSCZuPcwX1nspkAArphrBxVb5xxh62iJseb8xNDQAD2ctLN1e0v6YV3ThGZCHp88lwtRpialF8Lqbh9E9dbF4jOx9jfDQwdS1KTh2NRfvvFYysqSjoxa+m2WssF0AaGklxjdvGaOFpRjWpmIUSYFL9/MQEJEPQB+hMYW4F1mATq208MNsWT0BEQV499dUoQ5l4nnrVT0M6SwbZTRrfQoePClEerYURnqVJ9KIiIhIeUyuEBEREREREdUhqybicgmWYupIrBzxycERn5KREk0MNbBwVMXJkGKZObLhEyZlkjBlF1DcGOsAACAASURBVLQvnpqqIq2tNaEllj3ctzOXlc3KlSVsQp7IRsV8uTsdX+6WPy8uuWRURiNNUY0SKwBgbSqGxn9vobmZfPuKBEfLRgsdvZqDo1dz5I6VHWnUrkXlo2i0tUQwM9bAocs5iEqQIClNgpw8KfL+G5D0JElWX/c2JWvYtHfQgrZWSTJEmXiam5VM82ZrLsaDJ4XIyi2CkZ7i6d+IiIio5phcISIiIiIiIqpjZRMsxdQxYqWtvRY8nBtBLAacbTThVubhfUUCH8sSH2XX7FB2QXuNUk2VnTpL8t/0V19OMYKZkXwSx7ppSUJAo5qTmksrzpkobF+R4im5pvTXg4dzI7ljRvryFVRV3T83cvH9XxmwMROjv5s2rJpoY9PJrCrjKiqSlnpd/XjkY+NoFSIiInXimitEREREREREavTeplSM/eZ5uf3FCZbSi9pXllipqJ6qONloYsYgPUwboIeuTo2qlViJTZbgwKVsGOiK0K3MA31Vsv1vpIVEIoW7oxbcHbWgqQk8TZFAp1HlcRroaCA3X4rEVFn2ISy2EM8ziio9RxGNMs3YmstiSs0qEmKyMRPjcWIhGmkql7C4FpyHIimw86PGmD1UH73aNkJOXknipDiB5BOUJ+y7EZKPglIDUlQZDxEREakOR64QERERERERqZF/eMWL0hcnWCaueQ4tsajSESuV1aMKX+5Kh6ZYhMIiKYIeF0IkAr6ebgRDXfU9wB/gro0d57Px49FMhMUVQl9HhL8u50BbS4T+bpWPjnGx08Sth/mY/0sqBrpr4+K9PJgYKP8dUnMTMYACbPg7E/06aKOdvRY6t9LCSd9cFBTKptq6eC8P4XGF2L6osVJ1NzWSJUa2/JsFD+dG2HkhG+JSM3Q522jC1U4L/uEFWLk3A9ZNNeD7oEAuseTYTFNl8RAREZHqMLlCREREREREVI+smohxca1ZfYcB/whZ8sbWXIxhXXUwrpcu7C3Uu1ZHYwMNbHnfBPu8s+H7IB+PEyTo0FILc4fpVzlyZUp/PYTFFuJacD6O+OTg43GGOHQ5G5k5VcwNVsakfrrwj8jHwcs50NIUoZ29FlbPNMY+72zcDC3Aeb9c2JiJsWy8YZXry5Q1/VU9PE2R4MDFHHgF5GFUT12klBpdIxIBa2YaYduZLPgE5uNepAjLxhvii13pcvWoKh4iIiJSHVFmdp5y/+ogIiIqIzM7FxamRvUdBhEREZFCQQcH1mv7PRclAQCurqtdAkVV9RDVJdfxF+q1/YTkdBjo6dRrDERE1DBxzRUiIiIiIiIiIiIiIiIlMLlCREREREREVAf+vZVb43PVvd4KERERESmHk3MSERERERERqZG7o2zB8lX7M7Bqf0at6hrWhdMbEREREb0IOHKFiIgahJv+wZj63grhZ8GnP2LTn0cQ+zRR7W2v/XUP/jrhWeHxlLQMfPvzn3jr/ZU4431DJW1mZGbh/c9+xE3/IJXUV1p+fgFmLvwG12/fL3esUCLB7MXf4tJ1f5W3u+qnHdh75IzK632RPHwUjanvrcDuv06rvO4HYY+xbNUmTH1vBZ7EJgAADp/0wuoNOwEAP2zaiwN/nxfKnzh3BV+v3w4AiHgcg6nvrVB5THVp2apNOHHuSrn9V24EYP7S79XWbnRsPKa+twL5Ber7RvmRU974fM2WOomhqr6g6POs+PMo8EEEHoRHYcGnPyIlrXYPj9V9XYvvlbI/Dx9FA3g5Po9U/XegomsSHRtf5bmlP08UqYv75EX32QTDWidFrJqI4e6ohc8mGqooKiIiIiKqDY5cISKiBkNTU4yP3pkMAHgSl4iAwIdY/v1WLJo7Ea5ODvUW18nzPsjIzMaCt9+Ek6NdjeoICn2En7cexO8/LAMA6OnqoLm1BcybNlFlqACARo200MG1NW7fDUH3zu3kjt0PiUB+QQG6uruovF0HO2tYmpuqvN4Xia9fEGyszHErIBhTxw1Vad17jpyBpbkpJo4aBJtm5gAAK4umKCyUAADsm1vBwkz1/YXUz8rcFJktbOo7DACKP8+KP4+aNjGBhoYGmlubw8hAr54jrVqf7h3RvXNbuX02VrJ7p64+j/464YnomAQsfmeS0ueq4++Aomuijr8z/4+smojx2URDJkaIiIiIGhAmV4iIqMHQ0NAQkiiuTg4Y0s8Dv+44jN92HsPP3yyEhkb9DNhMSc1A2zYt0am9s8rqFIvF+Hj+FJXVV1ZXdxf8vudvFEok0BSLhf137obApbUDdHW0Vd7mxFGDVF7ni+Z2QAgmjxmMzX8eRXjkEzi2aK6yup+nZmDM8H5o7+Io7OvZpT3QRfZ67Ij+KmuL6laPLu3Ro0v7+g4DgOLPs7KfR0venVofoSnNwqxxhYn3l+HzSB1/Byq7JkREREREJI/JFSIiatBmTHgN8z9Zi6DQR2jXxhFrf90DGyszhEXG4FFUDDatWQIvn9sICAzDF4tmCuet2bgLrR2aY/TwfgCAu8FhOO15HRGPY2Df3AoendthwCudFbb5647DiIlLxLszx2LZqk3C/jNe17F0wTS4tG6B017Xcf32fcQnJsPJ0Q6jhvVFSztrACgX46RRg7Hnv+lppr63AmOG98PIoX0wa9EqYVROUVERTpzzwdVb95CZlY0endsjPTMLJkYGmDR6MAAgLj4JR/+9iMAHj2BkqAePTu3wxuBeEJdKnhTr2M5J9r6DwoSHqFKpFAGBYRg1vC8AIDsnF0dOeiMg6CFycvPg3tYJY0f0R2Nj2bdyZy1ahXGv9Yenz21oisVY/dl8JCWnYMeBkwh/HINGWlro1N4Zb40fDpFIhLW/7kELWyuMGzFAaPu013U8ioqFTTNz9O3REb093AHIpi76dsNOvD/rTfx95jJi4hLQ1rkl3nlrNBppaZV7P/uOnsVpr+vl9v+x/jM00tKSu5aAbPquVT/twM4NXwq/E/vmlkhISsH9kHC0d3HExFGDcODv87gbFAYTYwOMGzEAXTpUPKIn4nEMMrNz0KFta7Rr0xLX7wTKJVfKvn8AmPHB1/jkvalwbmVf4bW7eM0P2/efAACs27IfALD7lxU4ce5Klf26IlKptNI+OmvRKsycOAK3A0IQ+CACVhZN8e6MsRWOjJm1aBVmTngNF67cRkxcApwc7fD64F5o7WBbrfYU3bf6erqVvoeKZGRm4/BJL/gHPkRKajo6tXfGrEkjYGigX61+FRXzFEdPXURI2GNYmpvi1T5daxSHMsr+LquKoap7Mzo2HkdPXURQ6CMUFkowuJ8Hxr8xECKRqMIYEp+lYPGKn4Xt4s8zVyeHKu8fRZ8FZVX1nlTdJ6tS+n48ce4KQsKi0NbZAV4+t5GTm4f+r3TGmP/uI4lEgu37TyLwQQSyc3LRuqUt3pk+Ggb6stE7twNC8K/XNTyKioW+ni4mjR6Mnl3aY/OfR3Dtv+kXp763Al8smoms7Fys+21fuXgWzZsE97aty+0vfe1V8TlVGf/7oTjjfQOPomJhbWmGQf080KPM6MZi9XGfEBERERHVNa65QkREDZqerg6aWZohLuGZsM/n5j0MH9gDS96dCp1qjMCIT0zGj5v3wc7GEu/OGItuHV2x69ApBD6IKFd2z+EziIyOw6cfvAUbK3Ps/mUFunRwwdD+3bH7lxVwdXLA+cs3cfSUNzw6tcWcqSNhoK+HNRt2IjsnV2GMA/t0xdIF06Cro43dv6zAyKF9yrV77tJNnDzvg749OmLmxBFISk5BUOgj4XihRII1v+xGbl4+Zk0agQG9uuDiNT8c+/eSwvfcqJEW3Fxa4aZ/sLAvLPIJMrKy0O2/KcG27f0H9x9E4PXBvTFp1GA8TXyGX7b/JVePr38wpr85DG9Pfl12fY6cRWZWDpYtmI65U0fhXkg4Lt8IKNf+04Rn+PE32TWfO20U3FxaYcf+k7gbHCaUyc8vwJ17D/Dh7PH4cM4EPIqKxanzVxW+nwG9umDpgmnCj5VFU7i3ba0wEVOR67cDMbhvN3yxaCZi4hLxxXdb0Na5Jb77/F3YN2+GfcfOVXr+Tf9gOLW0RSMtLXRo2xq3Sl3b6qjo2vXr2Qm7f1kBQwN9LJo3Cbt/WaFUvYpUp4+ev3QTo4f1xcolc6Ct3UhI8FRk79Gz6N+zE1Z/Oh8G+nr4cfM+5ObmVbs9Ze/bivyx7x88fvIUsye/gaULpiE9Mwt/nfASjlfWrwolEny/aS+kAOZMGYkeXdrj4N8XahxLTVQnhsruzYKCQqz9ZQ/09XTx4ZwJeP/tN3HFNwA37gRW2q5508YKP8+qq+xngbLvSR19UhkhYZHQ1BRjxcezMf6Ngfjn7GU8jIgW2vW7H4qJowdh5ZI5KCyUYM9hWUI8KiYeG7cfQtcOLvh4/hSMGd4PW3f/jZTUdLzz1hi8PrgXOri2xu5fVqC1gy1atbCR+6zy6NQWpo2N4VzNKSVr+zlVkSdxCVj/+340b2aBedNHo52LI7bu/lvu70yxF+E+ISIiIiKqCxy5QkREDZ6+vi6ys0sewHV2c0ZntzbVPv/85Ztwb9tabpoYQwN9mBjJvgUuEgEiiHDG+wZu+AVi5ZI5MKxkvYGLV/0wa9LrwnomXTq4YPGKaNy5+wC9PDrUKMZL1/wwalhfDBvQAwDg3rY1PvhivXDc/34o9HS0sWjuRGF6NAM9XRw55V3hdFFd3F2wY/8JFBUVQUNDA7cDQtC6pR0M9PWQmZ0D//uhWLfyQ+Hb8C5OLfDB5+uQnJIG08bGAIBBfbqirXNLoc70jEx0bOeEFrbNAACffzgDhvrlr9WFK7fkrnmn9s7IzsmF5+VbcHNpJZQbM7wfjI0MYGxkgG4dXRERFavwvViYNRG+wX7+0k1kZmVjzuJZ1biyJdq7OKJ1S9lIi749O+HcxRvo0102kmbciP5Y9OXPyMjMgqGBvsLzb9wJxPBXewKQTbv258GTCI+MgWM119Ko7rVTher00UF9u6G5tQUAYNiAHti043Cldfbt0VE4d+7Ukfh45UZcvxOIfj07qeyeOPSPJw7941luf+nfyXuzxiE3Lx8G/418SUh6Di+fO3LlK+pXfvdCUVRUhA/eflMY8VVUVIT9NXxgXRNVxVCde3PVsnkwMtQXRqq4Ojkg4nFsuTWWVKnsZ4Ey7wlQT58s219MjAyx8dvFCss2bWKCQX26AQB6e7jjwuVbCIt8gtYtbZGangk7G0t4dJStVbLg7TchLZICAOxsLLHhm8UwNjIAILvWf5+5jEfRcehkYlSuHQN9PSFpFR0bj9sBIVj2wfRqT8VY28+pstfE1ckBSxdMg5fPHfTt0QlTxg4BIPtMfp6SDp+bd8sl2V6E+4SIiIiIqC4wuUJERA1eVlaOMD0LgEoTH4o8ioot91C3W0dX4bVUCty+9wCxTxPxzltj0ETBA7NikqIixDxNwKY/j2DTn0fkjiUmp9QoRolEgtj4RLRpZS/sE4vFcPhvuhwAiIyOQ2x8Eqa/v1LuXA0NEaRSqcLpgDq2c8LWPX8jJOwxXJ0c4B/4UHi4GBkVh0KJBO9/9mO58xKfpQjJFSND+Qd4wwf2xG87jyIo9BGaW1ugYzsnmCp44Kromjs52uHarfty+4ofWAKyUUp5+QXl6iotLuEZ9h07iw9nTxAerleXgX5JeS1NMfR0dYRtHe1GAID8gkKF5z5+8hQpaeno8t97MtDXQysHW/j6BVY7uVLda1db1e2jxqV+t/p6OsgvqPzaO5X65r1IJIKjvQ0io+PQu7u7yu4JRYtx3w+JkBsdpSESwdcvCP73QpGdm4vI6DiYmTaWO6eifhUZHQcHO2u5qfQqG1Ew9b0VVcas6D0oGt1RrKoYqnNvijXFOHb6EkLDo5CTm4fI6Dj069lJ6ViVUfazoLSq3pO6+mTZ/qKlWfF/jYzKJCP0dHWQl5cPAOjXsxNW/bQDy9f+jmYWTeHi1AKvdHUTymbl5OLvM5cRHRuPtPRMpKSmo6CCz4pi+QUF2LDtEAb17SZMn1cdtfmcAspfk+L6Hj95ivDIJ/C+Kp+IVNT/lb1PiIiIiIheVkyuEBFRg5adk4u4+CTYN7eqcR1SKSpdiwAAUlLT4dK6Bf76xxMdXFvJPdAqW5lUCsycOALmTeUf6JqZmtQsvopilEqFl0VFUrR2sMXo/9ZLqQ4d7UZwc2mFu0FhMG/aGPGJyUJSqUhaBF0dbXwwe3y584q/Oa5IZ7c22LBqMW4FhOCs9w2cv3QTU8cNFZI2pUNXdM0lRUXVjr+sQokEP289gN4e7nBzbVX1CSrk6xcEqRR4//N1cvufJadi8pgh1aqjuteu1tTQRwFZUqOsoqIilbanaDHu5ynpcu2t+GEbNEQiuLm2QiuH5gh79ATXq5gSq5hUKi33PqQVlAWAb5e9U+3Yi+nrV570qyqGqu7NhKTn+OrHbWjTqgU6tneCjZU5Lly+pXScqlTldVVTn1TV4u0WZk2wbuWHuB8cDs8rt7F1z3H4Bz7EB2+Px03/YPy26yj69eiEfj06wbSJMX7f83eVde48+C80xWK8+cbAWsenjIquiVQqxcBeXdC5g3zSW9HfOmXvEyIiIiKilxWTK0RE1KBt338Chgb6lY4O0NZuhPTMLLl9qemZwmsbK3M8jIgWptwCgFsBwbA0MxUSCQN6dcbrg3vjs9Wb8duuY1g0d6LCtsRiMSzNmkBLU1PuAdbtgBA0Nq54xEtlNMViNDExQkjYYyGJVFBQiPDHMbA0NwUA2Fpb4FZAMFxatxCSFk/iEoAqEkddO7ri6ClvmBgbopVDc+Hb5zZW5sjNy4OluakwSiUnNw+h4VGVjgh5lpwKAwM99Onujj7d3bHjwEn4339YLkFgY2WG0DLXPDQ8Cs2bmdfgCsns/us0JJIiTB4zuNwx7UaNkJ5R0gdS0zJq3I4itwOC0f+VzujqXrKQdG5ePn76/QAiomLR0s4aOtqNkJGZLRzPzM5BoUQibFf32gnvqYp+XRF19FEAeBAehXZtHAHIHr6GP45Bv56d1NaeIs+epyEyOg4bVy2GyX9TZkVGx1X7fPOmjXHFNwASiUT4Vn5waGSF5StLNNZUVTFUdW/e8g+Gnq4OFswaJ5xz6sI1GNYiptreP1W9p7rsIzWRmZ2DgoJCuLdzgns7J/j6BWHL7mMAgDt3Q9Cjc3tMHTcUgCxBnFnqPlfkzr0HuHb7HlYtnQexxouxRKaNlTnyCgrkrn9Q6COFIzWVvU+IiIiIiF5WL8a/1omIiFSgqKgIQaGPEBT6CPdDIrBh2yEEBD7E/BljKk0gONrbID4xGYdPeCEo9BEOHr8g93Bw1LA+CA6LxN+nLyEo9BF8fO9i044jeJ5a8o14kUgEHe1G+HDOBNwPCcfZizcqbG/CqEHYd+wcvK/eQUZmNo6c8savOw4j6Xlqhefo6eogNy8Pz1PT8UxBub49OuLoKW/4+gXhWXIqNu88KjdFlkenttDX08XGP/7Ck7gERETFYsPWgzh1QfEC8MU6tnNCckoaLl67g64dShIDpo2NMaiPB9ZvOYC7wWFITknDph1HsPvwaUhKJQTKWvf7fmz+8wjik5JxLzi8wodzo4b1RUipa+555RYuXLlV429x+90PhZfPbfTt0RFhj54I/ST3v2l9Wtha4fBJL9wNDsO12/fheeV2jdpR5ElcAuKTnmNQn65wdXIQfjq1d4aDnTV8/xs10cK2GXxu3sXVm3dxNygMOw+egpZWyfdgqnvtilXVrytTkz5aFV+/IFy67o+g0EfYuvc4UlLThfUz1NGeIkYGetAUi3HqwlVkZGbBy+c2rvgGVH3if7p0cEFBYSE2/XkEQaGPcPXWvSoXgle1qmKo6t40bWyMZ8mpuHrzLp6npuPYvxcR9ii6VjHV9v6pznVVRx9JSEoRPguKfzKzKk98KHL0lDe+27gLIWGPEROXiEvX/YR7s7GJEe6FhCM8MgbRsfHYuue43Ag8PV0dJDxLRkZmFnJy85CckoYtu4+hSwcXpKRlCHElp6TV+H2qwqhhfeB3LxSH/rmAlNR0+PoFYf2W/QgICitXtjq/zy27j2Hv0bN1FT4RERERkVpw5AoRETUYhYUSrNm4C4DsAaOzox2+/mQurCyaVnqeg501Rg3tg3/OXcH1O/fRr2cnufUhTBsb46N3JmPjtr/w9+lLsLWxxKhhfRVOLdW8mQWmjBmCPYfPwKVVC4XfXO/U3hmpaRnYc/g0tu8/AfOmjfHuzLFoVkmc9s2t0KWDKz74fB0G9e2GqWOHyh0fObQPNMQaOHLKG4lJz/Fqn65yC79raGhg8bxJ+HnbQXz67WaINTTQxd0FMya+Vum10dFuhPZtHOF3PxRdS60zAwCTRg/C9v0n8MOmvQCAVg7NsWjuRLl59st6b+Y4bNt7HB9/tRFisQbau7TChJHlEybF13zD1kM4csobujramDt1FFqWWkdGGT6+dwEAB49fkNu/atk82FpbYvqbw/H9r7vx05YDcHV2QP9XOuNB+OMatVWWr18QLMyawNqq/KibTu2d4XnlFiaNHowh/TzwMCIav+06hpb2NnhjSG/cD4kQylb32hWrql9XpiZ9tCrDBvTAGa/riE9KRptW9lj2/nThAbQ62lNER0cbs6e8gX1Hz+GM9w20d3FE/56d4VVmHYmKGBroYdmC6Th66iLW/bYPjU2MMGn0YKzfsl+lcdY2hsruzfYujni1T1ds2/cPpEVSDOzdFV1KJU5rorb3T3Xekzr6yKXrfrh03U9u36J5k+DetrVS9Ux441Vs3Xsc323cBUlRERzsrDFv2mgAwOuDeyEmLhFf/bgN+nq6mDJmCMIjnwjn9urWAVduBGD+0u/x4ZwJSE5JQ05OHq7fvo/rt0vWmJo8ejCG9O9e4/daW6aNjbFo3kRs2nEEJ875QFdHG0MH9ECf7u7lylbn95mYlILsnLy6fAtERERERConyszO4xS4RERUK5nZubAwrf+pWf7fZWXnQL/UlFzf/bIbrVvaYtTQPvUYFREwa9EqLJo7USXrWxAR1UTQwbpdv4aISriOv1B1ITVKSE6HgV4F6yESERHVAqcFIyIiagAO/H0e36zfgfjEZGRmZeOM13WEhEWiQx0v3E5ERERERERE9P+A04IRERE1AMMH9kBObh4+X/Mb8vIL0NjYEO/OGIsWts3qOzQiIiIiIiIiogaH04IREVGtcVowIiIiepFxWjCi+sNpwYiIqKHitGBERERERERERERERERKYHKFiIiIiIiIGjSxtnF9h0D0f4n3HhERNWRMrhAREREREVGDZuk2hw95ieqYWNsYlm5z6jsMIiIiteGaK0REVGtcc4WIiIiIiF5EXHOFiIjUhSNXiIiIiIiIiIiIiIiIlMDkChERERERERERERERkRKYXCEiIiIiIiIiIiIiIlICkytERERERERERERERERKYHKFiIiIiIiIiIiIiIhICUyuEBERERERERERERERKYHJFSIiIiIiIiIiIiIiIiUwuUJERERERERERERERKQEJleIiIiIiIiIiIiIiIiUwOQKERERERERERERERGREphcISIiIiIiIiIiIiIiUgKTK0REREREREREREREREpgcoWIiIiIiIiIiIiIiEgJTK4QEREREREREREREREpgckVIiIiIiIiIiIiIiIiJTC5QkREREREREREREREpAQmV4iIiIiIiIiIiIiIiJTA5AoREREREREREREREZESmFwhIiIiIiIiIiIiIiJSApMrRERERERERERERERESmByhYiIiIiIiIiIiIiISAlMrhARERERERERERERESmByRUiIiIiIiIiIiIiIiIlMLlCRERERERERERERESkBCZXiIiIiIiIiIiIiIiIlMDkChERERERERERERERkRKYXCEioloTiUQoKJTUdxhERERERESCgkIJRCJRfYdBREQNlGZ9B0BERC+/RlqaSEnPhlQqre9QiIiIiIiIAMi+BNZIi4++iIhIPfgXhoiIak1LUwwtTXF9h0FERERERERERFQnOC0YERERERERERERERGREphcISIiIiIiIiIiIiIiUgKTK0REREREREREREREREpgcoWIiIiIiIiIiIiIiEgJXNCeiIhUKj4hCbv2HcbZC5eqLCsWizF5/ChMnzy2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+u9W4OdNfyA84jEA2bRsb45+DbOmT8B36zYrHaOqfP7J+3B3c8U13zsIeRCGjMwsOLVuiQljXodDC9uX7iG5uvoEAPTo1gnbfv0e/57zgn9AIGKfJiA/Px/WVpZwadMKgwb0fiFHg6mj/zW0fkNEREREREQ1I8rMzpPWdxBEREREREREREREREQvCy5oT0REREREREREREREpAQmV4iIiIiIiIiIiIiIiJTA5AoREREREREREREREZESmFwhIiIiIiIiIiIiIiJSApMrRERERERERERERERESmByhYiIiIiIiIiIiIiISAlMrhARERERERERERERESmByRUiIiIiIiIiIiIiIiIlMLlCRERERERERERERESkBCZXiIiIiIiIiIiIiIiIlMDkChERERERERERERERkRKYXCEiIiIiIiIiIiIiIlICkytERERERERERERERERKYHKFiIiIiIiIiIiIiIhICUyuEBERERERERERERERKYHJFSIiIiIiIiIiIiIiIiUwuUJERERERERERERERKQEJleIiIiIiIiIiIiIiIiUoFnfARAR0csv+Xkq3pw6T+ExHR1tnDqys44jUt6A4ROwcMFsvDZkQJ21OW32h+jSyQ0L5s1A9JNYLFq6EiNHDMaUCaNrVa9EIsGg1ydj4Xtv47WhA2tV14ZN23Ht5h389vNqmBgb1aqusqbN/hCxcfHCtp6eLtq6OGHwgD7o27u7StuiEnn5+Vi7bjNu+d1FXl4+jh3YCj1dXYQ+jMCyL9fg/Xdmok8vD8yctxjt27bBwgWzhXPf/2g5LMzN8NmSBQDq575Rl+LPsS8/XYjePbvVuJ4/dh7AOc/LOLhrU43r+HHD7/j3rJewrd2oEVq1coB7exeMH/M6dHV1AACe3j749odfhHKammI0s7RABzdXjHp9KGxtmsnVW/aeK+3X9d/AubVjuf2q/Dx5WZXt97VR+nOfiIiIiIhebkyuEBGRyowdOQzdunSU2ycWi+spmpeLgYE+TEyMYWVhXift5ecXYOioqfjog7kYOqhfheWsrCxgZtoEOtraaonD3c0Vk94cBQDIyMzEzdsB+Pq7n5GVnY3hDeCB/Yvo0JETuHjlOsaNfg0O9s2hp6sLADA2NoKJiTHMzU0hEolgaWkOKyuLeo72/5eRkSG++OQDALJ74+KV69h36DjuBT7AujXL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",
    "media_type": "image/png"
  }
}
```

> AGENT

Ich sehe — das Telefon-Feld ist unten immer noch am Rand. 4 Spalten sind einfach zu eng. Ich ändere die Entgegennahme-Zeile auf 2 Spalten.

> TOOL

tool_use Edit
id: toolu_01RGN8mh43We1uDKN7vCshjH
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "old_string": "      <div class=\"krisen-form__section-title\">Entgegennahme durch</div>\n      <div class=\"krisen-form__row\">\n        <div class=\"krisen-form__group\">\n          <label for=\"rufzeichen\">Mein Rufzeichen</label>\n          <input type=\"text\" id=\"rufzeichen\" placeholder=\"z.B. OE8ABC\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"qth\">Mein QTH</label>\n          <input type=\"text\" id=\"qth\" placeholder=\"z.B. Klagenfurt\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"qrg\">QRG</label>\n          <input type=\"text\" id=\"qrg\" placeholder=\"z.B. 145.7625 MHz\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"telefon\">Telefon</label>\n          <input type=\"tel\" id=\"telefon\" placeholder=\"z.B. +43 664 ...\">\n        </div>\n      </div>",
  "new_string": "      <div class=\"krisen-form__section-title\">Entgegennahme durch</div>\n      <div class=\"krisen-form__row--2\">\n        <div class=\"krisen-form__group\">\n          <label for=\"rufzeichen\">Mein Rufzeichen</label>\n          <input type=\"text\" id=\"rufzeichen\" placeholder=\"z.B. OE8ABC\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"qth\">Mein QTH</label>\n          <input type=\"text\" id=\"qth\" placeholder=\"z.B. Klagenfurt\">\n        </div>\n      </div>\n      <div class=\"krisen-form__row--2\">\n        <div class=\"krisen-form__group\">\n          <label for=\"qrg\">QRG</label>\n          <input type=\"text\" id=\"qrg\" placeholder=\"z.B. 145.7625 MHz\">\n        </div>\n        <div class=\"krisen-form__group\">\n          <label for=\"telefon\">Telefon</label>\n          <input type=\"tel\" id=\"telefon\" placeholder=\"z.B. +43 664 ...\">\n        </div>\n      </div>"
}
```

> TOOL

tool_result
id: toolu_01RGN8mh43We1uDKN7vCshjH
```
The file /home/<USER>/bosarsa/src/krisenkommunikation.njk has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01STcG9yoBaQfoewiSugDSPQ
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy 2-column Entgegennahme fix",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01STcG9yoBaQfoewiSugDSPQ
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
src/
src/krisenkommunikation.njk

sent 70,567 bytes  received 9,209 bytes  53,184.00 bytes/sec
total size is 105,226,640  speedup is 1,319.03
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 0.6s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [stage-1 1/4] FROM docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#5 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba 0.0s done
#5 DONE 0.0s

#6 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#6 resolve docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa 0.0s done
#6 DONE 0.0s

#7 [internal] load build context
#7 transferring context: 1.80MB 0.1s done
#7 DONE 0.1s

#8 [build 2/6] WORKDIR /app
#8 CACHED

#9 [build 3/6] COPY package*.json ./
#9 CACHED

#10 [build 4/6] RUN npm ci --production
#10 CACHED

#11 [build 5/6] COPY . .
#11 DONE 0.7s

#12 [build 6/6] RUN npx @11ty/eleventy
#12 1.396 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 1.403 [11ty] Writing […]

> AGENT

Deployed. Die Entgegennahme-Felder sind jetzt auf 2x2 Spalten aufgeteilt — Rufzeichen + QTH oben, QRG + Telefon darunter. Damit hat jedes Feld genug Platz. Ctrl+Shift+R zum Cache leeren.

> DEVELOPER

pdf herunterladen für notfunk konzept needs 2 lines. see aufnahmeformular link

> TOOL

tool_use Edit
id: toolu_01JbDwacrwJrLDjxzPN5A13U
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/css/krisenkommunikation.css",
  "old_string": ".download-card .btn i {\n  width: 18px;\n  height: 18px;\n}",
  "new_string": ".download-card .btn {\n  white-space: nowrap;\n  flex-shrink: 0;\n}\n\n.download-card .btn i {\n  width: 18px;\n  height: 18px;\n}"
}
```

> TOOL

tool_result
id: toolu_01JbDwacrwJrLDjxzPN5A13U
```
The file /home/<USER>/bosarsa/src/css/krisenkommunikation.css has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01EqadRKbbNYgNPGpzNyHXkt
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy button nowrap fix",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01EqadRKbbNYgNPGpzNyHXkt
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

sent 189,558 bytes  received 9,663 bytes  398,442.00 bytes/sec
total size is 105,659,130  speedup is 530.36
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 0.8s

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
#7 transferring context: 2.23MB 0.1s done
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
#12 1.449 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 1.457 [11ty] Writing […]

> AGENT

Deployed. Die Buttons in den Download-Cards haben jetzt `white-space: nowrap` und `flex-shrink: 0` — "PDF herunterladen" bleibt einzeilig und wird nicht mehr umgebrochen.

> DEVELOPER

screenshot is in latest. see the 2 buttons and the differences

> TOOL

tool_use Bash
id: toolu_01TSMX6CqY12ehs3zjRamEey
```json
{
  "command": "ls -lt /home/<USER>/Pictures/Screenshots/*.png | head -3",
  "description": "Find latest screenshot"
}
```

> TOOL

tool_result
id: toolu_01TSMX6CqY12ehs3zjRamEey
```
-rw-r--r-- 1 achildrenmile users  124616 Mar  8 08:36 /home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-36-54.png
-rw-r--r-- 1 achildrenmile users  125851 Mar  8 08:26 /home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-26-44.png
-rw-r--r-- 1 achildrenmile users   71082 Mar  8 08:17 /home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-17-04.png
```

> TOOL

tool_use Read
id: toolu_01SZ4pdcUvUNEkn81A6eop3m
```json
{
  "file_path": "/home/<USER>/Pictures/Screenshots/Screenshot From 2026-03-08 08-36-54.png"
}
```

> TOOL

tool_result
id: toolu_01SZ4pdcUvUNEkn81A6eop3m
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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iIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERERERERKQGPIFA1KGug4iIiIiIiIiIiIiIyN+GUVwadA91JURERERERERERERERP4u1C2YiIiIiIiIiIiIiIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERERERERKQGFK6IiIiIiIiIiIiIiIjUgMIVERERERERERERERGRGlC4IiIiIiIiIiIiIiIiUgMKV0RERERERERERERERGpA4YqIiIiIiIiIiIiIiEgNKFwRERERERERERERERGpAYUrIiIiIiIiIiIiIiIiNaBwRUREREREREREREREpAYUroiIiIiIiIiIiIiIiNSAwhUREREREREREREREZEaULgiIiIiIiIiIiIiIiJSAwpXREREREREREREREREakDhioiIiIiIiIiIiIiISA0oXBEREREREREREREREakBhSsiIiIiIiIiIiIiIiI1oHBFRERERERERERERESkBhSuiIiIiIiIiIiIiIiI1IDCFRERERERERERERERkRpQuCIiIiIiIiIiIiIiIlIDCldERERERERERERERERqQOGKiIiIiIiIiIiIiIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERERERERKQGFK6IiIiIiIiIiIiIiIjUgMIVERERERERERERERGRGlC4IiIiIiIiIiIiIiIiUgMKV0RERERERERERERERGpA4YqIiIiIiIiIiIiIiEgNKFwRERERERERERERERGpAYUrIiIiIiIiIiIiIiIiNaBwRUREREREREREREREpAYUroiIiIiIiIiIiIiIiNSAwhUREREREREREREREZEaULgiIiIiIiIiIiIiIiJSAwpXREREREREREREREREakDhioiIiIiIiIiIiIiISA0oXBEREREREREREREREakBhSsiIiIiIiIiIiIiIiI1oHBFRERERERERERERESkBhSuiIiIiIiIiIiIiIiI1IDCFRERERERERERERERkRpQuCIiIiIiIiIiIiIiIlIDCldERERERERERERERERqQOGKiIiIiIiIiIiIiIhIDShcERERERERERERERERqQGFKyIiIiIiIiIiIiIiIjWgcEVERERERERE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IiIiBTC4QkREREREREREREREpAAGV4iIiIiIiIiIiIiIiBTA4AoREREREREREREREZECGFwhIiIiIiIiIiIiIiJSAIMrRERERERERERERERECmBwhYiIiIiIiIiIiIiISAEMrhARERERERERERERESmAwRUiIiIiIiIiIiIiIiIFMLhCRERERERERERERESkAAZXiIiIiIiIiIiIiIiIFMDgChERERERERERERERkQIYXCEiIiIiIiIiIiIiIlIAgytEREREREREREREREQKUPnSGSAiov8NSSmp8D19Gfcfh0JFVQXuLo7o1KYp1NVUy+0Y4ZHRWLxqC9YumVFuaUpKSknFb8s3oHeX1qhTs3qFHac4qWnpmDRnudRyZWVl/L3op2L3Pe9/Cyf8riIvLw9L506ESFRRufz6rdmyH0YG+ujp4y22PD0jE5PmLMMPw/vB2cFGWL5xxxHcuf8Yy3+dDA11NWH5rIWr0aJxXXg3rV/ksf4L5UrSqfPX8CD4GaaOHfils6KwgjriWM0Kk0Z/I7bu+LkruPcgBDMnDit1+orUI8l2afzMJfhucE9Ud7At9fGLsmrDblhVNUWX9s1lrve7HICAu48wffyQcj92RSvvOvLrsn8QHfMWACASiWBjaQavBrXRqF4tse3S0zNwwu8q7j4MQWJiCpzsrdGxdRNYW5iJbRcZFYOT56/haVgEjA31Ud/DFS0a1y0xH7sOncala3eklvfy6AM+XQAAIABJREFUaVVsmyGvH2Ysweghssvb56rjy9Zsh1VVU/Tq3KrEbb/mdoeIiIiISBKDK0REVGZp6RlYtHIzzE2N0K1jS7z/kIBrt4IQ+vwlfvp+MEQi4MjJi4h6HYuxQ3tXWD7K4xiVNDRgYWYMIwP9UqcRHBqOdf8exIp5k0udBgD07doGJsYGwmelEiIlKalpOHDcD22aN4S7qyMDK6Wkoa4GS3NTPAt/KRZcCYuIgkgkQtiLKLg4VQMAJCQm492HeDjZ28hO7CPJcvU56sP/B0+fR+J20GPUrVWj1GlI3gvWoy+jPNpeSY3r10Jd9xrIy83Dk2cvsOvQaaiqqKBebRcA+d9di1dtRV5eLhp4uMGgii6CHj3F739txYhvusHd1QkAEB7xCivW70TDerUwoEd7hEVE4eipS/gQl4AenbyLywIAwMbSTCogZmpkIHvj/5jv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egbU1dWEN5Xz8vLww8wlGD+in9CjgEqWmpYuNi/LSb+rePIsAhNH9f+CuaL/FaynREREREREReOwYERERPTZrVi/Cxt3HEFqWjrevovDjv0noaGuLva2OBXv4ZMwzFq4Go9CniMrOxt3H4Tg0vVAuDrbfems0f8I1lMiIiIiIqKisecKERERfXZR0bE4cuoiHj4JQ15eHqwsTDG4jw/MTY2+dNa+Grm5uTh3OQB+/gFISEyGupoaWnrVQ+e2zUo9GTVRYaynRERERERERWNwhYiIiIiIiIiIiIiISAEcFoyIiIiIiIiIiIiIiEgBDK4QEREREREREREREREpgMEVIiIiIiIiIiIiIiIiBTC4QkREREREREREREREpAAGV4iIiIiIiIiIiIiIiBTA4AoREREREREREREREZECGFwhIiIiIiIiIiIiIiJSAIMrRERERERERERERERECmBwhYiIiIiIiIiIiIiISAEMrhARERERERERERERESmAwRUiIiIiIiIiIiIiIiIFMLhCRERERERERERERESkAAZXiIiIiIiIiIiIiIiIFMDgChERERERERERERERkQIYXCEiIiIiIiIiIiIiIlIAgytEREREREREREREREQKYHCFiIiIiIiIiIiIiIhIAQyuEBERERERERERERERKYDBFSIiIiIiIiIiIiIiIgUwuEJERERERERERERERKQABleIiIiIiIiIiIiIiIgUwOAKERERERERERERERGRAhhcISIiIiIiIiIiIiIiUgCDK0RERERERERERERERApgcIWIiIiIiIiIiIiIiEgBDK4QEREREREREREREREpgMEVIiIiIiIiIiIiIiIiBTC4QkREREREREREREREpAAGV4iIiIiIiIiIiIiIiBTA4AoREREREREREREREZECGFwhIiIiIiIiIiIiIiJSAIMrRERERERERERERERECmBwhYiIiIiIiIiIiIiISAEMrhARERERERERERERESmAwRUiIiIiIiIiIiIiIiIFMLhCRERERERERERERESkAAZXiIiIiIiIiIiIiIiIFMDgChERERERERERERERkQIYXCEiIiIiIiIiIiIiIlIAgytEREREREREREREREQKYHCFiIiIiIiIiIiIiIhIAQyuEBERERERERERERERKYDBFSIiIiIiIiIiIiIiIgUwuEJERERERERERERERKQABleIiIiIiIiIiIiIiIgUwOAKERERERERERERERGRAhhcISIiIiIiIiIiIiIiUgCDK0RERERERERERERERApgcIWIiIiIiIiIiIiIiEgBDK4QEREREREREREREREpgMEVIiIqsw9x8fDu2Be+p/zKPW2/C1fg3bEvps6cL3P9ir83oMeAUeV2vE3/7kG/wePg3bEvbgUGlVu6AJCTk5N/nU6eK3KbW4FB8O7YF1GvXpfrsUuSl5eH4WN/xLQ5CxXab8OWXej97WiFj3fugj+69h2O24H3Fd63rCJfvkLPAaOwfffBz3K87yfPwW+L/yx2m4qqP/8ly/5cj+Fjf/zS2RDzperbn6s3oe/gsYhPSPysx5XHwBETZJbXy1duolWnfvj9jzVfIFefn+Q9Km1bV5pjkXztpjzkbe/ff8j/HXP56s0yH1NepWkTC34TFfxr22UAhoyahJWrNyIyKrqCciqtrO3El/wNIM9vsf91kvWiIr8Lv+S9JiIi+hwYXCEioq9C4L0H8LtwpdzSW7dxO/oNHie27MGjJ9ix5xBsrC0wcdxwuDg7ltvxvoTMzCx4d+yLk2culLitSCSCmakxqpqbfoacAUaGhtDTrQwDA3259xkzcSYWLv27zMfW1taCnp4uzEyMy5wWfV6y6m1FU6QeycvMzARGBlWgoa5eLumVV90oyqPgp5i/ZBU867pjyoTvKuw4/yXlfY8KyCrDFXWsilYRdaO8/a+29z9NGoMl82dh7oxJaNK4Pi7638CIsVNx/tLVL5YnRdqJ0vwGoPJTUfXixq278O7YF69jYoVlvNdERPS/TuVLZ4CIiEge9tVssHrDNnjWrw1tLa0KOUbBG3szpoyDjo6geCD2AAAgAElEQVR2hRzjv2ze7Cmf7Vi13Kpjy7rln+14hVXR18OGv3//IscmAoBe3TqiV7eOXzobcol69Rozfl4MJ4dq+GXWZCiJRF86S5/F57xHX1N5+Nr8r7b3NZwdYFHVDADQ0LMOenXthAk/zcXyP/9B7Vqu0NfT/az5UbSd+JK/Aejz1gveayIi+l/H4AoREZW7nJwctOk8AJN/GInHT0Jx5VoATE2NMWxgX5iZGuPPNZsQ/OQZdHS00KNLB/To2qHENAcO6Ik585Zi9fp/8ePE4odmiYiMwr87D+DRk6fIysqGWw0n9O/TFY721fLTGjEBr6JjAOQPx1Svjjtu3bkn7N+173AAwLH9m6GupoY2nQdg4rjh6NS+lbDNvoO+WL95J84e2wkgf8iYy1dv4seJo7F1x348efoMNV2cMWRgH9hXsykyr8EhzzB5+jy0bNYIU8Z/Gt4sPj4BK1dvwuMnT2FmagLPuu4YOrAPlJWVhW2eh0di2+4DePT4KTKzsuDm4owRQ/rDysIcfheuYMHSvwAAS1euw9KV6/DPX7/D2qoq2nQegB8njkZ4xEucOnsRA/v1QPcu7fH95DkwMTbErJ9+AJA/VNiuvUdw7eZthEe8RFUzU3i3aII+PXykzuPhoyf4a/1WRL6MhoO9Ldq1aob2bVoUed63AoMwbfZCbF3/h/CA6MjxMzh09BTexL6FoUEVNKjvgdEjBiIuLgG9v81/CzbkaRjOXfDH2JGD0L1Le5lpp6SkYsPWXbgX9Aix797D3s4W/Xp2RoP6HgA+lc+Ce1rw+adJY/D8RSSu3bgNAGjj3RT9+3QTe0hU3DWXV0JiEr6fPBuamhpY+fsv0NCQfls9IjIKew4cQ9CDx4h58xamJsb4YfQQeNarLXYOsu5jSecvy4Ytu3DG7zL2bhMfysWn1xD06tYRA/v3VOg6PXn6DNt2HsD9R09QWUcbnTu0luvaPHz0BGs2bEd4xEtoa2nC2ckBk74fAT3dylL1tnHDevh11mR8P3kObKwt4ORoh70HjsHG2hK/zpos1znJcsT3DFat3Yw50ycgKzNLZj16HxcnVX4BYOYvvyM9PQPLFs4GAIXyVlLZKqgzq/+Yj70HfXH1xm0snPsTpsz8DYB03VCk/hYlPiERU2fOh4GBPhb9Oh0qKuJ/OuzZfxRXb9xGWHgErC2rokF9D3zbrwdEH8vChi27cNH/OiZ9PxJrN2xD7Nt3aNSgLiZ9PxK79x/BGb/LePc+DjWc7TFt8lgYGlQp036y2hXJ+yJvOS6q/BTIzcvD3PnLcf/BY6xaNg+WFuZISkrG3oO+uHErEC8ioqChro5+vbugf++uAKS/ewrKsKxjXb95B0d8z+BxSCiq6Ouhpmt1jBjSHzra+S8XKFIfJcnTRhSU3RrODjh6/CzexL5F44b1MHJIf+joaBf5HVPN1qrYelzgRkAgDh87LZxf08ae6NPDB1palcTyevLMBfie9MPrmDdix5f3XCTbewDIzc3FvzsP4NqN24iKjoGzox1GDOmv8HX6HG2ivCpX1sbCX6ZhwNDv4XfxKnp+/F1V0ncJALx7/wHL/lyPkKdhyMrOhp2tNUYN+wbVnezlOnZx7YSsdmv1H/NltqHylBv/awE4duIsgkOeobKODup61MSoYQNQSVMTQPn+FpO3Dir6W7es+5XH79Gi0iqs8Hdh08aeyMvLw9HjZ3H+8jWEhj5HVnY2WjRrhMk/jIS6mhqW/bkeJ06fBwB8M+wH6Oho4/DuDTLb5bS0dGzcuht3gx4i9u17ODvZo0PbFmjRtJFw/JLaICIiov8KDgtGREQV5ojvGRga6GPqhO/gaF8Nv/+xBvN/XwWX6k6YNmUsGtTzwOp//sXDxyElpuVgZ4Ne3Tri9LlLuP8wuMjtkpJTMGn6PISGhaN75/YY1L8noqJjMOmnXxH79j0AYNrksWju1RB6erpYMn8Whg3sgyXzZ6F3904AgIW/TMOS+bMUHqIlPT0D/+7cj+ZeDTBmxEC8+xCHSdN+xYe4eJnbh7+IxE+zF6BJw7qY/MNIsXW/r1gLrUqamDr+O9RwdsDeg774/Y+1wvr4hERMmv4rQp+Fo3cPHwzo3RXPwl5gwtSfERefAI/ablj4yzQAQO/unbBk/iyYmX4a/mHHnkNQEokwbfJYeDX2lJm/rTv2YeO/u2FR1QyTvh8JK8uqWL9pBzZv2yu2XWpqGhYu+xtuLs6YMn4kNDXUsXTlOpw6e1Hua3f2vD/+XL0JXo3rY/a0CfDp0Bq+J89hz/6j0K2sjSXzZ8HSwhx1arthyfxZReYZyH+Qeu78FTRsUBc/jB6K3JwczPp1SYnjfe8/dBwiACOHDEDD+h7YtusgNmzZJawv6ZrLIzU1DZOnz4OaqiqWLZwtM7ASn5CI76fMwe3AIHTt1BZzZ06CjbUF5i5YLjbUBiD7Ppb2/OVV0nV6GRWNqTPmIyo6BkO+7QOfDq1x9MRZ3Lv/qNh0o169xo+zFsDY2ADTJo3B4G9640XESyz6ONyVZL0d8k0vYd/Aew9x995DDBvUV2y5os5d8MeqtZsxdcJ3aNrYs8R6JA958qZI2fpr3VY4Odph/s8/wt7Opsi6IW/9lUVJWQnvP8Rj+pxFAIClC2ahUiVNsW227z6If7bsgpmpCaaO/w72drbYsecQ/l6/VWy75JRUHDp2Cn17dcbwIf0R9OAxZsxdhDt3H2DowD4YO3IgYt++x+Lla8plP3mVVI5L8vvy1bgb9BBLF86G5ccA2Iy5i7H3oC/qedTC3BkT0a5Nc2zcuht+F/OHaiquDBcW9CAYs+ctRWZWFsaNGozmXg1w7cZtTJ35G3Jzc8t8HvK2EY+Dn+LWnSD06emDnt064kZAIKZ9LBNF1Y2S6jEA3H8YjFm/LkFmVhbGjhyEJg3rwffkOUydNR95eXnCdg+DQxBw+x56de+ILp3a4ozfZfw0e0GpzqWwlX9vxPbdB+Fgb4upE0bBoIo+Fn4MFJUm7YpqExVlYmwIR3tbIV15vktycnIwadqviItPwMihAzBl/Cioqali9q9LkJqaVuzx5GknChRut2S1ofKUm8B7DzB3/nJkZGRi3KjB8GpcH+cu+GP6z4vF0iqP32KK1MHS/tYtz9/IkhS9BpIkvwuB/DkJ/1yzCUYGVTBtylgMH9QXNwPu4u91+W1+r+6dMGxQXwD5PcCL6w09e94SnDl/GZ71amPCuOFQUVHGb4v/xJVrt8S2K64NIiIi+q9gzxUiIqowjRrUxaAB+W+HN/Ssg9PnLqFFs0bCssYN6uK03yXcDXoE1xpOxaaVnp6BIQP74KL/dSxZsRab1iyFqqqq1Ha79h1BZmYmtqxdJrzZ1rZ1MwwaMQGbt+3BT5PGoIazA/yNDKCmqgoPd1dh3zexbwEA7jVdoKaWn3ZOTo7c5xsXn4A1KxfCoIoeAMDD3Q39h4zDjYBAdGjbUmzbV9ExmDLjN9R0rY5pU8YJb3oXqOVWQ/gjv3nThrCztcafazahV7eOsLezwe59R6CqooK//5gP3co6AACvxp4YOnoKzp33R6/uneBe0wUAYGVZVTjPgvPxcHfFyKEDijyXxMRk7N5/DIO/6Y1v+3UHAHg3bwwdHS0cPnYagwb0hJJS/jsaaenpmDhuOLxbNAEAtGzWGL8s+ANr/tmG1i29xHrbFCXowWNYWZhj2MC+wjJry6qwq2YNFRUVeLi7olIlTejr6YndM0nXb97Bg0dPsOL3uXBzcQYAtGrRBGMmzMShY6dQ16Nmkfu61HDEqGHfAACaNKqHxKRknL90FSM/vtEszzUvTmZmFn6avQCZmZn4a9lvRQ5vV1lHGzOmjIO1lYXwEKqRZx107DEYN24FoptPO2FbyftYlvOXV0nXacuOfdDQUMfff3w6x1YtmmDwyEkwLSYwERzyDBmZmRg/ehj09PLfVLa3s4GSKL+cFVVvAeQ/DJw2vkzndfXGbSxevgbjxwxF21bNAAD6eroy65Ei5MmbImWrR5f2aN60ofBZVt1QpP7KkpWVhelzFiIsPAJdfdqiir6e2Pqk5BTs3HMY/Xp3Eeps86YNYWtjib/WbkH3zu1hbmYCAMjMyMScaeOF9jouLh5btu/DsX2bhQexKalp2Lh1F/Ly8oS2sLT7yaukclycVWs34/LVAPyxaI7Y2/BjRw1CZmYWarpWBwA0blgPz8Mj4X/1JrybNy62DBf2z+YdcKnhhGULZwvn1cyrIYaPmYozfpfRrnXzUp+HIm1EHoDZ08YLeaiir4clK9Yi+vUbmJuZyKwbJdVjAFi/aQdcJc6vedOG2LHnEN6++wBjIwMAQE52Dmb++ANUVPK/Q1RVVbBx6268jIqGpYV5qdq7l1HR8D3lhxFD+qNvz84AgBZNG2H1P//iwOETpbpOFdUmloa5mSmiovOHOJXnuyQuPgGvomMw66cfhF4DtdxqIPhJKDQ0NYo9VkntRGGS7ZYkecrNP5t3oU5tNyyaN0PoFeTsaId5i1Yi9Fk4HOxtAZTPbzFF6mBpf+uW529kSYpcA0myvgsBwKdDK9hVs0Zzr0/3MSMzE4ePncak70fAysIc1WytAQA1qjsW+SJCwO17uBv0CL//NhN1arsByP9++nn+MqzZsA2NG9YVrnlJbRCQ3xu4MBVlZakecERERBWJPVeIiKjCFPxRBwBKSkpQU1MVHhwWqKyjg9TU1BLTysvLg7qaGiaOG4Ho12/w764DMre7fvMOGnrWERsyQF1NDc2bNsKNW3dLeSby0derLHbOJsaGUFdXR3x8oth2H+Li8eOsBXB2tMMvMyfJHL5Fckitgj9wg0NCAeRPGurVuL7Y9TQ1MUJNF2cEFdOzp4Ddxz+Ai3L7bhCysrLQ1aet2PI23s2QnJKC5+GRwjINDXW0bN5YKr/JKSmIfv2mxLwA+Q+II6OisWrtZgSHPENWVhY869UWhvuR142AQNhaWwoPwwBAWVkZzZs2xINHT4rdt5qNldhnaysLJCR8undlueY5uTmYO3854uIT8MfiuahcueghLZSUlNCgvgdMTIzwLOwFAu89xKmzF5GTkyOWH0D6Ppbl/OVV0nV6EhKGRg3qigWPDA2qoHYJgYlabtWhqqqKRcv/xq07QUhOSYGjfTXY29mUnCdbqxK3Kc69B4/x2+KVGDow/63y8iRP3hQpW3bViq+7gGL1Vxb/qwF49/4DGnrWweFjp6V6C94JvI+MzEy0by3dTolEIrG2VltbSywQrqGuDlVVVbE33HW0tZCdnYOsrOwy7yevkspxUXbuPYyTpy9g4S/T4ORoJ7bO2dEeNV2rI/r1GwTeewj/awF4HfNG6uFfceITEhEc8gxtvZuKBYxsrS3h5FAN1wPulOk8FGkjbG0sxfJgY23xMY9F99QrqR4XnF8bifOzr2aDn6dPFAIrAODq4iQEVgCgdi1XIQ1Fz6XA4yf536HtWjUXW174IbKiaVdUm1hW8nyXGFTRh0VVM2zdsR/nLvgj9u176OlWRkPPOiXOm1JSO1FYSe1WieUmPhFPnz1Hp3atxPLVtEkDqKur496Dx8Kysv4WU7QOlva3bnn+RpYk7zWQVNx3obGRIZp7NURSUjLu3X+EW3eCcP9hsELtGwBcu3kbhgZVhMBKgfatWyDmTSxeRLwUlpXUBp08cwHd+40Q+/fz/GUK5YeIiKis2HOFiIi+Kp71aqNxw3rYe8AXLbwaSa1PTEqGsaGB1HITY0MkJiaV6g1n+Umnq6yshDzkiS3bumO/kKei8iL5B7aGhjrU1dWRnJL/R3ZScgqO+J7BEd8zUvtKPvCTmdMSrkFSUgoAoGufYTLXv/sQJzz00NbSkkpP9+MY6QX5LUnLZo2RlpaOrTv24/Cx01BSUkIddzfMmTFBGEtdHonJyQiPeAnvjn1lrs/MzIKysux3SyTPQVlJCYVGqCnTNb985SYA6ftalF37jmD/oeOIT0iEtpYWHB1soaamKpYfWXmW5/wLemWVVknXKS0tDZVljIeup1tZalizwoyNDLF0wSysWrsZ0+YsBJD/MGvG1O9LDFCIZNQ9Rfyx6h8A+ePAlzd58qZI2ZKn/VKk/spSqZImli6YDUsLM4z8fhoWLfsbG/5eIgQ2Ch6mmZoYie+nqYnKOtpyBSm+tJLKsSzvP8Rh49bdEIlEyMzKlFp/9cZtbNiyC5EvX0FFRQWO9tUgEimJDXVVkoJrZ2Qk/T1mbGQoBBZKex6KtBGSZVdZKT/QUVz6JdXj4s5PUsHxCqgoFxw/T+5zkWzvU9Pyh7qqrCveFuvpik8Ar0jaFdUmlsar6BixlxJK+i4RiURYumA2Vv+zFYuWrUZeXh50K+tgzMiBaNXCq9hjldROFFZSu1ViuUnMLze/LPxD5v4fPsQVPprUekV+iylaB/+b5LsGkor7LgyPeIl1G7bjVmAQgPyAqCJtW4GExCQYGxlKLTf5+H0SF58I24/LSmqDPOvVxtIFs8W20dGR3SuYiIioojC4QkREX53xY4Zi4IgJWLNhGywtzMTWVdbRRuy791L7vIl9h8qVdRQOrBRsn5MjPsZ2Vrbib0oXaOPdFG28m2HqzN+wduN2jBkxUGqbxKRkVC30OSk5BRkZGdDXy38AVFlHG641HNGlY1upfbWKGPNcEQVBgHlzpsqce6bwW6jJKSnIzcsTe5v07cd7UNwwIZI6tvNGh7Yt8So6BrcCg7B5216s3bAdk74foVC+zc1MMHGc7H1UVJRL9TAAKNs1t7GywLw5UzHhx7n4+belWPH7L2JvZBfmd+EK/o+9uw7LInsbOP6lQQEpKRFskBBFURDFwMbuXru7W9du11h77a7VtQPFbhS7u1FEAZGS9w/kWR/yeRDX3d97f66La9dh5sw5M3PuGc6ZOWf56k106dAKv/I+inPRoHmnVNf/lirlT42GhgbxycaRh8RhedRlbGzEO6WGrkSqNEi5OjuyaM5k3oW+5/qNOyxbvZGxk39jxaKZaudDnTIN6tuVNyFvWbFmM44F8+Hj7Zl+2iTFBeW04jIZF7K6PqtTf1NTxttT0aE1akhvuvQeypwFyxjSv7tS+q9ehyiGZoHEBrmP4RGKztV/Wlafl+T09BKHdpq/eBXjJ89h0dzJig6m12/eMnbSLKpVKs+vI/pj/3Uell8nzlJ5Tib4u2M6JCTlfexNyFuVOiXSTT+TMUId6dXj9MqnrszE+6Rr9+03w49Byq9xsvJe8j0xUR0hb0O5c+8B3SokPlOoei/JaWHG6KF9+RQVxZ27D9i4dSfTfluEm0thrCxTNoInyShOqEuV66ZNy0a4FE45RFZ6+UxLWs9iP7oOZtaPeB5NLr174ejxM7AwN+O3qWNwcXZEU0OD7Tv3M3fhcrX2kcPYiBs376ZY/vp14tC8piaq3z/MTE3Ues4UQgghfgQZFkwIIcR/jrmZKe1bNyXo8tUUw04VcS3MqdMXCI+IVCyLjonhcOAJpTGrNTQ1SUhI2fCanKamJtmzZ+PJs+dKy2/fva92vpP+MHZxdqSYuwsd2zRj6/Y9HD1xJsW6J06dU/r3uQuXE7ctXAhILOfDR09xc3HEo6ir4udd6HtsrK2+5j1xf8knX1VFEbfEOQM+fgxXSt/QMBuamhpKb+F+/hzNxWQT/F4IuoK5mYnKDR5nz1/i3IXLaGhoYJfLhnq1quHj5cml4GuKdTQ1NDI8Z+5uzrx89QZrq5xK+Y6OjsbCwizdeSYyosoxT42GBuTL64CtjRWjh/Xl7v2HzFmwLM31Hz19hqlJDurXrvZ3Q+C7UJWG3shs+Y2NjQgL+8DHjxGKZQ8fPSE6JuXb+RlxdipIUPA1vnzT8PgpKoorV9MfOu3e/UfsPXAESKzjvmVK0axRHZ4+e0HI21BA9XoLqpUpqTHe1dmRlk3r41ncnYnT5/H8xSvFOqnVI5OvjW+Pn/4dF+Lj47n/4LFKeUsus9eWIo/J6oY69Tc1MTGxiv/Pm8eetq2acPDwcU6ePq+U/r6DgUrb7TsUSEJCAu5ff/9Py+rz8i0NDQ2MDLOT1yE3Iwf3xiCbPsPHTCE2NvFYPXv+kri4eBo3qKXoWElISODBI+Uh2DK6hk1yGGNvZ8v+gGNKjfcPHj7h9t0HFHH5vmOblTEytbqRUT1OKt+BZOV78vQ5I8dOU3koycyWJWk+nPMXLystP3VGeainrDxO6sTEd6GqTTieXGTkJ6b9toBsBgaK+c9UuZe8fRfK5j93ExMTSzYDA4oWcaFvjw7ExcUR/M1QW6nJKE6oQ9Xr5sXL10rno2D+PLwP+6DUUZaRjJ7FfnQdzKysfB5NLqN7YXx8PC9evqZieR/cXJwUL9Pcf6gcW5OWp/fc6e7mzNt3oQRdvqq0fO/BIxhmz46DQ+7vLo8QQgjxT5IvV4QQQvwn1atdjQOHj3H+YjAmJn8P59GgTnX2HTxC977DqeNfBT09XXbsPsC70DCaNKilWM/aMichb0MJPH4aB3s78qbzx5yPlyd79x+hUIF85LQw58KlK7z6+oadOhR/pH/9b5OGtbl28w5TZi4gj70dDvZ2inXPXbzMqzch+PqU4lLwNQ4EHKeYuwu5vzbaJZVzyKjJNK5fk09RUVwIusK+g4GKiWm1tbUxMzXhxOnz2Fhb4exUEB0d1W79ZqYm+JX3Yc78ZURGfsLB3o679x+yZ/9hdHV0WDR3iuINZyMjQ35fvJKSJYri7FiQw8dOcfL0edq0bKzysTly7BTHT52jV9d2GBkZcurMBQ4fPUHlir6Kdawsc3Ll+i0uXrqKg32uVOdjKePtiZVlTgYMG0eHNs0w0Nfnxq27bN2+h8oVy9JXja9gklPlmKcmIeHvc+9SuBBdOrRi3sIVuLk4UbliymFXPD3cWbdxO/MWraBYERdiY+P4a89BDDKYXPh7yu/jVYIly9cxcdpcGjeoRXhEBLv3BSgaq9VRt1ZV9h86Sueeg6lZrRKfo6PZe+AIZmbpv1169/5Dps9exKvXIbi5OBF89Qa79wVgl8sGM9PEOq5evc24TElDpCQNFzhqaB869RjMsDFTWDRnMvr6eqnWo/z5EjvLlixfh56uLppamvy1+6BSLFJHZq+tJKnVDVXrryqaNKjFmXNBTJ21kJWFHRXxYd2m7YS+D8OzuLvifHkUdc1wTqcfJavPy7cSEhIU9djY2JAJowfRve8IJs+cz8jBvSnsVIBsBgbMX7IKX59SmJrkYOfeQykaGVW5hhvW82fm3CUMGjGRKn6+vH4Twvad+zExyUGVZHODqCsrY2RqdUOVepy8fKHvw/jzr70YGxmlGGouq8tiYW6GV0kP5i1awe27D/Ao6srps0E8TNYJlpXHSdWYOG/RCnbtDWD21DEZDjV549Zd3oS849OnKK7dvM3ufQHExsYxpH83RYxT5V7yKeozS1es5/KV69SvXZ0Hj56wZ/9h9PT0cHYqqHIZIWWcMFHjCwR1rht9fT3Kli7J46fPOXn6PDdv38OpUH5y2VqrtC9VnsV+ZB38Hln1PJqcKvfCokWc2b5zP58/R5Mvjz0XgoJTdMBZf53Eft/BQEqVKIrrN3MWJSnj7Ym1lSW/TvyN2jUrky+PPYcDT3Lq7EXatW6S4Vw/QgghxL+NfLkihBDiP0lDQ4NBfbqmeHvUPncuZkwahYGBPvOXrGLWvKXEx39h8rihSl+uVK1cDldnR8ZNns2M2YvS3Vfn9i1wLJSfqbMWMHD4eKKjo6njXyVLyjF8YE9yWpgx/NepirHgAcYM68fnz9GMnfQbu/YGUK6MF6OH9lUq58zJo4mJiWXYmCmMnzKH6zfvMKB3Z6WG2G6dWnP5ynUGDh+v9oTmA3p3oUG9GixfvYnBIyeyet1WCuTPw9QJw5UaZo2NEhsaT525wLgps7l46Qrtf2lKi6b1VN5Xn+4dqFjOh7kLljNy7DSOHDtFrRqV6dujg2KdVs0aQEICg0ZMYNtf+1JNR0dHh9nTxuDsVIiJ0+YxYuw0du8LoFaNSvTs2k6t8ien6jHPSL1a1Sjv682MOYtTvPUJiW9W9+3ZkQMBxxg1fgar1m+ldfMGSpMhpyWz5be1saJX17Zcv3mHgcPHs+iPNXRo0wxdXV2Vy5WkUIF8TBwzmOjoGOYsWMaqdVv4pUVDPIu7p7td9SoV6NS2OfsDjjJ45EQ2bPkLp0IFmDVlNFpf51pQp95mpkzZDAyYMHoQIW9DmTBtrmJ58nqkoaHB0AE9iI+PZ9iYKYyZMJMy3p6Z7lT43msrtbqhav1VhYaGBiOH9ObLly+K49K/d2eaNarD4cCTjJ30G7v3HaZWjcr8Ory/+gcgi2T1eUlP/rwO9O/VicBjp9n21z6yGRgwZfwwHj95xtRZC5gycz4lihXB2amQ0naqXMP+1fwY0Lszj588ZfKM31m+ehOOhfIzZ9qvGBl+33wCWR0jk9cNVeqxfzU/BvbpwtNnz5k843fWb9qOX/kyzJg8Sq0vQjJblqEDulO5oi979h9m3OTZhLx9x6SxQ37YcVI5Jn7TEZ+RKTPnM3D4eMZNmc2ly9eoUaUCyxZMp3xZb8U6qtxL7O1sGTuiP6GhYQwaMYGFS1ejra3FjEkjsctlk9qu05RanFCVOtfN2fOXGDh8Ar8vWklcXDxTxg5VuWMlLcmfxX5kHfweP/J59Fup3QuHD+qFSQ4jFixZxdDRk4n6/JkGdWsobWdvZ0ujev6s27Sd/sPGKT3XJtHR0WHWlNGUKF6EdRu3K+53Pbq0oXnjulleFiGEEOJH04j4FJ25gceFEEIIIYQQQgghhBBCCCH+H5IvV4QQQgghhBBCCCGEEEIIIdQgnStCCCGEEEIIIYQQQgghhBBqkM4VIYQQQgghhBBCCCGEEEIINUjnihBCCCGEEEIIIYQQQgghhBqkc0UIIYQQQgghhBBCCCGEEEIN0sU1eVAAACAASURBVLkihBBCCCGEEEIIIYQQQgihBulcEUIIIYQQQgghhBBCCCGEUIN0rgghhBBCCCGEEEIIIYQQQqhBOleEEEIIIYQQQgghhBBCCCHUIJ0rQgghhBBCCCGEEEIIIYQQapDOFSGEEEIIIYQQQgghhBBCCDVI54oQQgghhBBCCCGEEEIIIYQapHNFCCGEEEIIIYQQQgghhBBCDdK5IoQQIkt9+hRF1TotqVqnJRGRkd+V1vFT5+jQfRCVajZjyfJ1WZTDREtXrKdxq65ZmmZmPH7yjL6Df6Va3Vb07D/yZ2cnQ70GjGLC1Lk/Oxv/KTt2H6BRyy48f/GKh4+f0qBFZw4EHP1H89C6Yx/8/Jum+nPrzr0s3df5oGD8/Jvy7PnLLE1XqCYrY9uhI8ep27QDF4KuqLXdu9Aw/Pybcuzk2SzJh0hfQkICHboPYsioSVma7r+hLgccOZFm7OozaIxKafzIZwmRsRlzFuPn35S1G/9M9fdtu/Tn10mz/uFcpS46JoZxk2dTu3E7qtZpyaeoqJ+dpSwTHx+Pn39Tdu09lCXpSZwXQgghEmn/7AwIIYT433L42CkM9PWIi4sn8PgZalbzy1Q6MTGxTJ7xOxbmZvTr2RHHQvmzOKf/DnMXLufeg0d0bt8Ca8ucPzs7/zPOnL/E8DFTWPPHHGysLX/qPi0tzDEzNcHQMDtxcXGY5jDGwtxcadtufYeTO5ctQwd0V2ufi/5YQ+DxM6xfMS/DdYu5u9C8cb0Uy+3tcqm1z/9vYmJiqV6vFQN6d6Z6lQo/Ozv/qJwWFpjkMMbc3PRnZ+Wn+BlxRBXJ44WGhgY21pZY5jTPYMv/rsH9umFhbqa0zMgwe4bb/X95lvgvWLVuKxV8S2NrY5Ul6WX2vpmeTVt3Enj8NI3q1yRfntxkMzDIsrSFEEII8b9JOleEEEJkqSNHT1HSsxhRUZ8JOHIi050roe/D+Pw5mvatm+JbplQW5/Lf48XL11SuWJZ6tar97KyIH8S7VHG8SxVX/Hvp/Gk/JR8mOXLgUdT1p+xb/De5uxVmxaKZPzsbQgXjRg742Vn4oZydCmKXy0bt7f6/PEv821lZWhAZGcWMOYuZMenf+5Xu8xevyOuQmy7tW/7srAghhBDiP0I6V4QQQmSZt+9CuXzlOqOH9iUmNoZJ03/nTchbLHNaKNY5HxTMkJGTWLl4llJDyfBfp/L5czQzJo2kdcc+PH/xCkAxVMTYkQPw8SpBz/6jyONgh7NTQf7afZDXb0Lw8fakU9vmGBkZKtI7e/4Sf+0+wLUbd4iIjMTVxYlBfbqQy9ZaKc/Xbtxm9fqt3Lx9DzdnR9q2bkKBfHmAxCEUqtRuQf9enbhx6y4nTp3D2tqS9q2bYmNtyZwFy7h56x5GRtlpUKcGDerWUKSbkJDA+k07OHX2Ag8fPyWXjTV+FcrQpEEtIHGYjD37DwOwY9cBduw6QIO6NejWsTVRUZ/5Y+UGLgVf403IO5wcC1CjagUq+JZWpL90xXqOnTzLgN6d+WPVRp48fc6f65coju+c6WNZsWYzN2/dxblwQfr26MjjJ89YuXYLj588w9bWmh6df6FoEReVz0tqHj95xsatOwm+eoNXr0OwtrKkV9e2lPIspnQMB/XtysPHT9l3MJDWzRpQv071FGktXbGeAwHH2LR6gdLyWo3a0qieP62bN1SkN7hfNx48esKpMxcAqOLnS/Mm9dDU0FA6ti3b98LIyJDtG5YC8ODhE1Zv2Mr1G3eIiY3FzcWJjm2bY29nm2F+374LZcacxdy+c5/YuDjy53Wgc/uWFHYskOY+MyqTf7VKNG7VBYDbd+5z6Mhxunf6hfp1qtOyfS9evnqT4jh5Fndn8tihSvXEz78pPt6ejB3RP9XzlBFVz7+q9S+5HbsOMHfhckYN7YOvT2ID5+mzF9mx6wA3bt/FzNSEIq6F6di2ueJt9KQ8LZo7mUV/rOXGrTvYWFtRqkRR2rVugpaWliL9jM5rUlrzZ01g07ZdnDxzgfmzJpAvr326sSLgyAkmTk/8Kmj67EVMn72IJfOmki+vPQAbt/zFyTMXuP/wMQ65c+FV0oNWzRqgoaEBpF1PIXGoop17DnLz9j2MjYwo4VGEzu1bKN6UTtp2UN+urFy7hVt37lHExUkpRqXn2vVbzFu8kidPX1CwQF6qVSqX4subjPKQ1nXxrS9fvrBq3VZOnbnAsxevcCqUn45tm6dYLzLyE0tXrudy8HXevH1Hgfx5adawNl4lPRTrJF1fjoXys2nrTvI45E7zmr52/RYLlq7h4eOnGGY3wMmxIP16dsQkhzG79gUwa+4SVi35TSnmvwl5R7M23enXsyP+1fyIi4tj/uJVnD4XxIcPH8mVy5oGdWpQrXL5dONIRmX5nntHejH1XWhYmvGiZ/9RWFlaMGJwL4B041WSJ0+fs3LtFq7fukN0dAxensVo2bR+ivvk+7APrFq3hfNBV7CztaFRPf8UHRU/+npOT1pxe/uu/Wk+S2R071L1GO7YfYA//9rH6zchWJib4VXSg64dW6OpoaHIV98eHahZvZJim83bdrF4+ToO7kwcokzVuBoeHsHCP9YQfPUG4eGReBZ3p0K50owaN52t6xZjksM4xbEZP2UOV6/fYsPK3xVxCWDnnoP89vsfrF46G1sbK7WeOzJzDnV1dalZvRJ/rNzAgYCjVPErl+76j588Y9W6rVy/dYfY2DjcnB1p3qQuhQrky7AepBZDktcPgLv3HtKl91BmTRlNSMg7RayHxHtqgfx5WDRnMvDjrm9Vt1Plev0UFcWylRu5FHyNV29CcHV2pGnDOhRzd1HaZ/yXLyxetpYTp88Dys9PacmqOP89sVEIIYT4t5I5V4QQQmSZgMCT6Ovr4VncHa+SHujr63HoyAm10xnSvzvDBvQAoP0vTZk2YQSuzo6K39+4eYfzF4Np0rAWDev5c+ZcEENGTVb8/vzFYIaNmULYh3C6dGjJkP7diQiPYPivU0lISFCs9+lTFCvXbsbXpxRdO7Ti7v1H9B38K+9C3yvlZ8euA1iYmzKwTxcKFcjH1FkLmDB1Li6FHRkyoDtenh7MX7KKazduK7ZZuXYzf6zagF0uG/r17IR97lwsXraW5as3AdCofk2mTRiBiUkOypf1ZtqEEdTxrwLAyHHTOHD4GKU8i9GnRwe0tbUYP2UOJ06dV8rXx/AIVq3bQlU/3xQNkCvXbsa7VHEG9OlMfPwXJs/4nUV/rKFKJV8G9++GmWkORo2fQXRMjNrnJ0nYh4/0HDCKC0HB1K1ZlTHD+5HHwY4xE2em6BRYu/FPNDU0GNK/O2V9vv/t4S1/7kYD6NS2Bd4lPVi9fhtLV6wHEo9t+1+aAjBsQA/FG91hHz7Sb+hY7t57SOMGtWjRuC737j+iz8DRvA/7kG5+4+Pj6TdkLO/DPtCpXQsG9O6Mrq4OI8dO49OnqDT3mZEcxoZMmzCC3Ha2FC/mxrQJIxTHp26tarRsWl/xU76sNwBOX4e1GdK/O+XLemNikoNpE0bQtmWj7zuoKsqo/iV36Mhx5i5czsA+XRQdK8FXbzJy3HRiYmPp0bkN5ct6cerMBQYOH8+XL1+Utp8+exFFXJ0YObg3VSuVY/+ho0yZOV/xe3XO67xFK3EslJ8JowdhY22ZYazwKObGpF+HAND4a51NGh5qzYZtLFmxHhtrKwb27kKB/HlZu/FPfl+8UmmfqdXToMtXGTNhJtHRMfTo3IayPiU5dOQ4Q0dPUdr28+doVq3bQvmyXnTr2Jq3oe/pN2Qsoe/D0j1Hnz5FMWnG77i5ODGgdycM9PWYPnsR+w4GKtZRNQ8Zmf37H6zZsI2CBfIysE9nzM1MmTQ95TB1w3+dyqHDJ/D2KkGvru34Eh/PiLHTUsznEnT5GpcuX6P9L03TvKafPX/JoBETsbQ0Z0i/brRp2ZhHj58yefrvAPiV80FXV4eDh48pbbf3wBH09fWoWM4HgN9+/4OAwJM0ql+TEUN64+bsxLTfFnLj1p1067SqZVH33pFRTE0vXnwro3gFEB4RSb8hY7l7/yH1alWjbcvGXL95hy69h/L2XahSevMXryJ/vjz06d4eSOyoOHMu6Jtz9mOvZ1Ulj9tpPUuocu9S5RgePHycOfOXUdanJCOH9KFWjcrs2nuIjVv+UjvvqsTVoaMnc/L0ecqX9aZbp9a8CXmruO+lpWqlcl9ffLmhtDwg8CTOTgUVQ3Sp+tyR2XMYGxtHkwa1cHYqyMKlawgPj0hz3fCISPoNHcfd+w+pX7s6vzRvyLMXr+g3eCxvQt5lWA9UiSHJeXxNp3gxN3Lb2TJtwgj69ej4Nb0fe31ntJ2qz1qjx89IPIclPRjQuzNfvnxhwLBxnD57UWl/m7buJCEhgU5tW+BSuBDLV29iybK16eYxq+N8Zp6rhRBCiH8r+XJFCCFEljl89CTeJYtjYKAPgI9XCQKOnKB547pqpePsVBBTkxwA5MvrkGIoowRg5JDeircwzUxNmPbbQl68fI2tjRUuzoUY3K8bFcuVRls78VZnZWlB38G/8ujJM/I65AYg6vNnunVsTd48iW+hO9jb0bP/SE6duUCtGpUV+yvtVYJfWjQEEod42n/oKBXKlVYs8/Eqwf6Ao1wKvo6rsyMfP0awYctO2rRsTKtm9QHwK++DkVF2tu/czy8tGmJvZ4u9nS26OjpY5jRXlPHchctcCr7O1PHDKV7MTbHt6AkzWLB0NT7eJRTljoz8xLCBPTEzNUlxDFs0qY+7W2EAzM1M6TNojOKNXQAba0u69h7G3bsPcHVxUuv8JDE2MmTYgB442NspGpxLlyqOf4M2nDkfpDTUmUdRVzq1a5Gp/aTGxbkQnb8O21GmtCcfwyM4fPQknb5+rZAvrwMAzoULKfK2YfMOdLS1+X3WBHIYGwFQ1qcU7boO4NDh4zSqXzPN/L59F8rzF68YMbiX4k1edzdnbt66i76Bfpr7zIi2tjYeRV3Jls0AUxMTpWu94TdvbMbExNK552AcC+ajdYvExiJnp4Icz2mOro7OPzrcV0b171snz1xgyswF9O7WjqqV/n5Tecnytbg4OzJj0khFOuXKetOh20AOBByjWuXyinWLF3WjVbMGAHgBFuamjJ8yh8b1a1Egfx61zmuDOtUp7+ut+LcqsSLp6y773LkUxzk8IpJ1G7fTrHEd2rdObIAv7+tN3jy5mbdwBfVrV1cci9Tq6ZLl6ylezI3J44Yp3hZ2KpSfcZNnc/feQwoWyAskfjGwYPYkzM0St/Uo6kbztj04cy6IGlUrpnmOoj5/pm+PDvhVKANAxXI+/DpxFguWrKZyxbJoaWmpnIf0PH32gl37AujYtjlNG9YGoIJvaeYvWcXW7XsU650+e5Gr12/x29QxuH2NN5UqlKFbn+H8uXMfJTyKKNbV1dVh5JDe6e735u17RMfE0Ltre0xMEt/WL5A/D5oaie+NGRjoU66MF4eOnKBNy8aK7Q4EHMPXp5TiHnXl2k3K+3pTv3ZirCpdqjiuLo7ky+OAvr5eqnVanbKoe+9QJaamFS++9T7sQ7rxCmD95h3ExMayfOYMxdcRlSuWZeqsBTx5+lxpfpMqlXwV8dyrpAdNWnfj4JHjirfRf/T1DPBLp74pliWfByl53M5pYZbqs8SXL18yPM6qHMPgqzewt7NVxAAAh9y5yJ/PId2ypCajuHr2/CVu3r7HtAnD8Sia+GxQuWJZeg8cnW66JTyKYG5mSkDgCcUXDG9C3nHtxm16dW0HqPfckdlzGB0djZaWFn16dKBzzyHMW7QyzblS1m/eQUxMDCsW/n1tVq1cjl869mH56o0M7tct3XqgSgxJztQkB6ZFc7D/0FEiIj8ppfmjr++MtlMlLpy7cJmgy9eUro8KvqVZ+Mca3oS8U9pfwfx5lZ6fQt+HERB4QrEsuR8R59WNjUIIIcS/mXy5IoQQIks8f/GKe/cfUa6sl2JZed/SPHryjIePn2bpvvLmya00vEUeBzsAwj4kvqWezcCAKn6+fPmSwPWbdwi6fI3A46cT1wn7qNjOxCSHomMFEhur9fT0CPvw9zqA4g9eAE1NTXR1dRSNuEmMjYz49OkTABcuBRMbG0vdWlWV1qniV46IyEgePHySZtlOnb2AhbmZooEjSfXKFXj1+g2PvjmWpibGqXasJM+zvp5eYnm/GTLEyDCxwSLi6xu4maGpqYlXSQ+srHJy7/4jgi5fY9/BQOLj4/mQ7Bjmz6t+Y1N68n1z3iCxYyz5PpM7c/4SZX1KKp07a6ucFHFxIvjaTaV1k+fX3MwUu1w2rFy7hUNHjvMm5B0mOYzxLlU83aE0ssqseUt49z6MMcP7Z3p/R46dws+/qdLPqPEz1E4no/qX5PLVG4yfMpt2rZsodVaGffjIzdv3qOrnq5ROXofcOBbMx+lzym/Z+nh7Kv3bu2Ti/DU3b98F1DyvyRo9VY0VyV0MukJ0TAzVKysPs1W1Ujk0NDQ4c/6SYlnyehoW9pE79x5Qs1olpXPpW8YLPT09Ll+9obTtt3XZytIiMUalkzcg8euM8j4p8hYRGcmLl6/VykN6btxKPAfVKpVPsa9vnTkXRF6H3IoGNwAtLS3K+3pz9fotpXWThlxLj7tbYXR0dJg883fOXwwmIjKSQgXyUSB/HsU61atU5OWrN9y8fQ+AW3fu8er1G6VGzmJFXAg8dprN23bx+MkzviQkULGcD/r6emnuW52yqHvvUCempkeVeHX67EW8SnooDTtlYKDP6GF9FY2zSTzc/25o1tPVxalgfkV+/onrGRIntJ82YYTST8kSxZTWUfU+o8pxVuUYehR15cmzF8xduJybt+8RGxtLKc9iSh1Tqsoorl68fBUzUxOlc6OpqYlf+TLppquhoUGlCmU4fvIccXHxAAQEnkBHR5tKFRO3Vfe5IzPnMOmb4fx5HahfpzqHjhznUvD1VNc9ffYi3qWKK12berq6lPctrRRb06JKDFHVP3F9Z7SdKtdr0jlMXne7tG9JnZpVlJYVc1fujCpaxIWwD+Fp5u9HxHl1Y6MQQgjxbyZfrgghhMgS+w8dBWDMhJSTHx84dDTNN+IyQwPlxmUtzcS5F5JG/AqPiGTxsrUcCDhGXFwc1laWWFlafF0n4ZvtUr5joKWlqbROZoSHRwJQt0n7VH//NvS9UiPgtz58DFeaoyaJlVVOAN6HfeTv98l/fKN+RtZv3sGWP3cT9uEjhtmzU6hgXnR1dUh+CDWyuAMieXpampop9plceESkYn6b5By/DrWVVvoaGhpMnziS+UtWMnnGfBISEshhbES3Tq2pVKFs5gqhon0HAzkQcIzxowZimdM80+kUc3eheeN6SstMTVKO0Z+RjOpfkllzE+cWiYr6rLQ8qTEoZyplscxpkaJzM3mDi76+Hvr6ekREJja6fM95VTVWJPfhY2JDlPXXepkkm4EBxkaGyRrClff54WPi75LmgEguVGlYwpT1RktLkwTSv9gNs2dPUdYcXztXIyI/KYZeUy0PafsUldg5a5xD+RyZ5Mih9O+PERE8fPwUP/+mpCYmJhZdXR0g5fWVGsucFkyfOIK5C5czZNQkILFzbtjAnoqGVXe3wlhZWhBw5ASFHQtw6PAJrCwtlBr+unduQ3bD7Cxfs5mFf6xBX1+P6pUr0KNLmzT3rUpZtLQy//6aqjE1ParEq4/hEVhaqBZPvp3fCEBLW4vYuDjgn7meQbUJ7dW5z2R0nFU5hhXL+RAV9ZmVa7ewfed+NDU1KV7UjVHD+ijm4lBVRnE1JOQd1lYpv4hMbZ6V5GpWr8TGrTs5fe4iZUuXJCDwJF4lPRR5/N7nDlXPYZJ2rZpw7MQZZs5dzOK5KYchTOvatLK04OPHcBISEtI916rEEFX9M9d3xttldL2mdQ5Tkzw+aWtppXu/y8o4/z2xUQghhPi3ks4VIYQQWSIg8CSexd1pXL+W0vI/d+7j8NFTdGrXAg0NDcUfvfHx8UrrxX1tqMkKi5etJejyNYb27463V3H0dHV59PgZ7bupNg/G90pqDB43aqDiq5FvpTdkSA5jI27cvJti+evXIUDmGsNVkZnzEnDkBMtXb6JLh1b4lfdRlLtB806Zy4OGBvHJ5tsAiI+LT2Vt9RkbGeLqXIg6/lVT/C57towbwnJamDF6aF8+RUVx5+4DNm7dybTfFuHmUljRIJ/c95bp4eOnzJ7/BzWr+eFdqrhK26TFJEeONIcR+hH1clDfrrwJecuKNZtxLJhP8QVKUiN/SLKhSgDehLxN0eny4WO40gTbkZGf+Pw5WtGo+D3nNbOxIulaf/U6RGkotKioz3wMj1CUMdVtv/6uTctGuBROOdxJWteSOiIiI/mSkKD0pnXI28TjbWZqgp6ebpbkIek4vH0bqtTxl/wrphzGRtjaWNH36xwGyWlra6W6PD2uzo4smjOZd6HvuX7jDstWb2Ts5N9YsejvDn7/an5s+2sf3Tq15sixUzSs56+Uhq6uDp3aNqddqyY8fPSEQ0eOs2X7Hgo7FcQv2Zc/6pQlsx30WRlTM4pXxkaGvHmbsg6q65+4nrOaqsdZlZjvX82PGlUr8vzFK84HBbN89SYWLl1Dv54dFR0A8fHK94DYTMRVYyND7tx7mGJ58s7o1NjaWOFYKD+HA09ib2fLw0dP6NCmmeL3//Rzh76+Hr26tWfk2Gls3bEnxYsuaV2br9+8xdjYKFMva2hoQPwX5fubKufh33B9q3K9pnUOs0JWxvnvfXlJCCGE+DeSVweEEEJ8txu37iqGW/Eo6qr0U7tGZaXJVJMaRB8/fa7YPj4+nvsPHmdZfp48fY6zU0HK+3qjp5vYiHj/waMsSz8jRb7OdfLxY7jSsTA0zIampgbG3wx1kZy7mzNv34USdPmq0vK9B49gmD07Dl/ni8lqmTkvj54+w9QkB/VrV/v7j+93oYq3+tVlbGxEWNgHPn78e6Lbh4+eEB0To3ZaSY3K306OXsS1MA8fPcXNxVHpvLwLfY+NtVVaSQGJ5dr8525iYmLJZmBA0SIu9O3Rgbi4OIK/DguS2j5VLZOmhgYJCcoNcJ8/RzNq3HSsrSzp3rlNqvnS0NRMsV1mZGW9TOqocXV2pGXT+ngWd2fi9Hk8f/FKsS97O1v2BxxTamh58PAJt+8+oIhLYaX0Tp5WnlA56QsVl6/jsH/PeVUlVmhqpnItfa3j304QD7DvUCAJCQmK+Y5Sk1T+Fy9fK+W3YP48vA/78F1fJyX5/Dmai8kmEL4QdAVzMxOsLC2yLA9FXBPLef7iZaXlp84oD+3m7ubMy1dvsLbKqbS/6OhoLCzM0EzlK8L03Lv/iL0HjgCJwzf5lilFs0Z1ePrsBSFv/56MvWqlcnz8GM6qdVsJj4hUmssnNjaWvQeO8OjxM7S1tShYIC9dO7bG2spSEX9Tq9NZXZZvqRpTU4sX31IlXhVxLcyZc0GER0QqtouOiWHspN84d+FyWkmn8E9cz1lNleOsyjE8e/4S5y5cRkNDA7tcNtSrVQ0fL08uBV8DEoc7yp49G0+ePVfa/+2799XOs5urE69ev+HJsxeKZfHx8Rw6clyl7av6leP8xWBOnr5ADmMjShZ3V/zuZzx3lC5VHB9vT7bv3J/iy6giroU5dfpCimvzcOAJpfk3MqoH3zI2NuLp0xdKy27dyfg8/Buub1Wu17/P4TWlbZeuWK80L0pm/Kw4L4QQQvxXyJcrQgghvltA4An0dHUpncqb9cWLuWGYPbtiMtX8+RywtbFiyfJ16OnqoqmlyV+7D2JikiOVlDOnhEcRNm3bxZoN23AsmJ8XL19z8PCxLEs/I2amJviV92HO/GVERn7Cwd6Ou/cfsmf/YXR1dFg0d0qab2qX8fbE2sqSXyf+Ru2alcmXx57DgSc5dfYi7Vo3+WHze2TmvHh6uLNu43bmLVpBsSIuxMbG8deeg4rJotXl41WCJcvXMXHaXBo3qEV4RAS79wWoNOxJctZfJ33ddzCQUiWK4uriRIM61dl38AhDRk2mcf2afIqK4kLQFfYdDFSatDg1n6I+s3TFei5fuU792tV58OgJe/YfRk9PD2engmnuU9UyWVnm5Mr1W1y8dBUH+1xYmJsxY85iXrx8Te9u7bl247ZiXX19XZydCiXu0zInIW9DCTx+Ggd7O/JmshEsK+tl0lAmSUO3jBrah049BjNszBQWzZmMvr4eDev5M3PuEgaNmEgVP19evwlh+879mJjkoEqycdxPnbnAqzch+PqU4lLwNXbtDaCYuwv2drYA33VeVYkV2tramJmacOL0eWysrXB2Kqio4+s2bSf0fRiexd0JvnqD3fsC8CjqmuHcD0nl19fXo2zpkjx++pyTp89z8/Y9nArlV/pSJzOMjAz5ffFKSpYoirNjQQ4fO8XJ0+eVJnfPijxYmJvhVdKDeYtWcPvuAzyKunL6bBAPHynPK1XG2xMry5wMGDaODm2aYaCvz41bd9m6fQ+VK5alb8/U33ROy937D5k+exGvXofg5uKkOPZ2uWwwM/37mrUwN6N4UTc2bv0LT48iisnNIXGoqzUbtqGjo0Ondi2IjPzE4aMnefX6DcXcGwGp1+msLsu3VI2pqcWLb6kSr5LqTfe+w6njXwU9fT0OBhzj3oNHSpPCq+JHX8+Q+BJH8om5DQz0KexYQO20VDnOqhzDI8dOcfzUOXp1bYeRkSGnzlzg8NETVK7oq0jHx8uTvfuPUKhAPnJamHPh0hVeff0iRB3lynix+c/d9Bv8K/7V/LDLZcPOPQcVwyNmpGJ5H+YvWcX2XfupWqmcUkP3z3ru6NW1Lb906su9B4+wtf27IzzFtamny47dB3gXGkaTBn9/HZ1RPfhW2dIlmTprAUtXrMejqBvPnr/k1Jnzaa7/rX/i+k6PKtfr3+dwluIcnj57kYDAk4wa2ue79v+zE3k43AAAIABJREFU4rwQQgjxXyGdK0IIIb5LQkICgcdO412qONraKW8rmpqalCvrRUDgCfp074C2thZDB/Rg/JTZDBszJXF4iK7tCLp8jbfvQlPZg/paNKnHu9D3rF6/lbi4eDyLu9OxbQv6Dfk1S9JXxYDeXbCyysny1ZuI+vwZPV1dSpUsRo/ObdIdAkdHR4dZU0azaNka1m3cDiQOtdCjSxvq1kw57FFW0dDQUPu8FHEtTN+eHVm8bC1//rUPB3s7enVty5SZCzKVB1sbK3p1bcuiP9YycPh4rCwtGDO8H6PHp5zHJyP2drY0qufPuk3b2bRtJ39uWIp97lzMnDyahUvXMGxM4jjvue1sGdC7c7oN8EnpjR3RnxVrNjNoxAQgcdLcGZNGKuYBSG2fqpapVbMGDBk1kUEjJtCkYW3at27C4aMnAZg9/w+ldW2sLVnzxxwAqlYuR0DgCcZNnk1hxwLMmzle7WMFmTv/qspmYMCE0YPo2mc4E6bNZdzIAfhX80NTU5PlqzcyecbvAHiV9KBbx9YYGWZX2n744F4sX72JsZN+Q0NDg8oVfenWsZXi999zXlWNFd06tWbqrAWcu3CZyWOH4lncnf69O2NlmZOt2/ew98ARtLW1qVWjMu1aNcnwmPhX80NLS4tV67bw1+6DaGho4OrsyJSxQ7Okoc7YyJAJowcxeOREtm7fg76+Hu1/aUrTRnWyPA9DB3Rn8bJ17Nl/mN37AnB3c2bS2CE0btVVsY6Ojg6zp41h4dI1TJw2TzF/Ra0alejYVr2GfIDqVSrw8WM4f+7az5oN29DU1MTTw50BfTqneAu+UsUynA8KpnqVikrLNTU1mTJuGPMWrmD0+Bl8+fIFczMTBvTurJhTI7U6nc3AIEvL8i1VY2ryeNGpbXOl36sUr77Wm98Xr2T+klVoa2tRrowXA3p3TjGXUEZ+9PUMMGXm/BTL7HPnYvnCGWqnpcpxVuUY9uneAR0dHeYuWE7U58/o6+tRq0Zlunb4Oz51bt+CV6/fMHVWYtp1a1Wljn8VZs1bqlaedXR0mDp+OBOmzmHNhm1oaGjQoE51nBwLMH7KHDQ10v8qwMgwO94lPTh+6hxVk01M/rOeOyzMzWjfuim/L16ptNw+dy5mTBrF3IXLmb9kFQAO9nZMHjdU6cuVjOrBt6r4+XLtxm02bdvF+s07KOJamK4dW9G197AM8/lPXN/pUeV61dHR4bepY1iwZJXiHBZxLcyUccMo4VHku/PwM+K8EEII8V+hEfEpWga+FEIIIYQQ/yrng4IZMnISKxfPynAiayHSsnz1JnbtPcTmtYt+2Bv4QvwTQt6GktNC+euMdZu2s2b9NnZvW5mpuUiEEEIIIcT3kS9XhBBCCCGEEP9Tnj57wYuXr9mxaz81qvlJx4r4T3sX+p5fOvbBu1RxXF0cMTc15cKlK+w/FEi5st7SsSKEEEII8ZNI54oQQgghhBDif8r0OYu5cfMOJTyK0LJpvZ+dHSG+i7mZKRPGDGbDlh0sWLKa+Ph4smUzoG7NqnRMZzgsIYQQQgjxY8mwYEIIIYQQQgghhBBCCCGEEGpIf+Y7IYQQQgghhBBCCCGEEEIIoUQ6V4QQQgghhBBCCCGEEEIIIdQgnStCCCGEEEIIIYQQQgghhBBqkM4VIYQQQgghhBBCCCGEEEIINUjnihBCCCGEEEIIIYQQQgghhBqkc0UIIYQQQgghhBBCCCGEEEIN0rkihBBCCCGEEEIIIYQQQgihBulcEUIIIYQQQgghhBBCCCGEUIN0rgghhBBCCCGEEEIIIYQQQqhBOleEEEIIIYQQQgghhBBCCCHUIJ0rQgghvtv5oGD8/Jvy7PnLn5aHZas20rxtDz59iuJC0BXqNevI+aDgf1Ue1dF/6Dj8/Jum+tO515B0t12/eQeVajbj06copeVhYR/x829Ky/a9Umxz8swF/Pybcu3G7XTTfhcalma+/Bv8on5B/wNiYmJZs2EbvQeOplbDtvQeNIZ1m7YTFxenVjrx8fH4+Tdl195DPyin/22tO/Zh7sLlP2XfvQaMYsLUuWn+O6vMmb+Mpm26E/bho8rbLF2xnsatumZ5XrLCjDmL6dB90M/OhkouBF3Bz78pz1+8AuCPlRto0rrbT83Tj7rO/st+6dQ3U8ckOiaGcZNnU7txO6rWacmnqKiMN/oXSUhIoEP3QQwZNelnZ+Wn+VF19F1oGI1bdWXTtl0ADBk1iYHDJ3x3ukmSx8HMxHkhhBBC/Hdp/+wMCCGEEFnBxtqSnBbm6OrqYG5mgomxERZmplmW/pnzlxg+Zgpr/piDjbVllqWblsoVy+Lq7Jhi+ZbtuzHMnj3dbYsXc2PpivVcunIdH68SiuUXL19FW1uLl6/e8CbkHZY5zRW/C756A319PZydCqqUv4Z1a1DK00NpmZaWlkrb/pdERn6ie78RfPnyhVo1KtOwnj/BV2+w5c/dHD95jrkzxqKtLY9T/xbd+g4ndy5bhg7onqXpLvpjDYHHz7B+xbzvSsfGxoqc5mbo6+llUc6E+HH+6fve99i0dSeBx0/TqH5N8uXJTTYDg5+dpXQlj1UaGhrYWFsq3ZeFemJiYqlerxUDenemepUKiuUG+nqYm5liZWkBgK21FfFfvvywfEicF0IIIf5/kdYAIYQQ/xOqV6mg+GM6bx57li+a+ZNz9H2qVS6fYtnFS1dZs2Eb9WtXS3fbgvnzYmRkyOVknSuXgq/h5uLEtRt3uHjpilLjQ/DVGxR1c0ZTU7WPWnPb2eJR1FW1wvyHHTpygqfPXrB84Qzsc+cCoGzpklT1K0eX3kM5fuocFXxL/+Rciv+KRvX8aVTP/2dnQ4j/Oc9fvCKvQ266tG/5s7OSaeNGDvjZWfiflC2bAQtmT1T8u1e3dj90fxLnhRBCiP9fpHNFCCFElgkL+8Ds+cu4cesONtZWlCpRlHatmyh90fDg4RNWb9jK9Rt3iImNxc3FiY5tm2NvZ0tEZCR1m3SgS4dWNKxbA4Dw8AjqNetIqRJFmTBmsCKd9l0HkMchNyOH9Abg7PlL/LX7ANdu3CEiMhJXFycG9elCLltrpTy+D/vAqnVbOB90BTtbGxrV88e3TCnF73v2H0UeBzscC+Vn09ad5HHITQ5jI/bsPwxAy/a9MDIyZPuGpRmWBxKHIxsychKL5kxmw5a/uBAUTG67XCn2q4rV67dib2eLj7dnuutpaGjg7laYy1euKy2/FHydCr7exMbFc+nKdUXnSkRkJPfuP6JKRV+18pOWpDLPnzWBTdt2cfLMBebPmkC+vPYqnafw8AgW/rGG4Ks3CA+PxLO4OxXKlWbUuOlsXbcYkxzGwD9z7D9FRaGlpYWtjZXS8oIF8hKwe0OK9Tdv28XxU+e49+AxeexzUbN6JapVqYCmhoZinfgvX1i8bC0nTp8HoIqfL82b1FNaR9WyzZk+lhVrNnPz1l2cCxekb4+OPH7yjJVrt/D4yTNsba3p0fkXihZxUaStal35Vs/+o7CytGDE4L+HlLt77yFdeg9l1pTRFHEtrNbxPnTkOLv2BnDn3kPsbK3p2K65KqeDHbsP8Odf+3j9JgQLczO8SnrQtWNr3r//QONWXQC4fec+h44cp3unX6hfpzoJCQms37SDU2cv8PDxU3LZWONXoQxNGtRSaZ+tO/ZRDFPj598UH29Pxo7on+q6b9+FMmPOYm7fuU9sXBz58zrQuX1LCjsWABKH+DoQcIxNqxcotnny9Dkr127h+q07REfH4OVZjJZN66c4H9du3Gb1+q3cvH0PN2dH2rZuQoF8eRS/V6WcqcW3tMqS3K0791i9bitXrt/C2MiQ2jUqp1gnPDyCTdt2ceZ8EI8eP0NfT49mjevQvHFdxTpxcXHMX7yK0+eC+PDhI7lyWdOgTg2lDuVr12+xYOkaHj5+imF2A5wcC9KvZ0dF3U9NZq7r5DKqd6lJ65hm9ro7fuocO/cc5ObtexgbGVHCowid27cgm4EBu/YeYta8paxa8ptSuZ6/eEXrjn3o26MDNatX4vGTZ2zcupPgqzd49ToEaytLenVtSynPYkDiEIVVardgcL9uPHj0hFNnLgDKsWjGnMWZvu+pkr6qko6vs1NB/tp9kNdvQvDx9qRT2+YYGRkScOQEE6f//UWZn39TCuTPw6I5kwHYuOUvTp65wP2Hj3HInQuvkh60atYAja95SOt+5WCfiyq1W9C/Vydu3LrLiVPnsLa2pH3rpthYWzJnwTJu3rqHkVF2GtSpQYOvzyxAusc/cYiq1GNVanFW1fxnFHdVuR6XrljPsZNnGdS3KyvXbuHWnXsUcXFKEWu+9eLla1p16E2f7u2p9U1MSEhIoOkv3XFzcVKUJ6OyqCKte8CRwJOK62D67EVMn72IJfOmki+vvUpxKaPrLIkqcTC1OH/46El27jnE7bsPEu95bZuzfM0mChXIS5/uHVQuvxBCCCH+fbSGDR855mdnQgghxH/bi5evOXTkBFev38IqpwUtGtcjLj6eHbsO8OLlG8qWLglA2IePdO0zjIiISBrU9cfN2ZGTZy6we+8hqlQqRw5jIy5evkbou1D8ypcB4PS5ixw9cYZ3oWE0bVwHDQ0N3od9YPHydTRrXId8eR04fzGYoaMnY2hoSPMmdfEt40XQpascCjxBnZpV0NDQUOTxwcMneBR1o1KFMty4dZct23fjWDAfdrlsANh74AgPHj0hLjaOerWrUb6MF64uTliYm3Ip+BrDBvSgVo1KWFlaZFgeA319xX6fv3iJm2thKlcsy6s3b1i9fitOhfIr9puR6zfvsHLtZvp074CDvZ1ieURkJDGxsYqf+Pgv6Oho8zE8gn0HA6lfuxp6erq8eh3CqnVbaFy/Jl8SEjh99gKN6tcE4NyFYAKPn6ZLh1aYmBjz6VMU0TExSunq6uoCEBX1mc1/7sK7pAeFCuZL93p4+PgZHsXcaFjXn3x57Ll85XqG5wmg/9CxXL9xmyp+5ahUoQyXr1znzLkgPnwMp0mDWujr6/1jxz57tmzs2H2AR0+eUtixIIaGaQ/JtnbjnyxduYGiRVxo0qAWEZFRbNiyg0+Rnyjh4U5CQgKr12/j8ZNnOOTORfXKFfgcHc3W7XuI/hxNCY8iQMb15NuyvQl5i3ep4vhV8OHWnfscO3mWU2cuUKNaRSpXLMuz5y/Y/Odu6tepjraWlkp1JTV7DxzBMHs2pca60NAwdu0LoFrl8lhZ5lT5eAcEnmTS9HnY2ljRsmk99A30Wb95B5GfosiXx55SJYqlmoeDh48zY85ialb3o0Fdf2ysLdm0dSfaWlp4FHXF3c2ZW3fuUTB/Hvr17ISba2GyZzNg5drNrFi7mWLuLjSs6094eARbt+/hy5cvFHN3+aZ82fH1KZXi346F8hMV9Zmwj+GMGzkQ75IemJrkSJG/+Ph4uvUZTnx8PC2a1KNcGS8ePHzMth17qVm9Ejo6OgRdvsb9h48VdS88IpJufYYRHhFBbf8qeHq4c/TEGbZs300VP1+yZTMg6PI1rl6/xfOXryhXxouSxYsSEHiSXfsCqFqpnGL4I1XLmTy+pVaW5J4+e0GfgWOIjYujaaM6FMiXh517DvL6zVu0tbWp7Z/YwDhg2DiOnTxHpQplaFy/JoZG2Vm3cTt2uWzIl8cegJlzlxB4/AzNm9SjRrWKxMfFs2z1RjyLFyGnhTnPnr+k14DROBbKR6um9XEuXIgTp88TfOUGlSqWTTV/qt8DjlOvdjWMjQy5FPz1XHx9w1yVepeatI5pZq67oMtXGT5mKuZmprRoUg9jYyP2HTzCpeDrVK9cHjs7G7Zu34OBgb5Sh+nW7Xu4deceQ/p3J/JTFJ16DuZNyFsa1KlBzRqVePsulPWbd+BXvgxGhtkVsejVqzfY2lhRvXIFdHV12LRtF58/R1O8mBt2uWwyfd9TJf20bN+5H3MzU6W6+OLlKyI/ReFfrSK57Ww5dPg4p88F4V+tIqamOfAsXpTQ9+/R1tZm5ODelPMphYW5GWs2bGPZqo0UcXWmSYNaRMfE8ufOfXz4GE7JEkWBtO9XWlparF6/jZCQdzgWzEetGpX5/DmajVv+4uKlq3gUdaN2zSpoaWqyZsM2ihdzwzJn4vFJ7/ibmeZIM1Ylj7Pq5D+juKvK9Rh0+Rq37z7g8dNnlC/rRckSRQkKvsbW7XuoWqkcBgYp64CRkSEXgoJ5/PS5UgfppeDr7Ni1ny7tW5LL1lqNsqRdR9O7B5T1KUUxd1cCAk/QuH5N2rRsTN48udHR0VYpLmV0nYHqcTB5nD9z/hJjJszExtqKVs3qky2bAes2/klkZBS57WzxKqk8xKoQQggh/lvkyxUhhBBZxt3Nmf69OgFQ3teb/HkdmLNgGY3q+VMgfx42bN6BjrY2v8+aQA5jIwDK+pSiXdcBHDp8nEb1a1KqRFHWbdxOfHw8WlpaXLp8jepVKnA48CR37t7HqVABLl66AkDJ4omNsC7OhRjcrxsVy5VWzH9hZWlB38G/8ujJM/I65FbksUolX+rVShxWy6ukB01ad+PgkeNKf9zq6uoovohJki+vAwDOhQspxp5XpTxJalavRPmy3gCUK+NFi3a9CDh6UvEmcUaWrdqIvZ0tZX1KKpbtPXCE6bMXKa1XzN2F6RNHUqJYYkN9UPA1ypXx4sKlK2hoaOBR1A1tbW02b9vF02cvyG1ny+Ur1zHJYUweh8ROmw7dB/L6zVuldH+bOgY3FyeV8pqkQZ3qlPf1VvxblfN09vwlbt6+x7QJw/EomtgAV7liWXoPHK2UdlYe+/DwCL4kJCiln5Rmvrz29OzSlnmLVnDi1Hly2Sa+ZV+0iLNSJ1d4RCRrN/xJ88Z1ade6CQDly3pTtIgzN27eIeGb9Avmz0vnr0PXlCntSej7MAICTyiWqVO2Fk3q4+5WGABzM1P6DBrD2JEDFMPB2Vhb0rX3MO7efYCri5NadSWz0jveCQkJLF62Fs/i7kz6dYiiM8fNxYlR46anm27w1RvY29nSvnVTxTKH3LnIn88BbW1tPIq6ki2bAaYmJooh6z5+jGDDlp20admYVs3qA+BX3gcjo+xs37mfX1o0zHAoPGenghzPaY6ujk66Q+G9D/vA8xevGDG4l2KoOHc3Z27euot+Ko2SAOs37yAmNpblM2co3o6uXLEsU2ct4MnT51iYmwEQ9fkz3Tq2Ju/XhkAHezt69h/JqTMXqFWjslrlTC2+ZWTF2s3o6+vx+6zxijmfKlUoQ5tO/bD+Zi6O7p1/ISYmliKuidekj7cnDx4+4fjJs/iV9wHgyrWblPf1VgxvWLpUcVxdHMmXJzHG3rx9j+iYGHp3bY+JSeKXKgXy50FTI+3zlBXXtTr1LrnkxzSz192S5espXsyNyeOGKb7ucCqUn3GTZ3P33kMKFshL6VIlOHTkBG1aNlZsFxB4gtKlSpDNwAB9PT2GDeiBg72d4l5VulRx/Bu04cz5IMX9L+m4fRuLPoZHcPjoSTp9/Qrle+976aWvjgRg5JDeinhhZmrCtN8W8uLla2xtrDAtmoP9h44SEflJUUfDIyJZt3E7zRrXUcSM8r7e5M2Tm3kLV1C/dnWlLxKT36/i4+MTj51XCX5p0RAA71LF2X/oKBXKlVYs8/Eqwf6Ao1wKvo6rsyPGRoYZHv/UYlVy6uY/vbirzvX4PuwDC2ZPwtzMBACPom40b9uDM+eCqFG1Yqp5rVzRlzkLlvE+7IOis/bw0ZOYm5lSwqOI2mVJS3r3AFOTHIoOR/vcuZSOqypxCTK+zlSNg8mtXrcVVxcnpk8coUi7iGthho+ZkmGZhRBCCPHvp9rA6kIIIYQKvp3DA6BqpXIA3Lx9F0h8e6+sT0lFgwyAtVVOirg4EXztJgClS5Ug6vNnbt6+B8ClK9cp4upE/nx5uBScOMzVxUvXcHYqhLFxYmNkNgMDqvj58uVLAtdv3iHo8jUCj58GICzso1KePNz//oNbT1cXp4L5+fBBeZ18ee1VKq8q5UmS/2sjVZLcdjaEhX1QaT/Xb97h8pXrtG7RUOnLglKexZg+caTST5cO/8fefcdVXf1xHH+xQWWIIKC4t4CICu69U8vKLCubmpmVlVo5clVqZlmppWVmpWlajrTc29yCgHuLOBAHgoLK+v1x5QuXoVzFLH/v5+Ph43G/63zP+a4r388959MdgJIlvPH0LGYMDRYWvpsqlSrg5ORIrZr+psDVzeMZvnuv2S+Jh7z3Zo5yM37dmWH8xKm07PCU2b95C5eYt7m8eZvzc5527orEvaibEVgBsLa2NnoyZSjIY9/rzfd5rFtPs3+Re/Ybyzt3asvCX7/n4+HvUbVKRSZ//zMv9e7P6HGTjKDJztAIrt+4kSNXTttWTXn7jZ5m5y0o0PxlWs0afsRdTrijtmW8AAOM5LlZh05yLmK6R64kJgGW3St36lbHO/b8Bc5fuEjbVk3NjknDenUoVOjWCahr1fQnKvo0Eyb/wL4Dh0lOTqZucJARgMjNjrBwkpOT6dyprdn8Ni2bcuXqVY4ei7K0eXkq5l4U35I+/DjzN1au2cC52Au4ubpQv27tPIdB2rx1J/VCapkNO+Pk5MiwQW+b3QNubq5GYAVMAR8HB1MPLkvbmd/nW1b7DxyhQb06xgtFAI9i7gRlezFctXJFavhX4/SZGEJ37WbDpm2cORvD5fjM6zuohh9r129m7rzFnIiKJi09nRZNG+LoaLp+AwOqYWdnx5jPJ7F9ZzhXrl6lcsXyVKxQNs/6FcR1bcl9l132Y3on111cXDwHDx+lY7tWZtdLk0b1cHBwYFfk3ptlNOHM2XPGd+S+A4c5c/YcbVqahnW0tramXkgtvLw8OXzkOKG7drN0xVpSU1Nzftdle66XKe2bY53sLDlOd1J+bsqVLWX2vMj4IUDc5by/QzOeye1b5/x/iZWVFVu2h5nNz/59lSHrM9ba2hp7ezuztgO4ODuTmJhorJPf438rFtf/Fs9dS67Hom4uZm32Ku5hetbc4j5q1aIRdna2LF2xFoCUlFTWrN9Eq+aNsLKysrgtebmT7wDI33MJbn+d5fc5mFViYhL7Dx6mTYvGZmXXCw7CJdt1JCIiIv9N6rkiIiIFJvsLB0dHBxwcHLhy1fTSIeHKVRYuXs7CxctzbFulcgXA9Mesp4c7O0LD8fH24tTps9Twr87xE9FE7N5HtyceYVfEHmOYhoxyv502k+Wr1pOSkoK3V3G8insAmPUYAMzyvwDY2NqQnJJiNs+K/I3/nZ/2GGVme7lqY2NDWlpavvbz48y5lPDxMn6VmsG9qBvuRd3y2Apq1wxgV4TphdyuiL081Nb0YsPOzg7/6lUIi9hN08b1OHosii6dM5OvVq9a+bZ16tL5IeoGmw9lUSpbXoLsbc7PeYqNvYC3V85fgGbPtVCQx37Ie29y/Xqy2TrZXwoWLlyIesFB1AsOgv6vs3jpKsZP+I6aNarTvk1z4yWNt5dnjvpkZ2Nj/tsWWxsbs+vUkrZZypJ75U7d6nhfvRnkyQj6ZHW74alaNG1IUtI1fpz5GwsWLcPa2praNQMYOugtY2is7BISrgLQ+cmXc11+/uKlW760t4SVlRXjRn3A19/9yJjPviY9PR1XF2dee+U5WjXPfTir+IQrFPcodtuybXLp5WBjY22cM0vamd/nW1ZJSUm4OOc8Z26uLpw5e86Y/nvLDqZOn0XUyVPY2tpSuWJ5rKysza6tPr1eoHCRwvwwYy6Tv5+Bo6MD7Vs35/VXXwCguKcH40YNYcLkH3h/6GgAypUpxaABb+QZGCqI6/pu7rvsx/ROrrvL8aaX1yNGj891m4sXLwEQUqcmri7OrFqzkWpVKrJyzQZcXZyNoZXA1CPqt/l/Enc5niKFC1O5Ujns7e3Ifihy3KvW1jnWye6unr35KD832Y+vjbXpe/xWZeX1TC7k5ISLc5EcgQ5L8n7cTn6P/63cbf2zPnctux5zHgcbG2vSybvyhZycqBdSi9Xr/qbbE4+waesOrl27Tsf2re6oLXm5k+8AyN9zydTyW19n+X0OZnUu9gIAxW8+j7JvJyIiIv99Cq6IiEiBiU+4Qsks0wlXrnL9+nXjpamLcxH8q1fmkQ5tc2xbOMuv1uuF1CIsYi/eXsUp5VsCby9P6tetzcI/l3PseJSRZyLDt9NmErprNwP79aF+vdo42Ntz/EQ0L7/W/5611ZL23I2Dh4+yMyySgf37WPzyp1agP0tXrOXg4aPExV2mdpZfwgcF+rNw8TL27DsIYOT7yK9SviVuOURSbvJznlyci3Dw8LEc28Zle/lSkMf+VsGk/QcPY2trmyOZb8d2LflxxlwOHj5K+zbNjcDi2ZjYfA1vciv38rq603vFygpS01LN5mUPSuZHxsuki5cu5VgWn+1XxLnp0K4lD7VtwanTZ9keGs4PP89h8tQZvPNGz1zXzzgvHw4dYPTsySqvX6vfKU8Pd4YNfJvEpCQOHjrKr78v4tMvphDgV8142Z+Vi3MRzp2/cNf7vdftdHFx5sLFnOcs630Zc+48I0ePp12rZowY0s9Ibj5i1HguZekpZm9vxysvPs1L3Z/k2PEoVq7ZwG8L/qJa1UrGED3+1asw5asxXLh4iT17DzLt518ZOeYLpk/5PNf6FcR3QEHed3dyPlxv3hsvPPsEftWq5Fiecf1YWVnRtlVTlq/eQO+e3Vm7YYtZT7BVazbyw89zeLVHd1o2a2jU5fGnX7GoDXn5J773CkJez+SkpGvEJ1wxjndBK6jjX5D1/yeeg21bNWPw8E84ERXNmnWbqFK5glHvgmyLpd8B+X0u5Ud+noPZubqa2n7xYlyOZXfSi0tERET+fTQsmIiIFJiNm7aZTW/bsQsAv2qml9c1/Ktx7PhJAvyqUKumv/HvwsVL+Hhn/sFdL6Q2+w8cYvvOcIJrB5qVMWvuQjw93M03go4gAAAgAElEQVSGwIg6eYrqVSvRrEl9HG4mXj9y9HiBti1jmJasPR7y2567Me2nXynh40WLbMNi5Uftm3lX/vhzBfb2dvhXr5plWQCX4i6zacsOSvuWoJh70QKp763k5zwF+FflbMw5oqJPG/NSU1NZuWaD2Xr/xLEH+HnWPPoP/DDHC5VTp89y8VKc8dKoxs28J8tWrjNbb9Xavxn35ZR891KCe9u2O71XXFycOXnytNm8/QePWLz/om6ueHsVZ0dohNn83Xv2k3Dl6i233bo9jG07dmFlZYVvSR8e7dSOhvWCCQvfbaxjbWVFenqWe/TmeYmPTzA7lkWKFMLa2irXXyHnxsra2qzc3Jy/cJG58//kxo1kCjk5UbOGH2+/3oOUlBTCbw7plF0N/2ps2RZq1vbrN24wcvQXxvMzPwqqnXmpXrUSoeG7zXITJSYlERGZOQxU9KkzpKSk0vXxTsYLzPT0dI4ezxxyKDk5mSXL13D8RDS2tjZUqliO3j2fw9urOKG7IgE4fOQ4S5avAUxDrTVpVJduTzzCyejTxJ6/mGv9CuI7oCDvuzs5H26uLpT2LcHpMzFm21SqUJZLcZcp7pnZw6ld62bExV1m0V8riYu7bDYc4fGT0RR1c+Wxh9sZz6fzFy7mGAIpP+7X915ByDgHGUNVZVi6ci3p6elGrqqClt/jn/1ZlV1B1v9ePx8AQmoH4urizN9bdrBleyhtWzYt8Lbc7jvA2jrn9Zqf51J+5ec5mF1RN1dK+HjleJ5v3rrzju5JERER+fdRzxURESkw23bu4uy5WJo0rEtY+G6Wr9pAUKCfMVzU44+0Z+mKNbw/dAxdH+tIYlISO0IjWLpirVkS6DpBAdjY2LJ2w2bGfDgQMI1jXqdWDVat/ZsO7Vqa7bdOrRrMmbeYGbPnUaVSBU6fiWHF6vUF2raMZKVLV6ylbp2a+PtVzXd77tTBw0fZvjOcd9/unWfOhltxc3OhXJlSrFm/iUD/6tjaZg6JVq1KRQoVcmLV2o05cuXcK/k5T00b1WPu/D95570RdGjXEt+SPiz6a4UxtFyGe33sM3Tr8jBvvTeCnn3e5dUe3fEo5s7pszHMnruQkiW8eeJRU/Jm96JutGzWkJm/zufCxUsE1w7kwKGjzFu4hIfaNMfa2tpIkHw797Jtd3qvNG4Qwtjx3zB1+ixq1Qwg+tQZNm3Zfkd16NyxDZO/n8HVxCRaNG3IkaPH2bh5+y2HuANYs34TGzZt483eL+HsXIRNW3awet1GWrdoYqzjVdyTiD372RkWSZnSJfEo5k7LZg356utpXL2aSJnSvhw6coy/lq3G3s6OKRM+Mbsv8uJd3JPY8xdZu2EzZUr75pogPTHpGlOnz2JXxB4ee7g9R49H8dey1Tg4OFC9aqVcy804133eHswjHdrg4OjAilXrOXz0OK+89Mxt65Uh4/q7k3YePRbFuo1baNe6mZGAO7vOndqybOU6er3xHh3bteLa9essWb4G9yy5GapVrUghJye+/u4nmjSsS1E3VxYtWWn2otPGxoYZs+dhZ2fHKy89w9Wriaxe9zdnY84RFPgEAIeOHGPcl1M4GxNLgF9VwiP38ufSVfiW9MG9aO5DxxXEd0BB3nd3ej66PNqBzyd8h6OjA40bhHDi5Cn+3rydfQcOU7VyBUqW8AZMuUuqVK7AL3MWUKVyBcqU9jXKCK4VyC+/LmDilOkE1fAjOTmFP/5agZOTo0XHA+7P915ByTgHv8xZwMVLcQTXDjSupVo1/XPkKCko+T3+uT2r7lX97+b5kF/W1ta0bdWUBYuWkZaWTossieILqi23+w6wtbXFvagbGzdvx8fbi+pVK+XruZRf+XkO5ubl55/io0++ImnYNVq1aMThoydYs25TjqF0RURE5L9JwRURESkwwwe9w9ff/cTI0V9gZWVF6xZNeK1nd2N56VIl+XzMMCZPncGg4Z8ApuGl+vftZfZCxtbWlqAa1QmL2EvNgOrG/OBagWzctJ26WcaWB3jmyUe5cPESP8/6nZSUVIJrB9LzxWd45/0RBda20r4leOLRDvwyZwFz5i1i/uyp+W7Pnfpx5m94ehajdcsmt185D0E1/Tm2cEmOhKtWVlbUDKjOpq07qRUYkMfWBSs/58nOzo6xHw3m47FfMWP2PKysrHj8kfZUrVKRjz75CmsrU6fbe33sM/j7VeXzMUNZu34zvy/4i5OnzlC+bCmaNqrHk48/TOHChYx1+/XthZeXJ7/P/4sly9dQsoQ3fV55Lkcw8HbuZdvu9F5p07IJu/ceYM68xcyau5Aa/tXo3bM7vfsOsrgOjz9qyu/z8+x5bNkWSnFPD8aMfJ9R4ybecru3+vTAzs6OCd/8QNK1azg6OtDpodb07pH5jOne7XHeHzqKd4d8zJNdHuaVF5+mf99X8fLy5Ief55B07RoO9vbUDQni9V4v5PuFYtvWTVm1diMfjvmSalUqMvHzj3KsU9q3BCOH9GP6jLm8O+RjwJTo/LPRH+Bb0ifXcjPO9aRvf+Tr737C1taGpo3q0b9vr3zl78nqTtu5edtOfv19EV0e7ZDnOpUrlmfU8PeY9O2PfPXNNBwdHejftxf7DhwmdJfpV+OFnJz45KNBjPp0AmO3heLm6sJzT3ehkJMTMediAdML2E8+HMTEydMZ9tFnpKWlUczdjf59exl5adq3aU58fALzFy9jxux5WFtbE1wrkP5v9cqRMytDQXwHFPR9dyfno0O7ltjY2PDTL7/xx58rsLKywr96FT4ZOdAIrGRo3aIxEydPp1vXR8zm1/Cvxttv9OTbaTOZ/8dSypT25c3eL/LJ599Y3Ib78b1XkPr17YVXcU9+X2B6Jtva2tLpoda81P3Je7bP/B7/3J5V97L+BfEcvJ22rZoxZ95iGjcIwblIYbNlBdGW/HwHvPbKc4wd/w3bduxizMiBBNcOvO1zKb/y8xzMTbPG9blxI5lJU35k644w4ztv+Kjxxv9pRERE5L/L6kri9YLJXioiIiJSAGLPX8TTw/xXvL/MWcCMWfP4c96PBZp4WOT/3ehxk4g5F8sXY4ff76qIiDxw0tLTiYu7bNY788aNZB7r1pOnn+zM010738faiYiIyN1SzxURERH517hw8RLP93yL+nVr4+9XhWJFi7IjLIJlK9fStHF9BVZECtjJU6cJrhV4v6shIvJA+vrbH1m3YQsPd2hN2TKlOH0mhlVrNnL9xg0a1Q++39UTERGRu6SeKyIiIvKvEha+h9m/LSQsfA+pqakUKuTEQ22a0/PFp7G11e9CRApSpydeZMzIgfhVq3y/qyIi8sBJSrrGzF/ns3LtRmJjLwBQpVJ5+vR6Qc9dERGRB4CCKyIiIiIiIiIiIiIiIhZQBjURERERERERERERERELKLgiIiIiIiIiIiIiIiJiAQVXRERERERERERERERELKDgioiIiIiIiIiIiIiIiAUUXBEREREREREREREREbGAgisiIiIiIiIiIiIiIiIWUHBFRERERERERERERETEAgquiIiIiIiIiIiIiIiIWEDBFREREREREREREREREQsouCIiIiIiIiIiIiIiImIBBVdEREREREREREREREQsoOCKiIj8a0WdPEWXZ3oxY/a8+12Vf9wb/Yby0Sdf3e9q/Cs81/MtJkz+4X5XQ0RERERERETEoOCKiIj8axUpUhg3N1d8vIoDcONGMi07PMWS5Wvuc81EREREREREROT/me39roCIiEhe3Iu6MXXS2PtdDRERERERERERETMKroiIyF175fX38CruwYdDBxjzerw2gNjzF1nw61SsrKwA+OrraazZsJn5s74D4OixKH6e/Tt79h7kRnIyAX5V6fni05T2LQFAamoqbR5+hrdf74GToyOjxk0EYNyXUxj35RS+mziW8uVKc/VqIlN/nMWu8D2cO3+BihXK0a3Lw9QLqWXU541+QylbxpcqlSsw5/dFlC1TipFD+pGens6PM39j89adRJ8+Q5VKFXirz8u8+Go/PnivL82a1AfI1z7yW1Z6ejqz5ixk09YdHDtxkpI+3rRs3ognH++U49guXLyc3xb8SVxcPP5+VXima2f8/aqa7fN2ZWW0vXrVSvzx5wpizsXSsH4wr7z4NM7ORXI9pxs3bWfYx58xZcIYKpYvC8D6jVsZMXo8vV5+lq6PdQQg4cpVHn2qB2/2fomHO7TOV32mTp/F+r+30r9vL77/6VeiTp4yromVazaweMkqDh4+hm8Jb3q+9HSOut2rNouIiIiIiIiI5JeGBRMRkbtWL6QWYeF7SEtPByAuLp5jJ05y5epVDh05ZqwXFr6bhvXqmNa5HM87A0dy6PAxuj7eiWe6dubwkeO8NWAYl+Iu59hHraAARo94H4Cuj3Xk04+H4ONtGi5s8IixrFy9kfr16vBm75dIS01lyMhP2REaYVZG6K7dhO3azcvPP8WLzz4BwHfTZzFj9jwqlC/DgL6v4uHhzrCPP8+x//zsI79l/ThzLt//NBvfkj6888YrlC5Vkm+nzeSHn+eYrbf/4GFmzV1Au9bN6PFiN2LOnee9oaM5duKkxWXt3XeQ7TvDebJLJ7o82oEt20J5f+iYHHXLEFKnJnZ2doTu2m3MC4swfQ6P2GPM2xEaTnp6Og3q1baoPvEJV/jpl99o27IJI4f0A2DV2r8ZPW4SNjY2vNXnZWoFBfDZV98Sn3Dljo6fpW0WEREREREREckv9VwREZG7Vi+kFjN/nc+Bg0eoVqUioeGRlPYtgYeHO6G7dlO5YnkuXLxEVPRpXnr+KQBmz12Ina0tk8Z/jKuLMwCNG9blpd79Wbl6A0/c7BmRoaibKzVr+AFQulRJatX0B2Dz1p1E7tnPF2OHE3CzR0er5o147a3BzF+0lDq1ahhl2Nvb8cH7fY3pxKQkfl/wF0937cxLzz0JQLMm9Zny/QyiTp4y1svPPvJbVnz8FWb/togXnu1K926PAdCyWUOcnQuzYNEynn+mC9bWpt8+XLwYx3eTxlKyhDcAbVo0oUefd/n+x9l8NHSARWWlAx+839foReRe1I1Pv5jM6TMxlPDxynFO7e3tCAyoRmhYpNFLJSx8D492asfSFWtJT0/HysqKnWGRlC9XGo9i7hbV5+rVRAYNeAP3om6m+qWn8+20mQTXDmT0iPeNegb4VWXoh+Pu6PhZ2mYRERERERERkfxSzxUREblr1apUxM3NlZ1hpl4cobt2U61qJapUqsCucFMvhx2hEdja2hBSpyYAW7aH0bhhiBFYAfD28qSGX1XCd+/L9763bAulXJlSRtADwMbGhmZN6hO5Z7/ZuuXLlTabDgvfQ0pKCm1bNTWb37ZVM4v3kd+ydoSFk5ycTOdObc3mt2nZlCtXr3L0WJQxL8C/qhFYAXBycqRxwxAOHjpicVnlypYyggwAZcv4AhB3OWcvoQz1Q2oTvnsvqampXLh4iZPRp+ncqS3Xb9xg/8EjRrvr1gmyuD5F3VyMwApA7PkLnL9wkbatmprVs2G9OhQq5HRHx+9O2iwiIiIiIiIikh/quSIiInfNysqKkNqB7AyL5NmnHiNi9z66PfEI7kXdmL9oKWnp6YTu2k0N/+o42NsDplwdCxcvZ+Hi5TnKq1K5Qr73HX/lCsdOnKRlh6dyXX7jRjL29namemJltiw29gKAMbxYBjc3F4v3kd+yEhKuAtD5yZdzLev8xUtUrFAWABdn5xzLXV2cuXI1yeKysrfdxtoGgJsjueWqft3aTJj8AxG793Ph4kU8irnjW9KHyhXLExG5FzdXF87GnDPyzlhSH7LV52qiqU3ORXLmQynq5mp8vtdtFhERERERERHJDwVXRESkQNStE8TozyYSFX2aU6fPUjc4CBdnZ9LS0jhw8AihuyJ5qsvDxvouzkXwr16ZRzq0zVFW4Sw9FW7H1cWZEj5evP16z1yX29ra5Lmti4vpRf75Cxcp7ulhzI+Li7d4H5aUBfDh0AE4OjjkKKtC+TLG54RsuUYyyi96M2BjSVl3wqu4B6VLlSQsfDex5y9QL9jUQ6VeSBBh4XtwdHKkSOHCVK9W+a7r4+ZqatPFS5dyLIuPTzA+3+s2i4iIiIiIiIjkh4IrIiJSIEKCa5KeDrPmLKBi+bLGkE81a/gx/48lXLwUR/26tY31a/hXIyx8NwF+VbCzszPmr1i9gYrly+a6D2trU0+EtLQ0Y15gQHUWL1mFt5enWR6NzVt3UrKkj5F/Izc1/KsBsGVbGA93aG3MX7pijdl6+dlHfsuqEWBaLz4+gQatM4/HwcNHSUxMwsU5s+dGxJ79JCRcwfnmvPT0dHaERlC1SkWLy7pT9YKDiNyzn5hzsfR55XkAQmrXZNachdjZ2VI3JAjrm0Nv3U19irq54u1VnB2hEbRpmTm02u49+0m4ctWYLug2X4q7jKuri9EGEREREREREZH8UHBFREQKRCEnJwL8qrJ81Xq6PfGIMT+4dk0mTZmOb0kfs8DE44+0Z+mKNbw/dAxdH+tIYlISO0IjWLpiLUPee5PmTRrk2IetrS3uRd3YuHk7Pt5eVK9aiUb1g/Eq7kn/QR/S44VuODk6snf/IX5f8BetWzTm7Tdy720C4FHMnUc6tOGbqT9x8PBRgmsHsmnLTg7czGmSIT/7yG9Z7kXdaNmsIV99PY2rVxMpU9qXQ0eO8dey1djb2TFlwidGb5vinsXo884Q2rdpjnORwixeuoroU2cY0LeXxWXdqfp1azNn3mKsra2pHVQDgMqVyuPo6MCmrTsZNOCNO2pbbjp3bMPk72dwNTGJFk0bcuTocTZu3m6Wm6Ug2xxz7jw9+gygds0Ahg9+5w6PkIiIiIiIiIj8P1JwRURECkzd4CB2RewxktYDhNQOZBKYzQMoXaokn48ZxuSpMxg0/BMASvmWoH/fXrkGVjK89spzjB3/Ddt27GLMyIEE1w7ky0+HM3nqDEZ9OpH09HRcXZzp9FArer74zG3r/HrvF7G1s2X+H0tZsnwNgQHVGTX8Pbr36IvVzZ4ydnZ2+dpHfsoC6N/3Vby8PPnh5zkkXbuGg709dUOCeL3XC2aBgQC/qtQLqcXoTyeSdO0aXsU9GDmkH/5+VS0u604F+FWlUCEnKlc0BVTAlGOnVs0A1m7YTN1g8/N6N/V5/NEOAPw8ex5btoVS3NODMSPfZ9S4iQW2jxzSIR0lYRERERERERERy1hdSbyuNwoiIvJ/KzHJlEi9kFNmnpe9+w/xRr8PmPDZh1SvWum+lCUiIiIiIiIiIv9e6rkiIiL/1/oOGIaDvT2NGoRQqqQP+w8eYemKtXh7eVK1coX7VpaIiIiIiIiIiPx7qeeKiIj8Xztz9hw//fI7GzdtIzEpCVtbW0JqB9K3z8t4FHO/b2WJiIiIiIiIiMi/l4IrIiIiIiIiIiIiIiIiFrC+3xUQERERERERERERERH5L1FwRURERERERERERERExAIKroiIiIiIiIiIiIiIiFhAwRURERERERERERERERELKLgiIiIiIiIiIiIiIiJiAQVXRERERERERERERERELKDgioiIiIiIiIiIiIiIiAUUXBEREREREREREREREbGAgisiIiIiIiIiIiIiIiIWsL3fFRARkQfD2ZhYxo7/hphzsZyNiTVbFhhQncCA6jz/TJf7VDsREREREREREZGCo+CKiIgUiJ9++Y3wyL25LguP3GssU4BFRERERERERET+6xRcERGRArFs5ToAPh8zlMCA6jmW/fTLb/z0y2/UrFE9x3IREREREREREZH/EqsridfT73clRETkv69lh6cAWPXn7FyX/zjTFFzJr8CA6rz7dm+8vTwLpH4iIiIiIiIiIiIFRQntRUTkH/H8M1147uku+Q6WhEfutSgYIyIiIiIiIiIi8k9RzxURESkQt+u5YollK9cxdvw3ty3v6LEoer7+bq7LHB0dKOZeFB/v4jRuEEKLZg0p5OR013XLKnTXbgYM/siYHvPhQIJrBRboPuTeSEtP57f5f7J95y4OHz2BrY0NlSqUI6ROTTo91AobGxuLyuv8VA8SEq7kmG9ra0PRom4U9yhGcO2atG/TDI9i7gXVjH+lt98bQcTufQD4VavMV+NG3uca3VrX7r25cPESAK2aN2Zg/z73uUYiIiIiIiLyX6CcKyIi8q/TtlVTI7hyp65du86p02c5dfosO0IjmDp9Fu/360O9kFoFVEspCO8PHc32neEAlCtbmqmTxt7zfaampvLByHFs3RFmNn/rjjC27gjj2ImTvP16jwLZV0pKKrGxF4iNvcCefQf56ZffeOHZJ3i6a2esrKwKZB8iIiIiIiIi8s/TsGAiIvKPeu3twbz29uB/fL8JV64yeMRYlixf84/vW/5dFv210iyw4unhTqFCmb2aFi9ZyekzMfdk32lpaUz76Vc++fzre1K+iIiIiIiIiPwz1HNFRET+UQcOHrlnZb/Z+yUe6dgGgHOx5zl2/CSRe/Yzd/6fpKSkADBh8nQC/KriW9LnntVD/t22h4Ybnx/p2IY3e7/EjRvJjBj1OVu2m4IuobsiKeHjdUflN2lUl2ED3wZMQb1jx6M4cOgoc+ct4sLFOABWrN5AcO2atGzW8C5bIyIiIiIiIiL3g4IrIiLyQCru6UFxTw/qBgdRO6gG/Qd9CMD169f5adbvDOr/eo5t9uw7yPKV69h74BCnTsfg6GBPyRI+1KrpT/s2zfH28sz3/tPT0xn28ef8vXm7Ma9/3160b9M8X7laXny1H1EnTwEQXDuQMSMHAvDDz3OYMXseAFUqlefrL0Yxb+ESFv21grPnYvHx9qJ1i8Y81eVhrKysCAvfw48z53Ly1BmSk5OpWrkCD7VtQbPG9XOtd8KVq/y1bDVbt4dxMvo0SUnXqFypPH7VK9OpfWuKexYzWz97WxbMnkr06bPM+X0Re/cfIjExiUoVTblMnny8kzEU1tTps5g1d6FZWceORxm5ez79eAi1avoby6JPneGv5WvYFbGHk9Gnsbe3p0rF8tSpVYP2bZrj5OSYj7NikpR0zfgcFGjah729HZUqljeCK2lpBZOSzrlIYWr4V6OGfzVaN2/Mi737ER+fAMB303+hRdMGOYYHS0xMYsnyNWzZHkbUyVPEJyTg6VGMCuXL0LRhPZo1yTx34ZH7eOf9EcZ0757P0aXzQ8b0lu1hDB7+iTH99fiPqVK5gjH91dfTWPjncmP656lfUsLHi7feHU7knv2AKQD16svdmTt/Mev/3srJ6DN4eRajUqXyPPl4JyqUK2PxcVmzfhPrNmzh6PEozsVewM3VmdKlSlIvuBbt2jTLMz9S9KkzLF6ykoOHj3Hk6AmsrKCEjxeVKpanS+eHKOVbItftok6eYs68xYSF7yHhyhUC/avxZJeH8a9e5bZ13X/wMCtXb+To8SiOnziJlZUV5cuVoUql8nR6qDVexT0sbr+IiIiIiIj89ym4IiIi99w7748k5lwsn40easw7GxPL2PHfEHMulpnTJtzT/QcF+lEvOMh4cb5+41be7tPD7IV81qBFhuvXr3M5PoG9+w8y748lDB34Vr4T1n87baZZYKXbE4/Qvk3zAmhNpsSkayz6awWTvv3RmHciKpqp02eRlpZGlUoVGDhsDGlpacbynWGR7AyLJD7+Cg93aG1W3omoaAYNH8vZmHNm88Mj9xIeuZc5vy/i6a6P8vwzXfKs067IvYz6dAI3biTn2D761Bn69+1lcTs3bNrG6HGTuH79embbE5OMHCk/z55HvzdeoVGD4HyVV6Z0ScIj9wKwY2c4jRuEcPRYFHPnLwbAzs6OJg3rWlzP23Fzc6HbE48w5fsZAMTGXmBXxF6CAv2MdaJPnWHQ8E84dfqs2bYZ+YPWb9zKitXrGTboHezt7ajhX5VChZxITEwCYPee/WbBlV0Re8zK2RW51yy4snvvAeNzyRLeufbWSU1JZcTo8WzZFmrMi4o+TVT0af7evJ3JX47OM6iRXVLSNUaO+YJtO3aZzY89f5HY8xfZGRbJwj+X88mHg8yCmWnp6XwxcSp/Ll2Vo8wDh45y4NBRlq5YQ783e9GmZRPzNkfsYfCIsVy7lnn9bNq6k83bQnmxe9db1vf7n2bzy68LcswP3RVJ6K5I5s5fzMvPd6PrYx3z1X4RERERERF5cCjnioiI/CPOxsTSb+BIY3rs+G8Ij9yLV/H89wa5G40ahBifk5OTOXAoc3iyxUtW5gislPDxokjhwsZ0YmISwz/+nJPRp2+7r7+WrWbOvMXGdJNGdenxQre7qX6uLl6K4+vvfsLVxZnS2V5uz/l9MWM+m0R6ejplS/vi6OhgtnzSt9OJuxxvTCcmJjFk5KdGYMXKygp/v6p0aNcSNzdXwJSc/adffmPths151mnK9zNIS0ujXNnSOBcpbLZsyfI1HDp8DABv7+IE+FU1W8fR0YEAv6pm8w8dPsbHYycYgRUHBwca1g+mWZP6ODiY2hQfn8CoTyfkO09K6xaZL98XL13FiFHj6f3WIK5du46VlRXvvNETNzeXfJVlqaaN6plNZwR5wBR4yB5Ysbe3o2xpX7NttmwP46tvpgGm81S3TpCxLGuwBCAiS/kAEbv3GZ8Tk5I4ejzKmK4fUivXOu/cFcmWbaG4ublSrkwps542165dZ/LUn3NvbC7GfTXFLLBiZWVFuTKlsLXN/L1P9KkzDBw2xixA9/v8P80CKyV8vHikQxuaNa6Pg709YLo+P5/wHQkJV4z1LscnMGL0F2aBFVtbG0qXKkl6ejo/zvyNyzd7EmV3+Ohxs8CKj3dx2rdpToumDY37KSUllSnfz+D4ieh8HwMRERERERF5MKjnioiI3HPvvt2bfgNHcjYm1pgXHrkXby9PPh8z9BZbFpxKFcuZTZ+LPQ/AjRvJTJk205jvUcydD4f2p3LF8qSlpbFs5To+++pb0tPTuR0LovcAACAASURBVHbtOt9Nn8XIIf3y3E9Y+B7GT5xqTPv7VWXwgDcLuDUmV68m8nTXzrz8vGkorZ1hkbw75GMArly9ioODAz9M/oxSviVISUnhi0nfs2T5GsD0Ujgich9NGpl6aMz7Y4kRnLC1tWXcqCEE+FUFoO9rL/HByHFGEvhvvvs5z2HFkpNTmPH9BDw93ElLT+eb735i3sIlxvL1f2+lUsVydGzXko7tWvL+0NFs32nKgeLj7cUXY4eblfftD7+QnGx6yV7Cx4svxo6gmLsbAJfiLvP6Ox9wNuYc12/cYPqMOQwa8MZtj1v1qpVo3aIxK1ZvMOoEphf9/fvm7PlQkLyKe1CkcGGuXL0KZF6HAPMXLTULrHTp/BAvPNsVJydHYs9fZOToL9i7/yBgClQ9/kh7ypUtTf2QWqxZvwkwHZNTp89SsoQ3iYlJHDh01Gz/Ebv3kZaejrWVFZG795Oenjn8Wb2Q2rnW+czZc3Tv9hgvPGvq5XH8RDQDBn/ExUum/DE7wiK4fuOGEeTIy979h1i7PjMwFxhQncHvvkEx96IkJiXx3Q+/8MefKwDTMF6Ll6zksUfaA2Bvb0/toABOnY6hcqVyDHn3TWxsbABTL5IBg03XfXJyMttDw2nR1JTL5vcFfxnDsAF07tSWl7o/SeHChTgbE8vIMV/kmQcqInKf2fTnY4ZS3NM0BJjp2huCk5MTpXx9SExKumXbRURERERE5MGjnisiInLPeXt58tnooWbD/Hh7ed7z4cCyKnqz90WGS5cuA7B5205jSCWAF559gsoVywNgbW1N+zbNaZyl18uWbaFGzo7suTJOn45h6IfjjGG4fEv6MGrYu9ja2hR8g27q+ngn43PtoACz/BdBgX7GcE22trZ07tjWbNtLly8bn7O+9G7dorERWAGwsbHh9VdfMKbPX7jI4SPHc6/PYx3x9HAHwNrKit49upvlz8g+3NWtxMdfIXRXpDH93NNdjMAKmM7pM092NqY3bws1CxbkJTk5OUcgwNHRgbEfDaZd62aAKXAVums3obt2c/jo8XzXOT9cXZ2Nz5fiMs/BqjUbjc9exT3o1aO7MXSdp4c7/d58xaycFTfXrxsShLV15n/pMnqnZO0VU7KEN2DqoXT06AkAI6cKQOHChQgMqJZrfV1cnHnumSeM6bJlfI2gB5gCdTFZAqd5WXkzmJVhwFuvUsy9KACFnJx449UXcS+aeX5Xr/vb+PxIxzaM/WgwM6d9xbCBbxuBFYDChQqZlXvhYpzxOSNwBlDM3Y0+rzxP4cKm9b29PHMc06yy9qYB+GvZGuLjTb1iirq5MnPaBKZOGsuwgW9TvWqlWzdeREREREREHjjquSIiIv+IjABLz9ffJTk5+R8NrADEZxkqCEwvjMH0q/ysatbwI7uaNfyMl7SpqanEnDtP2TK+OV7kZwzVBKahh8Z+NNh4kXuvFMqWyL1QocxAhpOj+bKMNhuyVP9MljwrS5avMXq45OX0mRgqViibY3723BvW1tZ4FCtKVLQpgHX9xo1blpvVmWy5X8Z8Nokxn03Kc/3ExCSuXLmKs3ORPNeJi4vnzQFDcwR5rl27zqQp0/ly3AiKFC7M7r0HGHQzEXyDurX5cOiAfNf7dq5cuWp8dnHOPCdZr8UAv2pYZwvelS3ji4uLs9ET48zNnkZFChfGv3oVI6gSsXs/7ds0JzR8t7FttyceYdyXUwBT3pWKFcqaBV+CaweaBWiyKunjlaMuWQOlANev3/68nj6bOWxbcU8PfLyLmy23trbG368K6zea7rXs9yaYgnMHDh3hzNlznD4TQ8y52JxDcmW5L2POZQZ9/KpXydHGCuXK4FykMAlZzkmGeiFBTP7ewRiS7udZv/PzrN8pW9qXShXLUcO/Go3qh+Dikvf1JiIiIiIiIg8u9VwREZF/jLeXJ4vm/sDSBTP+8X1HnTxlNu3pUQzALD8DmPcqyJA9/0Z8Qu45GrJKSUll09YdllbzvkhLSzPLSZEf8Veu5Drfytoql5m5zMvPPvJxnHNuk3u9Moz+bKIRWPHxLs7XX4yidKmSAByPimbg0DFcv3HDLCePx82eOAUh7nK8WR2Le5quw9TUVLPAU27XIYB7lh5YWcupF5yZdyVj6LC9+w4Bpl4wrZo3MnLU7N13kLT0dA7ezH8D0CCPIcEArKxy/nfRCsvP6dWricbnvAISRV0z25c1F8r1GzcYPW4Sz/V8i4/HTmDaT7+ydMVawsL3mPX+ySolJcUsb4tr9uDiTW7ZerVlKO7pwYcf9MejmPn5Px4VzYrVG/jsq295onsvps+Ym+v2IiIiIiIi8mBTzxURESkQ3l6enI2J5WxMbI5ftVsq4xf1d1tOVkuWZfbEsLW1pWqVCkDOF6uXLyeYDWMFpt4OWWUfYiwvU76fSVANf8qW8b3leqkpqTnnpeacd69YW1tTuHAh4+V3RtLuWylTuuQ9r1fWF+0Ar7/6AmVK3fpY3ioQciIqmh2hEcZ039depkql8owb9QGvvzOEc7Hn2bv/EIOGfcKJqMzeENWqFNyQT0tXrDXr8VTD3zQUl42Njdk5uHw598DSxSyBhKxBv/r16vDtD78ApoTwl+Iuc/S4afiv6lUrY2dnh1+1SsYwZyeioklJSQFM579uSBD3mqtrZn0zhtfKLutQde5FM8//4OGfEBa+BzANx1e3Tk0Ca/hRuWI5SvmWoGv33jnKsrW1xd7ezgiw5JW4Pi6P4AyYhtqbOW0CYeG72REazt79hzl4+Khx7FJSUvl51u94eLjTsV3LPMsRERERERGRB4+CKyIiUiACA6pzNmYdz7x0+4Ti+eVVvGCCKwsWLWN7aLgx3aRhXYoULgxAuTKlzNbdFbEnx3BFuyL2GJ+dHB0p4eOV6346tm9Fg7q1jeGkkpOT+XDMF0z+ajR2dnbGevb2dmbbHTtxknohtYzpa9euE3v+giVNvGtlS/uyZ5+px0Nycgq1avqbLU9LTyf61BlKZxv2617yLemDra2t8SLb0cEhR70yXtLnZ2im8xcumU273XzZX8zdjbEfDeLNAcOIj08wO9/29nY0qJd3rw5LHDh01KyXg0cxd+rUqmFMZz0Hu/fuNxLPZzh+ItosOXuFspn5dUr7ljACnAALFy8zggrBtQMB0z0aums3p06fZdv2MGNb/+pVjPvhXipXphSbt+4E4Fzsec6cPWd2r6WlpbFn7wFjuuzNezPm3HkjsALQv28vIzcOwIWL5uc1K6/inpyMPg3Anr0HSEtLMxsa7MixE7kOCZbVxUtxlCld0jiOycnJrF63iS+/nmYMGbbh760KroiIiIiIiPyf0bBgIiJSIJ57uguBAdULrLdJ21ZN+XzM0LsqI+5yPD/8PIeJU6Yb8xwcHHj+mS7GdFCgH85FMl8sT58xl6ibL2MBVq39mw2bthnTdUOCzJJpZ9WoQTB1g4Po3CkzcfzxqGimTJtptl7WpN1gCv5kDFV1Ke4yn0/8zmw4o39Ck0b1jM/rNm7h4OGjZsv/WLycF3u9w2PdevLBh+MsHkYsL3ZZkoZfirts1qvD0dGBkJsvtAFm//YHcZczexGlpafzxaSpPNqtBy/2eofvf5x9y315Ffcwm57563wjcOPj7cXzT3fJsU2fV56/68BDcnIyS1es5d3BH5OcnHleX3npGayyBE+ynoOzMbF8N22mcTwSrlzl0y8mm5XbuGGI2XT9uplBoEVLVhmf694cMqxecGYAb/HSzOVZhxS7l5o2rmc2/ekXk42eOmnp6UycPN0sGX3jBqb2JSYlmW1XrFhRs+nlq9bnuc+MMsCU6H7Stz+SlHQNMAV4PruZhyY3EydPp/2j3en2Qh8Gjxhr1MPOzo7mTRqY9WBLS0vLsxwRERERERF5MKnnioiIFAhvL8+7Dobcra++mWaWVD43b/V5Cd+SPsa0jY0NPV7oxviJUwE4f+EivfsOpFKFcqSkpLDvwGFjXQd7+1xfwGfXu0d3wsL3GENLzf9jKXWDgwiuZQoUlPDxomL5shw+etzY5/OvvE3Z0r5ERZ8mNTWVkiW8cyRdv5c6tG3BH38u59TpsyQnJ9O77yCqVCpPzRp+HDl2whhO63J8AmmpqTg6OhTIfrOei7i4y/R8/T3sbG15q8/LVKlcgRe7P8n20AiSk5OJPnWGrt17ExToR+WK5dm4ebuRSycq+vQtE9ln7Kt2UAA7wyIB2LBpG08+34eSPl4cPnrC6IWQVV5DSd3K+o1badnhqVuu0651M1o2Mx96Les5AJgzbzFbtofh6uLMqdNnuXgpM/DQtlVTSmXrRVQ/pDbz/1gKZA51VaVSeaOHTsUKZXF1ceZyfAKnz2Qml88alLmXKpYvS7Mm9Vm7fjNgGv7vxVf7UcLHi7jL8UYPE4DSpUrSplVTAHy8imNnZ2cEpr6YOJWWzRphZWXFvgOHjPOZm8c7P8Siv1YYvVMWLFrG4iWrKFnCmxNR0djY2ODg4JDruQ+sUZ35i0zH8+ixKJ56vg/BtQKxs7Nl09adZjlkGtYLvsujIyIiIiIiIv816rkiIiL/F1xcnPn048G0adk0x7KO7VvRvdvjxvS1a9eJ3LPfLLDi5OjIiCH9jOTnt2Jra8vwwe+YDf816tOJZr0u3nq9B7a2mT1g0tPTOXbiJKmpqbRq3pjKFctb3Ma74eTkyMfD3jUb8uzAoaP8+vsiszwlgQHVGfzumwW2386d2lGoUGaOm2PHozh4+CiHbgaeypcrzdCBbxnBnNTUVHaERvDLnAVGYAXgyS4P0/Wxjrfd36ABb1CyhLcxHRd3mT37Dpq9XC/q5mr0KJn206/8maWXx92ysbHh5eeeYsBbr+ZYlts5iDp5isg9+80CK/Xr1qZvn5dzbB8U6Gckrc8QUqem2XT2QIq3l2e+rumC0v/NXsbwWmAa0ityz37zwIpvCUYNfw8He3vA1IOpzyvPGcvPxsQy89f5zJg9j51hkXRs15Ji7ua9WTK4ubow5L2+ZsclJSXFCHx27/ZYjh5NGRo3CDG7pq5eTWTths2sWL3BCKxYWVnx8nNPmfVWExERERERkf8P6rkiIiIPJEdHB4q5F6WEtxctmjWgUYOQHInqs3rh2ScIrh3I8pXr2HvgEKdOx+DoYE/JEj7UqulP+zbNLRryrLRvCXq++AyTbg5JFh+fwEeffMm4UR8AUK1KRcZ/Mpwvv/6ew0eOA6bE4l0f68jLzz/FJ59/c8dtv1OlfEswZcIYlq5Yx5ZtO4mKPs3ly/GUKlmCcmVLUz+kFk0b1zMbyupueRX3YMpXY/h22kz2HzzM+QuXSE9P5/z5i8Y6DerW5vuvx7F0xVp2hkVy6vQZrt+4QfmyZahUoSxtWjWhauWK+dqfm6sL300ay6w5C1m2ch3nYs8by0r7lqBRwxC6PtqRdRu3GL2Zxk+ciouLs9kQU/lla2tLMXc3PD09qFunJq1bNMHTwz3P9Uv5lmDKV2NYsnwNW7aHEXXyFPEJCXh6FKNC+TI0bViPZk3q57qttbU1IbUDzYexyzIUGEDdOkEsXbHWmP6neq1kcHJyZMzIgaxZv4l1G7Zw9HgU52Iv4ObqTOlSJakXXIt2bZrluFc7PdQaH28vlixfw/6DRzgbcw5vL0/at2nOM08+yubnXstzn3Vq1WDCZyP5bf6fROzex9mYWIoULszTT3bmycc7sXrdpjy37fXyszRv2oClK9Zy5FgUx45HcfVqInZ2dtQLDqL7049ToVyZPLcXERERERGRB5fVlcTr6bdfTUREREREREREREREREDDgomIiIiIiIiIiIiIiFhEwRURERERERERERERERELKLgiIiIiIiIiIiIiIiJiAQVXRERERERERERERERELKDgioiIiIiIiIiIiIiIiAUUXBEREREREREREREREbGAgisiIiIiIiIiIiIiIiIWUHBFRERERERERERERETEAgquiIiIiIiIiIiIiIiIWEDBFREREREREREREREREQsouCIiIiIiIiIiIiIiImIB2/tdARER+e9LTknlRnIK6enp97sqIiIiIiIiAFhZWWFvZ4udrc39roqIiDyAFFwREZG7diM5haIuhfRHi4iIiIiI/Gskp6RyKT5Rf6eIiMg9oWHBRETkrqWnp+sPFhERERER+Vexs7VR73oREblnFFwRERERERERERERERGxgIIrIiIiIiIiIiIiIiIiFlBwRURERERERERERERExAIKroiIiIiIiIiIiIiIiFhAwRURERERERERERERERELKLgiIiIiIiIiIiIiIiJiAQVXRERERERERERERERELKDgioiIiIiIiIiIiIiIiAUUXBEREREREREREREREbGAgisiIiIiIiIiIiIiIiIWUHBFRERERERERERERETEAgquiIiIiIiIiIiIiIiIWEDBFREREREREREREREREQsouCIiIiIiIiIiIiIiImIBBVdEREREREREREREREQsoOCKiIiIiIiIiIiIiIiIBRRcERERERERERERERERsYCCKyIiIiIiIiIiIiIiIhZQcEVERERERERERERERMQCCq6IiIiIiIiIiIiIiIhYQMEVERERERERERERERERCyi4IiIiIiIiIiIiIiIiYgEFV0RERERERERERERERCyg4IqIiIiIiIiIiIiIiIgFFFwRERERERERERERERGxgIIrIiIiIiIiIiIiIiIiFrC93xUQERERERERud/+XLebr2etJy4h6X5XReSB4ObsxGvdmtChqf/9roqIiMg9oZ4rIiIiIiIi8n9PgRWRghWXkMTXs9bf72qIiIjcMwquiIiIiIiIyP89BVZECp7uKxEReZApuCIiIiIiIiIiIiIiImIBBVdEREREREREREREREQsoOCKiIiIiIiIiIiIiIiIBRRcERERERERERERERERsYDt/a6AiIjIgyQ1NZWNm3dw7EQ016/foIZ/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yszO4xS4RERUK5nZubAwrf+pWf7fZWXnQL/UlFzf/bIbrVvaYtTQPvUYFREwa9EqLJo7USXrWxAR1UTQwbpdv4aISriOv1B1ITVKSE6HgV4F6yESERHVAqcFIyIiagAO/H0e36zfgfjEZGRmZeOM13WEhEWiQx0v3E5ERERERERE9P+A04IRERE1AMMH9kBObh4+X/Mb8vIL0NjYEO/OGIsWts3qOzQiIiIiIiIiogaH04IREVGtcVowIiIiepFxWjCi+sNpwYiIqKHitGBERERERERERERERERKYHKFiIiIiIiIGjSxtnF9h0D0f4n3HhERNWRMrhAREREREVGDZuk2hw95ieqYWNsYlm5z6jsMIiIiteGaK0REVGtcc4WIiIiIiF5EXHOFiIjUhSNXiIiIiIiIiIiIiIiIlMDkChERERERERERERERkRKYXCEiIiIiIiIiIiIiIlICkytERERERERERERERERKYHKFiIiIiIiIiIiIiIhICUyuEBERERERERERERERKYHJFSIiIiIiIiIiIiIiIiUwuUJERERERERERERERKQEJleIiIiIiIiIiIiIiIiUwOQKERERERERERERERGREphcISIiIiIiIiIiIiIiUgKTK0REREREREREREREREpgcoWIiIiIiIiIiIiIiEgJTK4QEREREREREREREREpgckVIiIiIiIiIiIiIiIiJTC5QkREREREREREREREpAQmV4iIiIiIiIiIiIiIiJTA5AoREREREREREREREZESmFwhIiIiIiIiIiIiIiJSApMrRERERERERERERERESmByhYiIiIiIiIiIiIiISAlMrhARERERERERERERESmByRUiIiIiIiIiIiIiIiIlMLlCRERERERERERERESkBCZXiIiIiIiIiIiIiIiIlMDkChERERERERERERERkRKYXCEioloTiUQoKJTUdxhERERERESCgkIJRCJRfYdBREQNlGZ9B0BERC+/RlqaSEnPhlQqre9QiIiIiIiIAMi+BNZIi4++iIhIPfgXhoiIak1LUwwtTXF9h0FERERERERERFQnOC0YERERERERERERERGREphcISIiIiIiIiIiIiIiUgKTK0REREREREREREREREpgcoWIiIiIiIiIiIiIiEgJXNCeiIhUKj4hCbv2HcbZC5eqLCsWizF5/ChMnzy2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+u9W4OdNfyA84jEA2bRsb45+DbOmT8B36zYrHaOqfP7J+3B3c8U13zsIeRCGjMwsOLVuiQljXodDC9uX7iG5uvoEAPTo1gnbfv0e/57zgn9AIGKfJiA/Px/WVpZwadMKgwb0fiFHg6mj/zW0fkNEREREREQ1I8rMzpPWdxBEREREREREREREREQvCy5oT0REREREREREREREpAQmV4iIiIiIiIiIiIiIiJTA5AoREREREREREREREZESmFwhIiIiIiIiIiIiIiJSApMrRERERERERERERERESmByhYiIiIiIiIiIiIiISAlMrhARERERERERERERESmByRUiIiIiIiIiIiIiIiIlMLlCRERERERERERERESkBCZXiIiIiIiIiIiIiIiIlMDkChERERERERERERERkRKYXCEiIiIiIiIiIiIiIlICkytERERERERERERERERKYHKFiIiIiIiIiIiIiIhICUyuEBERERERERERERERKYHJFSIiIiIiIiIiIiIiIiUwuUJERERERERERERERKQEJleIiIiIiIiIiIiIiIiUoFnfARAR0csv+Xkq3pw6T+ExHR1tnDqys44jUt6A4ROwcMFsvDZkQJ21OW32h+jSyQ0L5s1A9JNYLFq6EiNHDMaUCaNrVa9EIsGg1ydj4Xtv47WhA2tV14ZN23Ht5h389vNqmBgb1aqusqbN/hCxcfHCtp6eLtq6OGHwgD7o27u7StuiEnn5+Vi7bjNu+d1FXl4+jh3YCj1dXYQ+jMCyL9fg/Xdmok8vD8yctxjt27bBwgWzhXPf/2g5LMzN8NmSBQDq575Rl+LPsS8/XYjePbvVuJ4/dh7AOc/LOLhrU43r+HHD7/j3rJewrd2oEVq1coB7exeMH/M6dHV1AACe3j749odfhHKammI0s7RABzdXjHp9KGxtmsnVW/aeK+3X9d/AubVjuf2q/Dx5WZXt97VR+nOfiIiIiIhebkyuEBGRyowdOQzdunSU2ycWi+spmpeLgYE+TEyMYWVhXift5ecXYOioqfjog7kYOqhfheWsrCxgZtoEOtraaonD3c0Vk94cBQDIyMzEzdsB+Pq7n5GVnY3hDeCB/Yvo0JETuHjlOsaNfg0O9s2hp6sLADA2NoKJiTHMzU0hEolgaWkOKyuLeo72/5eRkSG++OQDALJ74+KV69h36DjuBT7AujXL5cp+smg+mpo2QV5eHoJDw3DytCf+PeuFTxbNR/8+PeXKlr7nSrO1sVbfm6lD1f1sIyIiIiIiqi0mV4iISGWa2zRDxw5t6zuMl1KTxibY9uva+g6jnHGjhmPcqOFqq9/E2Fiuz/R5xQMZmVk4fc6byRU1iY2LRwu75pg3a4rcfksLM2zf/IOwvfqrpXUdGpWipalZ7t74+8RZbPxtB0JCw9HGqWSUiYtzK9hYWwEAunfrhHEjX8OHn6zAug1b4e7WFo1NjIWyZe85IiIiIiIiqhkmV4iIqM5ERcdg174jCHrwEAUFhWjn4oRJ40eitaODUGbB4uWwt7OBU+uWOHTkBOztmmPl54ux7c/9uHjlOhYtmIPftu1GYtIz9PDojEUL5uDA4eM453kZz5JT4OLsiKWL30VT0yYAgG1/7sc5z8s4tHuzXCwjxs3AuFHDMW3SWIWx+t7yxz+nziEw+CEys7LQ1tUZSz6cB+tmlgCAW353sfSL1di0fhUOHT2JqzduY9P6VXBoYauwvgveV3DytCcehkfCppklZs+cJHe87NQ7xdtLFr6DyKgnOHP+IqZNHIPRbwxFVlY2tu3cj4C7QUh8lgzHli0wcezr8OjaUWHbABASGo7Fy75G/z494N7eVZhK6Ieft+CHn7dg6y9rFcZe9vrV9PegLImkSC6Gy1d98dEHc/HHroOIfhKLY/u3AgCu+97B8ZPnEBwahiaNTdC+bRvMnjEJhgb6yMzKwsjxb2Pe21MxduQwAEBGRiZGTZyNbp07YNWKT4Q2Zr3zEeztmuOLpbKRAsdPncOxf84gITEJTU2bwKNrR7wzexo0RCIAgFQqxf5Dx3HN9zYio57A2soSA/q9gvFjRgh1VtSXFYmKjsHBIydw934w4hOSYGlhjvffmYFuXdwBlPS3nb+vFx6iA8BnX61Fbm4eflz9BQCgsLAQm37fhes3/ZCWlg5ra0uMeWMYhrzat9wUUgOGT4BjS3ts2bCm2vVXRZnr4uLcCv+cOo+ExCT07N4Fc2ZMgqGhQYV1L1i8HBbmTfH5J+8L+8LCIzHvg2X/a+++w6OoGjYOP5tNdgOkJyT00HvvvVdBQJAiKIoC9t4Q9BWsIFZsiApKERRRRFGQKtKk9yK9hfReSN3vj8jKkrYTguGD331dXC87c+bMmbLjyzx7ztF7U19Ww/p17Mfx2fQpWvj9Um3fuUcVK5TXkNv6qmP7f4f6ysrK0pxvFmvTlu06FxKq2jWraezoEbntNsfxLV22UmvWb9LRoyeUnpGhLp3a6unHxslqseS6TX7XxKgWzRpJksLCIhzClSt5eXnozcnjNfLeR7V63Ub7/X81MrOyNHPWfG3YvE2S1LNbR40Ydpv9OyFJf27aqp9/XalDR47Jy9NTzZs21P33jbT3jsrruRkVE+PU/VfQvXP5PX7ls62g52Z+z9wrJSQk6rsfftGWbTt16vQ5uVutumPoAI0YOtChXEHPfenafmcAAAAAXFtMaA8A+E8kJCbpqRde1dHjJzWofx/dPeJ2nQsJ1VPPv6LwiCiHsjt379eu3ft1393DNfrOIfbliUnJ+vHn5Ro+pL/GjB6hPfsOasKkKdqxa5/uHTVMD48bpfCIKE1999Mrd2/Ith17NGHSVMXGJeiBMXdq/NMPKzEhURMnvyWbzeZQ9qPPvlatmtX0+svPqWyZ3If0Wr1uo958+2OZzWY98fB9atqkgd6ZPlPxCYkFtmX+tz/KxWTS+KcfVod/5oGYOPktrVqzQW1aN9djD96rrMxMvfjKNG3fuTfXOk6eOqPnX3pD7ds019OPjVPTJg3svRKGDuqnaa+/mGfbc3OtrkOWzabffl+rTVu25xjOJz4hUXO++V69unW0BxR79h3SS6++rbT0dD1y/z3q3KG1Nm3ZrmcnvqasrCx5lCqlenVradfuffZ6duzeJ5vNpj37Dinrn2sZExunU2fOqU2r7JesK9f8qemfzFKHdi310vgndOstPfTLb6v07fdL7fV8PX+RvpyzUBXKl9VTj45TpYrlNXPWfM2e+51Du/O6ly8XGxevR5/5n7bv3KOB/Xpp0sSnVDm4gia98a4uhIYbOofvf/ylVq/bqCGD+unF8Y+rQd3amvb+DB08/LeaNmmgaa+/qGZNGqhihXKa9vqLeuqRsQVXaoCz5+Xgob+1bcceDbv9Vt1+W19t2bpT4/83pcjaMePLuapRvYqefHSs/Py8NfnN9/TXtl329R98/KXmLfxBNapX0bNP3C9/P1+9eVnwlJdZc77V9E9nqbS/n8Y/87DG3D1cf23dpY8/y3teqfyuiVGX7ofSpf0LLBsUGKCa1ato994DhveTm+8W/yybzaZxo0eqXp2amj33O30+a759/c7d+zTp9XeVmpqmR+6/Rx3atdSqtX/qhZen5qjLmedmXvK7d/J7tjn73MztmXulCZOm6rsfflGLpo00acKT6t2zs778eqFWr9toL+Psc/96+c4AAAAAMI6eKwCA/8SCRT8pLS1NX814x/5L2149OunusU9o9txv9fxTD9nLWixu9h4El0tLTdP/xj8uNzc3SVJMTKy+mrdIPy+arZIls38ZnZScoi+/XiCbzSbTZb+oNqJe3Zr/zFXQVq6u2f+pDAoM0JPPT9apM+dUJbiivezgAX3ynXzdZrNp5qz5atGskd6cPN7epgb1aut/r76d53aXNG1cX+PuHWn/vPmvHdp34LDef2uSGtSrLUnq3qW9Hnpion78ebmaN23osP35kFA9M+E1NaxfR+OfeUQmk0m+Pt5q3LCeJKlSxfKGhwgqyuuwdv0mrV2/yWHZfXcPV/++PRyWJSUla8Kzj8rP18e+7PPZ81Wvbi298+ZL9n106tBGYx56Vr+vXq/ePTqrVfPG+ubbJcrMzJTZbNau3fvVp2cXrVm3UX8fPa7aNatrx67sl6stm2X3Etmz76AqVSin+0YNt+8ruGJ5VasaLEmKj0/Uwu9/1j13DtVddwySJHXr3E6enqW05OcVunvk7XJxyf79Sl738uW8PD004ZlHFFypgv1FcNtWzdR38D3asm2nbru1d77bX27v/kPq3LGNBvXvba+nfr1aqlo5WO7uVvk29taKVX8oMSm5yIeGMnJebJJeGv+4/br5+fpo2vszFHIhTOWKYJ6Xfn26q3OH7O9lp/atNfLex7T6j41q1aKJzp4L0S/LV2vs6BEafnt/SVKXjm31yedztHjJr/nWe+st3VWtarC9bklKTUvTkp9X6KlHcw+q8rsmRpw9F6IPPvlSQYEB+fZauVy5smV0LuSCof3kpUa1Krr/n6Hk2rdtoeiYWK1et8G+7PPZC9SsSQNNeXWCvTdL7ZrV9OqUD3T02EnVqF7FXldBz838FHTv5PZsM/LcvPKZm5uH779baWnpali/jiSpXZsWOnHyjP7c+Je6dW7n9HP/evrOAAAAADCOcAUAUGTe++gLvffRFw7LHh53twYN6KPNf+1Qm1bNHIYwsVos6tyxrVas+sNhm7yG1vLwKGV/oS9J7lar3Nzc7C/0JcnTo5QyMjKVnp4hi8Utt2oKVLJECfXs1lFpaek6cOhvpaamacPmrZKk2Nh46bJ3opdeuOclIjJKkVHRemDMnQ4hQ7vWzR3anZdqVRzr37J1p6oEV7S/IJQks9mszh3baMGinxzKRsfE6rkX31DtmtU0eeJTDsP3XI2ivA6XT66dkZGhI0eP6+v5i5SYlKxxlw3T5Ovj5RCsxMbFZw919tg4h/NaJbiiatWoqs1bd6h3j85q26q5vvx6oQ4dOab6dWtp194DunP4bTp95rx27TnwT7iyX3Vr15SXV/a92bRxff32+1p9OGO2unfpoOpVg+3Dc0nS9l17lJ6eroG39nI4lp7dOmnpspU6cfKMqlerLCnve/lyLi4uat2yqbJsNh07fkrxCYm6EBqmzMxMxcXFF7i9w/lsWE/r1m9WhXJl1LJ5Y1WsWD7HhObXipHzUqVyRYfrVjm4giQpNi6uSF4UX/m9qVihrGJj4yRJBw8flST17t7ZoUyv7p0KDFcCSwcosHSAEhISdfzkaaWnZ2jv/kOKi0/Ic5vCXpOo6Bh16/tvwGcymVS3dg099eg4+wv3wsgt0GzXpkWeQ9Zd0qSRYxjXuGE97dqT3SsmNjZefx87oZdfeNLhOdOxfWtZrTO0e99Bh3CloOdmfgpz7xh5bl557+Smds3scCvkQphCwyKUlJysC6FhygosLcn55/719J0BAAAAYBzhCgCgyNw+8Ba1auE470fFCuUkZQ/rFBiQcyiboMAAxccnOPRwMKloQoDCSkhM0sxZ8/X76vXKyMhQmaBABQUGSFKOYcEK6h2TlJwiSfL0yDku/uWTTOflyvrjExN18vRZh5eul0tLS5fZnP3i9ev530vKPseF7cVzrV05uXbL5o3lbrVqxpfzNKBvT/t51xX3xKXQIbfhkQJLByj2n/WVgyuodICftu/co7JlgnQ+JFQN69fVqdPntHf/Id0xZIB27z2gvr0X5rSYAAAgAElEQVS72rfv2qmdUlIu6uv532vJzyvk4uKiZo0b6H8TnlDJEiWUkJAkSRo47L5cjykyOsb+QtTZe3nBop/0/Y/LFBsXL49SpVSzRhVZLG664nYr0MP336NSHqU0e94izfhyntzdrerTo4seeeAeYxUVwtWcF7OLWZIMH29errzfzWazsrKy5/FJTsn+Tnp5ezqU8fEu+Pt48vRZffbFPG3buUeSVL1q5RzPhCsV9pp4eXnqpeezez1ZrRZVr1Y5z3ld8nI+JDTHvEeXB5qX+Pp4FVjXpefKJa5ms/3Y4+Kzv2+T33wv122jo2McPl/N86gw946R56Yzbdu4Zbu++GqBzpw9L1dXV9WsXlUmk4v9fDj73L+evjMAAAAAjCNcAQAUmYoVyuU51JCXp4fCI6NyLA8Lj5SXl+c1e/lvMpmUmZWVY3lmRmae28ycNV87d+/XC08/rDatm8lqsejU6XO676FnDO/fxzv7pWV0TEyOdfH5/No9L95enipXNkhP5jFXhqvrvy88e3brqJ7dOunZia9pxpfz9NDYUYb3VxzatGqmGV/O06nTZy8LVxx5/3NeIyJy3lPhEZEOoUvrlk21a+9BlQkKVMUK5VQmqLTatGqmn5b9rpOnzig8IlJtWjVzqKNv7266pVdXnQ8J1badezR77nea8cU8PfXoWHl7Zb+Uf/V/z8rdas2xf6O/yl+9doNmz/1OD4y5S906t7PXP3jEOHuZSy9WMzMd79uMjAyHzxaLm8aNHqF77xqmk6fOaNXaP/X9kl9Vp3YNdeucd28JZ+vPT1GflyuZTFJmlmP70g2075JL7YyMjFbgZfdJbFxcgdu+/No7CvD30/tvTVK9urXkYjJpyc8r9OGM2XluU9hr4ubqelVDt0VERuvvYyf0UBfH7/2VgWZRuPR9vOfOIapXp1aO9Xl9jy8pivsv3/YZeG4WJCw8Uq+8+Z56d++syS8+rUr//IBg8hvvKeaf3lHOPvev9XcGAAAAwLXFhPYAgP9Ew/p1tGnzdiUkJtmXpaalac26DapfN+fLuKLi5eWp2Ng4xcf/O4nwyVNnlJqWluc2Z86eV93aNdS5Yxv7L8WPnzhVqP37+nirTFBgjkmT9x847HAunNWoQV1dCA1XmaDSatq4vv1PamqqAgL85OLiYg+q6tWtpSaN6mnsPXdo8ZJf9ceGLfZ6XFyyy2TlEjwVtyNHT0iSwxByV/Lx9lKlCuW0YvV6h5eiJ06e0ZGjJ9SwXh37stYtm+nwkaPatmOPWjRrJEmqV6empOweI6UD/ByGAvpr2y5t3b5bJpNJFcqX1W239la71i20a89+SVLDBtl1x8cnOFwDD4+ScnExySufdufm1Nlz8vXx1qD+vf998R8V7TDU1KWXtafPnrcvy8zM1PETp+2f09PT9dvva3Xq9Dm5uppVo3oVPTh2lMoEBWrn7n35tsGZ+gtS1OflSl5enjp7NsRh2eG/jxuu59I8Gdt27HZYvmnLjny3y8zMVMiFMHXt3E4N6tW2D391/GTe5+hqrsnVSEpK1rT3P1XJEiXUrUv7a7afSy59H0MuhDlc+xrVKismNs4hxMpre+nq7r9Lcnu2OfPcdNa58xeUkZGpoYNvtQcrNptNJ06dsZdx9rlf1N+ZmNg4ZdGVBQAAAPjP0HMFAPCfGDygj5avXKuHn5yoAX17ymq16KdlvysqOlbDBt96zfbbrnVzfT77G70x7UMNHXyrEhITtWz5avvLvNw0b9pQ3/3wi+Yt/EG1alRTyIUwrVyzvtBtGNivp2Z8OU9JySnq2qmdjp84pQ2btznMIeKs9m1aKCiwtJ6Z8KrG3HOHSri76+Dho1q85Ff16NpBTz469t+w4Z//HXZ7f+0/9LemvvupKleqoOBKFeTq6io/Xx9t2LxNZcsEqW7tGnJ3z/nL6WstNi5OO3dnhxZpaWnatWe/lvzyu5o2rq+6tWvku+3tt/XVux9+rudefEM9u3VUWHiElvy8Qj4+3urZvZO9XPMmDWQ2u2rdn5s15dUXJGXPc9K8aUOtXrdRfXt3c6h37fpN+nPTVj324L3y9PTQpi3bteaPDerRtaOk7Imku3Vup+mfzFJSUrKCK1XQ0eMn9euKNbK4uemzD6fK1dXs9Dlo0bSRvvl2iT767Cs1aVhP6ekZWvrrSpUo4W4vU61qsMqVDdLns7+R1WKRi9lFS5etlM9lQwyZzWbNW/iD3NzcNO7ekUpKStaaPzYqNCxcTRoNybcNztRfkKI+L1fq0Lal3nrvU33x1QI1bdxA585f0KYt2wzXE+Dvp9Ytm+qjz77SkaMn1LRxfW3+a6dOXvZyPDdms1mNG9bVkp9X6OLFVFWtXEnbd+7Rnn0H892msNfEiIOHjyo8IkrJySnaf+iIli1frfT0DI1/+qF8n3VF6dL30d3dqg5tW+r02fPauHmbDh05pto1q6l8uTJ5blsU998luT3bnHluOqtO7eoqWaKEPvl8jjq2ayVfH2/9/NuqHEG1M8/9ovzOhIVHaszDz6pZ4waaNPEpp48HAAAAQOERrgAA/hOVKpbXO2/+Tx/OmK1PPp8jSQquVEFTXn3hmvZcKVc2SI89OFqffTlfz058TUGBAZo08Sm9/Nq7eW4zcthtioqO0dwFi5WRkakWzRpp7OiRemr85EK1YfBtfSVJcxf+oC1bdyqwdICmvDJeb7z9keG63Nzc9MG0SZrxxTy9Me0j2Ww2eXt56tZbumvs6JF5bjfx2Ud1/2PjNXHyW5r50VSVLFFCD40bpbfe+1Rbt+/WlFdesPfq+C/t2nPAPim2q6urqletrCG39dXIYbcVsGX20F0uLi6aPfdbTXnnY0nZQ4A9NHaUPD1K2cu5urqqScO62rX3oBo3qGtf3qJpI23YtE2tmjd2qPeJh8fIzc1NH346WykXL8rd3apbb+mhB8fcZS/zzOMPKCiotGbP/U4pFy/KarGoVcsmeuT+ewwHCA3r19GTj47VzFnz9ePS5QquVEGPPThaU9/91F7GZDLphWce0WtTP9CESVPl7m7VYw/eq5279ysyKlpSdmA09dUJ+mjGV3r5tXeUlZUlfz8fPfP4/erepUO+bXCmfmcU5Xm5Us9uHbX/4BF998MvWrDoJzWsX0cPjr1LDz4+wXBdLzzzsGbO+ka/rlijZctXq1GDunrzlfEaeteD+W438bnH9Ppb0/Xp53Pk6uqqW3p10eCBt2j6J7NyLX8118SIqe9+Iin7Xq9cqYJu6dlFA/r1+k8nOu/bu5vMZrPmfPO9li5bKZPJpPp1a2nqKy/kG6xIRXf/XZLbs60wz83clCxRQlNfm6A3pn2ot7bulI+3l0aNuF0lS5RQWHiEvZyzz/0i/c7YJJvouQIAAAD8V0yJyan8P3AAAAAAAAAAAAAnMecKAAAAAAAAAACAAYQrAAAAAAAAAAAABhCuAAAAAAAAAAAAGEC4AgAAAAAAAAAAYADhCgAAAAAAAAAAgAGEKwAAAAAAAAAAAAa4FncDAAD//6VnZCotPUM2m624mwIAAAAAkiSTySSLm6vcXM3F3RQAwA2IcAUAcNXS0jPk61WSf7QAAAAAuG6kZ2QqJj6Zf6cAAK4JhgUDAFw1m83GP1gAAAAAXFfcXM30rgcAXDOEKwAAAAAAAAAAAAYQrgAAAAAAAAAAABhAuAIAAAAAAAAAAGAA4QoAAAAAAAAAAIABhCsAAAAAAAAAAAAGEK4AAAAAAAAAAAAYQLgCAAAAAAAAAABgAOEKAAAAAAAAAACAAYQrAAAAAAAAAAAABhCuAAAAAAAAAAAAGEC4AgAAAAAAAAAAYADhCgAAAAAAAAAAgAGEKwAAAAAAAAAAAAYQrgAAAAAAAAAAABhAuAIAAAAAAAAAAGAA4QoAAAAAAAAAAIABhCsAAAAAAAAAAAAGEK4AAAAAAAAAAAAYQLgCAAAAAAAAAABgAOEKAAAAAAAAAACAAYQrAAAAAAAAAAAABhCuAAAAAAAAAAAAGEC4AgAAAAAAAAAAYADhCgAAAAAAAAAAgAGEKwAAAAAAAAAAAAYQrgAAAAAAAAAAABhAuAIAAAAAAAAAAGAA4QoAAAAAAAAAAIABhCsAAAAAAAAAAAAGEK4AAAAAAAAAAAAYQLgCAAAAAAAAAABgAOEKAAAAAAAAAACAAYQrAAAAAAAAAAAABhCuAAAAAAAAAAAAGEC4AgAAAAAAAAAAYADhCgDghvDG25+odddBSktLz3X9xi07NOK+J9S66yCt2/BXjvVnzoWodddBmrvgxwL3tWLVerXuOkijxj2trKysHMvXb9xa+AMBAAAAAADAdY9wBQBwU/j487lKSEjUlMnPqX6dmkVS59/HTmrh978USV0AAAAAAAD4/4NwBQBwQzt/IUytuw7SiZNnFBEZrfEvv6XYuHjZbDbNmrtIA4aP0x2jH9e+/YcN192zawfNmDVfoeGRua6fMHmaBg4fp1emfqhOfYbr4OGjV3s4AAAAAAAAuA4QrgAAbmil/f304duT5Ovjrbq1a+jDtyepfNkgffrFfM2cvUC9unXUfaOGaulvqw3X3b1LO5X299PUd2fkWSYqJk7JySl67on7VTrA/2oOBQAAAAAAANcJ1+JuAAAA15LF4qYWTRvKanGTl5eHWjRtKElatW6jgiuW10Nj75QkBQT46oHHXzRUd5bNpjH3DNfkNz/Q2vWbcy1jdnHRm5OelclkuroDAQAAAAAAwHWDnisAgJtSQkKiKlUsZ/9c2t/PcB22rCz16dFJTRrV01vvz1TmZZPbX2KxuBGsAAAAAAAA3GAIVwAANyUfHy+dOHlGNptNkhRyIbzQdU185iElJiXrjw1/FVXzAAAAAAAAcB0jXAEA3FC++PpbfTZrgf1PekZGruXatmqm8xfC9NnsBdqybbdmzVvksH7dn1vUc8Aobdi8rcB9VihfVnePGFRguBIaHql+Q+7TjFnfOH9AAAAAAAAAuO4w5woA4IYyZ8EPDp/vGj5Qbq45/3M3ZtRQuZrN+nXFWi1bvkZPPDRau/YcsK/PyrIpPiFRWVk2p/Y7+s7btWL1ep09dyHfcklJyUpNTXOqTgAAAAAAAFyfTInJqc69NQIAIA+JyRcV5O9V3M0AAAAAAAdhUfHyKOle3M0AANyAGBYMAAAAAAAAAADAAMIVAAAAAAAAAAAAAwhXAAAAAAAAAAAADCBcAQAAAAAAAAAAMIBwBQAAAAAAAAAAwADCFQAAAAAAAAAAAAMIVwAAAAAAAAAAAAwgXAEAAAAAAAAAADCAcAUAAAAAAAAAAMAAwhUAAAAAAAAAAAADXIu7AQAAFIXouESFhMcoMzOruJsCAAAA3PTMZheVC/SVn7dHcTcFAIBrgnAFAHBDCAmPUblAP1ktbsXdFAAAAOCml5qWrpDwaMIVAMANi2HBAAA3hMzMLIIVAAAA4DphtbjRqxwAcEMjXAEAAAAAAAAAADCAcAUAAAAAAAAAAMAAwhUAAAAAAAAAAAADCFcAAAAAAAAAAAAMIFwBAAAAAAAAAAAwgHAFAAAAAAAAAADAAMIVAAAAAAAAAAAAAwhXAAAAAAAAAAAADCBcAQAAAAAAAAAAMIBwBQAAAAAAAAAAwADCFQAAAAAAAAAAAANci7sBAAD8f7Fq5Qpt3PCn/bOHh4eq16ipbt17ysPDw+l6MjIytGb1Ku3Zs0tWq1XNmjVX23YdZTI5X8Zmk9auWaU///xDwcGVdc/o+4rqMAEAAAAAAFAAwhUAAAzw8/NX31v7S5LiYmO1bdtfmv3l53rksSdkujwdyccP33+nC6EX1KlTF6WmXtSmjRuUnJyiHj17OVUmMzNT38yfq4jwMFWtUlWZWVnX5FgBAAAAAACQO8IVAAAMsFgsqlq1mv1zrVq1Ne2tNxV64YLKlitX4PYh58/r0KGDeuyJp+Tr6ydJKlu2nBZ8M1+t27SVp6dngWUkKS0tTQ889KjW/7FWoaGh1+BIAQAAAAAAkBfCFQDATWvN6pX6c/0fOZaPvOtuVa9ew6k6sv7pNZKZmelU+b//PqygoDL20ESSqlWvITc3Vx0/dlSNmzQtsEyDho00+t4xcnFh6jQAAAAAAIDiQLgCALhpNWnaTJWrVLV/3rRxg6KjolSpUrBT26empmr58l/l5+evcuXLO7VNXFycAkqXdlhmMpnk7x+guLhYp8qYzWan9gUAAAAAAIBrg3AFAHDT8vX1s/cOOXH8mE6dPKH7xtwvi8WS5zahoRc0+eUX7Z+tVquGDh/hdC+S9PR0ubm55VjuZrEoLS3N6TIAAAAAAAAoPoQrAICbXmJCgr5f9K26dO1e4Lwpl09on3oxVX//fVjfzJujseMeVFCZMgXuy5JHQJKeliar1ep0GQAAAAAAABQfBmsHANzUbDabvl34jQKDyqhd+w4Flr80oX3VqtVUp25dDRg4SEFBZbRr1w6n9ufn56+IiHCHZVlZWYqKipSfn7/TZQAAAAAAAFB8CFcAADe11atWKiYmWkOHDi90HT6+vkpJSXGqbNVq1RQeFqaQkPP2Zfv27lF6erqCgys7XQYAAAAAAADFh3AFAHDTOn7sqDZuWK/GTZopNCxUJ04c14kTxxUfHy9JOrB/n76YOUNpqan2bdLS0uzlDh7YryU/LtaRw4fUqFFjSVJEeLg++Wi6QkMv5LrPcuXKq06dulr8/Xc6dvRvHTp4UCtW/KaWrdrI08vL6TIAAAAAAAAoPsy5AgC4ae3atVOStHHDem3csN6+vM8t/dSyVWtFR0cpMjJCNpvNvi46Okpzv55t/2x1d1fvPn1VtVp1SdLFiymKjIxQSnJynvu9bfAQrV71u378cbEsFotat26jDh07Gy4DAAAAAACA4mFKTE61FVwMAIC8JSZfVJB/8fao2HP4tKoHly3WNgAAAAD417HTF9SodnCxtiEsKl4eJd2LtQ0AgBsTw4IBAAAAAAAAAAAYQLgCAAAAAAAAAABgAOEKAAAAAAAAAACAAYQrAAAAAAAAAAAABhCuAAAAAAAAAAAAGEC4AgAAAAAAAAAAYADhCgAAAAAAAAAAgAGEKwAAAAAAAAAAAAYQrgAAAAAAAAAAABhAuAIAAAAAAAAAAGAA4QoAAAAAAAAAAIABhCsAgBuC2eyi1LT04m4GAAAAAEmpaekym3ntBAC4cbkWdwMAACgK5QJ9FRIerczMrOJuCgAAAHDTM5tdVC7Qt7ibAQDANUO4AgC4Ifh5e8jP26O4mwEAAAAAAICbAP0zAQAAAAAAAAAADCBcAQAAAAAAAAAAMIBwBQAAAAAAAAAAwADCFQAAAAAAAAAAAAMIVwAAAAAAAAAAAAwgXAEAAAAAAAAAADCAcAUAAAAAAAAAAMAAwhUAAAAAAAAAAAADCFcAAAAAAAAAAAAMIFwBAAAAAAAAAAAwgHAFAAAAAAAAAADAAMIVAAAAAAAAAAAAAwhXAAAAAAAAAAAADCBcAQAAAAAAAAAAMIBwBQAAAAAAAAAAwADCFQAAAAAAAAAAAAMIVwAAAAAAAAAAAAwgXAEAAAAAAAAAADCAcAUAAAAAAAAAAMAAwhUAAAAAAAAAAAADCFcAAAAAAAAAAAAMIFwBAAAAAAAAAAAwgHAFAAAAAAAAAADAAMIVAAAAAAAAAAAAAwhXAAAAAAAAAAAADCBcAQAAAAAAAAAAMIBwBQAAAAAAAAAAwADCFQAAAAAAAAAAAAMIVwAAAAAAAAAAAAwgXAEAAAAAAAAAADCAcAUAAAAAAAAAAMAAwhUAAAAAAAAAAAADCFcAAAAAAAAAAAAMIFwBAAAAAAAAAAAwgHAFAAAAAAAAAADAAMIVAAAAAAAAAAAAA1yLuwEAABSF6KNLdGHnRw7LfCr3VPlWzzksO7X2GaXGn1at/t9JJpMiDy1UctQhVWo/2V4mfN9sRRycn2MfZounat/2Y47lEQfnK+b4L8pMT5ZX+bYq2/RRubiVdChzdtMrij+73mFZ+ZbPyqdKr0LVd+Snocq4GO2wrGb/hXIrEWD/nByxVyfXPKUyTR6Uf83BkqRDi/urSvcP5O5dxXC5S1LjTin29Cr5Vesnt1JlcqwP3zdbF+NO2c9pUtgundv8mmoNXOxQ7sTKR5SeFKpaAxdJMil83yxFHPxGVXt8pBJ+tf/dX/xZHftttMO2Fo9yqtF3To59O+PkmieVHLFPZounrN5VFNRojEr6181R7syfL8rdt6YC64+SJIXu+kSZaYk57qnT655XYtgOSSZZvYPlX3OQfKvekuu+48+uV/i+2UpPiVCpwCYKajROVq+KDmUOfNdT1Xp9Zj/3J9c8Ka8K7e3XBgAAAAAAFD/CFQDADaOkf11V6T69wHJZGSlKCNksz/Jtc10f2GC0Ahtkv8w/umyUghqNlVeFDrmWjTnxq6L//lEV20+SxbOi4k6vUUZqjCxXhCGSFFBnuIIajsm3bUbqC+40RR5lmudbn8lsVeypVQW+mHe2nCTFnVmr6KNL5erue3Uv/E0muVg8lBS+V6UCGynhwtZ/wqHcO9bWG7aq8Pu6QpkmD8qzfDvFnvxdp9Y+q1r9F8ps8Sx0fYENRiug9jDFnlyuCzumy+JRXqUCGzmUuRhzVOf/mqpyLZ+WR5kWSgjZoqz0xKs9FAAAAAAAUAwYFgwAcHMxmeRZvr1iTi4vkuqiDi/K7vkQUF+uVm/517xNFo/y10l9JrlaveRitig17lQRlMuWFL5bftVvVVL47kK261+e5doo/uwfSksMkVuJ0pKLq6Ssq67XGZZSZRRYf5RK+NVQzPFlV12fycVVvtX6qYRfLSVH7s+xPvLwd/Kp0kvelbrKbPGUT+UeKuFf56r3CwAAAAAA/nuEKwCAm06p0vWVGntCmWkJV1VPVmaqUhPOqlRQsyJpV1HXd4lPlV6KPv5LkZTLykzVxdiT8q81WMkROQMEo0qVbqDkiH2KO71KXhXaX3V9hWH1qqzU+NNFUld6SqRS406rhF+tHOtSoo+oVGDjItkPAAAAAAAoXgwLBgC4YSRHHdSBb7vbPwc1GqeA2kNzLesd3E2xV9l7JT0pXJJktnpJyh5CLC0xRIENRqt03ZE5ykceWqjIQwvtn6v1nCF33+qFru/0H+Ptf89rPhgp+1gjDsxV2SYP53s8zpRLCt8td58qcnX3k9nqrYsxR+XuWyNHuYTzGx2uhavVO2dlNpskyd23uqKPLlX1vl8r/MDcPPd9eX2e5VqrUofX8j0eZ5ktHroYG3ZVdYTvm63wfbMlk4uCGt6X63BtGRdjnR567PjysQ6fiyt4AgAAAAAAuSNcAQDcMJydc0WSfKv105n1E+Qd3K3Q+3N195EkZabGy6VkadXoO0fnNr+eZ/mC5lwxWp8zc65IkovZqlKBjRV/fsNVl0sK26WSAfUkSSX96ygxdEeu4Ypn+XY5JrTPi3dwN5nMFpndSuXbvqKcc+VymWmJcrX65FxhMjm3TNlzrvhV76+Q7e//MyTYsBxlzFYvp3tLVev9ucOE9gAAAAAA4PrCsGAAgJuLzSabbHIrWVouFk+lJpyVKY8X5gUxWzzlavVWStShImlaUdcn2ex/86nSJ5+eOs6Wk5Ij9ioxdIdOrnpMKTFHlRSx96pb6VGmuco1L74AITX+lNxKBeVYbnKx6PJzY8vKlIvZPc96zBZPlW/1nFKijighZHOO9VavikqJPlwkbQYAAAAAAMWLcAUAcNPyrdJL8WfXy2azFVw4DwF1RyjyyCLZsjIk2ZSeHH5VbSrq+i4pFdhQqQnnZctKK3S5rPRkXYw5rirdp6tK9+mq3OUdJUfs1eUBxP8naUmhCt8/RylRR+QT3D3H+lKlGyrh3AZlpEQrLfGCEkO3yupVMd86XcxW+dUYqMiDC3KsK133TsWeXq30pOwhyOLOrCvCIA0AAAAAAPyXGBYMAHDDuHLOFY+gZgruPDXP8l6VOuvCDueGEcuLf83BykxL1NFf7lR6SqQ8gprJp3LPXMteOedKbnOpGKnv8jlXJKlKtw/sQ3blxrtSV0UcmFPgMeVVLjFsp9z9asrFbJWUPY+Kq7u/kqMOqaR/3QLrvVqXX1sXs1V1bl9W6LpCd32qiAPzZPWuospd35HFs0KOMn7V+yst6YKOrxgnk4urfKr0km+1fgXW7VdjgCIOzldKzN8q4VvTvrxkQD2VafKQTq17TmlJIXK1eCu481uFPgYAAAAAAFB8TInJqf8/f24KALhuJCZfVJC/V3E3AwAAAAAchEXFy6Nk3kO7AgBQWAwLBgAAAAAAAAAAYADhCgAAAAAAAAAAgAGEKwAAAAAAAAAAAAYQrgAAAAAAAAAAABhAuAIAAAAAAAAAAGAA4QoAAAAAAAAAAIABhCsAAAAAAAAAAAAGEK4AAAAAAAAAAAAYQLgCAAAAAAAAAABgAOEKAAAAAAAAAACAAYQrAAAAAAAAAAAABhCuAAAAAAAAAAAAGOBa3A0AAKAohEXFF3cTAAAAAFwhyN+ruJsAAMA1QbgCALgh8I82AAAAAAAA/FcYFgwAAAAAAAAAAMAAwhUAAAAAAAAAAAADCFcAAAAAAAAAAAAMIFwBAAAAAAAAAAAwgHAFAAAAAAAAAADAAMIVAAAAAAAAAAAAAwhXAAAAAAAAAAAADCBcAQAAAAAAAAAAMIBwBQAAAAAAAAAAwADCFQAAAAAAAAAAAAMIVwAAAAAAAAAAAAwgXAEAAAAAAAAAADCAcAUAAAAAAAAAAMAAwhUAAAAAAAAAAAADCFcAAAAAAAAAAAAMIFwBAAAAAAAAAAAwgHAFAAAAAAAAAADAAMIVAAAAAAAAAAAAAwhXAAAAAAAAAAAADCBcAQAAAAAAAAAAMIBwBQBwQ3jj7U/Uuusgdeg5VAkJiQ7rps/4Sq27DlLrroMUGRVTYF2/rfxDfQaN1vETpwvdjkt/bhl8r0jiE5sAAAVtSURBVJ6e8LpiY+OdruOr+YvV9/Z71a7HEEPbXclms+mO0Y/rjbc/cap8n0GjNWHytELvDwAAAAAA4GZBuAIAuGFYrRa5upq1cu0G+zKbzabfV2+Qj7eX0/UElvZX9arB8vb2LHRbRt0xSKPvHKIuHVtr81879dq0j5zaLi4+QTO+nK9KFcvrjZefkY+P8+2+kslkUu2aVRVcqXyh6wAAAAAAAEBOrsXdAAAAilKTRvW0fNV6DerfW5K0bedeRUZFq3OH1lr35xZ7uZSUi5r51UKt37hVyckp6tqpjZ5+dIxcXFx08tRZbdu5V7FxCQrw91OfQaPVrnUz+Xh7admKtfLx9tIj949Su9bN8mzHmLuHyWJxkyRdCA3Xjl37JEnfL/lNb0//XPO+eE/VqwZn77vfSA0f3E9Vq1Sy9zLZteeAjp84rU7tW+ml197VyjUbHOpv3bKJ3p/ykiRpy7bdWrBoqfYdPKKqlSvq0fvvVqMGdezrklMuauTQAdnnY8dezV/0k/buP6xaNaqqT49O6n9Ld4e6P545V0t/XSUfHy89NOZOdWrfSpJ0PiRUM79aqC1bd8nP10fDBvfVwH49JUkTJk/T0eOndPeIwZrzzQ9KTrmowQN6afSdQwpxFQEAAAAAAK5v9FwBANww0tPS1ap5Y+3df1jnL4RJkn77fZ1KB/ipQrkyDmVfm/axfvt9ne4aPlBj7xmuFavW6+OZc/Os+48Nf8licdOdwwfqQmi4Zs5eUGB7MjIytWHzdh08ckwBAX4Flm/bqpkmT3hCkjSgbw+99dp4SVLnDq01+s4hGn3nELVs1kiS1Kd7J0nS8ROn9fSE1+XhUUovPvuIAvz99PSE1xURGZ2j/pOnz+rJF15VCXd3vfDUg0pNTdMbb3+ig4eP2cvs3X9Ybm6uGjVikMLCIvX5VwslSenp6Xr46Zd1+sx5Pfv4OHXq0EpT3p2hjVt22LeNjIrR5q27NGrEILm5ueqLr79TQmJSgccNAAAAAADw/w09VwAAN4wsm029unXUh599/U9wcpvW/blFQ27rq8zMTHu52Lh4rV63UeNG32HveXH2XIh+WLpcD4+7K9e6a1avonGj75AknTx1VstWrFVmZqbMZnOu5Tv2Hmb/u5enhz00yU+Av6/q16slSapQrowaN6grSerWqa26dWqr8IgoLf7pN/Xo2l69uneUJC35ZaUsbq6aNOFxubm6qmXzRurZ/y4tW7FW94wc7FD/4p+WKyMjU88/eb98vL3Uvm1zLV22ymH4s+CK5R2O85fla5Senq4Nm7crNCxCkyc8oUYN6qh7l3ba/NdOfbv4F3sPnoyMTL0y8QmZzWa5uLjolSnTdejIMXsgBAAAAAAAcKMgXAEA3FA8PUupdYumWrVuo6pUrqiUi6nq3aOTli1fYy9zaVL7mbMX5OiBEh0Tl2u9Hh6l/v17qZKy2WzKzMzKM1x5b8qLiotL0OQp0zWgbw/VrV3jqo4rIyNTz7z4htzdrXr+yQfsy8Mjo5RyMVUdeg51KB/yT8+dy4WFR8rL08M+/0wJd3cNG9zPocyVxylJ6ekZCo+IkiTd//hEh/IVK5S1/72Eu9V+Pi7fFgAAAAAA4EZDuAIAuOH06dFRE195R2vXb1b1qsGqWrmiw/oAf19J2T1CBt7a02Gdt5dHkbShWeMGsljctHzVH1r4/c8aNrivAvz95OKSPSJncnKKJDk9bNY7H36uY8dO6bPpr9uDC0kKDPCXi4uL3nr1eVmtVvvy0v45hyELCgxQfEKiIqNiFODvq7S0dC1eulwd2jRXhfJlc5S/XGBpf0nSA/eNVL06/wZF7u7WvDYBAAAAAAC4Yf0fnneNbeZnMyEAAAAASUVORK5CYII=",
    "media_type": "image/png"
  }
}
```

> AGENT

Der Browser cached die alte CSS-Datei. Ich füge Cache-Busting hinzu.

> TOOL

tool_use Edit
id: toolu_01CQRw4CnQQWbvvbp7d1taaK
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/krisenkommunikation.njk",
  "old_string": "pageCSSFile: \"/css/krisenkommunikation.css\"",
  "new_string": "pageCSSFile: \"/css/krisenkommunikation.css?v=2\""
}
```

> TOOL

tool_result
id: toolu_01CQRw4CnQQWbvvbp7d1taaK
```
The file /home/<USER>/bosarsa/src/krisenkommunikation.njk has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01RFVQE6TZpE1FXcafUMWyCA
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy with CSS cache bust",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01RFVQE6TZpE1FXcafUMWyCA
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
src/
src/krisenkommunikation.njk

sent 63,938 bytes  received 10,685 bytes  149,246.00 bytes/sec
total size is 105,737,397  speedup is 1,416.95
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 0.5s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [stage-1 1/4] FROM docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#5 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba 0.0s done
#5 DONE 0.0s

#6 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#6 resolve docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa 0.0s done
#6 DONE 0.0s

#7 [internal] load build context
#7 transferring context: 2.31MB 0.1s done
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
#12 1.404 [11ty] Writing ./_site/llms.txt from ./src/llms.njk
#12 1.412 [11ty] Writing […]

> AGENT

Deployed mit `?v=2` Cache-Busting. Einfach normal die Seite neu laden — der Browser wird die neue CSS-Datei holen, da sich die URL geändert hat.

> AGENT

No response requested.

> DEVELOPER

update sicherheitstage veranstaltung based on Terminkalender 2026 (SiTage) (1) in downloads folder. change picture and text accordingly!

> TOOL

tool_use Bash
id: toolu_01Ub9E38dno5jsuccUQ1uqbj
```json
{
  "command": "ls -lt /home/<USER>/Downloads/*SiTage* /home/<USER>/Downloads/*Terminkalender* /home/<USER>/Downloads/*sicherheitstage* 2>/dev/null",
  "description": "Find Terminkalender SiTage file"
}
```

> TOOL

tool_result ERROR
id: toolu_01Ub9E38dno5jsuccUQ1uqbj
```
Exit code 2
-rw-r--r-- 1 achildrenmile users 3234625 Mar  9 14:07 /home/<USER>/Downloads/Terminkalender 2026 (SiTage) (1).pdf
-rw-r--r-- 1 achildrenmile users 3234625 Mar  9 14:07 /home/<USER>/Downloads/Terminkalender 2026 (SiTage) (1).pdf
-rw-r--r-- 1 achildrenmile users 4663302 Mar  6 07:00 /home/<USER>/Downloads/Terminkalender 2026 (SiTage).pdf
-rw-r--r-- 1 achildrenmile users 4663302 Mar  6 07:00 /home/<USER>/Downloads/Terminkalender 2026 (SiTage).pdf
```

> TOOL

tool_use Read
id: toolu_01AP2Zy5yb2iPDHwoE373gTM
```json
{
  "file_path": "/home/<USER>/Downloads/Terminkalender 2026 (SiTage) (1).pdf",
  "pages": "1-5"
}
```

> TOOL

tool_result
id: toolu_01AP2Zy5yb2iPDHwoE373gTM
```
PDF pages extracted: 1 page(s) from /home/<USER>/Downloads/Terminkalender 2026 (SiTage) (1).pdf (3.1MB)
```

> AGENT

Let me find the current Sicherheitstage content on the site.

> TOOL

tool_use Grep
id: toolu_016vSXYWPPZqT1qmZjBf6vcf
```json
{
  "pattern": "icherheitstag",
  "path": "/home/<USER>/bosarsa/src",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_016vSXYWPPZqT1qmZjBf6vcf
```
Found 2 files
src/_data/termine.json
src/_data/presse.json
```

> TOOL

tool_use Read
id: toolu_01ByG6MRz8k8FWgFEjKPMHj2
```json
{
  "file_path": "/home/<USER>/bosarsa/src/_data/termine.json"
}
```

> TOOL

tool_result
id: toolu_01ByG6MRz8k8FWgFEjKPMHj2
```
     1→[
     2→  {
     3→    "date": "April – Oktober 2026",
     4→    "tag": "veranstaltung",
     5→    "tagLabel": "Sicherheitstage",
     6→    "title": "Sicherheitstage 2026 in K\u00e4rnten mit BOS-ARSA und \u00d6VSV-Notfunk-Beteiligung",
     7→    "image": "/sicherheitstage-2026.webp",
     8→    "imageAlt": "Sicherheitstage 2026 – Terminkalender K\u00e4rnten",
     9→    "intro": "Der K\u00e4rntner Zivilschutzverband organisiert auch 2026 wieder Sicherheitstage in ganz K\u00e4rnten. BOS-ARSA ist als Partnerorganisation mit dabei. Hier alle Termine auf einen Blick.",
    10→    "sections": [
    11→      {
    12→        "heading": "Die Termine",
    13→        "type": "table",
    14→        "columns": ["Datum", "Ort"],
    15→        "rows": [
    16→          ["Samstag, 25. April 2026", "Bleiburg"],
    17→          ["Samstag, 23. Mai 2026", "Glanhofen"],
    18→          ["Samstag, 13. Juni 2026", "Preitenegg"],
    19→          ["Samstag, 20. Juni 2026", "K\u00f6tschach-Mauthen"],
    20→          ["Samstag, 27. Juni 2026", "Lendorf"],
    21→          ["Mittwoch, 1. Juli 2026", "Strandbad Greifenburg (Jugend-Wasser-Sicherheitstag)"],
    22→          ["Donnerstag, 2. Juli 2026", "Maltschacher See (Jugend-Wasser-Sicherheitstag)"],
    23→          ["Dienstag, 7. Juli 2026", "offen (Jugend-Wasser-Sicherheitstag)"],
    24→          ["Samstag, 12. September 2026", "N\u00f6tsch im Gailtal"],
    25→          ["Samstag, 19. September 2026", "M\u00f6lbling"],
    26→          ["Samstag, 26. September 2026", "Villach"],
    27→          ["Samstag, 3. Oktober 2026", "Magdalensberg"]
    28→        ]
    29→      },
    30→      {
    31→        "heading": "Was sind Sicherheitstage?",
    32→        "type": "text",
    33→        "content": "Sicherheitstage sind Veranstaltungen des K\u00e4rntner Zivilschutzverbandes, bei denen Einsatzorganisationen und Sicherheitseinrichtungen ihre Arbeit pr\u00e4sentieren. Besucher k\u00f6nnen Ausr\u00fcstung hautnah erleben, Vorf\u00fchrungen sehen und […]

> TOOL

tool_use Read
id: toolu_0146yMnrCtFuTtCJ6zJRnWZf
```json
{
  "file_path": "/home/<USER>/bosarsa/src/termine.njk"
}
```

> TOOL

tool_result
id: toolu_0146yMnrCtFuTtCJ6zJRnWZf
```
     1→---
     2→layout: base.njk
     3→title: "Termine — BOS-ARSA"
     4→description: "Aktuelle Termine, Übungen und Veranstaltungen von BOS-ARSA – Amateurfunk im Sinne der Sicherheit"
     5→canonical: "https://bosarsa.oeradio.at/termine/"
     6→activeNav: termine
     7→pageCSSFile: "/css/termine.css"
     8→permalink: /termine/
     9→---
    10→
    11→<div class="page-content page-content--wide">
    12→  <h1>Termine & Veranstaltungen</h1>
    13→  <p class="subtitle">Aktuelle Übungen, Schulungen und Events von BOS-ARSA</p>
    14→
    15→  {% for event in termine %}
    16→  <article class="event">
    17→    {% if event.image %}
    18→    <div class="event__image">
    19→      <img src="{{ event.image }}" alt="{{ event.imageAlt }}" loading="lazy">
    20→    </div>
    21→    {% endif %}
    22→    <div class="event__body">
    23→      <div class="event__meta">
    24→        <span class="event__date">{{ event.date }}</span>
    25→        <span class="article__tag article__tag--{{ event.tag }}">{{ event.tagLabel }}</span>
    26→      </div>
    27→      <h2 class="event__title">{{ event.title }}</h2>
    28→      <p class="event__intro">{{ event.intro }}</p>
    29→
    30→      {% for section in event.sections %}
    31→      <h3 class="event__heading">{{ section.heading }}</h3>
    32→      {% if section.type == "table" %}
    33→      <div class="event__table-wrap">
    34→        <table class="event__table">
    35→          <thead>
    36→            <tr>
    37→              {% for col in section.columns %}
    38→              <th>{{ col }}</th>
    39→              {% endfor %}
    40→            </tr>
    41→          </thead>
    42→          <tbody>
    43→            {% for row in section.rows %}
    44→            <tr>
    45→              {% for cell in row %}
    46→              <td>{{ cell }}</td>
    47→              {% endfor %}
    48→            </tr>
    49→            {% endfor %}
    50→          </tbody>
    51→ […]

> AGENT

I can see the differences. The new Terminkalender has updated dates and a new entry (Lendorf moved to 5. September, and "Freizeitanlage St. Andräer See" added for 7. Juli). Let me update the data and replace the image.

> TOOL

tool_use Task
id: toolu_01J2vA9afXVCm7iZEFQqNpxU
```json
{
  "description": "Convert PDF to webp image",
  "prompt": "Check if ImageMagick (convert) or pdftoppm is available on this NixOS system. Run: which convert pdftoppm 2>/dev/null; nix-shell -p imagemagick --run \"which convert\" 2>/dev/null. I need to convert the first page of a PDF to a webp image.",
  "subagent_type": "Bash"
}
```

> TOOL

tool_result
id: toolu_01J2vA9afXVCm7iZEFQqNpxU
```
Here are the results:

- **`convert` (ImageMagick)**: Not available globally, but accessible via nix-shell:
  ```
  nix-shell -p imagemagick --run "which convert"
  /nix/store/.../bin/convert
  ```

- **`pdftoppm` (Poppler)**: Already available globally on your system at `/home/<USER>/.nix-profile/bin/pdftoppm`.

Since `pdftoppm` is already installed, the simplest approach to convert the first page of a PDF to WebP would be a two-step pipeline (pdftoppm outputs PNG/PPM, then convert to WebP), or you can use ImageMagick directly via nix-shell.

**Option A — Using pdftoppm + ImageMagick (via nix-shell) in one shot:**
```bash
pdftoppm -png -f 1 -l 1 -r 300 input.pdf - | nix-shell -p imagemagick --run "convert png:- output.webp"
```

**Option B — Using only ImageMagick via nix-shell:**
```bash
nix-shell -p imagemagick ghostscript --run "convert -density 300 'input.pdf[0]' output.webp"
```
(Ghostscript is needed as the PDF delegate for ImageMagick.)

Would you like me to run one of these on a specific PDF file?
agentId: a7d4ce6 (for resuming to continue this agent's work if needed)
<usage>total_tokens: 6026
tool_uses: 2
duration_ms: 15909</usage>
```

> TOOL

tool_use Bash
id: toolu_014BGs8E4tFFHi42KjUASvtn
```json
{
  "command": "pdftoppm -png -f 1 -l 1 -r 200 \"/home/<USER>/Downloads/Terminkalender 2026 (SiTage) (1).pdf\" /tmp/sitage && nix-shell -p imagemagick --run \"convert /tmp/sitage-1.png -quality 85 /home/<USER>/bosarsa/sicherheitstage-2026.webp\"",
  "description": "Convert PDF first page to webp",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_014BGs8E4tFFHi42KjUASvtn
```
WARNING: The convert command is deprecated in IMv7, use "magick" instead of "convert" or "magick convert"
```

> AGENT

Good, the image is updated. Now update the termine.json with the corrected dates from the new Terminkalender:

> TOOL

tool_use Edit
id: toolu_01WhDGrN8pE7FpvT8UM6YD7p
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/_data/termine.json",
  "old_string": "        \"rows\": [\n          [\"Samstag, 25. April 2026\", \"Bleiburg\"],\n          [\"Samstag, 23. Mai 2026\", \"Glanhofen\"],\n          [\"Samstag, 13. Juni 2026\", \"Preitenegg\"],\n          [\"Samstag, 20. Juni 2026\", \"K\\u00f6tschach-Mauthen\"],\n          [\"Samstag, 27. Juni 2026\", \"Lendorf\"],\n          [\"Mittwoch, 1. Juli 2026\", \"Strandbad Greifenburg (Jugend-Wasser-Sicherheitstag)\"],\n          [\"Donnerstag, 2. Juli 2026\", \"Maltschacher See (Jugend-Wasser-Sicherheitstag)\"],\n          [\"Dienstag, 7. Juli 2026\", \"offen (Jugend-Wasser-Sicherheitstag)\"],\n          [\"Samstag, 12. September 2026\", \"N\\u00f6tsch im Gailtal\"],\n          [\"Samstag, 19. September 2026\", \"M\\u00f6lbling\"],\n          [\"Samstag, 26. September 2026\", \"Villach\"],\n          [\"Samstag, 3. Oktober 2026\", \"Magdalensberg\"]\n        ]",
  "new_string": "        \"rows\": [\n          [\"Samstag, 25. April 2026\", \"Bleiburg\"],\n          [\"Samstag, 23. Mai 2026\", \"Glanhofen\"],\n          [\"Samstag, 13. Juni 2026\", \"Preitenegg\"],\n          [\"Samstag, 20. Juni 2026\", \"K\\u00f6tschach-Mauthen\"],\n          [\"Mittwoch, 1. Juli 2026\", \"Strandbad Greifenburg (Jugend-Wasser-Sicherheitstag)\"],\n          [\"Donnerstag, 2. Juli 2026\", \"Maltschacher See (Jugend-Wasser-Sicherheitstag)\"],\n          [\"Dienstag, 7. Juli 2026\", \"Freizeitanlage St. Andr\\u00e4er See (Jugend-Wasser-Sicherheitstag)\"],\n          [\"Samstag, 5. September 2026\", \"Lendorf\"],\n          [\"Samstag, 12. September 2026\", \"N\\u00f6tsch im Gailtal\"],\n          [\"Samstag, 19. September 2026\", \"M\\u00f6lbling\"],\n          [\"Samstag, 26. September 2026\", \"Villach\"],\n          [\"Samstag, 3. Oktober 2026\", \"Magdalensberg\"]\n        ]"
}
```

> TOOL

tool_result
id: toolu_01WhDGrN8pE7FpvT8UM6YD7p
```
The file /home/<USER>/bosarsa/src/_data/termine.json has been updated successfully.
```

> AGENT

Now update the intro text and the Hinweis to match the new PDF:

> TOOL

tool_use Edit
id: toolu_01TeXPyoZUUCxJ6XTvjZE2xK
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/bosarsa/src/_data/termine.json",
  "old_string": "    \"intro\": \"Der K\\u00e4rntner Zivilschutzverband organisiert auch 2026 wieder Sicherheitstage in ganz K\\u00e4rnten. BOS-ARSA ist als Partnerorganisation mit dabei. Hier alle Termine auf einen Blick.\",",
  "new_string": "    \"intro\": \"Der K\\u00e4rntner Zivilschutzverband organisiert auch 2026 wieder Sicherheitstage in ganz K\\u00e4rnten. BOS-ARSA ist als Partnerorganisation mit dabei. Hier alle Termine auf einen Blick (Stand: 09.03.2026).\","
}
```

> TOOL

tool_result
id: toolu_01TeXPyoZUUCxJ6XTvjZE2xK
```
The file /home/<USER>/bosarsa/src/_data/termine.json has been updated successfully.
```

> AGENT

Now deploy:

> TOOL

tool_use Bash
id: toolu_017SiDjmxdxYvsxTXggiyHSH
```json
{
  "command": "bash /home/<USER>/bosarsa/deploy-production.sh 2>&1",
  "description": "Deploy updated Sicherheitstage",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_017SiDjmxdxYvsxTXggiyHSH
```
[0;32m=== Deploying BOS-ARSA to achildrenmile@host-node-01 ===[0m
Host: achildrenmile@host-node-01
Remote dir: /home/<USER>/apps/bosarsa
Container: bosarsa
Port: 3417:80

[0;32mStep 1: Syncing files...[0m
sending incremental file list
sicherheitstage-2026.webp
.claude/
.claude/settings.local.json
.entire/logs/entire.log
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/context.md
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/full.jsonl
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/prompt.txt
.entire/metadata/af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6/summary.txt
.entire/tmp/
.entire/tmp/pre-prompt-af7b3b86-8238-4ee0-8e9e-bf8a458d5fd6.json
src/_data/
src/_data/termine.json

sent 646,862 bytes  received 13,884 bytes  1,321,492.00 bytes/sec
total size is 106,392,274  speedup is 161.02
[0;32mStep 2: Building and starting container...[0m
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 325B done
#1 DONE 0.1s

#2 [internal] load metadata for docker.io/library/nginx:alpine
#2 DONE 0.2s

#3 [internal] load metadata for docker.io/library/node:20-alpine
#3 DONE 1.1s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.1s

#5 [internal] load build context
#5 DONE 0.0s

#6 [stage-1 1/4] FROM docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#6 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba
#6 resolve docker.io/library/nginx:alpine@sha256:1d13701a5f9f3fb01aaa88cef2344d65b6b5bf6b7d9fa4cf0dca557a8d7702ba 0.2s done
#6 DONE 0.3s

#7 [build 1/6] FROM docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa
#7 resolve docker.io/library/node:20-alpine@sha256:b88333c42c23fbd91596ebd7fd10de239cedab9617de04142dde7315e3bc0afa 0.3s done
#7 DONE 0.3s

#5 [internal] load build context
#5 transferring context: 3.31MB 0.1s done
#5 DONE 0.2s

#8 [build 3/6] COPY package*.json ./
#8 CACHED

#9 [build 2/6] WORKDIR /app
#9 CACHED

#10 [build 4/6] RUN npm ci --production
#10 CACHED

#11 [build 5/6] COPY . .
#11 DONE 1.4s

#12 [build 6/6] […]

> AGENT

Deployed. Änderungen am Sicherheitstage-Eintrag:

**Bild**: Neues Terminkalender-Plakat (aus dem aktuellen PDF) als `sicherheitstage-2026.webp` ersetzt

**Termine aktualisiert** (Stand 09.03.2026):
- Lendorf von 27. Juni auf **5. September** verschoben
- 7. Juli: "offen" durch **Freizeitanlage St. Andräer See** ersetzt
- Intro-Text mit "(Stand: 09.03.2026)" ergänzt

> AGENT

No response requested.