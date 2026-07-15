> DEVELOPER

hey man so I wanna make my brother a website for his music studio bang bang studios. I need to have some kind of cms set. Ideally I would host everything here and not use netlify or anything. I want it to be very cool and I have heard about a couple of claude skills that could help with the ui (https://impeccable.style/, https://www.tasteskill.dev/, https://emilkowal.ski/skill). The main thing I want is that one the hero element we have a music visualiser from an mp3 that we choose in the cms and it needs to look fucking cool I dont really have any design refrences but I would like for you to compile some for me and then I can pcik the aethetic of the stime

> AGENT

Cool project. Before I dive in, let me peek at your existing setup and ask a couple of questions so I send you down the right path.

> TOOL

tool_use Bash
id: toolu_01HvkCBTjihkSafTKifY6tR9
```json
{
  "command": "ls /Users/sumeet/matrix/web/aether/ && echo \"---services---\" && ls /Users/sumeet/matrix/web/aether/services/",
  "description": "List aether project structure"
}
```

> TOOL

tool_result
id: toolu_01HvkCBTjihkSafTKifY6tR9
```
AGENTS.md
docker-compose-dev.yml
docker-compose-mailcow.yml
docker-compose-plausible.yml
docker-compose-prod.yml
docker-compose.yml
README.md
scripts
services
---services---
ao3
arcanecodex
bucketbot
card
gateway
goblinbot
reliq
sumeetsaini_com
vulkan
```

> TOOL

tool_use Bash
id: toolu_01PvoXFeQhWh8m4cuohnA3EL
```json
{
  "command": "cat /Users/sumeet/matrix/web/aether/AGENTS.md 2>/dev/null | head -80 && echo \"---\" && ls /Users/sumeet/matrix/web/aether/services/sumeetsaini_com 2>/dev/null | head -20",
  "description": "Inspect aether docs and similar service"
}
```

> TOOL

tool_result
id: toolu_01PvoXFeQhWh8m4cuohnA3EL
```
# Aether Chest - Agent Guidelines

## Build & Development Commands

### Frontend (sumeetsaini_com)
- `npm run dev` - Start live-server on port 8080
- No linting/testing configured - use browser console for debugging

### Backend (vulkan) 
- `npm run dev` - Start nodemon for Express.js on port 3000
- `npm test` - No tests configured (placeholder)

### Full Stack
- `docker compose -f docker-compose.yml -f docker-compose-dev.yml up` - Start all services (dev, zero setup)
- `docker compose -f docker-compose.yml -f docker-compose-prod.yml up` - Start all services (prod, requires GitHub Secrets)

## Code Style Guidelines

### JavaScript/TypeScript
- **Frontend**: ES6 modules, import statements at top
- **Backend**: CommonJS require() statements
- Use camelCase for variables/functions
- Use UPPER_SNAKE_CASE for constants
- Event-driven architecture with custom emit/on functions
- Error handling with console.error() and early returns

### CSS
- CSS custom properties (variables) in :root
- BEM-style naming for classes
- Mobile-first responsive design
- Flexbox/Grid for layouts

### File Organization
- Modular structure: controller/, shape/, popup/, shared/
- Configuration in separate config.js files
- State management in dedicated state files
- Route handlers in routes/ directory (backend)

### Security
- Helmet middleware for security headers
- […]

> AGENT

You've already got a docker-compose VPS setup at `aether` with a static-site pattern (`sumeetsaini_com` with a `content/` folder). I can drop a `bangbang_studios` service alongside it. Two quick questions before I start compiling references:

> TOOL

tool_use AskUserQuestion
id: toolu_01WtutH7AgQa5YrEmcYWgoBv
```json
{
  "questions": [
    {
      "question": "How do you want me to deliver the design references?",
      "header": "References format",
      "multiSelect": false,
      "options": [
        {
          "label": "Live aesthetic prototypes (Recommended)",
          "description": "I build 4-5 self-contained HTML files, each a working music visualizer in a different aesthetic (brutalist, glassy/liquid, retro-CRT, organic/blob, minimal-mono). You open them in a browser with your brother's MP3 and pick. This is what the three skills you mentioned (impeccable.style, tasteskill, emilkowal) are best at."
        },
        {
          "label": "Curated reference gallery",
          "description": "I gather ~20 links to real music studio sites + visualizer examples (Awwwards, codepens, studio sites) and write up the aesthetic of each. You browse, then I build."
        },
        {
          "label": "Both",
          "description": "Gallery first to narrow the vibe, then 2-3 prototypes in the directions you liked."
        }
      ]
    },
    {
      "question": "What's the CMS shape? Your brother needs to upload an MP3 + edit text — how technical is he?",
      "header": "CMS technicality",
      "multiSelect": false,
      "options": [
        {
          "label": "Git-based / markdown files (Recommended)",
          "description": "Same pattern as sumeetsaini_com — a `content/` folder with markdown + an `assets/` folder for the MP3. You commit on his behalf, or he uses Decap/Sveltia CMS […]

> TOOL

tool_result
id: toolu_01WtutH7AgQa5YrEmcYWgoBv
```
Your questions have been answered: "How do you want me to deliver the design references?"="Just static images is fine for the vibe", "What's the CMS shape? Your brother needs to upload an MP3 + edit text — how technical is he?"="Git-based / markdown files (Recommended)", "What does the site need beyond the hero visualizer?"="Services / pricing, Past work / portfolio, About / studio photos, Contact / booking form". You can now continue with these answers in mind.
```