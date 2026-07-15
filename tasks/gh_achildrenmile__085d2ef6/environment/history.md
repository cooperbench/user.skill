> DEVELOPER

Implement the following plan: # Plan: "Aktuelles" Seite mit Einzelartikeln ## Context BOS-ARSA braucht eine eigene Seite für Vereinsnachrichten, Veranstaltungsberichte und Wissensartikel. Die aktuelle Termine-Seite enthält z.B. den Sicherheitstage-Beitrag, der eigentlich eher ein Artikel als eine reine Terminliste ist. `/aktuelles/` wird die zentrale Anlaufstelle für solche Inhalte, mit eigenen Unterseiten pro Beitrag. ## Neue Dateien (4) ### 1. `src/_data/aktuelles.json` Array von Artikeln (neueste zuerst). Erster Eintrag: Sicherheitstage 2026 (adaptiert aus termine.json). Felder: `slug`, `date` (ISO), `dateDisplay`, `tag`, `tagLabel`, `title`, `image`, `imageAlt`, `intro`, `sections[]`, `author` Section-Typen: `text`, `table`, `image` (figure+caption), `list` (ul/li) ### 2. `src/aktuelles/index.njk` — Listing `/aktuelles/` - Layout base.njk, `activeNav: aktuelles`, `pageCSSFile: "/css/aktuelles.css"` - Karten mit: Bild-Thumbnail, Datum+Tag, Titel, Teaser, "Weiterlesen →" - Jede Karte verlinkt zu `/aktuelles/{slug}/` ### 3. `src/aktuelles/artikel.njk` — Einzelartikel (Pagination) - Eleventy Pagination im Front Matter (kein .eleventy.js nötig): ```yaml pagination: data: aktuelles size: 1 alias: article permalink: /aktuelles/{{ article.slug }}/ eleventyComputed: title: "{{ article.title }} — BOS-ARSA" ``` - "← Zurück zu Aktuelles" Link, Hero-Bild, Meta, Sections-Rendering - Wiederverwendung der event__* Styles (kopiert in aktuelles.css) ### 4. `src/css/aktuelles.css` - Listing-Karten (`.aktuelles-card`): Bild oben, Body unten, Hover - Artikel-Detail (`.aktuelles-article`): Hero-Bild, Body mit Sections - Zurück-Link, figure/figcaption, ul/li Styles - Event-Styles aus termine.css kopiert (event__meta, […]

> AGENT

I'll implement the "Aktuelles" section. Let me start by reading the existing files I need to understand and modify.

> AGENT

Now let me read the existing files I need.

> AGENT

Let me also read the termine index.njk and the base layout for reference.

> AGENT

Now I have everything I need. Let me now read the plan transcript for any specific details. Now let me implement everything. Starting with Task #1: creating the data file.

> AGENT

Now creating the CSS file.

> AGENT

Now creating the two Nunjucks templates.

> AGENT

Now updating the existing files. Nav: add "Aktuelles" before "Termine".

> AGENT

Footer: add "Aktuelles" before "Termine".

> AGENT

Sitemap: add Aktuelles listing + dynamic single articles.

> AGENT

You've hit your limit · resets 6pm (Europe/Vienna)