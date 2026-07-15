[DEVELOPER]: Implement the following plan: # Plan: Krisenkommunikation-Seite mit PDF-Download & Online-Formular ## Context Das Krisenkommunikation-Aufnahmeformular ist ein zentrales Dokument für den Notfunkbetrieb. Es soll als eigene Seite auf der BOS-ARSA-Website verfügbar sein — sowohl als druckbare PDF als auch als interaktives Online-Formular, das client-seitig ausgefüllt und als PDF heruntergeladen werden kann. ## Neue Dateien (5) ### 1. `src/krisenkommunikation.njk` — Seitentemplate - Layout: `base.njk`, `pageCSSFile: "/css/krisenkommunikation.css"` - **Abschnitt 1**: Download-Card mit Link zur statischen PDF - **Divider**: "oder online ausfüllen" - **Abschnitt 2**: HTML-Formular mit allen Feldern des Aufnahmeformulars: - Lfd. Nr., Entgegennahme (Rufzeichen, QTH, QRG, Telefon), Datum/Uhrzeit - Notruf durch, 7 W-Fragen (WER–WARUM) als Textareas - Weitergabe-Tabelle (3 feste + 2 freie Organisationen mit Checkboxen) - Erledigt (Wann, Durch) - **Buttons**: "Als PDF herunterladen" + "Formular leeren" - Scripts am Seitenende: `jspdf.umd.min.js` + `krisenkommunikation-pdf.js` ### 2. `src/css/krisenkommunikation.css` — Seitenstile - Download-Card, Divider, Formularfelder, Weitergabe-Grid - Responsive: 4-Spalten → 2 → 1 auf Mobil; Weitergabe-Tabelle stapelt sich ### 3. `js/jspdf.umd.min.js` — jsPDF-Bibliothek (self-hosted) - Download von cdnjs (~300KB), Root-`js/`-Ordner neben `lucide.min.js` ### 4. `js/krisenkommunikation-pdf.js` — PDF-Generierung - Liest Formularwerte, erzeugt A4-PDF mit jsPDF - Logo (bosarsa.jpeg) wird beim Seitenaufruf als Base64 vorgeladen - Tabellenstruktur mit Linien/Rahmen wie das Original - Seitenumbruch […]

[AGENT]: I'll implement this plan step by step. Let me start by reading the existing files I need to modify, and download jsPDF.

[AGENT]: Now let me read all the files I need to understand and modify in parallel.

[AGENT]: Now let me read a few more reference files and check for existing assets.

[AGENT]: Now let me look at an existing page for reference, and check for the logo file and existing JS.

[AGENT]: Let me also check the plan transcript to get the PDF content details and the form fields.

[AGENT]: Now let me check the plan transcript for more details about the form structure.

[AGENT]: Now I have all the details. Let me start implementing. First, let me handle Task #1 — download jsPDF and check for the static PDF.

[AGENT]: Now download jsPDF from cdnjs.

[AGENT]: That's way too small — likely a redirect or error page. Let me try a different version/URL.

[AGENT]: Not found. Let me find the correct URL.

[AGENT]: That's the right size (~356KB). Let me verify it's valid JS.

[AGENT]: jsPDF is downloaded. Task 1 done.

[AGENT]: Now Task #2 — update `.eleventy.js` passthrough rules.

[AGENT]: Now Task #3 — create the CSS, JS, and page template. Let me start with all three files.

[AGENT]: Now create the PDF generator JS.

[AGENT]: Now create the main page template.

[AGENT]: Now Task #4 — update footer, sitemap, and llms.txt.

[AGENT]: Now Task #5 — build and verify.

[AGENT]: Build succeeded. Let me verify the key output files exist.

[AGENT]: All files present and correct.

[AGENT]: All done. Here's a summary of what was implemented: **New files (5):** - `src/krisenkommunikation.njk` — Page template with download card + full interactive form - `src/css/krisenkommunikation.css` — Responsive styles (4-col → 2 → 1 on mobile, stacking Weitergabe table) - `js/jspdf.umd.min.js` — Self-hosted jsPDF 2.5.1 library (364KB) - `js/krisenkommunikation-pdf.js` — Client-side PDF generator (logo preload, A4 layout with sections, page breaks) - `Krisenkommunikation-Aufnahmeformular.pdf` — Static PDF from Downloads (586KB) **Modified files (4):** - `.eleventy.js` — Added passthrough for `js/` and `*.pdf` - `src/_includes/footer.njk` — Added "Krisenkommunikation" link after "Presse" - `src/sitemap.njk` — New entry `/krisenkommunikation/` with lastmod 2026-03-08 - `src/llms.njk` — Added Krisenkommunikation section describing the form **Build:** Successful — all 9 templates written, 27 files copied. Ready for `bash deploy-production.sh`.

[DEVELOPER]: deploy

[AGENT]: Deployment successful. Die Krisenkommunikation-Seite ist jetzt live unter **https://bosarsa.oeradio.at/krisenkommunikation/**.

[DEVELOPER]: telefon field does not fit on the formular space it is overlapping into grey area.

[AGENT]: The issue is that grid items with `<input>` elements have a default `min-width` that prevents them from shrinking below their intrinsic size. I need to add `min-width: 0` to the form group, and also add a medium breakpoint so the 4-column row wraps to 2 columns on tablets.

[AGENT]: Also ensure inputs respect their container width:

[AGENT]: Now add a medium breakpoint so 4 columns become 2 on tablets:

[AGENT]: Fix deployed. The changes: - Added `min-width: 0` to `.krisen-form__group` and inputs so they shrink properly within the grid - Added `width: 100%` to inputs to fill their container - Added a medium breakpoint at 900px where the 4-column row becomes 2 columns, giving each field more space before collapsing to 1 column on mobile

[DEVELOPER]: not visible. see latest screenshot

[AGENT]: Those are ChatGPT images, not screenshots. Let me check for actual screenshots elsewhere.

[AGENT]: I can see the issue — the Telefon field overflows past the white form card's right edge. The CSS fix with `min-width: 0` isn't enough; the grid tracks themselves need `minmax(0, 1fr)` to allow shrinking properly.

[AGENT]: Also fix the `display: grid` on `--2` and `--3` rows — they were missing `display: grid` since they only override `grid-template-columns` but the template uses them as standalone classes (not combined with `krisen-form__row`).

[AGENT]: The `--2` and `--3` classes are used standalone. They need their own `display: grid` and gap:

[AGENT]: Deployed. The fixes: - Changed all grid columns from `1fr` to `minmax(0, 1fr)` — this allows grid tracks to shrink below their content's intrinsic minimum width - Added `overflow: hidden` on `.krisen-form` as a safety net - Fixed `--2` and `--3` row variants to include `display: grid` (they were used standalone without the base `krisen-form__row` class) Do a hard refresh (Ctrl+Shift+R) to bypass the CSS cache and check again.