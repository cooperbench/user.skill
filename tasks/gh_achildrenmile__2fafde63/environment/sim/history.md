[DEVELOPER]: Implement the following plan: # Plan: Nav-Gruppierung mit Dropdowns ## Context Die Navigation hat 10 Einträge (11 mit Aktuelles). Das ist zu viel für eine Zeile. Lösung: Zwei Dropdown-Gruppen fassen die Homepage-Anker zusammen. Eigenständige Seiten bleiben Top-Level. ## Neue Nav-Struktur (6 sichtbare Items statt 11) | Nav-Item | Typ | Inhalt | |----------|-----|--------| | **Verein** ▾ | Dropdown | Über uns, Videos, Vorstand, Ziele, Mitglied werden | | **Funk** ▾ | Dropdown | Funkbetrieb, Krisenkommunikation | | Aktuelles | Link | `/aktuelles/` | | Termine | Link | `/termine/` | | Presse | Link | `/presse/` | | Kontakt | Link | `#kontakt` / `/#kontakt` | ## Technischer Ansatz CSS-only Dropdowns auf Desktop (`:hover` öffnet Panel). Auf Mobile (≤768px) werden Sub-Items flach eingerückt angezeigt (immer sichtbar, kein Hover). Minimales JS nur für `aria-expanded` Accessibility + Touch-Tap-Support. ## Dateien (3 Änderungen) ### 1. `src/_includes/nav.njk` Flache `<ul>` wird ersetzt durch Dropdown-Gruppen: - `<li class="nav__dropdown">` mit `<button class="nav__dropdown-toggle">` + `<ul class="nav__dropdown-menu">` - Verein-Dropdown: Über uns, Videos, Vorstand, Ziele, Mitglied werden - Funk-Dropdown: Funkbetrieb, Krisenkommunikation - Direkte Links: Aktuelles, Termine, Presse, Kontakt ### 2. `src/css/base.css` Neue CSS-Regeln nach `.nav__links a.active`: **Desktop:** - `.nav__dropdown` — `position: relative` - `.nav__dropdown-toggle` — Button gleich gestylt wie Nav-Links, […]

[AGENT]: I'll implement the nav dropdown grouping. Let me start by reading the current files.

[AGENT]: Now let me check if there's an aktuelles page to reference.

[AGENT]: Good, the aktuelles page exists. Now I'll create the task list and implement all changes.

[AGENT]: Now add the dropdown CSS to base.css. I'll insert the dropdown styles after the `.nav__links a.active` rule (line 135) and update the mobile media query.

[AGENT]: Now update the mobile media query to handle dropdowns on mobile (flat, indented, always visible).

[AGENT]: Now add the dropdown JS in base.njk. I'll add it after the existing mobile menu code.

[AGENT]: Now add the Aktuelles link to the footer.

[AGENT]: Build successful. Let me verify the output looks correct.

[AGENT]: Everything checks out. Let me verify the footer too.

[AGENT]: All done. Here's a summary of the changes: ### `src/_includes/nav.njk` - Replaced flat 10-item `<ul>` with **6 visible items**: 2 dropdown groups + 4 direct links - **Verein** dropdown: Über uns, Videos, Vorstand, Ziele, Mitglied werden - **Funk** dropdown: Funkbetrieb, Krisenkommunikation - Direct links: Aktuelles, Termine, Presse, Kontakt ### `src/css/base.css` - Added dropdown styles: `.nav__dropdown`, `.nav__dropdown-toggle`, `.nav__dropdown-menu`, `.nav__chevron` - **Desktop**: CSS-only `:hover` opens dropdown panel (absolute positioned, dark navy background, box-shadow) - **Mobile (≤768px)**: Sub-items are always visible, flat/indented with `padding-left: 16px`, group headers styled as gold labels, chevron hidden ### `src/_includes/base.njk` - Added JS for **touch/keyboard support**: clicking toggle buttons opens/closes dropdowns with `aria-expanded` + `.open` class - Closes other dropdowns when opening one; closes all on outside click ### `src/_includes/footer.njk` - Added Aktuelles link to footer navigation list