> DEVELOPER

https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/

[Image #1] remova o italico dos textos da colmeia

> AGENT

Vou primeiro entender a estrutura da página da colmeia (Grupos de Trabalho) para localizar onde está aplicado o itálico nos textos.

Pelas memórias do projeto, a "colmeia" é o SVG dos Grupos de Trabalho (hexágonos 6 eixos, posts 26666 PT / 71726 EN, em `/atuacao/grupos-de-trabalho/`). O itálico que você quer remover está nos nomes das instituições facilitadoras (ex: "Instituto de Governança de Terras - IGT", "para Políticas de Saúde - IEPS", "Plataforma Parceiros pela Amazônia - PPA").

Deixa eu localizar a fonte desses textos.

> TOOL

tool_use Bash
id: toolu_01Tg73nYASzgFDLVsavYL6dD
```json
{
  "command": "find wordpress/wp-content/mu-plugins -name \"*colmeia*\" -o -name \"*grupos*\" 2>/dev/null; echo \"---SVG widget---\"; ls -la wordpress/wp-content/mu-plugins/bit-elementor-svg-widget/svg/ 2>/dev/null",
  "description": "Localizar arquivos da colmeia/grupos de trabalho"
}
```

> TOOL

tool_use Bash
id: toolu_01LVUyezM54FResfdQpt9HFv
```json
{
  "command": "grep -rl \"Governança de Terras\\|Políticas de Saúde\\|Parceiros pela Amazônia\\|Facilitação\\|Roda Educativa\\|Segurança Pública\" wordpress/wp-content/ 2>/dev/null | head -20",
  "description": "Buscar textos da colmeia no wp-content"
}
```

> TOOL

tool_result
id: toolu_01Tg73nYASzgFDLVsavYL6dD
```
---SVG widget---
total 120
drwxr-xr-x@ 4 dcambria  staff    128 13 mar 18:10 ./
drwxr-xr-x@ 4 dcambria  staff    128  1 mai 05:01 ../
-rwxr-xr-x@ 1 dcambria  staff  12021 13 mar 18:10 espiral-concertacao.svg
-rwxr-xr-x@ 1 dcambria  staff  46039 13 mar 18:10 logo-concertacao.svg
```

> TOOL

tool_result
id: toolu_01LVUyezM54FResfdQpt9HFv
```
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/estudos/experiencias-promissoras-de-preservacao-e-enfrentamento-ao-crime-e-a-violencia-a-amazonia/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#eixo=eixo20&jsf=jet-engine%3aestudos&tax=eixos%3a2401/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#_label=mudanca-do-uso-do-solo&eixo=eixo8&jsf=jet-engine%3aestudos&tax=eixos%3a180/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#_label=cidades&eixo=eixo18&jsf=jet-engine%3aestudos&tax=eixos%3a2360/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#eixo=eixo4/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#_label=cultura&eixo=eixo7&jsf=jet-engine%3aestudos&tax=eixos%3a178/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#jsf=jet-engine%3aestudos&tax=eixos%3a172/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/mapa-das-plataformas/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#eixo=eixo5&jsf=jet-engine%3aestudos&tax=eixos%3a177/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#eixo=eixo3&jsf=jet-engine%3aestudos&tax=eixos%3a175/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#eixo=eixo14&jsf=jet-engine%3aestudos&tax=eixos%3a1819/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#eixo=eixo13&jsf=jet-engine%3aestudos&tax=eixos%3a185/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/conhecimento/espiral-de-conhecimento/#jsf=jet-engine%3aestudos&tax=eixos%3a184/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/en/knowledge/spiral-of-knowledge/#eixo=eixo14&jsf=jet-engine%3aestudos&tax=eixos%3a1819/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/en/knowledge/spiral-of-knowledge/#eixo=eixo14&tax=eixos%3a1819/index-https.html
wordpress/wp-content/cache/wp-rocket/concertacao.bureau-it.com/en/knowledge/spiral-of-knowledge/index-https.html
wordpress/wp-content/uploads/pre-orphan-fonts-removal-20260518-235712.sql
wordpress/wp-content/uploads/pre-barlow-removal-20260518-232334.sql
wordpress/wp-content/uploads/2023/02/gt9_en_mobile1-2.svg
```

> AGENT

A imagem da colmeia parece ser composta por logos de instituições (não texto SVG editável). Os títulos com itálico ("Instituto de Governança de Terras - IGT", etc.) provavelmente estão no conteúdo Elementor da página ou em um SVG. Vou verificar o conteúdo real da página `/atuacao/grupos-de-trabalho/`.

Primeiro, deixa eu confirmar qual ambiente está rodando e o ID do post.

> TOOL

tool_use Bash
id: toolu_01B7LtVEsd6TUiRNQruyJHmG
```json
{
  "command": "/home/<USER>/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh status 2>/dev/null | head -20",
  "description": "Verificar status dos containers"
}
```

> TOOL

tool_use Bash
id: toolu_0177Pbxc4qhK8gPFP3NpcLT4
```json
{
  "command": "grep -rl \"Governança de Terras\\|gt9_en_mobile\\|Facilitação:\" wordpress/wp-content/uploads/2023/02/ 2>/dev/null; echo \"---svgs grupos---\"; ls -la wordpress/wp-content/uploads/2023/02/*.svg 2>/dev/null | grep -i \"gt\\|grupo\\|colmeia\" | head",
  "description": "Buscar SVGs de grupos de trabalho nos uploads"
}
```

> TOOL

tool_result
id: toolu_01B7LtVEsd6TUiRNQruyJHmG
```
[38;2;102;217;239mCores ativadas![0m

[38;2;126;142;145m ╭───────────────────────────────────  [38;2;231;221;109mBIT BPO[38;2;126;142;145m  ─────────╮ [0m
[38;2;126;142;145m │  [38;2;166;226;46m▄[38;2;126;142;145m                                                    │ [0m
[38;2;126;142;145m │  [38;2;166;226;46m██▄[0m   [1;38;2;166;226;46mDocker[38;2;126;142;145m                                         │ [0m
[38;2;126;142;145m │  [38;2;166;226;46m████▄[0m  [1;38;2;166;226;46mDevil[38;2;126;142;145m                                         │ [0m
[38;2;126;142;145m │  [38;2;166;226;46m█▀[38;2;126;142;145m                                                   │ [0m
[38;2;126;142;145m ├───────────────────────────────────────────────────────┤ [0m
[38;2;126;142;145m │  [38;2;255;255;255mdocker-dev.sh[38;2;126;142;145m                                        │ [0m
[38;2;126;142;145m │  [38;2;255;255;255mVersao: 2.13.1[38;2;126;142;145m                                       │ [0m
[38;2;126;142;145m │  [38;2;255;255;255mAmbiente WordPress DEV em Docker[38;2;126;142;145m                     │ [0m
[38;2;126;142;145m ╰───────────────────────────────────────────────────────╯ [0m


  ✅ mysql: rodando
  ✅ redis: rodando
  ✅ wordpress: rodando
  ✅ nginx: rodando

  ✅ WordPress: configurado
```

> TOOL

tool_result
id: toolu_0177Pbxc4qhK8gPFP3NpcLT4
```
wordpress/wp-content/uploads/2023/02/gt9_en_mobile1-2.svg
---svgs grupos---
-rwxrwxr-x@ 1 dcambria  _appstore  188220 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_en_desk.svg
-rwxrwxr-x@ 1 dcambria  _appstore  188800 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_en_desk1-1.svg
-rwxrwxr-x@ 1 dcambria  _appstore  188800 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_en_desk1-3.svg
-rwxrwxr-x@ 1 dcambria  _appstore  188193 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_en_desk1.svg
-rwxrwxr-x@ 1 dcambria  _appstore  189720 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_en_mobile.svg
-rwxrwxr-x@ 1 dcambria  _appstore  190293 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_en_mobile1-2.svg
-rwxrwxr-x@ 1 dcambria  _appstore  189693 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_en_mobile1.svg
-rwxrwxr-x@ 1 dcambria  _appstore  198564 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_pt_desk.svg
-rwxrwxr-x@ 1 dcambria  _appstore  198537 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_pt_desk1.svg
-rwxrwxr-x@ 1 dcambria  _appstore  200142 26 fev  2023 wordpress/wp-content/uploads/2023/02/gt9_pt_mobile.svg
```

> AGENT

A colmeia é um SVG (`gt9_pt_desk.svg`, `gt9_en_desk.svg`, etc.) embutido na página. O itálico está dentro do SVG. Vou descobrir qual SVG está realmente sendo usado na página de produção e como o itálico está aplicado.

Deixa eu verificar primeiro qual é o post da página e qual SVG ele referencia, e ao mesmo tempo inspecionar o itálico dentro de um dos SVGs desktop.

> TOOL

tool_use Bash
id: toolu_01JcjphvfQrZJ93Uhhce5mj9
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ngrep -o 'font-style[^;\"]*italic[^;\"]*\\|font-style:italic\\|font-style: italic\\|italic' wordpress/wp-content/uploads/2023/02/gt9_pt_desk.svg | sort | uniq -c\necho \"=== contagem total de 'italic' por arquivo ===\"\nfor f in wordpress/wp-content/uploads/2023/02/gt9_pt_desk.svg wordpress/wp-content/uploads/2023/02/gt9_en_desk.svg wordpress/wp-content/uploads/2023/02/gt9_pt_mobile.svg wordpress/wp-content/uploads/2023/02/gt9_en_mobile.svg; do\n  echo \"$f: $(grep -o 'italic' \"$f\" | wc -l | tr -d ' ') ocorrências de 'italic'\"\ndone",
  "description": "Contar ocorrências de italic nos SVGs da colmeia"
}
```

> TOOL

tool_result
id: toolu_01JcjphvfQrZJ93Uhhce5mj9
```
=== contagem total de 'italic' por arquivo ===
wordpress/wp-content/uploads/2023/02/gt9_pt_desk.svg: 0 ocorrências de 'italic'
wordpress/wp-content/uploads/2023/02/gt9_en_desk.svg: 0 ocorrências de 'italic'
wordpress/wp-content/uploads/2023/02/gt9_pt_mobile.svg: 0 ocorrências de 'italic'
wordpress/wp-content/uploads/2023/02/gt9_en_mobile.svg: 0 ocorrências de 'italic'
```

> AGENT

Esses SVGs antigos (2023) não têm itálico, então provavelmente não são os usados atualmente na página em produção. O itálico pode estar:
1. Num SVG diferente/mais recente
2. No texto Elementor (HTML) com `<em>` ou `font-style: italic` no CSS

Deixa eu inspecionar a página real em produção para ver exatamente como o itálico está sendo aplicado (no DOM).

> TOOL

tool_use ToolSearch
id: toolu_01Jo92DmjPQCrDxxExVBNrJ3
```json
{
  "query": "select:mcp__playwright__browser_navigate,mcp__playwright__browser_evaluate,mcp__playwright__browser_close",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_01Jo92DmjPQCrDxxExVBNrJ3
```
{
  "type": "tool_reference",
  "tool_name": "mcp__playwright__browser_navigate"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__playwright__browser_evaluate"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__playwright__browser_close"
}
```

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_01S4iNx6ddhm8YZYKMLS4cCx
```json
{
  "url": "https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/"
}
```

> TOOL

tool_result
id: toolu_01S4iNx6ddhm8YZYKMLS4cCx
```
### Ran Playwright code
```js
await page.goto('https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/');
```
### Page
- Page URL: https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/
- Page Title: Grupos de Trabalho – Uma Concertação pela Amazônia
### Snapshot
- [Snapshot](.playwright-mcp/page-2026-06-05T21-31-59-542Z.yml)
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-31-54-487Z.log#L1-L2
```

> AGENT

Agora vou inspecionar onde está o itálico — procurar elementos com `font-style: italic` que contenham os textos da colmeia.

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01XjkZ95G1NSPEfC1ZUFXW2Q
```json
{
  "function": "() => {\n  const results = [];\n  // Procurar todos os elementos com font-style italic computado\n  const all = document.querySelectorAll('body *');\n  for (const el of all) {\n    const cs = getComputedStyle(el);\n    if (cs.fontStyle === 'italic' || cs.fontStyle === 'oblique') {\n      const txt = (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 80);\n      if (txt && el.children.length === 0) { // leaf nodes com texto\n        results.push({\n          tag: el.tagName.toLowerCase(),\n          cls: el.className && typeof el.className === 'string' ? el.className : '',\n          txt: txt,\n          fontStyle: cs.fontStyle\n        });\n      }\n    }\n  }\n  // Também checar tags <em> e <i>\n  const ems = [...document.querySelectorAll('em, i')].map(e => ({\n    tag: e.tagName.toLowerCase(),\n    txt: (e.textContent||'').trim().slice(0,80)\n  }));\n  return JSON.stringify({ italicComputed: results, emTags: ems }, null, 2);\n}"
}
```

> TOOL

tool_result
id: toolu_01XjkZ95G1NSPEfC1ZUFXW2Q
```
### Result
"{\n  \"italicComputed\": [\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Instituto de Governança de Terras - IGT\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"(Instituto de Governança de Terras - IGT)\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"para Políticas de Saúde - IEPS\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"para Políticas de Saúde - IEPS\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Roda Educativa\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Roda Educativa\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Plataforma Parceiros\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"pela Amazônia - PPA\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Parceiros pela Amazônia\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Platform - PPA\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Instituto de Governança de Terras - IGT\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"(Instituto de Governança de Terras - IGT)\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"para Políticas de Saúde - IEPS\",\n      \"fontStyle\": \"italic\"\n    },\n    {\n      \"tag\": \"tspan\",\n      \"cls\": \"\",\n      \"txt\": \"Instituto de Estudos\",\n      \"fontStyle\": \"italic\"\n    },\n […]

> AGENT

Confirmado: o itálico está em elementos `<tspan>` **dentro de SVGs inline**. Há tanto a versão PT quanto a EN (note "Instituto de Estudos / para Políticas de Saúde - IEPS" e "Parceiros pela Amazônia Platform - PPA"). O itálico vem de `font-style: italic` aplicado via atributo no `<tspan>` ou via classe CSS dentro do `<svg>`.

Vou inspecionar como exatamente o itálico está definido nesses tspans (atributo inline `font-style` ou classe CSS) e de qual SVG/`<img>` esses SVGs inline vêm — preciso saber se é SVG inline no DOM (via mu-plugin SVG widget) ou um arquivo `.svg` referenciado.

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01Arv9HwbLFxAFV3f5xx9VhS
```json
{
  "function": "() => {\n  // Encontrar o tspan italic e subir até o <svg> raiz\n  const tspans = [...document.querySelectorAll('tspan')].filter(t => {\n    const cs = getComputedStyle(t);\n    return cs.fontStyle === 'italic';\n  });\n  const out = [];\n  const svgsSeen = new Set();\n  for (const t of tspans.slice(0,4)) {\n    // como o italic é aplicado?\n    const inlineStyle = t.getAttribute('style');\n    const fontStyleAttr = t.getAttribute('font-style');\n    const cls = t.getAttribute('class');\n    // achar svg raiz\n    let svg = t.closest('svg');\n    let rootSvg = svg;\n    // pegar id do svg e quem é o parent (img? object? inline?)\n    let svgId = rootSvg ? rootSvg.getAttribute('id') : null;\n    let svgClass = rootSvg ? rootSvg.getAttribute('class') : null;\n    let svgKey = svgId + '|' + svgClass;\n    out.push({\n      tspanText: t.textContent.slice(0,40),\n      inlineStyle, fontStyleAttr, cls,\n      svgId, svgClass,\n      // classes definidas no <style> do svg?\n    });\n  }\n  // procurar blocos <style> dentro dos SVGs com 'italic'\n  const styleBlocks = [...document.querySelectorAll('svg style')]\n    .map(s => s.textContent)\n    .filter(txt => /italic/i.test(txt))\n    .map(txt => txt.match(/[^{}]*italic[^{}]*\\{[^}]*\\}|\\.[\\w-]+\\s*\\{[^}]*italic[^}]*\\}/gi) || txt.slice(0,300));\n  return JSON.stringify({ tspans: out, svgStyleBlocksWithItalic: styleBlocks }, null, 2);\n}"
}
```

> TOOL

tool_result
id: toolu_01Arv9HwbLFxAFV3f5xx9VhS
```
### Result
"{\n  \"tspans\": [\n    {\n      \"tspanText\": \"Instituto de Governança de Terras - IGT\",\n      \"inlineStyle\": null,\n      \"fontStyleAttr\": null,\n      \"cls\": \"italic\",\n      \"svgId\": \"mobile\",\n      \"svgClass\": \"gtSVG mobile\"\n    },\n    {\n      \"tspanText\": \"(Instituto de Governança de Terras - IGT\",\n      \"inlineStyle\": null,\n      \"fontStyleAttr\": null,\n      \"cls\": \"italic\",\n      \"svgId\": \"mobile\",\n      \"svgClass\": \"gtSVG mobile\"\n    },\n    {\n      \"tspanText\": \"para Políticas de Saúde - IEPS\",\n      \"inlineStyle\": null,\n      \"fontStyleAttr\": null,\n      \"cls\": \"italic\",\n      \"svgId\": \"mobile\",\n      \"svgClass\": \"gtSVG mobile\"\n    },\n    {\n      \"tspanText\": \"para Políticas de Saúde - IEPS\",\n      \"inlineStyle\": null,\n      \"fontStyleAttr\": null,\n      \"cls\": \"italic\",\n      \"svgId\": \"mobile\",\n      \"svgClass\": \"gtSVG mobile\"\n    }\n  ],\n  \"svgStyleBlocksWithItalic\": []\n}"
### Ran Playwright code
```js
await page.evaluate('() => {\n  // Encontrar o tspan italic e subir até o <svg> raiz\n  const tspans = [...document.querySelectorAll(\'tspan\')].filter(t => {\n    const cs = getComputedStyle(t);\n    return cs.fontStyle === \'italic\';\n  });\n  const out = [];\n  const svgsSeen = new Set();\n  for (const t of tspans.slice(0,4)) {\n    // como o italic é aplicado?\n    const inlineStyle = t.getAttribute(\'style\');\n    const fontStyleAttr = t.getAttribute(\'font-style\');\n    const cls = t.getAttribute(\'class\');\n    // achar svg raiz\n    let svg = t.closest(\'svg\');\n    let rootSvg = svg;\n    // pegar id do svg e quem é o parent (img? object? inline?)\n    let svgId = rootSvg ? rootSvg.getAttribute(\'id\') : null;\n    let svgClass = rootSvg ? […]

> AGENT

Agora está claro. O itálico vem de **`<tspan class="italic">`** dentro de SVGs inline (`<svg class="gtSVG mobile">` e provavelmente `<svg class="gtSVG desktop">`). A classe `.italic` aplica `font-style: italic`. O SVG está inline no DOM — não é um `<img src>`, é o SVG inline. 

Vou descobrir:
1. Onde a regra `.italic { font-style: italic }` está definida (CSS externo, não no `<style>` do SVG)
2. De onde esses SVGs inline vêm — qual mu-plugin/widget os injeta

Vou inspecionar o source HTML cru da página e localizar os SVGs `gtSVG`.

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01DJLtwGog67yD2KpirTS3u3
```json
{
  "function": "() => {\n  // De onde vem a regra .italic? procurar nas stylesheets\n  const rules = [];\n  for (const sheet of document.styleSheets) {\n    let cssRules;\n    try { cssRules = sheet.cssRules; } catch(e) { continue; }\n    if (!cssRules) continue;\n    for (const r of cssRules) {\n      if (r.selectorText && /\\.italic\\b/.test(r.selectorText) && /italic/i.test(r.cssText)) {\n        rules.push({ href: sheet.href ? sheet.href.split('/').slice(-2).join('/') : 'inline', sel: r.selectorText, css: r.cssText.slice(0,160) });\n      }\n    }\n  }\n  // listar os SVGs gtSVG e seus ids/classes + parent container\n  const svgs = [...document.querySelectorAll('svg.gtSVG')].map(s => ({\n    id: s.id, cls: s.getAttribute('class'),\n    parentTag: s.parentElement.tagName.toLowerCase(),\n    parentCls: s.parentElement.className,\n    italicCount: s.querySelectorAll('tspan.italic').length,\n    totalTspanItalicByAttr: s.querySelectorAll('[class*=\"italic\"]').length\n  }));\n  return JSON.stringify({ italicRules: rules, gtSVGs: svgs }, null, 2);\n}"
}
```

> TOOL

tool_result
id: toolu_01DJLtwGog67yD2KpirTS3u3
```
### Result
"{\n  \"italicRules\": [\n    {\n      \"href\": \"inline\",\n      \"sel\": \".gtSVG .italic\",\n      \"css\": \".gtSVG .italic { font-style: italic; fill: var(--GT-TEXT); }\"\n    }\n  ],\n  \"gtSVGs\": [\n    {\n      \"id\": \"mobile\",\n      \"cls\": \"gtSVG mobile\",\n      \"parentTag\": \"div\",\n      \"parentCls\": \"elementor-element elementor-element-da94e3a elementor-widget elementor-widget-html\",\n      \"italicCount\": 10,\n      \"totalTspanItalicByAttr\": 10\n    },\n    {\n      \"id\": \"desktop\",\n      \"cls\": \"gtSVG desktop\",\n      \"parentTag\": \"div\",\n      \"parentCls\": \"elementor-element elementor-element-da94e3a elementor-widget elementor-widget-html\",\n      \"italicCount\": 9,\n      \"totalTspanItalicByAttr\": 9\n    }\n  ]\n}"
### Ran Playwright code
```js
await page.evaluate('() => {\n  // De onde vem a regra .italic? procurar nas stylesheets\n  const rules = [];\n  for (const sheet of document.styleSheets) {\n    let cssRules;\n    try { cssRules = sheet.cssRules; } catch(e) { continue; }\n    if (!cssRules) continue;\n    for (const r of cssRules) {\n      if (r.selectorText && /\\.italic\\b/.test(r.selectorText) && /italic/i.test(r.cssText)) {\n        rules.push({ href: sheet.href ? sheet.href.split(\'/\').slice(-2).join(\'/\') : \'inline\', sel: r.selectorText, css: r.cssText.slice(0,160) });\n      }\n    }\n  }\n  // listar os SVGs gtSVG e seus ids/classes + parent container\n  const svgs = [...document.querySelectorAll(\'svg.gtSVG\')].map(s => ({\n    id: s.id, cls: s.getAttribute(\'class\'),\n    parentTag: s.parentElement.tagName.toLowerCase(),\n    parentCls: s.parentElement.className,\n    italicCount: s.querySelectorAll(\'tspan.italic\').length,\n    totalTspanItalicByAttr: s.querySelectorAll(\'[class*="italic"]\').length\n  }));\n  return JSON.stringify({ italicRules: rules, gtSVGs: svgs }, null, 2);\n}');
```
```

> AGENT

Diagnóstico completo e empírico:

- A colmeia são **dois SVGs inline** (`#mobile` e `#desktop`, classe `gtSVG`) dentro de um **widget Elementor HTML** (`elementor-element-da94e3a`).
- O itálico vem de uma regra **`<style>` inline dentro do próprio HTML do widget**: `.gtSVG .italic { font-style: italic; fill: var(--GT-TEXT); }`
- Os textos em itálico têm `class="italic"` nos `<tspan>` (10 no mobile, 9 no desktop).

A correção mais limpa e cirúrgica: alterar a regra CSS `.gtSVG .italic { font-style: italic; ... }` → `font-style: normal`. Isso remove o itálico de todos os textos de uma vez (PT e EN, mobile e desktop), sem precisar mexer em cada `<tspan>`.

Esse SVG+CSS vive dentro do `_elementor_data` do post (widget HTML). Vou confirmar o conteúdo bruto do widget e os post IDs (26666 PT / 71726 EN) no banco para fazer a edição correta.

> TOOL

tool_use Bash
id: toolu_01TwShZDSRHDas8oE1Pbs7iz
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=/home/<USER>/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh\necho \"=== PT post 26666: existe widget com gtSVG/italic? ===\"\n$DD wp eval '\n$ids = [26666, 71726];\nforeach ($ids as $id) {\n  $d = get_post_meta($id, \"_elementor_data\", true);\n  if (!$d) { echo \"$id: SEM _elementor_data\\n\"; continue; }\n  $hasGt = strpos($d, \"gtSVG\") !== false ? \"SIM\" : \"nao\";\n  $hasItalicRule = strpos($d, \".italic\") !== false ? \"SIM\" : \"nao\";\n  $countItalicClass = substr_count($d, \"class=\\\"italic\\\"\") + substr_count($d, \"class=\\\\\\\"italic\\\\\\\"\");\n  $title = get_the_title($id);\n  echo \"$id [$title]: gtSVG=$hasGt | regra .italic=$hasItalicRule\\n\";\n}\n' 2>&1 | grep -v \"Cores ativadas\\|BIT BPO\\|Docker\\|Devil\\|docker-dev\\|Versao\\|Ambiente\\|^\\s*[│╭╰├]\"",
  "description": "Verificar _elementor_data dos posts PT e EN da colmeia"
}
```

> TOOL

tool_result
id: toolu_01TwShZDSRHDas8oE1Pbs7iz
```
=== PT post 26666: existe widget com gtSVG/italic? ===

[38;2;126;142;145m │  [38;2;166;226;46m▄[38;2;126;142;145m                                                    │ [0m
[38;2;126;142;145m │  [38;2;166;226;46m█▀[38;2;126;142;145m                                                   │ [0m
[38;2;126;142;145m ├───────────────────────────────────────────────────────┤ [0m
[38;2;126;142;145m ╰───────────────────────────────────────────────────────╯ [0m

26666 [Grupos de Trabalho]: gtSVG=SIM | regra .italic=SIM
71726 [Workgroups]: gtSVG=SIM | regra .italic=SIM
```

> AGENT

Confirmado. Ambos os posts (PT 26666 e EN 71726) têm o SVG `gtSVG` com a regra `.italic` no `_elementor_data`.

Vou extrair o trecho exato da regra CSS de cada post para fazer a substituição precisa. Preciso ver como `font-style: italic` está escrito dentro do JSON (escapes).

> TOOL

tool_use Bash
id: toolu_01SPxvE8vbYFfg5VjvyvnGnX
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=/home/<USER>/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh\n$DD wp eval '\nforeach ([26666, 71726] as $id) {\n  $d = get_post_meta($id, \"_elementor_data\", true);\n  echo \"===== POST $id =====\\n\";\n  // Contar todas as ocorrências de \"italic\" e mostrar contexto\n  echo \"font-style:italic ocorre: \" . substr_count($d, \"font-style: italic\") . \" (com espaco)\\n\";\n  echo \"font-style:italic ocorre: \" . substr_count($d, \"font-style:italic\") . \" (sem espaco)\\n\";\n  echo \"class=italic (escaped) ocorre: \" . substr_count($d, \"class=\\\\\\\"italic\\\\\\\"\") . \"\\n\";\n  // mostrar 200 chars ao redor da regra .gtSVG .italic\n  $pos = strpos($d, \".italic\");\n  if ($pos !== false) {\n    echo \"CONTEXTO regra:\\n\";\n    echo substr($d, max(0,$pos-30), 120) . \"\\n\";\n  }\n}\n' 2>&1 | grep -vE \"Cores ativadas|BIT BPO|Docker|Devil|docker-dev\\.sh|Versao|Ambiente WordPress|^\\s*[│╭╰├╮]|^\\s*$\" ",
  "description": "Extrair formato exato da regra italic no elementor_data"
}
```

> TOOL

tool_result
id: toolu_01SPxvE8vbYFfg5VjvyvnGnX
```
[38;2;126;142;145m │  [38;2;166;226;46m▄[38;2;126;142;145m                                                    │ [0m
[38;2;126;142;145m │  [38;2;166;226;46m█▀[38;2;126;142;145m                                                   │ [0m
[38;2;126;142;145m ├───────────────────────────────────────────────────────┤ [0m
[38;2;126;142;145m ╰───────────────────────────────────────────────────────╯ [0m
===== POST 26666 =====
font-style:italic ocorre: 1 (com espaco)
font-style:italic ocorre: 0 (sem espaco)
class=italic (escaped) ocorre: 19
CONTEXTO regra:
GT-TITLE);\n    }\n    .gtSVG .italic {\n        font-style: italic;\n        fill: var(--GT-TEXT);\n    }\n\n    .gtSVG
===== POST 71726 =====
font-style:italic ocorre: 1 (com espaco)
font-style:italic ocorre: 0 (sem espaco)
class=italic (escaped) ocorre: 19
CONTEXTO regra:
GT-TITLE);\n    }\n    .gtSVG .italic {\n        font-style: italic;\n        fill: var(--GT-TEXT);\n    }\n\n    .gtSVG
```

> AGENT

Perfeito. Cada post tem exatamente **uma** ocorrência de `font-style: italic` dentro da regra `.gtSVG .italic`. A correção é trivial e cirúrgica: trocar `font-style: italic` → `font-style: normal` no `_elementor_data` de ambos os posts. Isso remove o itálico de todos os textos da colmeia (mobile + desktop, PT + EN) de uma vez.

Antes de aplicar, preciso esclarecer **escopo e ambiente** com você:

> TOOL

tool_use AskUserQuestion
id: toolu_01JopSRprq7LETgMkAhm9rTa
```json
{
  "questions": [
    {
      "question": "Onde aplico a remoção do itálico da colmeia (Grupos de Trabalho)?",
      "header": "Ambiente",
      "multiSelect": false,
      "options": [
        {
          "label": "DEV agora, depois prod",
          "description": "Aplico no docker-dev local (cambrasmax.local), você valida visualmente, e em seguida deployo para produção (concertacaoamazonia.com.br). Fluxo recomendado e seguro."
        },
        {
          "label": "Direto em produção",
          "description": "Edito _elementor_data dos posts 26666 (PT) e 71726 (EN) direto no servidor prod via SSH/WP-CLI + regen Elementor CSS + invalidação de cache cirúrgica. Mais rápido, sem etapa de validação em dev."
        },
        {
          "label": "Só em DEV",
          "description": "Aplico apenas no ambiente local por enquanto. Não toco em produção."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01JopSRprq7LETgMkAhm9rTa
```
Your questions have been answered: "Onde aplico a remoção do itálico da colmeia (Grupos de Trabalho)?"="DEV agora, depois prod". You can now continue with these answers in mind.
```

> AGENT

Vou aplicar em DEV primeiro, você valida, depois deployo para prod. Vou criar uma task list e começar pela edição em DEV.

> TOOL

tool_use ToolSearch
id: toolu_01VYBfYM6QqGM2P1jQJDCnEy
```json
{
  "query": "select:TaskCreate,TaskUpdate",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_01VYBfYM6QqGM2P1jQJDCnEy
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskUpdate"
}
```

> TOOL

tool_use TaskCreate
id: toolu_011ZuKBnrxQdHDf9AUuUJkUy
```json
{
  "subject": "Remover itálico da colmeia em DEV (posts 26666 PT + 71726 EN)",
  "description": "Editar _elementor_data dos posts 26666 e 71726 trocando `font-style: italic` → `font-style: normal` na regra `.gtSVG .italic`. Regen Elementor CSS + clean cache. Validar em https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/ (PT) e /en/ (EN).",
  "activeForm": "Removendo itálico da colmeia em DEV"
}
```

> TOOL

tool_result
id: toolu_011ZuKBnrxQdHDf9AUuUJkUy
```
Task #1 created successfully: Remover itálico da colmeia em DEV (posts 26666 PT + 71726 EN)
```

> TOOL

tool_use TaskCreate
id: toolu_01KWZMvawrYYpjZSdyTFE1De
```json
{
  "subject": "Deploy da remoção do itálico para produção",
  "description": "Após validação em DEV, aplicar mesma edição em produção (concertacaoamazonia.com.br) nos posts PT/EN, regen Elementor CSS, reload php-fpm, invalidação cirúrgica de cache (WP Rocket + CloudFront) da página /atuacao/grupos-de-trabalho/ e /en/.",
  "activeForm": "Fazendo deploy para produção"
}
```

> TOOL

tool_result
id: toolu_01KWZMvawrYYpjZSdyTFE1De
```
Task #2 created successfully: Deploy da remoção do itálico para produção
```

> TOOL

tool_use TaskUpdate
id: toolu_01Y5hdP3qfZxRSNYxXKNzgW4
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01Y5hdP3qfZxRSNYxXKNzgW4
```
Updated task #1 status
```

> AGENT

Importante: a página que estou inspecionando (`concertacao.bureau-it.com`) é o **tunnel do DEV**, não prod. Então o DOM que vi já é o DEV. Vou aplicar a edição no banco DEV. Vou usar um eval-file PHP para fazer a substituição de forma segura e idempotente, com backup do valor original.

> TOOL

tool_use Bash
id: toolu_0151Y9HxEtR83ntJHSFpd7pC
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/remove-colmeia-italic.php <<'PHP'\n<?php\n/**\n * Remove itálico da colmeia (Grupos de Trabalho).\n * Troca `font-style: italic` -> `font-style: normal` na regra `.gtSVG .italic`\n * do _elementor_data dos posts PT (26666) e EN (71726).\n * Idempotente. Faz backup do meta original em _elementor_data_pre_italic_fix.\n *\n * Uso:  wp eval-file remove-colmeia-italic.php          (dry-run, só relata)\n *       APPLY=1 wp eval-file remove-colmeia-italic.php   (aplica de fato)\n */\n\n$apply  = getenv( 'APPLY' ) === '1';\n$ids    = array( 26666, 71726 );\n$search = 'font-style: italic';\n$repl   = 'font-style: normal';\n\nforeach ( $ids as $id ) {\n    $title = get_the_title( $id );\n    $data  = get_post_meta( $id, '_elementor_data', true );\n\n    if ( ! $data ) {\n        echo \"[$id] $title — SEM _elementor_data, pulado\\n\";\n        continue;\n    }\n\n    $count = substr_count( $data, $search );\n    echo \"[$id] $title — ocorrências de '$search': $count\\n\";\n\n    if ( $count === 0 ) {\n        echo \"      nada a fazer (já normal ou ausente)\\n\";\n        continue;\n    }\n\n    if ( ! $apply ) {\n        echo \"      [DRY-RUN] trocaria $count ocorrência(s) por '$repl'\\n\";\n        continue;\n    }\n\n    // backup uma única vez\n    if ( ! get_post_meta( $id, '_elementor_data_pre_italic_fix', true ) ) {\n        update_post_meta( $id, '_elementor_data_pre_italic_fix', wp_slash( $data ) );\n        echo \"      backup salvo em _elementor_data_pre_italic_fix\\n\";\n    }\n\n    $new = str_replace( $search, $repl, […]

> TOOL

tool_result
id: toolu_0151Y9HxEtR83ntJHSFpd7pC
```
Arquivo criado:
-rw-r--r--@ 1 dcambria  staff  1994  5 jun 18:37 tmp/remove-colmeia-italic.php
```

> AGENT

Vou copiar o script para o container e rodar primeiro em **dry-run** para confirmar.

> TOOL

tool_use Bash
id: toolu_01PkKpQrFrjC5jqV6z3fehSX
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ndocker cp tmp/remove-colmeia-italic.php concertacao-dev-wordpress:/tmp/remove-colmeia-italic.php\necho \"=== DRY-RUN ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp eval-file /tmp/remove-colmeia-italic.php --path=/var/www/html 2>&1",
  "description": "Dry-run da remoção do itálico em DEV"
}
```

> TOOL

tool_result
id: toolu_01PkKpQrFrjC5jqV6z3fehSX
```
=== DRY-RUN ===
[26666] Grupos de Trabalho — ocorrências de 'font-style: italic': 1
      [DRY-RUN] trocaria 1 ocorrência(s) por 'font-style: normal'
[71726] Workgroups — ocorrências de 'font-style: italic': 1
      [DRY-RUN] trocaria 1 ocorrência(s) por 'font-style: normal'
Done.
```

> AGENT

Dry-run confirma: 1 ocorrência em cada post. Vou aplicar de fato.

> TOOL

tool_use Bash
id: toolu_01Xx42h28empfZtbhTWohbca
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== APLICANDO ===\"\ndocker exec -u www-data -e APPLY=1 concertacao-dev-wordpress wp eval-file /tmp/remove-colmeia-italic.php --path=/var/www/html 2>&1\necho \"\"\necho \"=== Limpando caches (WP Rocket + Redis + OPcache) ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp cache flush --path=/var/www/html 2>&1\ndocker exec -u www-data concertacao-dev-wordpress wp eval 'if(function_exists(\"rocket_clean_domain\")){rocket_clean_domain();echo \"WP Rocket limpo\\n\";}' --path=/var/www/html 2>&1\ndocker exec -u www-data concertacao-dev-wordpress wp eval 'if(function_exists(\"opcache_reset\")){opcache_reset();echo \"OPcache reset\\n\";}' --path=/var/www/html 2>&1",
  "description": "Aplicar remoção do itálico e limpar caches em DEV"
}
```

> TOOL

tool_result
id: toolu_01Xx42h28empfZtbhTWohbca
```
=== APLICANDO ===
[26666] Grupos de Trabalho — ocorrências de 'font-style: italic': 1
      backup salvo em _elementor_data_pre_italic_fix
      Elementor CSS regenerado
      APLICADO: 1 ocorrência(s) -> 'font-style: normal'
[71726] Workgroups — ocorrências de 'font-style: italic': 1
      backup salvo em _elementor_data_pre_italic_fix
      Elementor CSS regenerado
      APLICADO: 1 ocorrência(s) -> 'font-style: normal'
Done.

=== Limpando caches (WP Rocket + Redis + OPcache) ===
Success: The cache was flushed.
WP Rocket limpo
OPcache reset
```

> AGENT

Aplicado e caches limpos. Agora vou validar no browser (DEV via tunnel) que o itálico foi removido — tanto PT quanto EN.

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_013c6QaE8aKg5uHHNjoL54pT
```json
{
  "url": "https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/?nocache=1"
}
```

> TOOL

tool_result ERROR
id: toolu_013c6QaE8aKg5uHHNjoL54pT
```
### Error
Error: browserBackend.callTool: net::ERR_CONNECTION_CLOSED at https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/?nocache=1
Call log:
[2m  - navigating to "https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/?nocache=1", waiting until "domcontentloaded"[22m
```

> AGENT

Conexão fechou momentaneamente (provavelmente OPcache reset/cache flush reiniciando o pool). Vou tentar de novo sem query string.

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_015aE35b9dwkvLBnzAGnVs3i
```json
{
  "url": "https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/"
}
```

> TOOL

tool_result
id: toolu_015aE35b9dwkvLBnzAGnVs3i
```
### Ran Playwright code
```js
await page.goto('https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/');
```
### Page
- Page URL: https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/
- Page Title: Grupos de Trabalho – Uma Concertação pela Amazônia
### Snapshot
- [Snapshot](.playwright-mcp/page-2026-06-05T21-38-19-148Z.yml)
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-38-17-734Z.log#L1-L2
```

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_011Q6FAounembCne7Lvq3wxV
```json
{
  "function": "() => {\n  // Verificar a regra .gtSVG .italic agora\n  const rules = [];\n  for (const sheet of document.styleSheets) {\n    let cssRules;\n    try { cssRules = sheet.cssRules; } catch(e) { continue; }\n    if (!cssRules) continue;\n    for (const r of cssRules) {\n      if (r.selectorText && /\\.gtSVG\\s+\\.italic/.test(r.selectorText)) {\n        rules.push(r.cssText);\n      }\n    }\n  }\n  // Computed font-style nos tspans .italic\n  const tspans = [...document.querySelectorAll('svg.gtSVG tspan.italic')];\n  const styles = {};\n  for (const t of tspans) {\n    const fs = getComputedStyle(t).fontStyle;\n    styles[fs] = (styles[fs]||0) + 1;\n  }\n  // amostra de textos que antes eram italic\n  const sample = tspans.slice(0,5).map(t => ({ txt: t.textContent.trim().slice(0,45), fontStyle: getComputedStyle(t).fontStyle }));\n  return JSON.stringify({ gtSVGItalicRule: rules, tspanCountByFontStyle: styles, sample }, null, 2);\n}"
}
```

> TOOL

tool_result
id: toolu_011Q6FAounembCne7Lvq3wxV
```
### Result
"{\n  \"gtSVGItalicRule\": [\n    \".gtSVG .italic { font-style: normal; fill: var(--GT-TEXT); }\"\n  ],\n  \"tspanCountByFontStyle\": {\n    \"normal\": 19\n  },\n  \"sample\": [\n    {\n      \"txt\": \"Instituto de Governança de Terras - IGT\",\n      \"fontStyle\": \"normal\"\n    },\n    {\n      \"txt\": \"(Instituto de Governança de Terras - IGT)\",\n      \"fontStyle\": \"normal\"\n    },\n    {\n      \"txt\": \"para Políticas de Saúde - IEPS\",\n      \"fontStyle\": \"normal\"\n    },\n    {\n      \"txt\": \"para Políticas de Saúde - IEPS\",\n      \"fontStyle\": \"normal\"\n    },\n    {\n      \"txt\": \"Roda Educativa\",\n      \"fontStyle\": \"normal\"\n    }\n  ]\n}"
### Ran Playwright code
```js
await page.evaluate('() => {\n  // Verificar a regra .gtSVG .italic agora\n  const rules = [];\n  for (const sheet of document.styleSheets) {\n    let cssRules;\n    try { cssRules = sheet.cssRules; } catch(e) { continue; }\n    if (!cssRules) continue;\n    for (const r of cssRules) {\n      if (r.selectorText && /\\.gtSVG\\s+\\.italic/.test(r.selectorText)) {\n        rules.push(r.cssText);\n      }\n    }\n  }\n  // Computed font-style nos tspans .italic\n  const tspans = [...document.querySelectorAll(\'svg.gtSVG tspan.italic\')];\n  const styles = {};\n  for (const t of tspans) {\n    const fs = getComputedStyle(t).fontStyle;\n    styles[fs] = (styles[fs]||0) + 1;\n  }\n  // amostra de textos que antes eram italic\n  const sample = tspans.slice(0,5).map(t => ({ txt: t.textContent.trim().slice(0,45), fontStyle: getComputedStyle(t).fontStyle }));\n  return JSON.stringify({ gtSVGItalicRule: rules, tspanCountByFontStyle: styles, sample }, null, 2);\n}');
```
```

> AGENT

DEV validado:
- A regra agora é `.gtSVG .italic { font-style: normal; fill: var(--GT-TEXT); }`
- Todos os 19 tspans `.italic` computam `font-style: normal` — **zero itálico**.

Vou confirmar visualmente com um screenshot da colmeia em DEV (PT), e também checar a versão EN.

> TOOL

tool_use ToolSearch
id: toolu_01BS6LZJ5gdVVaypLtjck6vL
```json
{
  "query": "select:mcp__playwright__browser_take_screenshot",
  "max_results": 3
}
```

> TOOL

tool_result
id: toolu_01BS6LZJ5gdVVaypLtjck6vL
```
{
  "type": "tool_reference",
  "tool_name": "mcp__playwright__browser_take_screenshot"
}
```

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01DcPse5BJoUQkZxFNqx66MS
```json
{
  "function": "() => {\n  // scroll até a colmeia desktop para o screenshot pegar\n  const svg = document.querySelector('svg.gtSVG.desktop') || document.querySelector('svg.gtSVG');\n  if (svg) svg.scrollIntoView({block:'center'});\n  return svg ? 'scrolled to ' + svg.getAttribute('class') : 'no gtSVG';\n}"
}
```

> TOOL

tool_result
id: toolu_01DcPse5BJoUQkZxFNqx66MS
```
### Result
"scrolled to gtSVG desktop"
### Ran Playwright code
```js
await page.evaluate('() => {\n  // scroll até a colmeia desktop para o screenshot pegar\n  const svg = document.querySelector(\'svg.gtSVG.desktop\') || document.querySelector(\'svg.gtSVG\');\n  if (svg) svg.scrollIntoView({block:\'center\'});\n  return svg ? \'scrolled to \' + svg.getAttribute(\'class\') : \'no gtSVG\';\n}');
```
### Page
- Page URL: https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/
- Page Title: Grupos de Trabalho – Uma Concertação pela Amazônia
- Console: 0 errors, 1 warnings
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-38-17-734Z.log#L3
```

> TOOL

tool_use mcp__playwright__browser_take_screenshot
id: toolu_01SKnRkR9EFb8orZikosT3mD
```json
{
  "type": "png",
  "element": "Colmeia (SVG gtSVG desktop) com os títulos das facilitações",
  "target": "svg.gtSVG.desktop",
  "filename": "colmeia-dev-pt-sem-italico.png"
}
```

> TOOL

tool_result
id: toolu_01SKnRkR9EFb8orZikosT3mD
```
### Result
- [Screenshot of Colmeia (SVG gtSVG desktop) com os títulos das facilitações](./colmeia-dev-pt-sem-italico.png)
### Ran Playwright code
```js
// Screenshot Colmeia (SVG gtSVG desktop) com os títulos das facilitações and save it as ./colmeia-dev-pt-sem-italico.png
await page.locator('svg.gtSVG.desktop').screenshot({
  path: './colmeia-dev-pt-sem-italico.png',
  scale: 'css',
  type: 'png'
});
```
```

> TOOL

tool_use Read
id: toolu_01TBALkp6M8NceJZD7nZvKc5
```json
{
  "file_path": "/home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao/.playwright-mcp/colmeia-dev-pt-sem-italico.png"
}
```

> TOOL

tool_result ERROR
id: toolu_01TBALkp6M8NceJZD7nZvKc5
```
File does not exist. Note: your current working directory is /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao.
```

> TOOL

tool_use Bash
id: toolu_019NhxKknPys1ybD6zwWw4iz
```json
{
  "command": "find /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao -name \"colmeia-dev-pt-sem-italico.png\" 2>/dev/null; echo \"---\"; ls -la /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao/.playwright-mcp/ 2>/dev/null | tail -5",
  "description": "Localizar screenshot salvo"
}
```

> TOOL

tool_result
id: toolu_019NhxKknPys1ybD6zwWw4iz
```
/home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao/colmeia-dev-pt-sem-italico.png
---
-rw-r--r--@    1 dcambria  staff    783896  1 dez  2025 sobre-nos-final.png
-rw-r--r--@    1 dcambria  staff     83402  3 fev 00:35 sobre-nos-full.png
-rw-r--r--@    1 dcambria  staff    100281  1 dez  2025 sobre-nos.png
-rw-r--r--@    1 dcambria  staff      1822 23 mai 02:18 uma-concertacao-pela-amazonia-2a981d5c2e0.ics
-rw-r--r--@    1 dcambria  staff   2538514 27 mai 19:18 Versao-Final-de-Estudo-da-GO-Associados-Ranking-do-Saneamento-de-2025-Rio-Corrigido-V4.pdf
```

> TOOL

tool_use Read
id: toolu_01C4XFAWNNLU25b7Zbawb7tg
```json
{
  "file_path": "/home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao/colmeia-dev-pt-sem-italico.png"
}
```

> TOOL

tool_result
id: toolu_01C4XFAWNNLU25b7Zbawb7tg
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "iVBORw0KGgoAAAANSUhEUgAAAR0AAADBCAIAAAB9g/PMAADZKElEQVR4Ae3AA6AkWZbG8f937o3IzKdyS2Oubdu2bdu2bdu2bWmMnpZKr54yMyLu+Xa3anqmhztr1a8eXbyPq6666j9UcNVVV/1HC6666qr/aMFVV131Hy246qqr/qMFV1111X+04KqrrvqPFvwnSNs297PNv0naafMABmMewDaX2eaqq/5nqPxHs73Zz4wP12sJUFfKME2SbEuAwIANIMm2JNslAmiZkmopi9rZPlyvJIFtaimhmLJlWpLtvtYpMzP7WtNumbZLBP+tbBtCAgDbkgBjIa76v67yH8r2vOv/8randaW8xIMfTmtk3rd/6ZrjJ8kkRBqbEIZSyCSTUshGqavVUrDY3GKazh3s/c25e+dd/5I3PwQbiYi9g/1hmo5tbHTz3m1S7e69eP74YmNjc/ueC2c3+tnOfEEpq9XS/Lcx7mutpRyt12lLmtW6niZBLWU9TUWSxFX/d1X+46S9OZv/4VOf8It/+xezrvur255+/fETt56777YL517hwQ/fnM3PH+yd3NzuSjlcryLitgvnrts5fnp7544L589s75w/2L9z98KJzc2+1Edff9Mjr73hW373V285eeYf7rr9puMn79nbnXfdfXt7Tzl794vdcPO89tfsHLt4eHD7xfOPvu7GYRr//q7b3v2VX/vJ9931+LvveLuXfRX+mxhqlDsuXrhwuP+SNz2odr1be/q5ex986gxw/uDgzMlTOQyrcZDEVf9HVf7j2KbUOy6ev3bneFfKD/3p773Kwx71jPNnD4fV7zzpHx5y+prjG5ugi4f7t188/4hrrjdumbedP3d8Y+PM9rHN2fxovZK0nqa/uePWL3r3D3mNhz/21vP3fevv/uoNx08+4prr19N4bLFxsFr94VOfWCPuubR704lTJze3fvwv/vDx99z5qGtv6Er5pt/+laefu/e1Hvni1x87MUyjJP5rCQxf+is/tT2b237K2XsefOrMnRcv7B4d/sYT/tb2w85c95DT177UzQ9ej6Mkrvq/SEcX7+M/jiDt7/mj37r+2MlHXnv9out//fF/e8Pxkwfr1YmNzdNbO0ObnnH+7NTaTSdOLfpe6O5LF8c23XzydIly4XAfuGv3wovdcPPLP+jhf/S0J/alPuPC2ZtPnN6azcc2Sbrn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u7t78uTJiOB+0zSt12sukzSfzyMCkATYBrquAyKCy2wDtZTMBD709d/y83/6B37yj3/3bV/x1Q8OD0oE/40yD4f1ic1tABvpiU984l133XXp0qXVavUWb/EWERERs9mM+7XWSimAJC6TxANk5uHh4fb2NrBeryMiM2ut4zhKms1m0zTVWm1L2t3djQhJtdZpmjKz7/uIqLUCkiKC+53eOb6/WqIwiP9clX+3Kdv2xtY0Dj/yB7/5x8942pu+/Kt95Iu97J/84R+dn9923bXXHh0dSVoul33f932/Xq+nabruuutOnz4N3HvvvXfffffm5mZmArYlScpMScMwvNiLvVhE2JZ0cHBw6dKl8+fPl1Ie+chH/tmf/dmZM2duv/32l3rplz518uT7v86b3n7h3Hf/zi/9/N/9xQe8xutff/rao6ND2yHxokm79v2P/uUffcAbvFWNYqil8ADTNF26dOn48eOZeddddwHXX3993/c8p8yMiD/+4z/+0z/90w/4gA/Y3t7OTEmS/uzP/uxxj3vcyZMnDw4O5vP5K7zCKzz4wQ+2LekHf/AHr7322rNnz/7t3/7t05/+9Ld/+7ff2dkBJAG2I4LLPukt3/kjv/OrX+8xLzHv+rT5byKJTKTN2Zz73XPPPev1+h/+4R9uu+22hzzkIYeHh/P5/NGPfvTJkyeB8+fPnz9//uzZs1tbWw960IPuu+++2Wy2v78/m80y8yEPeUjf9xHxLd/yLQcHBx/4gR/4e7/3e6/yKq/yvd/7vQ9/+MMPDg7OnDlz9uzZxz72sa/6qq8q6d577/2N3/iNkydPjuNYSjl27NhyuRzH8RGPeMTDH/5wLrMticvm3exoWCPxn6/y72DA3t4+9oeP+5uf+ts/f+RND/2K9/zwkO6+554f/NEfueH669/8zd98uVweHByUUk6fPn3vvfcOwzBN06lTpwDg0qVLp0+fPnny5DiOgKRpmtbr9YkTJ5bL5T333LNarTY2NiQBt912W0Tcdddd991338WLF1er1fXXX/93f//399x996mTJ8dpuvnk6c94m/f406c98Yt/7edf8rob3vfVXs9wNKxLBP8S25uz2eNvf/rB1F72QQ9fj0MbpnEaNzY2JNVabT/96U9fr9cXL17c2Nj4rd/6rcVi8eqv/uo33njjer2OiIgopdiOiGc84xl33XXXbDb7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W7uuO3HiBJe9wiu8gqSI4Pl5xCMewWWZCdRa1+v1crmczWZ93wMv+ZIvee7cuVLKS73US126dGljY2M+n9turUnKTADE/xS+7tjxW8/d81K3PNQ2EgBkZkT82I/92OMe97itra23fdu33drauuOOOx772MfOZjOeH9uAJB5A0jAMf/M3f7O7u3vs2LFXeIVXmM1mtgHbklar1U//9E+/5mu+5tmzZyPiD/7gD+67777P/MzP3NzctC0JAKQALu5fuu7YialNSPwnq/z7SGTmbbfd1nVda+3SpUvb29tPeMITaq3TNG1sbBw/fryUAkTE0dHRsWPHXvmVX/lzPudzXv7lX/7UqVO2bUt64hOf+KQnPekhD3lIa+3ee++96667HvnIR1577bXA3t7eU57ylFLKDTfccOHChT/+4z/e2tp61KMe1XUd8JIv+ZJbW1sPetCDHvGIRywWi4ODg8ViYVvSddddx7+SpGmaNjY2PvTDPuwJj398a+093uM9HvSgB9mez+ev9VqvBQAnT57kfq/6qq/K/WyXUngRRATwju/4jm//9m9vu5TCZV3XvdEbvRGXnTp16vTp0zwn2/zPEJKn6cVvuPmH//rP3uplX9WY+0kCbrnllszksp/4iZ/Y398HXuZlXsb2hQsX9vf3Syld181ms+PHj0viOdmWdHh4uLe31/f9xYsXj46OZrOZbUmSbJ86derRj370H/zBH1x//fX/8A//cOutt77My7zM5uYmIInLjEO6e/fCNA43nTxzuF6FxH+yyr+PTSnlpV/6padpysxSiu3M7LrO9jiOpRRAEtB13Uu/9Et3Xfd6r/d6P/ADP/CRH/mRtiUBr/7qr37LLbccP358e3v77rvvfomXeInM5LJxHKdpWi6X6/Xa9tHRUdd1AGD7JV/yJXnB0g6JF40BCAVw6uTJV3u1V+OyzIwIwLZtSYBt7idJEiCJf6WI4DllJhARgG1AEveThM1l5r+TpKNh/ZgbHzT88e8+6Z47H3ndjekMBfe75ZZb5vP50dHRyZMnH/3oR991113XX389IOmuu+46f/789vb2crk8derUU5/61I2NjVLKox71KNuSgIgATpw48ehHP/r8+fPXXnvtiRMngIiwLUkS8Cqv8iqbm5v7+/uPecxjgLd5m7cBbEvisqm1rtRf/Os/ebmbH0wptpH4T1b5jzCb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617av0RrT79w7l1f4hWBkADbkv72b//2tttuu+aaa06dOrW9vd113ROf+MSHP/zhpRTuN46jpMViceHCBUnz+Zz7nTt37k/+5E9uuumm48ePnzhxYn9/f2NjY2dnZ3d3t5Qym83uvPPOhzzkIbYlnT9//vd+7/fGcbxw4cI0TYvF4uVe7uVWq1Vrrda6tbUVEbYlZeb58+dXq9Xm5uZiscjMruvGcQSWy+WFCxe6rrvhhhs2NzeB7e3tzc3NS5cubW1t3Xrrra/yKq9y5513SprP5wAg6Wd+5me6ruu67t5777148eLW1tZv/MZvvNzLvdzJkydtS5IEPPqGm//08X8F2CD+16n8D2N7czb7q1ufcuL4qcdcf/PUWi2F+9l+iZd4ieuvv36xWPzu7/7u9vb2/v5+rfVVX/VVuWx/f//6668/PDw8f/78NE0HBwe2Syk7OztnzpyZpqmU0lq7/fbbI+IlXuIljo6O1ut1a62Ukpm/+Zu/ef311999993TNN1+++07Ozvr9ToirrnmmlLKarWazWZv8iZvMpvNzp8/v7u7e/78+TNnzlx//fV3331313XL5fJhD3vYxsYG9+tKBd7hFV/zk3/wm99o98LmbL4e1lPm6e1jgCTu13XdbDbb29ubpklS3/fjOPKcTp48ube3d/bs2dlsdv311/MAP/zDP/xyL/dyJ0+e/Ju/+Zu+79frda31YQ972N7eXinlkY985OHhISAJuPHGG7e3t8+fP//Kr/zKmfnrv/7rly5dGsdxd3cX2NjYOHbs2M7Oju1a6+Hh4R133HHy5MlnPOMZW1tbtqdpuu6667a3t48fP37hwoVaK5edPn16c3PTdq31rd7qrU6ePPnQhz50uVwuFgtAku2Xf/mXv3jx4h133LG5uXnNNdfUWm+88catrS1AEiAAbjhx+sLRIdkQ/xtV/odJm9r93lMe/5ov8QpARPAAGxsbN9988w033PCgBz3opptuOjo6On78+GKxAGxLKqVcunRpGIbNzc1a6/b2dkS01rquA0ope3t7BwcHp06dOnHixL333nt4eDhNUykFaK31fX/x4sXDw8PDw8MTJ05cunTpzJkzm5uby+Wy1npwcDAMAxARmWn75MmTtda//uu/lrSxsbFcLg8ODjY2NmxL4rIpW43ykGtv+pOnP+lNXuaVdy9djCjzruc5HT9+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sL29HRG2Jd12223/8A//8NIv/dKnT58+f/78bDabpmk+n29vbwO2uUwSl0mapunJT37ytddee+LECUlcVkq5/fbbT548ubm5yXO6dOnS9vZ2RBwcHGxtbV24cEHSiRMnbEvisrSn1hIEwN/eceus1mOLzWu2j03ZVuOws7HVfHDv3u5jbnowz5JJJqW4TY+/+86XuOlBD73meiQiaJMzFXGwXJaIzX42ZStRWraxNf5DVf5nsy1pb29P0mw2W61Wx44du3DhQtd1tltrs9ksIiTdeeedT3nKU06dOjUMw1133XXTTTf9wz/8w7333vtyL/dyfd/fcMMNtu+444477rhjuVy+2Iu92F133bVcLh/2sIcBmRkRGxsbOzs729vb+/v7W1tbpZTNzU0AePSjH72zs/P0pz99f38f2NnZKaUcHR1FxKu8yqtExN///d9fe+21p06duuuuu+66665rr70WsC2Jf4ltSZKe+MQn3nvvvYeHh3/4h3+4sbHx1m/91qdPn7YtCbh06dI0TXt7e6dPnz579uzOzs5sNrvzzjvPnDmzWq2maQIe9KAHAbYlPfWpT7148eKlS5fuueee+XxeSrnvvvtaaxFx8uTJS5cuATs7O0dHR+fOnXvJl3zJvu8lnT9//g//8A9rrX/4h3/4Mi/zMnffffdsNmutAS//8i9fSpHE/WxL+pEf+ZG+7w8ODvb29l791V/993//91/mZV7m5MmTd9555zOe8Yw3fdM3nc/nrbW+74HMjIjbb7/9KU95yrlz506dOiVpGIbXeq3X4rlIEpiQjobhV/7hr9K+4diJB5+65s7dCyFdd+zEU8/eI3TLqdOH61XLvHh0eGZ758TG1mocXuHBj/iZv/6Tzdn8tgtnbY+tpfPExta5g/3N2ezi0eHxxUZEYLpSXu3hjx6mSRL/QSr/s0kCaq2r1erGG2+cz+f33Xef7e3t7cwcx7HrOi7rum57e3u9Xkva2NjY3Nzc2tra2Njgsr/5m795+tOfLqnv+3EcJd14441cZvtRj3rUox71KOAlXuIleB62SymnTp3a3d09c+bM0dHRNE2lFNvHjh3ruq7v+7d7u7eTFBFAZkYEEBH8S2xLGobhu77ru/b391/u5V7u1KlTmflbv/Vb3/qt3/qRH/mRW1tbmRkRf/d3f3fbbbc96lGP+uu//utf//Vf39nZ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yxtvvHE2m91zzz1nz559uZd7uVOnTgG2b7vttvl8XmttrbXW5vM50Pd9RACSjo6O7r777osXL95666033ngjYNt2RAB/+7d/e8cdd9xwww1Pf/rTl8vlcrkE+r6X9KhHPWo+n+/t7QGbm5t9369WqwsXLtx5552r1Wpzc/Oxj30sl21sbGxtbc3n89bayZMnI2IYBuDSpUsv+7Ive8stt/zFX/zFn/3Zn731W7/1dddd9xu/8RuS+D+k8j/M1NrW5vZW1z3tvrsfdf1NtiVxme2IyEzbpRQusy2JyyRN07Rer6dpAiKilCIJmM/nkrifJC6TxGWSeAFs33PPPRGxWCx2dnYyU5LtiLB9zz33zOfzEydOXH/99Tw/aRfpb2976s3HTxLBc5IEHDt27G//5m/uuuuuu+68a2t7+9rrrvv7v/u7F3+JlwCGYZjP51tbW/v7+9dff/2tt956/Pjxvb29Y8eOLRaL3d3dl3zJl/yZn/mZEydOnDp1istWq9XR0dE4jvP5/OjoaDabZeapU6ciAuj7/sVe7MX+9m//dr1eX3/99Y985CMB2xFx2223/cEf/ME111wzm82mabr++usvXLhwzTXXHB4ebmxs1FprrcCxY8f29/cf/vCHnzx58t577z127Ni5c+e2t7eXy+UwDH3fA33fr1arpzzlKTfeeOP58+e7rjt9+vQwDLb/8i//8klPetLe3t4rv/IrP/7xj3/yk59s+8SJE4Ak/k+o/A8jicxXeNBDf+8Jf/uo629qmbUULpM0juNtt912/PjxU6dOcZkkHmCapv39/WEYhmGwbXtjY6Prulpr13VcZvvixYullAsXLozjWErZ3t6epuno6GhraysiTp8+HRGAbUn33Xff/v7+Ix/5yKc//enb29sRAUgCnvSkJx0cHIzjeNNNN9100022JfGcBMCT7nzGe73Cq7JeRYjnZLvW+jIv+7KP+4d/OHny5KMf8xhgtVpxme2IWK/XBwcHfd8/9rGPHcex67r5fD6fz2+55Za//Mu/fJ3XeZ1HPvKRtiVJevjDHz6fzzNTEmAbWK1W0zQBrbXVanXNNddI2tvbe+pTn/qwhz2s1vq0pz3t677u62y/7uu+7rFjx+bz+T333HPbbbedOXNmmqYbb7xxNpvZBm699db77rsvIm699db1ev3oRz96HMfValVrfcITnnDz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",
    "media_type": "image/png"
  }
}
```

> AGENT

O screenshot confirma visualmente: os textos das facilitações agora estão **em estilo normal (sem itálico)**. Comparando com a sua imagem original:

- **Antes:** "Instituto de Governança de Terras - IGT", "para Políticas de Saúde - IEPS", "Plataforma Parceiros pela Amazônia - PPA" estavam em *itálico*.
- **Agora:** todos em romano (reto).

DEV está validado — PT e EN (a regra é a mesma em ambos os posts, e confirmei `font-style: normal` nos 19 tspans). Vou marcar a task 1 como concluída.

> TOOL

tool_use TaskUpdate
id: toolu_01DGjPg1DRQxwEcHwfNZHUZs
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01DGjPg1DRQxwEcHwfNZHUZs
```
Updated task #1 status
```

> AGENT

✅ **DEV pronto.** O itálico foi removido da colmeia em Grupos de Trabalho (PT post 26666 + EN post 71726).

**O que fiz:**
- Diagnóstico empírico via browser: o itálico vinha da regra CSS `.gtSVG .italic { font-style: italic }` embutida no widget Elementor HTML, aplicada aos `<tspan class="italic">` dos SVGs inline da colmeia (mobile + desktop).
- Troquei `font-style: italic` → `font-style: normal` no `_elementor_data` de ambos os posts (com backup em `_elementor_data_pre_italic_fix`), regenerei o Elementor CSS e limpei os caches.
- Validei: regra agora é `font-style: normal`, os 19 tspans computam `normal`, e o screenshot confirma os textos em romano.

A imagem acima é a colmeia em DEV já sem itálico.

---

**Você confirma que quer que eu siga para o deploy em produção?** Já confirmou "DEV agora, depois prod" no início — então, se o resultado acima estiver bom para você, eu sigo. O deploy em prod fará:

1. Mesma troca `italic → normal` nos posts PT/EN de produção (com backup)
2. Regen do Elementor CSS de cada post
3. `reload php-fpm` (obrigatório em prod — OPcache do pool FPM)
4. Invalidação **cirúrgica** de cache (WP Rocket + CloudFront) só de `/atuacao/grupos-de-trabalho/` e `/en/...` — sem flush […]