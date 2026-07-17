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

> DEVELOPER

alterei também 2 widgets de texto no elementor data. Ajuste primeiro o EN em dev para aplicar essa alteração que fiz em PT

> AGENT

Você editou diretamente no Elementor (PT) dois widgets de texto e quer que eu replique essa mesma alteração no EN (post 71726) em DEV. Para fazer isso corretamente, preciso primeiro **descobrir o que mudou** no PT — comparando o estado atual do `_elementor_data` do PT com o que estava antes, identificar os 2 widgets de texto alterados, e então aplicar o equivalente traduzido no EN.

Deixa eu primeiro inspecionar as alterações que você fez no PT. Vou comparar o `_elementor_data` atual com algum backup/revisão para isolar as mudanças.

> TOOL

tool_use Bash
id: toolu_018V4VGEPYX8qVtTFbF8ZiYD
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=\"docker exec -u www-data concertacao-dev-wordpress wp\"\necho \"=== Revisões recentes do post PT 26666 ===\"\n$DD post list --post_type=revision --post_parent=26666 --fields=ID,post_date,post_modified --format=table --posts_per_page=8 --orderby=date --order=DESC --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|^\\s*$\"\necho \"\"\necho \"=== Meta backups disponíveis no PT 26666 ===\"\n$DD eval '\n$keys = get_post_custom_keys(26666);\nforeach ($keys as $k) {\n  if (strpos($k, \"_elementor_data\") !== false) echo $k . \"\\n\";\n}\n' --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|^\\s*$\"",
  "description": "Listar revisões e backups do post PT"
}
```

> TOOL

tool_result
id: toolu_018V4VGEPYX8qVtTFbF8ZiYD
```
=== Revisões recentes do post PT 26666 ===
ID	post_date	post_modified
92891	2026-06-05 18:32:08	2026-06-05 18:32:08
92889	2026-06-05 18:32:07	2026-06-05 18:32:07
92890	2026-06-05 18:32:07	2026-06-05 18:32:07
92759	2026-05-21 12:24:37	2026-05-21 12:24:37
92760	2026-05-21 12:24:37	2026-05-21 12:24:37

=== Meta backups disponíveis no PT 26666 ===
_elementor_data
_elementor_data_pre_italic_fix
```

> AGENT

Há revisões recentes de hoje (18:32) — essas são as suas edições no Elementor. Tenho dois pontos de comparação úteis:
1. `_elementor_data_pre_italic_fix` — backup que **eu** salvei antes do fix de itálico (estado antes de hoje à noite, mas talvez já com suas edições de texto, ou não).
2. As revisões 92891/92889/92890 de 18:32.

Preciso entender a ordem temporal. Você editou os 2 widgets de texto — pode ter sido antes ou depois do meu fix de itálico. Vou comparar o `_elementor_data` atual do PT contra o backup `_pre_italic_fix` para ver se a diferença é **só** o italic→normal ou se inclui também as edições de texto.

> TOOL

tool_use Bash
id: toolu_014PJy9vjtWVLFhpRjtjgWEY
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=\"docker exec -u www-data concertacao-dev-wordpress wp\"\n$DD eval '\n$cur  = get_post_meta(26666, \"_elementor_data\", true);\n$bak  = get_post_meta(26666, \"_elementor_data_pre_italic_fix\", true);\necho \"len atual: \" . strlen($cur) . \" | len backup pre_italic: \" . strlen($bak) . \"\\n\";\necho \"diferença de tamanho: \" . (strlen($cur) - strlen($bak)) . \" chars\\n\";\n// quantas diferenças além do font-style?\n$curN = str_replace(\"font-style: normal\", \"font-style: italic\", $cur); // normaliza o fix de italic\necho \"São idênticos exceto pelo font-style? \" . ($curN === $bak ? \"SIM (única mudança foi o italic)\" : \"NAO (há outras edições)\") . \"\\n\";\n' --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|^\\s*$|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente\"",
  "description": "Comparar elementor_data atual vs backup pre_italic do PT"
}
```

> TOOL

tool_result
id: toolu_014PJy9vjtWVLFhpRjtjgWEY
```
len atual: 48669 | len backup pre_italic: 48669
diferença de tamanho: 0 chars
São idênticos exceto pelo font-style? SIM (única mudança foi o italic)
```

> AGENT

Importante: o backup `_pre_italic_fix` é **idêntico ao atual exceto pelo italic**. Isso significa que suas 2 edições de widget de texto **já estavam presentes** quando salvei o backup (você editou *antes* do meu fix), OU você editou depois mas o backup não captura. Como os tamanhos são iguais e a única diferença é o font-style, o backup não me serve para isolar as suas edições de texto.

Preciso comparar contra um estado **anterior às suas edições**. As revisões de hoje 18:32 são o caminho. Vou comparar o `_elementor_data` atual do PT contra a revisão mais antiga de hoje (ou a de 21/05) para encontrar exatamente os 2 widgets de texto que você mudou.

> TOOL

tool_use Bash
id: toolu_01LxKk6dS28RYVj9AFgHpzmx
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=\"docker exec -u www-data concertacao-dev-wordpress wp\"\necho \"=== Cada revisão tem _elementor_data? E qual tamanho? ===\"\nfor rev in 92891 92889 92890 92759 92760; do\n  $DD eval \"\n  \\$d = get_post_meta($rev, '_elementor_data', true);\n  echo '$rev: ' . (\\$d ? strlen(\\$d).' chars' : 'SEM elementor_data') . ' | modified: ' . get_post_field('post_modified', $rev) . \\\"\\n\\\";\n  \" --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|^\\s*$|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente\"\ndone",
  "description": "Verificar tamanho do elementor_data em cada revisão PT"
}
```

> TOOL

tool_result
id: toolu_01LxKk6dS28RYVj9AFgHpzmx
```
=== Cada revisão tem _elementor_data? E qual tamanho? ===
92891: 48669 chars | modified: 2026-06-05 18:32:08
92889: 49387 chars | modified: 2026-06-05 18:32:07
92890: 49387 chars | modified: 2026-06-05 18:32:07
92759: 49811 chars | modified: 2026-05-21 12:24:37
92760: 49809 chars | modified: 2026-05-21 12:24:37
```

> AGENT

Agora vejo a evolução temporal:
- **21/05 (92759/92760):** ~49811 chars — estado antigo
- **05/06 18:32:07 (92889/92890):** 49387 chars — estado intermediário
- **05/06 18:32:08 (92891):** 48669 chars — estado atual

A diferença entre 49387 → 48669 (−718 chars) é grande demais para ser só o italic→normal (que é +0/−0... na verdade "italic"→"normal" é mesmo número de chars). Então **suas edições de texto reduziram ~718 chars** entre a revisão 92889 e a 92891.

Espera — mas o backup pre_italic tinha 48669 (igual ao atual). Isso quer dizer que a revisão 92891 (48669) **já é depois das suas edições E do meu fix**, e 92889/92890 (49387) é **antes das suas edições de texto** mas a sequência está confusa pelos timestamps quase idênticos.

Vou comparar diretamente o conteúdo da revisão 92889 (49387, estado pré-suas-edições) contra o atual (48669) para isolar exatamente os 2 widgets de texto que mudaram. Vou extrair ambos para arquivos e fazer um diff estrutural por widget.

> TOOL

tool_use Bash
id: toolu_01WbAnTwtTT5XXGCdUwqVZh2
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=\"docker exec -u www-data concertacao-dev-wordpress wp\"\n# Exportar atual (PT) e revisão 92889 para arquivos JSON, pretty, dentro do container\n$DD eval '\n$cur = get_post_meta(26666, \"_elementor_data\", true);\nfile_put_contents(\"/tmp/pt_current.json\", $cur);\n$rev = get_post_meta(92889, \"_elementor_data\", true);\nfile_put_contents(\"/tmp/pt_rev92889.json\", $rev);\necho \"exportados\\n\";\n' --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente|^\\s*$\"\n# Copiar para host\ndocker cp concertacao-dev-wordpress:/tmp/pt_current.json tmp/pt_current.json\ndocker cp concertacao-dev-wordpress:/tmp/pt_rev92889.json tmp/pt_rev92889.json\necho \"=== Extrair só widgets de TEXTO (widgetType text-editor / heading) e comparar via jq ===\"\n# Pretty + extrair editor widgets\npython3 - <<'PY'\nimport json\ncur = json.load(open('tmp/pt_current.json'))\nrev = json.load(open('tmp/pt_rev92889.json'))\n\ndef walk(nodes, acc):\n    for n in nodes:\n        wt = n.get('widgetType') or n.get('elType')\n        if wt in ('text-editor','heading'):\n            s = n.get('settings',{})\n            content = s.get('editor') or s.get('title') or ''\n            acc[n.get('id')] = (wt, content)\n        if n.get('elements'):\n            walk(n['elements'], acc)\n\na, b = {}, {}\nwalk(cur, a)\nwalk(rev, b)\n\nprint(\"=== Widgets de texto cujo CONTEÚDO mudou (atual vs rev92889) ===\")\nallids = set(a)|set(b)\nchanged=0\nfor i in allids:\n    wa = a.get(i); wb = b.get(i)\n    if wa and wb and wa[1]!=wb[1]:\n        changed+=1\n        print(f\"\\n--- widget id={i} type={wa[0]} ---\")\n        print(\"ANTES (rev92889):\", repr(wb[1])[:400])\n        print(\"AGORA (atual)   :\", repr(wa[1])[:400])\n    elif wa and not wb:\n        print(f\"\\n[+] widget id={i} só no ATUAL: {wa[0]} {repr(wa[1])[:200]}\")\n    elif wb and not wa:\n        print(f\"\\n[-] widget id={i} só na rev92889: {wb[0]} {repr(wb[1])[:200]}\")\nprint(f\"\\nTotal de widgets de texto com conteúdo alterado: {changed}\")\nPY",
  "description": "Diff de […]

> TOOL

tool_result
id: toolu_01WbAnTwtTT5XXGCdUwqVZh2
```
exportados
=== Extrair só widgets de TEXTO (widgetType text-editor / heading) e comparar via jq ===
=== Widgets de texto cujo CONTEÚDO mudou (atual vs rev92889) ===

[-] widget id=b723f80 só na rev92889: text-editor '<p><span style="font-weight: 300;">Facilitação: Fórum Brasileiro de Segurança Pública</span></p>'

[-] widget id=c3ba9a7 só na rev92889: text-editor '<p><span style="font-weight: 300;">Facilitação: Roda Educativa</span></p>'

Total de widgets de texto com conteúdo alterado: 0
```

> AGENT

Interessante — a comparação mostra que dois widgets `text-editor` (`b723f80` e `c3ba9a7`) existem na revisão 92889 mas **não** no atual. Isso sugere que a revisão 92889 não é o par certo, ou que a estrutura/IDs mudaram. O diff "só na rev" indica que esses widgets de texto foram **removidos ou tiveram o ID alterado** — não que seu conteúdo mudou.

Os textos "Facilitação: Fórum Brasileiro de Segurança Pública" e "Facilitação: Roda Educativa" são exatamente os títulos que aparecem na colmeia (Segurança e Direitos Humanos / Educação). Pode ser que você tenha **movido esses textos para dentro do SVG** ou editado de outra forma.

Deixa eu reabordar: comparar o atual contra o backup `_pre_italic_fix` não ajuda (idêntico exceto italic). Preciso ver o que mudou de fato. Vou fazer um diff **textual completo** entre o estado mais antigo de hoje e o atual, ignorando o italic, para ver TODAS as diferenças — não só widgets text-editor.

> TOOL

tool_use Bash
id: toolu_01RJR6s9Qg8y3GrXJNhtfbAd
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\npython3 - <<'PY'\nimport json, re\n\ndef load(p):\n    return json.load(open(p))\n\ncur = load('tmp/pt_current.json')\nrev = load('tmp/pt_rev92889.json')\n\n# Normalizar o fix de italic para não poluir o diff\ndef norm(s):\n    if isinstance(s,str):\n        return s.replace('font-style: normal','font-style: italic')\n    return s\n\n# Coletar TODOS os campos de texto de QUALQUER widget (editor, title, html, text, etc.)\nTEXT_KEYS = ('editor','title','html','text','description','content','caption','tab_title','heading','sub_heading')\ndef walk(nodes, acc, path=\"\"):\n    for idx,n in enumerate(nodes):\n        wid = n.get('id','?')\n        wt = n.get('widgetType') or n.get('elType') or '?'\n        s = n.get('settings',{}) or {}\n        for k in TEXT_KEYS:\n            if k in s and isinstance(s[k], str) and s[k].strip():\n                acc[(wid,k)] = (wt, s[k])\n        if n.get('elements'):\n            walk(n['elements'], acc, path+f\"/{wid}\")\n\na, b = {}, {}\nwalk(cur, a)\nwalk(rev, b)\n\nprint(\"=== TODAS as diferenças de campos de texto (atual vs rev92889), ignorando italic fix ===\\n\")\nallk = set(a)|set(b)\nnchg=0\nfor key in sorted(allk):\n    wa=a.get(key); wb=b.get(key)\n    va = norm(wa[1]) if wa else None\n    vb = norm(wb[1]) if wb else None\n    if va==vb:\n        continue\n    nchg+=1\n    wid,fld = key\n    print(f\"--- id={wid} field={fld} ---\")\n    print(f\"  rev92889: {repr(wb[1])[:300] if wb else '(ausente)'}\")\n    print(f\"  atual   : {repr(wa[1])[:300] if wa else '(ausente)'}\")\n    print()\nprint(f\"Total campos de texto diferentes: {nchg}\")\nPY",
  "description": "Diff completo de todos os campos de texto PT atual vs revisão"
}
```

> TOOL

tool_result
id: toolu_01RJR6s9Qg8y3GrXJNhtfbAd
```
=== TODAS as diferenças de campos de texto (atual vs rev92889), ignorando italic fix ===

--- id=b723f80 field=editor ---
  rev92889: '<p><span style="font-weight: 300;">Facilitação: Fórum Brasileiro de Segurança Pública</span></p>'
  atual   : (ausente)

--- id=c3ba9a7 field=editor ---
  rev92889: '<p><span style="font-weight: 300;">Facilitação: Roda Educativa</span></p>'
  atual   : (ausente)

--- id=da94e3a field=html ---
  rev92889: '<style type="text/css" data-scope="Hide and Show">\n    .gtSVG.desktop {\n        display: none;\n    }\n    @media screen and (min-width: 1024px) {\n        .gtSVG.mobile {\n            display: none;\n        }\n        .gtSVG.desktop {\n            display: block;\n        }\n    }\n    .gtSVG .
  atual   : '<style type="text/css" data-scope="Hide and Show">\n    .gtSVG.desktop {\n        display: none;\n    }\n    @media screen and (min-width: 1024px) {\n        .gtSVG.mobile {\n            display: none;\n        }\n        .gtSVG.desktop {\n            display: block;\n        }\n    }\n    .gtSVG .

Total campos de texto diferentes: 3
```

> AGENT

Agora está claro. As diferenças entre rev92889 e atual:
1. `b723f80` e `c3ba9a7` (widgets text-editor "Facilitação: Fórum..." e "Facilitação: Roda Educativa") — **ausentes no atual** → mas isso é provavelmente porque a rev92889 ainda **não** é a base correta, ou esses widgets sempre existiram. Na verdade o html `da94e3a` (o SVG da colmeia) também mudou.

O ponto-chave: o html `da94e3a` mudou (além do italic). Esse é o widget HTML que contém o SVG inteiro. As suas "2 edições de widget de texto" provavelmente estão **dentro do SVG** (os `<tspan>`), não em widgets text-editor separados.

Deixa eu fazer o diff linha-a-linha do conteúdo HTML do widget `da94e3a` (a colmeia), ignorando o italic, para ver exatamente o que você mudou no texto.

> TOOL

tool_use Bash
id: toolu_01VJbzX7aFLuC5SQSKSDmX6D
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\npython3 - <<'PY'\nimport json\ncur = json.load(open('tmp/pt_current.json'))\nrev = json.load(open('tmp/pt_rev92889.json'))\n\ndef find_html(nodes, wid):\n    for n in nodes:\n        if n.get('id')==wid:\n            return (n.get('settings',{}) or {}).get('html','')\n        if n.get('elements'):\n            r=find_html(n['elements'], wid)\n            if r is not None: return r\n    return None\n\nha = find_html(cur,'da94e3a') or ''\nhb = find_html(rev,'da94e3a') or ''\n\n# normalizar italic fix\nhb_norm = hb.replace('font-style: italic','font-style: normal')\n\nimport difflib\nla = ha.splitlines()\nlb = hb_norm.splitlines()\nprint(f\"linhas atual={len(la)} rev={len(lb)}\")\ndiff = list(difflib.unified_diff(lb, la, fromfile='rev92889', tofile='atual', lineterm='', n=1))\n# filtrar linhas de contexto vazias\nout=[d for d in diff if d.strip() and not d.startswith('@@')]\nfor d in out:\n    print(d[:220])\nPY",
  "description": "Diff linha-a-linha do HTML da colmeia PT"
}
```

> TOOL

tool_result
id: toolu_01VJbzX7aFLuC5SQSKSDmX6D
```
linhas atual=422 rev=422
--- rev92889
+++ atual
                 ></path>
-                <image width="640" height="593" transform="translate(56 76) scale(.21)" xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/otrf.png">
+                <image width="640" height="593" transform="translate(56 76) scale(.21)" xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/otrf.png">
                     <title>Empresas ligadas ao Grupo de Trabalho "Ordenamento Territorial e Regularização Fundiária"</title>
                 ></path>
-                <image width="506" height="563" transform="translate(210 78) scale(.22)" xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/saude.png">
+                <image width="506" height="563" transform="translate(210 78) scale(.22)" xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/saude.png">
                     <title>Empresas ligadas ao Grupo de Trabalho "Saúde"</title>
                 ></path>
-                <image width="548" height="640" transform="translate(152 193) scale(.24)" xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/educacao.png">
+                <image width="548" height="640" transform="translate(152 193) scale(.24)" xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/educacao.png">
                     <title>Empresas ligadas ao Grupo de Trabalho "Educação"</title>
                 ></path>
-                <image width="506" height="563" transform="translate(10 188) scale(.22)" xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/seguranca.png">
+                <image width="506" height="563" transform="translate(10 188) scale(.22)" xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/seguranca.png">
                     <title>Empresas ligadas ao Grupo de Trabalho "Segurança"</title>
                     transform="translate(274 148) scale(.33)"
-                    xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/bioeconomia.png"
+                    xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/bioeconomia.png"
                 >
                 ></path>
-                <image width="640" height="593" transform="translate(55 63) scale(.215)" xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/otrf.png">
+                <image width="640" height="593" transform="translate(55 63) scale(.215)" xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/otrf.png">
                     <title>Empresas ligadas ao Grupo de Trabalho "Ordenamento Territorial e Regularização Fundiária"</title>
                 ></path>
-                <image width="506" height="563" transform="translate(204 55) scale(.23)" xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/saude.png">
+                <image width="506" height="563" transform="translate(204 55) scale(.23)" xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/saude.png">
                     <title>Empresas ligadas ao Grupo de Trabalho "Saúde"</title>
                 ></path>
-                <image width="506" height="563" transform="translate(404.5 45) scale(.23)" xlink:href="https://cambrasmax.local:8484/wp-content/uploads/gts-202506/seguranca.png">
+                <image width="506" height="563" transform="translate(404.5 45) scale(.23)" xlink:href="https://concertacao.bureau-it.com/wp-content/uploads/gts-202506/seguranca.png">
                     <title>Empresas ligadas ao Grupo de Trabalho "Segurança"</title>
                 ></path>
-                <image width="548" height="640" […]

> AGENT

Agora entendo o quadro completo. O diff entre rev92889 e atual mostra **apenas mudanças de URL** (`cambrasmax.local:8484` → `concertacao.bureau-it.com`) — isso é só o rewrite de tunnel, **não** são suas edições de texto. A rev92889 foi salva com URLs locais; o atual está com URLs de tunnel.

Isso significa que **a revisão 92889 NÃO captura suas 2 edições de texto** — ou elas já estavam lá antes, ou são mais recentes que todas as revisões. As revisões do Elementor às vezes não são criadas a cada save manual via editor.

Preciso de uma abordagem diferente. Deixa eu **perguntar diretamente a você** quais foram as 2 alterações, porque comparar revisões está se mostrando inconclusivo (as revisões têm URLs locais e ruído de tunnel-rewrite). Mas antes, deixa eu verificar o estado atual real dos textos no SVG do PT renderizado — talvez eu consiga ver o que você mudou comparando com a sua imagem original e o EN atual.

Vou extrair todos os textos `<tspan>` (títulos e facilitações) do SVG atual do PT e do EN para comparar lado a lado.

> TOOL

tool_use Bash
id: toolu_01EeVYejoA7mbdGYzuBn4m7n
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=\"docker exec -u www-data concertacao-dev-wordpress wp\"\n# Exportar EN atual também\n$DD eval '\n$en = get_post_meta(71726, \"_elementor_data\", true);\nfile_put_contents(\"/tmp/en_current.json\", $en);\necho \"ok\\n\";\n' --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente|^\\s*$\"\ndocker cp concertacao-dev-wordpress:/tmp/en_current.json tmp/en_current.json\n\npython3 - <<'PY'\nimport json, re, html\ndef get_html(p, wid='da94e3a'):\n    data=json.load(open(p))\n    def f(nodes):\n        for n in nodes:\n            if n.get('id')==wid: return (n.get('settings',{}) or {}).get('html','')\n            if n.get('elements'):\n                r=f(n['elements'])\n                if r is not None: return r\n        return None\n    return f(data) or ''\n\ndef extract_texts(h):\n    # pegar conteúdo de <text> e <tspan>, juntando, e os <title> dos botões\n    texts=[]\n    # capturar todos os <text ...>...</text> com seus tspans\n    for m in re.finditer(r'<text\\b[^>]*>(.*?)</text>', h, re.S):\n        inner=m.group(1)\n        # juntar tspans\n        parts=re.findall(r'<tspan\\b[^>]*>(.*?)</tspan>', inner, re.S)\n        if parts:\n            txt=' '.join(html.unescape(p.strip()) for p in parts if p.strip())\n        else:\n            txt=html.unescape(re.sub(r'<[^>]+>','',inner)).strip()\n        txt=re.sub(r'\\s+',' ',txt).strip()\n        if txt: texts.append(txt)\n    return texts\n\npt=extract_texts(get_html('tmp/pt_current.json'))\nen=extract_texts(get_html('tmp/en_current.json'))\nprint(\"=== PT (atual) — textos do SVG colmeia ===\")\nfor i,t in enumerate(pt): print(f\"{i:2} | {t}\")\nprint(\"\\n=== EN (atual) — textos do SVG colmeia ===\")\nfor i,t in enumerate(en): print(f\"{i:2} | {t}\")\nPY",
  "description": "Extrair textos do SVG colmeia PT e EN atuais"
}
```

> TOOL

tool_result
id: toolu_01EeVYejoA7mbdGYzuBn4m7n
```
ok
=== PT (atual) — textos do SVG colmeia ===
 0 | Ordenamento Territorial e Regularização Fundiária Facilitação: Gabriel Siqueira Instituto de Governança de Terras - IGT
 1 | Land Use Planning and Land Regularization Facilitation: Gabriel Siqueira (Instituto de Governança de Terras - IGT)
 2 | Saúde Facilitação: Instituto de Estudos para Políticas de Saúde - IEPS
 3 | Health Facilitation: Instituto de Estudos para Políticas de Saúde - IEPS
 4 | Educação Facilitação: Roda Educativa
 5 | Education Facilitation: Roda Educativa
 6 | Segurança e Direitos Humanos Facilitação: Fórum Brasileiro de Segurança Pública
 7 | Security and Human Rights Facilitation: Fórum Brasileiro de Segurança Pública
 8 | Bioeconomia Facilitação: Plataforma Parceiros pela Amazônia - PPA
 9 | Bioeconomy Facilitation: Parceiros pela Amazônia Platform - PPA
10 | Ordenamento Territorial e Regularização Fundiária Facilitação: Gabriel Siqueira Instituto de Governança de Terras - IGT
11 | Land Use Planning and Land Regularization Facilitation: Gabriel Siqueira (Instituto de Governança de Terras - IGT)
12 | Saúde Facilitação: Instituto de Estudos para Políticas de Saúde - IEPS
13 | Health Facilitation: Instituto de Estudos para Políticas de Saúde - IEPS
14 | Segurança e Direitos Humanos Facilitação: Fórum […]

> AGENT

Importante descoberta: o SVG da colmeia é **bilíngue por construção** — cada hexágono mostra o título em PT **e** EN sobrepostos (controlados por WPML via display). Por isso o PT e o EN têm textos idênticos no SVG. E os textos atuais do PT e EN do SVG da colmeia já são **exatamente iguais** — não há divergência nos textos do SVG entre os dois posts.

Então suas 2 edições de widget de texto **não estão no SVG da colmeia** (PT e EN já batem). Devem estar em **outros 2 widgets de texto** da página — fora da colmeia. O diff por revisão não capturou porque a revisão tinha URLs locais (ruído de tunnel).

Vou fazer um diff completo PT-atual vs EN-atual de **todos** os campos de texto da página inteira (não só o widget da colmeia) para encontrar onde PT tem algo que o EN ainda não recebeu.

> TOOL

tool_use Bash
id: toolu_01KXSXDRmvKxKDa4Khk2hN7G
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\npython3 - <<'PY'\nimport json\nTEXT_KEYS=('editor','title','html','text','description','content','caption','tab_title','heading','sub_heading','title_text','description_text')\n\ndef walk(nodes, acc):\n    for n in nodes:\n        wid=n.get('id','?'); wt=n.get('widgetType') or n.get('elType')\n        s=n.get('settings',{}) or {}\n        for k in TEXT_KEYS:\n            v=s.get(k)\n            if isinstance(v,str) and v.strip():\n                acc.setdefault(wt,[]).append((wid,k,v))\n        if n.get('elements'): walk(n['elements'], acc)\n\npt=json.load(open('tmp/pt_current.json'))\nen=json.load(open('tmp/en_current.json'))\nap, ae = {}, {}\nwalk(pt,ap); walk(en,ae)\n\n# achatar em listas ordenadas por tipo\ndef flat(d):\n    out=[]\n    for wt,items in d.items():\n        for wid,k,v in items:\n            out.append((wt,wid,k,v))\n    return out\n\nfp=flat(ap); fe=flat(ae)\nprint(f\"PT campos texto: {len(fp)} | EN campos texto: {len(fe)}\")\n\n# Comparar por (widgetType, fieldKey) na MESMA ordem de aparição (IDs diferem entre traduções no WPML)\nfrom collections import defaultdict\ndef seq(d):\n    # lista preservando ordem de árvore por (wt,k) -> [valores]\n    return d\n# Mais robusto: comparar texto-a-texto na ordem do documento, ignorando html da colmeia (já sabemos igual) e URLs\nimport re\ndef clean(v):\n    v=re.sub(r'https?://[^\\s\"\\')]+','URL',v)\n    return v\n\n# pegar todos os strings de texto na ordem do documento\ndef walk_seq(nodes, acc):\n    for n in nodes:\n        s=n.get('settings',{}) or {}\n        wt=n.get('widgetType') or n.get('elType')\n        for k in TEXT_KEYS:\n            v=s.get(k)\n            if isinstance(v,str) and v.strip() and k!='html':  # html=colmeia, tratado à parte\n                acc.append((wt,k,n.get('id'),v))\n        if n.get('elements'): walk_seq(n['elements'],acc)\n\nsp=[]; se=[]\nwalk_seq(pt,sp); walk_seq(en,se)\nprint(f\"\\nPT widgets de texto (não-html): {len(sp)} | EN: {len(se)}\")\nprint(\"\\n=== PT (não-html, na ordem) ===\")\nfor wt,k,wid,v in sp:\n    print(f\"[{wt}/{k}] {wid}: {clean(v)[:160]}\")\nprint(\"\\n=== EN (não-html, na ordem) ===\")\nfor wt,k,wid,v in se:\n    print(f\"[{wt}/{k}] {wid}: {clean(v)[:160]}\")\nPY",
  "description": […]

> TOOL

tool_result
id: toolu_01KXSXDRmvKxKDa4Khk2hN7G
```
PT campos texto: 18 | EN campos texto: 20

PT widgets de texto (não-html): 17 | EN: 19

=== PT (não-html, na ordem) ===
[heading/title] dadb0fa: Grupos de trabalho
[divider/text] 106ade8: Divisor
[heading/title] 28b9b4a: Bioeconomia
[divider/text] dc886e2: Divisor
[text-editor/editor] f191e80: <p style="text-align: left;"><strong>Objetivo: </strong>O Grupo de Trabalho de Bioeconomia tem como objetivo promover ações coletivas, participativas e inclusiv
[heading/title] 21edc0f: Educação
[divider/text] de20021: Divisor
[text-editor/editor] 08a2d9e: <p style="text-align: left;"><strong>Objetivo: </strong>Desde 2023, o Grupo de Trabalho de Educação visa a) consolidar a iniciativa Uma Concertação pela Amazôni
[heading/title] 5aab952: Ordenamento Territorial e Regularização
[divider/text] 375d000: Divisor
[text-editor/editor] ced8bb4: <p style="text-align: left;"><strong>Objetivo: </strong>O Grupo de Trabalho de Ordenamento Territorial e Regularização Fundiária tem como objetivo promover o en
[heading/title] 5c015d2: Saúde
[divider/text] 80c01f4: Divisor
[text-editor/editor] 99b0d1a: <p style="text-align: left;"><strong>Objetivo: </strong>O Grupo de Trabalho (GT) Saúde surgiu no início de 2024 com o intuito de fortalecer a agenda de saúde na
[heading/title] 643ff48: Segurança & Direitos Humanos
[divider/text] 513d13a: Divisor
[text-editor/editor] 3f0b361: <p style="text-align: left;"><strong>Objetivo: </strong>O Grupo de Trabalho (GT) Segurança e Direitos Humanos surge em 2025 com os objetivos de: unir organizaçõ

=== EN (não-html, na ordem) ===
[heading/title] dadb0fa: Workgroups
[divider/text] 106ade8: Divisor
[heading/title] 28b9b4a: Bioeconomy​
[divider/text] […]

> AGENT

Agora a peça do quebra-cabeças encaixa perfeitamente.

Comparando PT vs EN, o EN tem **2 widgets text-editor a mais** que o PT:
- `c3ba9a7`: `Facilitation: Roda Educativa` (após a seção Education)
- `b723f80`: `Facilitation: Fórum Brasileiro de Segurança Pública` (após a seção Security & Human Rights)

Esses são exatamente os IDs `b723f80` e `c3ba9a7` que apareceram no diff anterior como "presentes na rev92889, ausentes no atual". Ou seja: **você REMOVEU esses 2 widgets de texto do PT** (eram redundantes — a facilitação já aparece dentro do SVG da colmeia). Essa foi a sua edição: **deletar os 2 widgets "Facilitation: ..." soltos**.

O EN (post 71726) ainda tem esses 2 widgets. Para aplicar a mesma alteração no EN, preciso **remover os widgets `c3ba9a7` e `b723f80`** do `_elementor_data` do EN.

Deixa eu confirmar com você antes de deletar, mostrando exatamente o que será removido:

> TOOL

tool_use AskUserQuestion
id: toolu_01BjxEGRSuJ6Cmf2waSUboz8
```json
{
  "questions": [
    {
      "question": "Detectei que sua alteração no PT foi REMOVER 2 widgets de texto soltos (que repetiam a facilitação já mostrada dentro do SVG da colmeia). Aplico o mesmo no EN, removendo esses 2 widgets?",
      "header": "Confirmação",
      "multiSelect": false,
      "options": [
        {
          "label": "Sim, remover os 2 do EN",
          "description": "Remove do post EN (71726) os widgets text-editor 'Facilitation: Roda Educativa' (c3ba9a7) e 'Facilitation: Fórum Brasileiro de Segurança Pública' (b723f80), igualando à estrutura do PT. Com backup + regen CSS + cache."
        },
        {
          "label": "Não — foi outra coisa",
          "description": "Minha edição não foi a remoção desses 2 widgets. Vou descrever exatamente o que mudei para você replicar no EN."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01BjxEGRSuJ6Cmf2waSUboz8
```
Your questions have been answered: "Detectei que sua alteração no PT foi REMOVER 2 widgets de texto soltos (que repetiam a facilitação já mostrada dentro do SVG da colmeia). Aplico o mesmo no EN, removendo esses 2 widgets?"="Sim, remover os 2 do EN". You can now continue with these answers in mind.
```

> AGENT

Confirmado. Vou remover os 2 widgets (`c3ba9a7` e `b723f80`) do EN (post 71726), com backup, regen do Elementor CSS e limpeza de cache. Vou usar um eval-file que parseia o JSON, remove os nós por ID recursivamente e regrava.

> TOOL

tool_use Bash
id: toolu_01GKdT28oxEat9NT5pkFypmP
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/remove-en-facilitation-widgets.php <<'PHP'\n<?php\n/**\n * Remove do EN (71726) os 2 widgets text-editor \"Facilitation: ...\" que repetem\n * a facilitação já presente dentro do SVG da colmeia — espelhando a edição feita\n * manualmente no PT (26666), onde esses widgets já não existem mais.\n *\n * IDs alvo: c3ba9a7 (Roda Educativa) e b723f80 (Fórum Brasileiro de Segurança Pública).\n *\n * Idempotente. Backup em _elementor_data_pre_facilitation_rm.\n *\n * Uso: wp eval-file ...               (dry-run)\n *      APPLY=1 wp eval-file ...        (aplica)\n */\n\n$apply   = getenv( 'APPLY' ) === '1';\n$post_id = 71726;\n$targets = array( 'c3ba9a7', 'b723f80' );\n\n$raw = get_post_meta( $post_id, '_elementor_data', true );\nif ( ! $raw ) {\n    echo \"ERRO: post $post_id sem _elementor_data\\n\";\n    return;\n}\n\n$data = json_decode( $raw, true );\nif ( ! is_array( $data ) ) {\n    echo \"ERRO: _elementor_data não é JSON válido\\n\";\n    return;\n}\n\n$removed = array();\n\n// Remove recursivamente quaisquer nós cujo id esteja em $targets.\n$filter = function ( array $nodes ) use ( &$filter, $targets, &$removed ) {\n    $out = array();\n    foreach ( $nodes as $node ) {\n        if ( isset( $node['id'] ) && in_array( $node['id'], $targets, true ) ) {\n            $settings = isset( $node['settings'] ) ? $node['settings'] : array();\n            $label    = isset( $settings['editor'] ) ? wp_strip_all_tags( […]

> TOOL

tool_result
id: toolu_01GKdT28oxEat9NT5pkFypmP
```
=== DRY-RUN ===
Widgets encontrados/removidos: 2
  - c3ba9a7 => "Facilitation: Roda Educativa"
  - b723f80 => "Facilitation: Fórum Brasileiro de Segurança Pública"
[DRY-RUN] não gravado. Rode com APPLY=1 para aplicar.
```

> AGENT

Dry-run confirma exatamente os 2 widgets corretos. Vou aplicar.

> TOOL

tool_use Bash
id: toolu_01PQiiDTuNqMnRKXmycc6QyA
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== APLICANDO ===\"\ndocker exec -u www-data -e APPLY=1 concertacao-dev-wordpress wp eval-file /tmp/remove-en-facilitation-widgets.php --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente|^\\s*$\"\necho \"\"\necho \"=== Limpando caches ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp cache flush --path=/var/www/html 2>&1 | grep -i success\ndocker exec -u www-data concertacao-dev-wordpress wp eval 'if(function_exists(\"rocket_clean_domain\")){rocket_clean_domain();echo \"WP Rocket limpo\\n\";} if(function_exists(\"opcache_reset\")){opcache_reset();echo \"OPcache reset\\n\";}' --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente|^\\s*$\"",
  "description": "Aplicar remoção dos 2 widgets no EN e limpar cache"
}
```

> TOOL

tool_result
id: toolu_01PQiiDTuNqMnRKXmycc6QyA
```
=== APLICANDO ===
Widgets encontrados/removidos: 2
  - c3ba9a7 => "Facilitation: Roda Educativa"
  - b723f80 => "Facilitation: Fórum Brasileiro de Segurança Pública"
Backup salvo em _elementor_data_pre_facilitation_rm
Elementor CSS regenerado
APLICADO. Novo tamanho _elementor_data: 42815 chars
Done.

=== Limpando caches ===
Success: The cache was flushed.
WP Rocket limpo
OPcache reset
```

> AGENT

Aplicado. Agora vou validar comparando novamente PT vs EN — a estrutura de widgets de texto deve estar idêntica agora (mesma contagem, sem os 2 widgets "Facilitation:").

> TOOL

tool_use Bash
id: toolu_01UDpAnbKq3kwWvn8q9rTDZK
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=\"docker exec -u www-data concertacao-dev-wordpress wp\"\n$DD eval '\n$en = get_post_meta(71726, \"_elementor_data\", true);\nfile_put_contents(\"/tmp/en_after.json\", $en);\necho \"ok\\n\";\n' --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente|^\\s*$\"\ndocker cp concertacao-dev-wordpress:/tmp/en_after.json tmp/en_after.json\n\npython3 - <<'PY'\nimport json,re\nTEXT_KEYS=('editor','title')\ndef walk_seq(nodes, acc):\n    for n in nodes:\n        s=n.get('settings',{}) or {}\n        wt=n.get('widgetType') or n.get('elType')\n        for k in TEXT_KEYS:\n            v=s.get(k)\n            if isinstance(v,str) and v.strip():\n                acc.append((wt,k,n.get('id'),re.sub(r'<[^>]+>','',v).strip()[:60]))\n        if n.get('elements'): walk_seq(n['elements'],acc)\n\npt=json.load(open('tmp/pt_current.json'))\nen=json.load(open('tmp/en_after.json'))\nsp=[];se=[]\nwalk_seq(pt,sp);walk_seq(en,se)\n# checar ausência dos targets\nids_en=[x[2] for x in se]\nprint(\"c3ba9a7 ainda no EN?\", 'c3ba9a7' in ids_en)\nprint(\"b723f80 ainda no EN?\", 'b723f80' in ids_en)\nprint(f\"\\nPT widgets texto(editor/title): {len(sp)} | EN agora: {len(se)}\")\nprint(\"(devem ser iguais agora)\")\n# listar IDs em comum / divergentes\nsp_ids=set(x[2] for x in sp); se_ids=set(ids_en)\nprint(\"\\nSó no PT:\", sp_ids - se_ids)\nprint(\"Só no EN:\", se_ids - sp_ids)\nPY",
  "description": "Validar paridade de estrutura PT vs EN após remoção"
}
```

> TOOL

tool_result
id: toolu_01UDpAnbKq3kwWvn8q9rTDZK
```
ok
c3ba9a7 ainda no EN? False
b723f80 ainda no EN? False

PT widgets texto(editor/title): 11 | EN agora: 11
(devem ser iguais agora)

Só no PT: set()
Só no EN: set()
```

> AGENT

Validação estrutural perfeita:
- Os 2 widgets `c3ba9a7` e `b723f80` foram removidos do EN.
- PT e EN agora têm **11 widgets de texto cada**, com **conjuntos de IDs idênticos** (nada exclusivo de um lado).

Agora vou confirmar visualmente no browser que a página EN renderiza sem os textos "Facilitation: ..." duplicados.

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_01HzHykFLgJ1bzGjuDhqo9hT
```json
{
  "url": "https://concertacao.bureau-it.com/en/workgroups/"
}
```

> TOOL

tool_result
id: toolu_01HzHykFLgJ1bzGjuDhqo9hT
```
### Ran Playwright code
```js
await page.goto('https://concertacao.bureau-it.com/en/workgroups/');
```
### Page
- Page URL: https://concertacao.bureau-it.com/en/activities/workgroups/
- Page Title: Workgroups – Uma Concertação pela Amazônia
### Snapshot
- [Snapshot](.playwright-mcp/page-2026-06-05T21-46-30-474Z.yml)
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-46-26-501Z.log#L1-L2
```

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01WsU2zbAQzWriQQpQZFRiGA
```json
{
  "function": "() => {\n  // Procurar por textos \"Facilitation:\" soltos no corpo (fora do SVG)\n  const bodyText = [...document.querySelectorAll('.elementor-widget-text-editor')]\n    .map(el => el.textContent.trim().replace(/\\s+/g,' '))\n    .filter(t => /Facilitation:/i.test(t));\n  // Também verificar o italic da colmeia (deve estar normal)\n  const italicTspans = [...document.querySelectorAll('svg.gtSVG tspan.italic')];\n  const fontStyles = {};\n  italicTspans.forEach(t => { const fs=getComputedStyle(t).fontStyle; fontStyles[fs]=(fontStyles[fs]||0)+1; });\n  return JSON.stringify({\n    looseFacilitationTextWidgets: bodyText,\n    italicTspanFontStyles: fontStyles,\n    svgCount: document.querySelectorAll('svg.gtSVG').length\n  }, null, 2);\n}"
}
```

> TOOL

tool_result
id: toolu_01WsU2zbAQzWriQQpQZFRiGA
```
### Result
"{\n  \"looseFacilitationTextWidgets\": [],\n  \"italicTspanFontStyles\": {\n    \"normal\": 19\n  },\n  \"svgCount\": 2\n}"
### Ran Playwright code
```js
await page.evaluate('() => {\n  // Procurar por textos "Facilitation:" soltos no corpo (fora do SVG)\n  const bodyText = [...document.querySelectorAll(\'.elementor-widget-text-editor\')]\n    .map(el => el.textContent.trim().replace(/\\s+/g,\' \'))\n    .filter(t => /Facilitation:/i.test(t));\n  // Também verificar o italic da colmeia (deve estar normal)\n  const italicTspans = [...document.querySelectorAll(\'svg.gtSVG tspan.italic\')];\n  const fontStyles = {};\n  italicTspans.forEach(t => { const fs=getComputedStyle(t).fontStyle; fontStyles[fs]=(fontStyles[fs]||0)+1; });\n  return JSON.stringify({\n    looseFacilitationTextWidgets: bodyText,\n    italicTspanFontStyles: fontStyles,\n    svgCount: document.querySelectorAll(\'svg.gtSVG\').length\n  }, null, 2);\n}');
```
```

> AGENT

EN validado em DEV:
- **`looseFacilitationTextWidgets: []`** — não há mais nenhum widget de texto "Facilitation:" solto na página EN (os 2 foram removidos com sucesso).
- **Itálico:** 19 tspans, todos `font-style: normal` — o fix de itálico também está aplicado no EN.
- 2 SVGs (mobile + desktop) intactos.

A página EN agora está em paridade com o PT: itálico removido + os 2 widgets de facilitação redundantes removidos.

**Resumo do que foi feito em DEV:**

| Item | PT (26666) | EN (71726) |
|------|-----------|-----------|
| Itálico da colmeia → normal | ✅ (feito antes) | ✅ (feito antes) |
| Remover widget "Facilitation: Roda Educativa" (`c3ba9a7`) | ✅ (você fez no Elementor) | ✅ (apliquei agora) |
| Remover widget "Facilitation: Fórum Brasileiro de Segurança Pública" (`b723f80`) | ✅ (você fez no Elementor) | ✅ (apliquei agora) |

Backups salvos no EN: `_elementor_data_pre_facilitation_rm` (e `_elementor_data_pre_italic_fix` do fix anterior).

DEV está pronto e em paridade PT/EN. Quando você validar visualmente a página EN (`/en/activities/workgroups/`), me avise e eu sigo para o **deploy em produção** de tudo de uma vez (itálico + remoção dos 2 widgets, em PT e EN), com regen de CSS, reload do php-fpm e invalidação […]

> DEVELOPER

prossiga

> AGENT

Vou prosseguir com o deploy em produção. Primeiro vou descobrir os IDs dos posts em **produção** (podem diferir de DEV) e validar o estado atual antes de aplicar qualquer mudança.

> TOOL

tool_use TaskUpdate
id: toolu_01YNHM9NpDgmAv3JdYziZjgK
```json
{
  "taskId": "2",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01YNHM9NpDgmAv3JdYziZjgK
```
Updated task #2 status
```

> TOOL

tool_use Bash
id: toolu_01YEpJEiSLwzmbVoDv3W5YEw
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Teste de conexão SSH prod ===\"\nssh -o ConnectTimeout=10 -o BatchMode=yes concertacaoamazonia.com.br-prod-sa \"echo CONECTADO; hostname\" 2>&1 | head -5",
  "description": "Testar conexão SSH com produção"
}
```

> TOOL

tool_result
id: toolu_01YEpJEiSLwzmbVoDv3W5YEw
```
=== Teste de conexão SSH prod ===
CONECTADO
auto-blueprod-20260518-concertacaoamazoniacombr
```

> AGENT

SSH OK. Agora vou identificar os posts da colmeia em produção e validar o estado atual (italic presente? widgets presentes?). Em prod os IDs podem ser diferentes — vou buscar pela URL/slug.

> TOOL

tool_use Bash
id: toolu_017CmMptWRqkW47CD8yJezs9
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nWP=\"sudo -u www-data wp --path=/var/www/concertacaoamazonia.com.br\"\nssh concertacaoamazonia.com.br-prod-sa \"\n$WP post list --post_type=page --name=grupos-de-trabalho --field=ID 2>/dev/null | head -1\necho '---EN workgroups---'\n$WP post list --post_type=page --name=workgroups --field=ID 2>/dev/null | head -1\necho '---busca por gtSVG nos posts---'\n$WP db query \\\"SELECT post_id FROM wp_postmeta WHERE meta_key='_elementor_data' AND meta_value LIKE '%gtSVG%' LIMIT 10;\\\" --skip-column-names 2>/dev/null\n\" 2>&1",
  "description": "Identificar posts da colmeia em produção"
}
```

> TOOL

tool_result
id: toolu_017CmMptWRqkW47CD8yJezs9
```
26666
---EN workgroups---
---busca por gtSVG nos posts---
71726
26666
26666
91786
92154
92463
92575
92576
92577
92578
```

> AGENT

Os IDs de produção batem com DEV: PT=26666, EN=71726 (WPML mantém os mesmos IDs em multisite/blog 1). Há outros posts com `gtSVG` (revisões e outras páginas). Vou validar o estado atual **exato** desses 2 posts em prod antes de tocar: italic presente? Os 2 widgets presentes?

> TOOL

tool_use Bash
id: toolu_0116zCVmCg2vhdpbTJ64WDN2
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nWP=\"sudo -u www-data wp --path=/var/www/concertacaoamazonia.com.br\"\n# Criar um eval-file de DIAGNÓSTICO (read-only) para prod\ncat > tmp/prod-diag.php <<'PHP'\n<?php\nforeach ([26666 => 'PT', 71726 => 'EN'] as $id => $lang) {\n    $d = get_post_meta($id, '_elementor_data', true);\n    if (!$d) { echo \"[$id/$lang] SEM _elementor_data\\n\"; continue; }\n    $italic = substr_count($d, 'font-style: italic');\n    $normal = substr_count($d, 'font-style: normal');\n    $hasC3  = strpos($d, '\"id\":\"c3ba9a7\"') !== false ? 'SIM' : 'nao';\n    $hasB72 = strpos($d, '\"id\":\"b723f80\"') !== false ? 'SIM' : 'nao';\n    echo \"[$id/$lang] len=\" . strlen($d)\n       . \" | font-style:italic=$italic | normal=$normal\"\n       . \" | widget c3ba9a7=$hasC3 | widget b723f80=$hasB72\\n\";\n}\nPHP\nscp -q tmp/prod-diag.php concertacaoamazonia.com.br-prod-sa:/tmp/prod-diag.php\necho \"=== DIAGNÓSTICO PROD (read-only) ===\"\nssh concertacaoamazonia.com.br-prod-sa \"$WP eval-file /tmp/prod-diag.php 2>&1\"",
  "description": "Diagnóstico read-only do estado dos posts em prod"
}
```

> TOOL

tool_result
id: toolu_0116zCVmCg2vhdpbTJ64WDN2
```
=== DIAGNÓSTICO PROD (read-only) ===
Deprecated: Creation of dynamic property Tribe__Events__Pro__Integrations__WPML__Event_Listener::$wpml is deprecated in /var/www/concertacaoamazonia.com.br/wp-content/plugins/events-calendar-pro/src/Tribe/Integrations/WPML/Event_Listener.php on line 52
[26666/PT] len=49382 | font-style:italic=1 | normal=0 | widget c3ba9a7=SIM | widget b723f80=SIM
[71726/EN] len=44265 | font-style:italic=1 | normal=0 | widget c3ba9a7=SIM | widget b723f80=SIM
```

> AGENT

Estado atual de produção confirmado:
- **PT (26666):** italic=1, normal=0, widgets `c3ba9a7` e `b723f80` **presentes** → precisa: italic→normal **e** remover os 2 widgets.
- **EN (71726):** mesma situação → idem.

Importante: em prod, **ambos** os posts ainda têm os 2 widgets (no DEV você já tinha removido do PT manualmente; prod não recebeu isso). Então em prod preciso aplicar as **duas** mudanças nos **dois** posts: (1) italic→normal e (2) remover widgets `c3ba9a7` + `b723f80`.

Há um detalhe importante: o `_elementor_data` de prod tem URLs de produção (`concertacaoamazonia.com.br`), não as URLs de DEV. Por isso **não** vou copiar o JSON do DEV — vou aplicar as mesmas **transformações** (italic→normal + remoção dos 2 widgets por ID) diretamente no JSON de prod, preservando as URLs e tudo mais. Isso é cirúrgico e seguro.

Vou montar um único eval-file que faz as duas transformações nos dois posts, com backup.

> TOOL

tool_use Bash
id: toolu_01NnyapAhU7reLX1uoGQLBkq
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/prod-apply-colmeia.php <<'PHP'\n<?php\n/**\n * PROD — Aplica nos posts da colmeia (Grupos de Trabalho / Workgroups):\n *   1) font-style: italic -> font-style: normal  (remove itálico dos textos da colmeia)\n *   2) remove os 2 widgets text-editor redundantes \"Facilitação/Facilitation: ...\"\n *      (ids c3ba9a7 e b723f80) — espelhando a edição manual feita no PT em DEV.\n *\n * Posts: 26666 (PT), 71726 (EN). Idempotente. Backups por post.\n *\n * Uso: wp eval-file ...            (dry-run, read-only)\n *      APPLY=1 wp eval-file ...     (aplica + regen Elementor CSS + clean cache)\n */\n\n$apply   = getenv( 'APPLY' ) === '1';\n$posts   = array( 26666 => 'PT', 71726 => 'EN' );\n$targets = array( 'c3ba9a7', 'b723f80' );\n\nforeach ( $posts as $post_id => $lang ) {\n    echo \"===== [$post_id / $lang] =====\\n\";\n\n    $raw = get_post_meta( $post_id, '_elementor_data', true );\n    if ( ! $raw ) { echo \"  SEM _elementor_data, pulado\\n\"; continue; }\n\n    // ---- (1) italic -> normal (em string, antes do decode) ----\n    $italic_count = substr_count( $raw, 'font-style: italic' );\n    $raw_fixed    = str_replace( 'font-style: italic', 'font-style: normal', $raw );\n\n    // ---- (2) remover widgets por id (decode -> filtra -> encode) ----\n    $data = json_decode( $raw_fixed, true );\n    if ( ! […]

> TOOL

tool_result
id: toolu_01NnyapAhU7reLX1uoGQLBkq
```
=== DRY-RUN PROD ===
===== [26666 / PT] =====
  italic->normal: 1 ocorrência(s)
  widgets removidos: 2
    - c3ba9a7 => "Facilitação: Roda Educativa"
    - b723f80 => "Facilitação: Fórum Brasileiro de Segurança Pública"
  [DRY-RUN] não gravado.
===== [71726 / EN] =====
  italic->normal: 1 ocorrência(s)
  widgets removidos: 2
    - c3ba9a7 => "Facilitation: Roda Educativa"
    - b723f80 => "Facilitation: Fórum Brasileiro de Segurança Pública"
  [DRY-RUN] não gravado.
Done.
```

> AGENT

Dry-run de prod confirma exatamente o esperado: em cada post (PT e EN), 1 italic→normal + 2 widgets removidos com os labels corretos. Vou aplicar.

> TOOL

tool_use Bash
id: toolu_01XghLAYmzJxoULckMw8xzgC
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nWP=\"sudo -u www-data wp --path=/var/www/concertacaoamazonia.com.br\"\necho \"=== APLICANDO EM PROD ===\"\nssh concertacaoamazonia.com.br-prod-sa \"APPLY=1 $WP eval-file /tmp/prod-apply-colmeia.php 2>&1\" | grep -vE \"Deprecated:\"",
  "description": "Aplicar mudanças em produção"
}
```

> TOOL

tool_result
id: toolu_01XghLAYmzJxoULckMw8xzgC
```
=== APLICANDO EM PROD ===
===== [26666 / PT] =====
  italic->normal: 1 ocorrência(s)
  widgets removidos: 2
    - c3ba9a7 => "Facilitação: Roda Educativa"
    - b723f80 => "Facilitação: Fórum Brasileiro de Segurança Pública"
  [DRY-RUN] não gravado.
===== [71726 / EN] =====
  italic->normal: 1 ocorrência(s)
  widgets removidos: 2
    - c3ba9a7 => "Facilitation: Roda Educativa"
    - b723f80 => "Facilitation: Fórum Brasileiro de Segurança Pública"
  [DRY-RUN] não gravado.
Done.
```

> AGENT

Mostrou `[DRY-RUN]` — o `APPLY=1` não passou pelo `sudo -u www-data` (a env var não atravessa o `sudo`). Preciso passar a variável de forma que o `sudo` preserve. Vou usar `sudo -u www-data env APPLY=1 wp ...`.

> TOOL

tool_use Bash
id: toolu_01SoXnt3rQeMrw3NDg8mmNaP
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== APLICANDO EM PROD (env via sudo) ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data env APPLY=1 wp --path=/var/www/concertacaoamazonia.com.br eval-file /tmp/prod-apply-colmeia.php 2>&1\" | grep -vE \"Deprecated:\"",
  "description": "Aplicar em prod com env preservado pelo sudo"
}
```

> TOOL

tool_result
id: toolu_01SoXnt3rQeMrw3NDg8mmNaP
```
=== APLICANDO EM PROD (env via sudo) ===
===== [26666 / PT] =====
  italic->normal: 1 ocorrência(s)
  widgets removidos: 2
    - c3ba9a7 => "Facilitação: Roda Educativa"
    - b723f80 => "Facilitação: Fórum Brasileiro de Segurança Pública"
  backup -> _elementor_data_pre_colmeia_fix
  Elementor CSS regenerado
  APLICADO. novo len=47450
===== [71726 / EN] =====
  italic->normal: 1 ocorrência(s)
  widgets removidos: 2
    - c3ba9a7 => "Facilitation: Roda Educativa"
    - b723f80 => "Facilitation: Fórum Brasileiro de Segurança Pública"
  backup -> _elementor_data_pre_colmeia_fix
  Elementor CSS regenerado
  APLICADO. novo len=42813
Done.
```

> AGENT

Aplicado em prod com sucesso (backups salvos, CSS regenerado). Agora preciso completar o deploy conforme o procedimento de prod do CLAUDE.md:
1. **Reload php-fpm** (OPcache do pool FPM — obrigatório em prod)
2. **Invalidação cirúrgica de cache** — WP Rocket + CloudFront só das páginas afetadas

Vou fazer o reload do php-fpm e a invalidação cirúrgica.

> TOOL

tool_use Bash
id: toolu_01FBCTSvc8CMmug7pCNceCua
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== 1) Reload php-fpm ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo systemctl reload php8.3-fpm && echo 'php8.3-fpm reloaded OK'\" 2>&1 | grep -vE \"Deprecated:\"\necho \"\"\necho \"=== 2) WP Rocket — limpar cache das 2 páginas (PT + EN) ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --path=/var/www/concertacaoamazonia.com.br eval '\nforeach ([26666, 71726] as \\$id) {\n  if (function_exists(\\\"rocket_clean_post\\\")) { rocket_clean_post(\\$id); echo \\\"WP Rocket limpo post \\$id (\\\" . get_permalink(\\$id) . \\\")\\n\\\"; }\n}\n' 2>&1\" | grep -vE \"Deprecated:\"",
  "description": "Reload php-fpm e limpar WP Rocket das páginas"
}
```

> TOOL

tool_result
id: toolu_01FBCTSvc8CMmug7pCNceCua
```
=== 1) Reload php-fpm ===
php8.3-fpm reloaded OK

=== 2) WP Rocket — limpar cache das 2 páginas (PT + EN) ===
WP Rocket limpo post 26666 (https://concertacaoamazonia.com.br/atuacao/grupos-de-trabalho/)
WP Rocket limpo post 71726 (https://concertacaoamazonia.com.br/en/activities/workgroups/)
```

> AGENT

php-fpm recarregado e WP Rocket limpo para ambas as páginas. Agora a invalidação do CloudFront para os dois paths. Vou usar o comando `cache-flush --prod` do docker-dev que já trata CloudFront, ou invalidar diretamente. Vou pegar a distribution ID e invalidar os 2 paths.

> TOOL

tool_use Bash
id: toolu_01Eeer66EBFojkCtDxzUteGJ
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\n# CF distribution conhecida da memória: E2F1QD7E7YOYEB. Confirmar e invalidar os 2 paths.\nDD=/home/<USER>/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh\necho \"=== CloudFront — invalidação cirúrgica via cache-flush --prod ===\"\n$DD cache-flush --prod --cf-only \"/atuacao/grupos-de-trabalho/\" 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|^\\s*$|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress\" | tail -25",
  "description": "Invalidar CloudFront da página PT"
}
```

> TOOL

tool_result
id: toolu_01Eeer66EBFojkCtDxzUteGJ
```
=== CloudFront — invalidação cirúrgica via cache-flush --prod ===


[38;2;102;217;239m[INFO][0m Target: PROD (alias=concertacaoamazonia.com.br-prod-sa, wp_root=/var/www/concertacaoamazonia.com.br)
[38;2;102;217;239m[INFO][0m WP Rocket: pulando (--cf-only)
[38;2;102;217;239m[INFO][0m CloudFront (E2F1QD7E7YOYEB): invalidando /atuacao/grupos-de-trabalho/...
[38;2;102;217;239m[INFO][0m Invalidacao I76F3FVOO3Z04KOJUB4F2V9923 criada — aguardando propagacao...
[38;2;166;226;46m[OK][0m Cache limpo e propagado!
[38;2;102;217;239m[INFO][0m Verificacao: render fresco da origin em /atuacao/grupos-de-trabalho/ (bypassa WP Rocket + CloudFront)...
[38;2;166;226;46m[OK][0m Verificacao: HTTP 200 em /atuacao/grupos-de-trabalho/
[38;2;166;226;46m[OK][0m Verificacao: render fresco OK em /atuacao/grupos-de-trabalho/
```

> AGENT

PT invalidado e verificado (HTTP 200, render fresco OK). Agora o EN.

> TOOL

tool_use Bash
id: toolu_0135SdezcAkc73rcinY8QyJu
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=/home/<USER>/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh\necho \"=== CloudFront — invalidação cirúrgica EN ===\"\n$DD cache-flush --prod --cf-only \"/en/activities/workgroups/\" 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|^\\s*$|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress\" | tail -25",
  "description": "Invalidar CloudFront da página EN"
}
```

> TOOL

tool_result
id: toolu_0135SdezcAkc73rcinY8QyJu
```
=== CloudFront — invalidação cirúrgica EN ===


[38;2;102;217;239m[INFO][0m Target: PROD (alias=concertacaoamazonia.com.br-prod-sa, wp_root=/var/www/concertacaoamazonia.com.br)
[38;2;102;217;239m[INFO][0m WP Rocket: pulando (--cf-only)
[38;2;102;217;239m[INFO][0m CloudFront (E2F1QD7E7YOYEB): invalidando /en/activities/workgroups/...
[38;2;102;217;239m[INFO][0m Invalidacao I221OFIXAKZGE6W0JDA5H9JBVC criada — aguardando propagacao...
[38;2;166;226;46m[OK][0m Cache limpo e propagado!
[38;2;102;217;239m[INFO][0m Verificacao: render fresco da origin em /en/activities/workgroups/ (bypassa WP Rocket + CloudFront)...
[38;2;166;226;46m[OK][0m Verificacao: HTTP 200 em /en/activities/workgroups/
[38;2;166;226;46m[OK][0m Verificacao: render fresco OK em /en/activities/workgroups/
```

> AGENT

Ambas as páginas invalidadas e verificadas. Agora a validação final em produção real (não tunnel) via browser — confirmar que: (1) itálico removido na colmeia, (2) sem widgets "Facilitação:" duplicados, em PT e EN.

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_017LQJCgFe41Hn6pQr9qXhqJ
```json
{
  "url": "https://concertacaoamazonia.com.br/atuacao/grupos-de-trabalho/"
}
```

> TOOL

tool_result
id: toolu_017LQJCgFe41Hn6pQr9qXhqJ
```
### Ran Playwright code
```js
await page.goto('https://concertacaoamazonia.com.br/atuacao/grupos-de-trabalho/');
```
### Page
- Page URL: https://concertacaoamazonia.com.br/atuacao/grupos-de-trabalho/
- Page Title: Grupos de Trabalho – Uma Concertação pela Amazônia
### Snapshot
- [Snapshot](.playwright-mcp/page-2026-06-05T21-51-44-229Z.yml)
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-51-41-286Z.log#L1-L3
```

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_012aTcdQdCEfJsQtpZ8V2Z2T
```json
{
  "function": "() => {\n  const r = {};\n  // regra italic\n  let rule=null;\n  for (const sheet of document.styleSheets) {\n    let cr; try { cr=sheet.cssRules; } catch(e){ continue; }\n    if(!cr) continue;\n    for (const x of cr) if (x.selectorText && /\\.gtSVG\\s+\\.italic/.test(x.selectorText)) rule=x.cssText;\n  }\n  r.gtSVGItalicRule = rule;\n  const tspans=[...document.querySelectorAll('svg.gtSVG tspan.italic')];\n  const fs={}; tspans.forEach(t=>{const s=getComputedStyle(t).fontStyle; fs[s]=(fs[s]||0)+1;});\n  r.tspanFontStyles = fs;\n  // widgets Facilitação soltos\n  r.looseFacilitacao = [...document.querySelectorAll('.elementor-widget-text-editor')]\n    .map(e=>e.textContent.trim().replace(/\\s+/g,' '))\n    .filter(t=>/^Facilita(ção|tion):/i.test(t));\n  r.svgCount = document.querySelectorAll('svg.gtSVG').length;\n  return JSON.stringify(r,null,2);\n}"
}
```

> TOOL

tool_result
id: toolu_012aTcdQdCEfJsQtpZ8V2Z2T
```
### Result
"{\n  \"gtSVGItalicRule\": \".gtSVG .italic { font-style: normal; fill: var(--GT-TEXT); }\",\n  \"tspanFontStyles\": {\n    \"normal\": 19\n  },\n  \"looseFacilitacao\": [],\n  \"svgCount\": 2\n}"
### Ran Playwright code
```js
await page.evaluate('() => {\n  const r = {};\n  // regra italic\n  let rule=null;\n  for (const sheet of document.styleSheets) {\n    let cr; try { cr=sheet.cssRules; } catch(e){ continue; }\n    if(!cr) continue;\n    for (const x of cr) if (x.selectorText && /\\.gtSVG\\s+\\.italic/.test(x.selectorText)) rule=x.cssText;\n  }\n  r.gtSVGItalicRule = rule;\n  const tspans=[...document.querySelectorAll(\'svg.gtSVG tspan.italic\')];\n  const fs={}; tspans.forEach(t=>{const s=getComputedStyle(t).fontStyle; fs[s]=(fs[s]||0)+1;});\n  r.tspanFontStyles = fs;\n  // widgets Facilitação soltos\n  r.looseFacilitacao = [...document.querySelectorAll(\'.elementor-widget-text-editor\')]\n    .map(e=>e.textContent.trim().replace(/\\s+/g,\' \'))\n    .filter(t=>/^Facilita(ção|tion):/i.test(t));\n  r.svgCount = document.querySelectorAll(\'svg.gtSVG\').length;\n  return JSON.stringify(r,null,2);\n}');
```
### Page
- Page URL: https://concertacaoamazonia.com.br/atuacao/grupos-de-trabalho/
- Page Title: Grupos de Trabalho – Uma Concertação pela Amazônia
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-51-41-286Z.log#L4-L5
```

> AGENT

PT em produção real validado:
- `.gtSVG .italic { font-style: normal; ... }` ✅
- 19 tspans, todos `normal` (zero itálico) ✅
- `looseFacilitacao: []` — sem widgets duplicados ✅

Agora o EN em produção.

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_016Cc8UQxn5tRJavEcVYYwrD
```json
{
  "url": "https://concertacaoamazonia.com.br/en/activities/workgroups/"
}
```

> TOOL

tool_result
id: toolu_016Cc8UQxn5tRJavEcVYYwrD
```
### Ran Playwright code
```js
await page.goto('https://concertacaoamazonia.com.br/en/activities/workgroups/');
```
### Page
- Page URL: https://concertacaoamazonia.com.br/en/activities/workgroups/
- Page Title: Workgroups – Uma Concertação pela Amazônia
### Snapshot
- [Snapshot](.playwright-mcp/page-2026-06-05T21-52-02-081Z.yml)
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-52-00-169Z.log#L1-L3
```

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01DUYKtq5zCMXEpMKi2btE77
```json
{
  "function": "() => {\n  const r = {};\n  const tspans=[...document.querySelectorAll('svg.gtSVG tspan.italic')];\n  const fs={}; tspans.forEach(t=>{const s=getComputedStyle(t).fontStyle; fs[s]=(fs[s]||0)+1;});\n  r.tspanFontStyles = fs;\n  r.looseFacilitacao = [...document.querySelectorAll('.elementor-widget-text-editor')]\n    .map(e=>e.textContent.trim().replace(/\\s+/g,' '))\n    .filter(t=>/^Facilita(ção|tion):/i.test(t));\n  r.svgCount = document.querySelectorAll('svg.gtSVG').length;\n  return JSON.stringify(r,null,2);\n}"
}
```

> TOOL

tool_result
id: toolu_01DUYKtq5zCMXEpMKi2btE77
```
### Result
"{\n  \"tspanFontStyles\": {\n    \"normal\": 19\n  },\n  \"looseFacilitacao\": [],\n  \"svgCount\": 2\n}"
### Ran Playwright code
```js
await page.evaluate('() => {\n  const r = {};\n  const tspans=[...document.querySelectorAll(\'svg.gtSVG tspan.italic\')];\n  const fs={}; tspans.forEach(t=>{const s=getComputedStyle(t).fontStyle; fs[s]=(fs[s]||0)+1;});\n  r.tspanFontStyles = fs;\n  r.looseFacilitacao = [...document.querySelectorAll(\'.elementor-widget-text-editor\')]\n    .map(e=>e.textContent.trim().replace(/\\s+/g,\' \'))\n    .filter(t=>/^Facilita(ção|tion):/i.test(t));\n  r.svgCount = document.querySelectorAll(\'svg.gtSVG\').length;\n  return JSON.stringify(r,null,2);\n}');
```
### Page
- Page URL: https://concertacaoamazonia.com.br/en/activities/workgroups/
- Page Title: Workgroups – Uma Concertação pela Amazônia
### Events
- New console entries: .playwright-mcp/console-2026-06-05T21-52-00-169Z.log#L4-L5
```

> AGENT

EN em produção real validado:
- 19 tspans, todos `normal` — zero itálico ✅
- `looseFacilitacao: []` — sem widgets duplicados ✅

Vou tirar um screenshot final da colmeia em prod para registro visual e fechar a task.

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01LFZGPLVJXZz3F7uLNZqHg7
```json
{
  "function": "() => { const s=document.querySelector('svg.gtSVG.desktop')||document.querySelector('svg.gtSVG'); if(s)s.scrollIntoView({block:'center'}); return s?'ok':'no'; }"
}
```

> TOOL

tool_result
id: toolu_01LFZGPLVJXZz3F7uLNZqHg7
```
### Result
"ok"
### Ran Playwright code
```js
await page.evaluate('() => { const s=document.querySelector(\'svg.gtSVG.desktop\')||document.querySelector(\'svg.gtSVG\'); if(s)s.scrollIntoView({block:\'center\'}); return s?\'ok\':\'no\'; }');
```
```

> TOOL

tool_use mcp__playwright__browser_take_screenshot
id: toolu_01G4L4ttLND6Es8sLFD3B3i4
```json
{
  "type": "png",
  "element": "Colmeia SVG desktop em produção (EN)",
  "target": "svg.gtSVG.desktop",
  "filename": "colmeia-prod-final.png"
}
```

> TOOL

tool_result
id: toolu_01G4L4ttLND6Es8sLFD3B3i4
```
### Result
- [Screenshot of Colmeia SVG desktop em produção (EN)](./colmeia-prod-final.png)
### Ran Playwright code
```js
// Screenshot Colmeia SVG desktop em produção (EN) and save it as ./colmeia-prod-final.png
await page.locator('svg.gtSVG.desktop').screenshot({
  path: './colmeia-prod-final.png',
  scale: 'css',
  type: 'png'
});
```
```

> TOOL

tool_use Read
id: toolu_011iCE1xbXdvjQ1fCrGGhU4V
```json
{
  "file_path": "/home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao/colmeia-prod-final.png"
}
```

> TOOL

tool_result
id: toolu_011iCE1xbXdvjQ1fCrGGhU4V
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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u03Ztje2pnH4kT/4zT9+xtPe9OVf7SNf7GX/5A//6Pz8tuuuvfbo6EjScrns+77v+/V6PU3Tddddd/r0aeDee++9++67Nzc3MxOwLUlSZkoahuHFXuzFIsK2pIODg0uXLp0/f76U8shHPvLP/uzPzpw5c/vtt7/US7/0qZMn3/913vT2C+e++3d+6ef/7i8+4DVe//rT1x4dHdoOiRdN2rXvf/Qv/+gD3uCtahRDLYUHmKbp0qVLx48fz8y77roLuP766/u+5zllZkT88R//8Z/+6Z9+wAd8wPb2dmZKkvRnf/Znj3vc406ePHlwcDCfz1/hFV7hwQ9+sG1JP/iDP3jttdeePXv2b//2b5/+9Ke//du//c7ODiAJsB0RXPZJb/nOH/mdX/16j3mJedenzX8TSWQibc7m3O+ee+5Zr9f/8A//cNtttz3kIQ85PDycz+ePfvSjT548CZw/f/78+fNnz57d2tp60IMedN99981ms/39/dlslpkPechD+r6PiG/5lm85ODj4wA/8wN/7vd97lVd5le/93u99+MMffnBwcObMmbNnzz72sY991Vd9VUn33nvvb/zGb5w8eXIcx1LKsWPHlsvlOI6PeMQjHv7wh3OZbUlcNu9mR8Maif98lX8HA/b29rE/fNzf/NTf/vkjb3roV7znh4d09z33/OCP/sgN11//5m/+5svl8uDgoJRy+vTpe++9dxiGaZpOnToFAJcuXTp9+vTJkyfHcQQkTdO0Xq9PnDixXC7vueee1Wq1sbEhCbjtttsi4q677rrvvvsuXry4Wq2uv/76v/v7v7/n7rtPnTw5TtPNJ09/xtu8x58+7Ylf/Gs//5LX3fC+r/Z6hqNhXSL4l9jenM0ef/vTD6b2sg96+Hoc2jCN07ixsSGp1mr76U9/+nq9vnjx4sbGxm/91m8tFotXf/VXv/HGG9frdURERCnFdkQ84xnPuOuuu2az2Z//+Z+/4iu+4ubmpu2/+Zu/WSwWr/qqr9pa29zcXK/X+/v7t99++8033wxk5g/8wA9EBHDLLbd0XQf82q/92m/91m+11kopy+VymqZP/KRPuvmmm17nxV/+5//2z9/t1V//4GC/RPDfR8g826VLlx7/+Mcvl8vZbLaxsbFarS5cuLBarQCglLJare66666HPexhd9999x/8wR8A+/v7991335kzZ977vd/75MmTwAd90Ad9yqd8yq//+q+/x3u8x6VLlx70oAe9xEu8xC/8wi887GEPu+OOO26++WYue+pTnzqfz6dp2t7eXq/X8/n83Llzkp7whCc87nGPq7W+xEu8xM0332yb+0niv0Tl38ogWMxm3/irP3Pb/v4nvNW7X7NzHGiZ11933Zu+yZtcd911ki5dutT3/Xw+f+ITn3j99de/5mu+JpdlZkSUUi5cuAC01oCIaK211qZpmqbp8PCwlALYlnTvvfc+/vGPP378+OnTpx/84Affdtttd99990u+xEtsb28DtRTbab/iQx/1ig991I/96e9+xI985ye+4Vvecuqag9WyRPBCpa3a/+VtT3vFR734wcXdP/qLP2tT29vbG8fxlltueY3XeI1xHNfr9ebm5uHh4alTp17sxV5sf3//cY973B133NFa293d3d7efomXeImdnR1JrbWTJ0+eOHGilGIbkHTDDTesVivg6OgoM3d2djJze3ubyx7zmMfs7e3dfvvtOzs7j3rUo2wDD3nIQ/q+39zcPDg46Pv+4OBge3sbeNVHvdi3/+pPMY2S+G9mAWAMXLx48S//8i8Xi8UNN9zwiEc8wvY4jjs7O4Dt48ePl1JuvvnmzNze3n70ox89TVPXda01oJQC2N7e3v76r//61Wol6dixY+/xHu8BPPzhD5/NZq/zOq/D/V7mZV5muVwul8vZbDYMw+bm5o033ijp4sWL8/l8sVhsbW0BkrD5r1X5t7K9MV980S/82M3XP+iL3+ydgam1WkpIwGu+5mv2fb9er8+cOZOZkq6//vq+7wHbkiICuOWWW3Z3dyXxAJJsAydOnJjNZtzvVV/1VXd2dkopj33sY5fL5SMf+cjFYjFNU9/3gCSgSJkp6R1e8TVf5sGP+Ipf/NGPfd03fdCpaw6HdUi8cG637158jZd+la1jOw960INOnTzVWrvvvvuuvfZaoO/7G2644ezZszfddFMpJTNvuumm3d3d2WzWdd3x48eXy+XjHve4l3u5l5vNZg996ENns9nR0dGpU6e2trZsSzpz5gwwDMM999wzn8+vueYaHuDBD35w13VPf/rTz5w584hHPGJjY8P2wx/+8Ic//OE8J9s3nThdu/7c3qWdjc2Wyf8AoQDe+Z3f+R3e4R2AiJjP58BiseAySba3t7d5gK7rgFIK95NkW9J8PgckAZk5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tiUBtvl3kMT9bEsCbEtarVa/+Zu/2ff9q77qq25sbNiWJInLJPFCScpMSZJsSwJsA5IA20gYMCDJdmut1gpM0xSl8D+Y7e3tbcC2JB5AEmBbEv8SSdxPEiCJ/yUq/0Fuv/32Ukop5dprr+U5rVaraZokTdN0dHS0sbEhiftJOjw8fOpTn2r7EY94xMbGBg/wZ3/2Z49//OMf+tCHvvqrvzpgW5JtQBLPQxKXSQJs869irrjzzjslrdfrkydPHjt2jMsys5Tyrd/6rb/4i7944sSJ++67713f9V0lDcNw6dKlzc3NUso4jrYzs5QyjmNEHDt2jAe4cOHCn//5n588efIlX/Il+74HAEncTxKAAHHZcrn8q7/6q4c//OFPeMITbrnlloc85CH8T2UbsA0Atm0DkgBJgCT+89mWxH+Tyr+XgYODgwsXLrzUS73U7bffvlqt5vM5sF6v9/b2aq0HBwdbW1utNaC1dnBwsFgstre3gac97Wnnz59/qZd6qdOnT0uKCODo6GixWEgahuHv//7vgac//ekv8RIvcezYMUmAJJ7T0dHRHXfcsb29ffvttx8eHto+PDx87GMf+7CHPYx/HUfEOAxPevKTT508ee7cubNnz95www2/9Eu/9FZv9VbXXHPNNE1//ud//pCHPOQv/uIvnvCEJxweHm5ubp47d+6nfuqnXv/1X3+5XP7FX/wFMJ/Px3FcrVanT59+67d+61orkJkR8Xd/93fnz59fLpenT59+8IMfnJmS9g8Odra3z1+4ME7T9tZWKQXAnlrb2twcx3FjY2OxWGxvb0cE/4NJ4jlJ4l/JNgBI4gFsA5J4EUjiv0/lP8LW1tY0TX/0R380n89vvvlmLluv109/+tMz8/jx47fffvvm5mbXdavVand395prrnnxF39x4Hd/93cf+tCH/u3f/u3BwcGJEyfuueeeY8eOlVKuu+662Wxm++TJk8vl8oYbbjh27Njh4eH58+f7vh/Hse/7M2fORIRtSefPn7/11ltvvvnmvb29zc3Nvu9Xq9UwDPwrGSLicG//yU960h2LRURsb28vl8vXeZ3X2dnZAWqtL/ESL/H7v//7L/7iL/7Yxz52c3MTOH369Eu+5EvedNNN991334033njTTTcdHR3t7++P42i71splEQE8+tGP3t3dveWWW2688UYgIoBLe3v33HvvxUuX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c88bvuEbvtZrvVZmRsTf/M3fLJfL8+fP33nnnSdOnLj55puPHz8OrFarw8PDl37pl97Z2XnsYx976tSpixcvXrx4cZqmzDx16tQjHvEIIDOPlkcPf+jDH/fEx509fzYipmnisrRDesLdt59aLLY2tw8OD0oEL4KWOe/62vfPuPeun/7rP73n4OC6E6cffeODXuIRL7E5m8+7fjmsD1bLOy6c/c2nPfnH//pPH3Li1Os9+iUefMPN43K5moYahRcgpMPl0ce+6dv92B/99sd879e/92u/6Uvd8lCg6/vZbMaLwLYknoft+XzOA9iWxGWSgJ2dnZd7uZfjfoYpW40CfP8f/MafPvFvP+513/Sh1924f3hQI/ivUvlXksDua122iedhW9JyufylX/ol4M477/zLv/zL93mf93mxF3ux8+fPR8SDH/zg+XxuW5Jt2xFxcHBwdHR0/Pjx1hoAlFL6vud+u7u74zieOXOmtQZEhCTuZ5v7SeJ5pHPR94gXIqTVevUKD3nE7/z6L6RdIoCjo6O77rrrYQ972G233bazsxMRtiUBpZRSyjRNL/mSL/nXf/3X586de83XfE3ANnDttdeuVqtTp07t7OwAks6fPz+bzTJzGAbbQNd1N91009Of/vRpmrqu29vbG4YBAB5884Nf6rEv/aqv/Kof+v4f9ozbbr35plvGcQQiYmotSvmlv/6T13zww8mUxL+kZdZStrZ27rzv7h/8s99bo9d87Mu82iNfrCh4Hi91y0Pf7KVfacr8ncf/zdf93q9fu7HxXq/yOteevvboYM84FDw/IR0c7L/Dq7z2yz/44d/+e7/yGyfPfMDrvNn2fNGyCUUEL5Qknh9JPCdJPA/bANAyayk1yt/c9rTv/K1feKnrbviqd3zvkA6ODmsE/4Uq/2rC3pkvnnrvPYAxz0OS7Yc97GG7u7sHBwfr9frSpUsXL14spdx5550PfvCDSykAEBG7u7t//dd/fe2119re398/PDyUdOrUqRtvvNG2pIsXLz71qU/d2toahmGxWNx3331bW1v7+/t935dSdnd3t7e3H/awh/GC7a+W89pRqr1C4gWYWtvZOvbSN9z83b/7K+/7Wm88tnb8+PHW2q233vpXf/VXb/7mb3769OnTp0/zAJKAY8eOPehBD8pMQBJw4403AuM4PuQhD5E0jqOkUkprDVgsFkBE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53ibRqGxtY2+v/382Y2+P7Vz/HB52DJ3FpurcbDNv1vlfzbbkvb29iTNZrPVanXs2LELFy50XWe7tTabzSJC0p133vmUpzzl1KlTwzDcddddN9100z/8wz/ce++9L/dyL9f3/Q033GD7jjvuuOOOO5bL5Yu92Ivdddddy+XyYQ97GJCZEbGxsbGzs7O9vb2/v7+1tVVK2dzcBIBHP/rROzs7T3/60/f394GdnZ1SytHRUUS8yqu8SkT8/d///bXXXnvq1Km77rrrrrvuuvbaawHbkviX2JYk6YlPfOK99957eHj4h3/4hxsbG2/91m99+vRp25KAS5cuTdO0t7d3+vTps2fP7uzszGazO++888yZM6vVapom4EEPehBgW9JTn/rUixcvXrp06Z577pnP56WU++67r7UWESdPnrx06RKws7NzdHR07ty5l3zJl+z7XtL58+f/8A//sNb6h3/4hy/zMi9z9913z2az1hrw8i//8qUUSdzPtqQf+ZEf6fv+4OBgb2/v1V/91X//93//ZV7mZU6ePHnnnXc+4xnPeNM3fdP5fN5a6/seyMyIuP3225/ylKecO3fu1KlTkoZheK3Xei2eU9pd1z/xnif98j/89cve8pBTW9urcWyZs9p1pZw/3F90/TBN867vaz1/uP+qD33UxaPDJ9171/Z8sb9aIma1u2b72IvdcPOX/PJPvusrvsat58+up/HFb7jl7ksXz2zv3HHx/DhNfe0kQnFme+e+/b3XftSLzWpnm3+fyv9skoBa62q1uvHGG+fz+X333Wd7e3s7M8dx7LqOy7qu297eXq/XkjY2NjY3N7e2tjY2Nrjsb/7mb57+9KdL6vt+HEdJN954I5fZftSjHvWoRz0KeImXeAmeh+1SyqlTp3Z3d8+cOXN0dDRNUynF9rFjx7qu6/v+7d7u7SRFBJCZEQFEBP8S25KGYfiu7/qu/f39l3u5lzt16lRm/tZv/da3fuu3fuRHfuTW1lZmRsTf/d3f3XbbbY961KP++q//+td//dd3dnYWi8Xp06eXy+WlS5de5mVeZn9//z3f8z0zMyKe8pSn/Pqv//rrvd7r7e7u9n3/tKc97aabbprNZrVW2+v1uu9728vlspRyww03RASXDcNw/PjxjY2NYRh2d3drrev1upRSSvnbv/3baZouXLiwubl54403PuQhD7Etab1e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pmmS1HUdYHscx2maNjY2aq3AMAznzp275pprDg8Pt7a2MnOaplKKJEnr9brve6DrOuA7v/M7X+d1Xmd3d/f222/v+35ra8t2a21ra2sYhoODg52dHf59xP8Ulf/xJAGPfvSjAUlclplARACSgDd8wzd83dd93b29Pdvb29t93wO2JQEPf/jDuWxra4vnNJvNuN+bv/mbS+I5lVKAN33TN33TN31TnlNEALXWU6dOAbYBh/nXsP1Hf/RHe3t7v/Vbv7W9vX3fffe96qu+6tbW1hOf+MStra1a62Me8xjbpZRSim1JT3/605/ylKeM43jjjTdKuuuuu+69996jo6P3eI/32NraysxaKzCfz8dxBKZpiohpmmxP09T3vSTbZ86cufbaa20DpRSg1nr8+PG/+7u/29nZedKTnnT+/PnMtF1Ksd1aO3HixMu8zMvUWoE//uM/vuOOO17mZV4mMw8PD/u+L6VkZq01Ig4ODqZpuuGGGx70oAcBN91008/93M99yId8yGKx+PM///PW2rFjx06ePAns7++31gDbkvjfr/K/hCQeICJ4TplZaz158iSXZaYkSVxmG5BkWxJgWxJgWxIASOIFsA3Y5n6SAEm2JQGSAEmAbUm8UJKAEydOfMiHfMjR0dHGxoakaZokrdfrt3u7t5NkG4gIHuDJT37yX/zFX5w/f/4pT3nKgx70oDd5kzd59Vd/9Z2dna2tLduSSinb29sHBwfz+byUAkzTNJvNtre31+v15uZmZl66dGlra2s+n/MAth/60IeeO3fuzJkz99xzz2233bZarU6fPr1cLjNzvV7/wz/8wyMf+cjFYgG85Eu+5CMe8YiTJ0+O49ha6/semKap6zpgmibb8/mcy97mbd5mGIa+75fL5ZkzZ9br9blz586cOXPPPffcdNNNT33qU0spN9xwg21J/C9X+V8iMyMCsG1bEpdJ4rKIsG0bkCRJEveTZNs295PEZZK4n23AtiTuJ8k2IEkSz0PSMAx/8id/cvvttz/ucY/b3t5+gzd4g5d92Ze1LYl/iaSNjY2NjQ0eYGtri+dHEvAar/Eaj370o4dhuHjx4kMe8pDTp0/znObz+cbGBi/UzTffDNiWxP0kAS//8i8fEa/6qq/6yq/8yplZa12v113XAeM4zmYzADh+/Pjx48eB2WzGvyQz+74Huq47fvw4cObMGdsn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JtuSuMx2RGSm7VIKl9mWxGWSpmlar9fTNAERUUqRBMznc0ncTxKXSeIySbwAtu+5556IWCwWOzs7mSnJdkTYvueee+bz+YkTJ66//nqen7SL9Le3PfXm4yeJ4DlJAo4dO/a3f/M3d91111133rW1vX3tddf9/d/93Yu/xEsAwzDM5/Otra39/f3rr7/+1ltvPX78+N7e3rFjxxaLxe7u7ku+5Ev+zM/8zIkTJ06dOsVlq9Xq6OhoHMf5fH50dDSbzTLz1KlTEQH0ff9iL/Zif/u3f7ter6+//vpHPvKRgO2IuO222/7gD/7gmmuumc1m0zRdf/31Fy5cuOaaaw4PDzc2NmqttVbg2LFj+/v7D3/4w0+ePHnvvfceO3bs3Llz29vby+VyGIa+74G+71er1VOe8pQbb7zx/PnzXdedPn16GAbbf/mXf/mkJz1pb2/vlV/5lR//+Mc/+clPtn3ixAlAEv8nVP6HkUTmKzzoob/3hL991PU3tcxaCpdJGsfxtttuO378+KlTp7hMEg8wTdP+/v4wDMMw2La9sbHRdV2ttes6LrN98eLFUsqFCxfGcSylbG9vT9N0dHS0tbUVEadPn44IwLak++67b39//5GPfOTTn/707e3tiAAkAU960pMODg7Gcbzppptuuukm25J4TgLgSXc+471e4VVZryLEc7Jda32Zl33Zx/3DP5w8efLRj3kMsFqtuMx2RKzX64ODg77vH/vYx47j2HXdfD6fz+e33HLLX/7lX77O67zOIx/5SNuSJD384Q+fz+eZKQmwDaxWq2magNbaarW65pprJO3t7T31qU992MMeVmt92tOe9nVf93W2X/d1X/fYsWPz+fyee+657bbbzpw5M03TjTfeOJvNbAO33nrrfffdFxG33nrrer1+9KMfPY7jarWqtT7hCU+4+eabT5w4sbOz88hHPvKee+65++67d3Z2brzxRi674YYb5vP5XXfd9djHPvbBD37w0572tL29vRtuuGG1Ws3nc/6vqPwPE9LRevVqD3/sT/3E9+4evdbxjU3bkgDA9l133XV0dPT4xz++tVZrHYahlPISL/ESJ06cACQdHR2tVqvNzc1aK7C3t7ezsyOJy2zfeuutFy5cuO666/7kT/5kf3//7rvvvuaaazJztVrt7Ozs7++/x3u8x+nTp21z2ebm5tOe9rS77rprHEdJ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",
    "media_type": "image/png"
  }
}
```

> AGENT

Screenshot de produção confirma: textos das facilitações em **estilo normal** (sem itálico), e sem os textos "Facilitation:" duplicados soltos. Tudo aplicado corretamente.

Vou fechar a task e o browser.

> TOOL

tool_use TaskUpdate
id: toolu_01WpAwipnoFRkNtBpXjwnhS6
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> TOOL

tool_use mcp__playwright__browser_close
id: toolu_01VMmbcRdHHvVdM8vJDX1TUj
```json
{}
```

> TOOL

tool_result
id: toolu_01WpAwipnoFRkNtBpXjwnhS6
```
Updated task #2 status
```

> TOOL

tool_result
id: toolu_01VMmbcRdHHvVdM8vJDX1TUj
```
### Result
No open tabs. Navigate to a URL to create one.
### Ran Playwright code
```js
await page.close()
```
```

> AGENT

Vou limpar os arquivos temporários criados durante o trabalho.

> TOOL

tool_use Bash
id: toolu_01Wwb5JvFvrYYqzczC2rAGbw
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nrm -f tmp/remove-colmeia-italic.php tmp/remove-en-facilitation-widgets.php tmp/prod-apply-colmeia.php tmp/prod-diag.php tmp/pt_current.json tmp/pt_rev92889.json tmp/en_current.json tmp/en_after.json colmeia-dev-pt-sem-italico.png colmeia-prod-final.png\n# limpar do container e prod também\ndocker exec concertacao-dev-wordpress rm -f /tmp/remove-colmeia-italic.php /tmp/remove-en-facilitation-widgets.php /tmp/pt_current.json /tmp/pt_rev92889.json /tmp/en_current.json /tmp/en_after.json 2>/dev/null\nssh concertacaoamazonia.com.br-prod-sa \"rm -f /tmp/prod-apply-colmeia.php /tmp/prod-diag.php\" 2>/dev/null\necho \"Temporários limpos.\"",
  "description": "Limpar arquivos temporários"
}
```

> TOOL

tool_result
id: toolu_01Wwb5JvFvrYYqzczC2rAGbw
```
Temporários limpos.
```

> AGENT

Tudo concluído e validado em produção. 

## Resumo do deploy

Apliquei em **produção** (concertacaoamazonia.com.br), nos posts **26666 (PT)** e **71726 (EN)** da colmeia Grupos de Trabalho / Workgroups, espelhando o que você fez no PT em DEV:

**1. Itálico removido** — a regra `.gtSVG .italic { font-style: italic }` → `font-style: normal`. Os 19 textos de facilitação da colmeia agora aparecem em estilo reto, em PT e EN.

**2. Dois widgets de texto redundantes removidos** (em PT e EN), que repetiam fora do SVG o que a colmeia já mostra:
- `c3ba9a7` → "Facilitação/Facilitation: Roda Educativa"
- `b723f80` → "Facilitação/Facilitation: Fórum Brasileiro de Segurança Pública"

**Procedimento de prod seguido integralmente:**
- ✅ Backup do `_elementor_data` original de cada post (meta `_elementor_data_pre_colmeia_fix`)
- ✅ Regen do Elementor CSS de cada post + limpeza do `_elementor_element_cache`
- ✅ `reload php8.3-fpm` (OPcache do pool FPM)
- ✅ WP Rocket limpo cirurgicamente nos 2 posts
- ✅ CloudFront invalidado nos 2 paths (`/atuacao/grupos-de-trabalho/` e `/en/activities/workgroups/`) — render fresco HTTP 200 confirmado
- ✅ Validação final no browser em **produção real**: itálico ausente (19 tspans `normal`), zero widgets "Facilitação:" soltos, em ambos os idiomas

**Observação:** em DEV o PT já estava sem os 2 widgets […]

> DEVELOPER

faça o deploy da pagina https://concertacao.bureau-it.com/cultura/galeria para prod, incluindo EN

> AGENT

Você quer fazer deploy da página `/cultura/galeria` (blog 2 — Cultura) de DEV para produção, incluindo a versão EN. Esta é uma página do **blog 2 (`/cultura/`)**, que tem particularidades importantes (Network Media Library, attachments cross-blog, WPML).

Antes de agir, preciso entender exatamente o que mudou e qual o escopo do deploy. Deixa eu investigar a página em DEV e seu estado em prod.

> TOOL

tool_use Bash
id: toolu_01NpA4KMD7YAZnJZ7hoD9NnW
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=\"docker exec -u www-data concertacao-dev-wordpress wp\"\necho \"=== DEV: identificar página /cultura/galeria (blog 2) ===\"\n$DD eval '\nswitch_to_blog(2);\n// buscar por slug galeria\n$pages = get_posts([\"post_type\"=>\"any\",\"name\"=>\"galeria\",\"post_status\"=>\"any\",\"numberposts\"=>5,\"suppress_filters\"=>true]);\nforeach ($pages as $p) {\n  echo $p->ID . \" | \" . $p->post_type . \" | \" . $p->post_status . \" | \" . $p->post_title . \" | \" . get_permalink($p->ID) . \"\\n\";\n}\nrestore_current_blog();\n' --path=/var/www/html 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|Docker|Devil|docker-dev|Versao|Ambiente|^\\s*$|Deprecated\"",
  "description": "Identificar página galeria no blog 2 em DEV"
}
```

> TOOL

tool_result
id: toolu_01NpA4KMD7YAZnJZ7hoD9NnW
```
=== DEV: identificar página /cultura/galeria (blog 2) ===
26767 | page | publish | Galeria | https://cambrasmax.local:8484/cultura/galeria/
```

> AGENT

Encontrei: página **26767 "Galeria"** no blog 2 (Cultura). Agora preciso da tradução EN (via WPML) e comparar o estado entre DEV e prod para entender exatamente o que mudou. Isto é uma operação WPML em site com WPML ativo — devo invocar o agente Poliglota conforme as regras do projeto.

> TOOL

tool_use Skill
id: toolu_01QUys1wbvNKUBbP6czd8ePf
```json
{
  "skill": "bit-translate-wpml",
  "args": "diagnosticar página Galeria (blog 2 /cultura/, post 26767 PT) e sua tradução EN, no contexto de deploy DEV→prod incluindo EN"
}
```

> TOOL

tool_result
id: toolu_01QUys1wbvNKUBbP6czd8ePf
```
Launching skill: bit-translate-wpml
```

> AGENT

Sou o **Poliglota**. Vou diagnosticar a página Galeria (PT 26767) e sua tradução EN no contexto deste deploy DEV→prod.

Já conheço a configuração deste site (concertação, blog 2 `/cultura/`, EN como par de idioma). Vou direto ao diagnóstico WPML do post 26767.

> TOOL

tool_use Bash
id: toolu_01Fzc1r9ZC7kSqsmxE3Vo3EU
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/wpml-diag-galeria.php <<'PHP'\n<?php\n$post_id = 26767;\nswitch_to_blog(2);\n$post = get_post($post_id);\n$post_type = $post ? $post->post_type : null;\n\nglobal $wpdb;\n$result = [\n    'blog'             => 2,\n    'post_id'          => $post_id,\n    'post_type'        => $post_type,\n    'post_title'       => $post ? $post->post_title : null,\n    'post_status'      => $post ? $post->post_status : null,\n    'post_name'        => $post ? $post->post_name : null,\n    'is_translatable'  => $post_type ? apply_filters('wpml_is_translated_post_type', null, $post_type) : null,\n];\n\n$wpml_row = $wpdb->get_row($wpdb->prepare(\n    \"SELECT * FROM {$wpdb->prefix}icl_translations WHERE element_id = %d AND element_type LIKE 'post_%'\",\n    $post_id\n), ARRAY_A);\n$result['wpml'] = $wpml_row ?: ['status' => 'not_registered'];\n\n$translations = [];\nif ($wpml_row) {\n    $element_type = apply_filters('wpml_element_type', $post_type);\n    $trid = $wpml_row['trid'];\n    $tr = apply_filters('wpml_get_element_translations', [], $trid, $element_type);\n    foreach ($tr as $lang => $t) {\n        $tid = (int) $t->element_id;\n        $tp  = get_post($tid);\n        $translations[$lang] = [\n            'element_id'   => $tid,\n            'lang'         => $lang,\n            'source_lang'  => $t->source_language_code,\n            'status'       => $tp ? $tp->post_status : 'MISSING',\n            'title'        => $tp ? $tp->post_title : null,\n            'permalink'    => $tp ? get_permalink($tid) : null,\n            'has_elementor'=> (bool) get_post_meta($tid, '_elementor_data', true),\n            'elementor_len'=> strlen((string) get_post_meta($tid, '_elementor_data', true)),\n            'edit_mode'    => get_post_meta($tid, '_elementor_edit_mode', true),\n            'modified'     => $tp ? $tp->post_modified : null,\n        ];\n    }\n}\n$result['translations'] = $translations;\nrestore_current_blog();\necho json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);\nPHP\ndocker cp tmp/wpml-diag-galeria.php concertacao-dev-wordpress:/tmp/\necho \"=== DIAGNÓSTICO WPML — Galeria DEV (blog 2) ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp eval-file /tmp/wpml-diag-galeria.php --url=https://cambrasmax.local:8484/cultura/ […]

> TOOL

tool_result
id: toolu_01Fzc1r9ZC7kSqsmxE3Vo3EU
```
=== DIAGNÓSTICO WPML — Galeria DEV (blog 2) ===
{
    "blog": 2,
    "post_id": 26767,
    "post_type": "page",
    "post_title": "Galeria",
    "post_status": "publish",
    "post_name": "galeria",
    "is_translatable": true,
    "wpml": {
        "translation_id": "84",
        "element_type": "post_page",
        "element_id": "26767",
        "trid": "227584",
        "language_code": "pt-br",
        "source_language_code": null
    },
    "translations": {
        "en": {
            "element_id": 26999,
            "lang": "en",
            "source_lang": "pt-br",
            "status": "publish",
            "title": "Gallery",
            "permalink": "https:\/\/cambrasmax.local:8484\/cultura\/galeria\/",
            "has_elementor": true,
            "elementor_len": 28585,
            "edit_mode": "builder",
            "modified": "2026-05-13 10:27:07"
        },
        "pt-br": {
            "element_id": 26767,
            "lang": "pt-br",
            "source_lang": null,
            "status": "publish",
            "title": "Galeria",
            "permalink": "https:\/\/cambrasmax.local:8484\/cultura\/galeria\/",
            "has_elementor": true,
            "elementor_len": 28686,
            "edit_mode": "builder",
            "modified": "2026-05-13 10:27:06"
        }
    }
}
```

> AGENT

Diagnóstico WPML limpo:

```
╔══════════════════════════════════════════════════════════════════╗
║  Poliglota — Galeria (blog 2 /cultura/)  trid=227584             ║
╠══════════════════════════════════════════════════════════════════╣
║  Idioma  │ ID     │ trid    │ source │ status   │ elementor      ║
║  pt-br   │ 26767  │ 227584  │ (orig) │ publish  │ 28686 chars    ║
║  en      │ 26999  │ 227584  │ pt-br  │ publish  │ 28585 chars    ║
╠══════════════════════════════════════════════════════════════════╣
║  Issues: nenhuma — trid íntegro, ambos publish, ambos Elementor ║
╚══════════════════════════════════════════════════════════════════╝
```

WPML está perfeito em DEV: **PT=26767, EN=26999**, mesmo `trid`, ambos publicados, ambos com Elementor data. Os IDs em prod devem ser os mesmos (multisite mantém IDs).

Agora, antes de decidir a estratégia de deploy, preciso entender **o que efetivamente mudou** na página Galeria entre DEV e prod — porque o método de deploy depende disso. A página é do blog 2 (Cultura), e mudanças aqui podem envolver: estrutura Elementor, attachments cross-blog (NML), uploads novos, etc.

Vou comparar o estado de DEV vs prod para PT e EN.

> TOOL

tool_use Bash
id: toolu_01UNC7XxSMdCn2Sf1NsTMhwN
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\n# Script de fingerprint para comparar DEV vs PROD\ncat > tmp/galeria-fingerprint.php <<'PHP'\n<?php\nswitch_to_blog(2);\n$out = [];\nforeach ([26767 => 'PT', 26999 => 'EN'] as $id => $lang) {\n    $d = get_post_meta($id, '_elementor_data', true);\n    $p = get_post($id);\n    $out[$lang] = [\n        'id'            => $id,\n        'status'        => $p ? $p->post_status : 'MISSING',\n        'modified'      => $p ? $p->post_modified : null,\n        'elementor_len' => strlen((string)$d),\n        'elementor_md5' => $d ? md5($d) : null,\n        'page_settings' => md5((string)get_post_meta($id, '_elementor_page_settings', true)),\n    ];\n    // extrair IDs de attachments referenciados no elementor_data\n    preg_match_all('/\"id\":(\\d+)/', (string)$d, $m);\n    $ids = array_values(array_unique($m[1]));\n    sort($ids);\n    $out[$lang]['referenced_ids_count'] = count($ids);\n    $out[$lang]['referenced_ids'] = $ids;\n    // URLs de uploads referenciadas\n    preg_match_all('#/wp-content/uploads/[^\\s\"\\\\\\\\]+\\.(?:jpg|jpeg|png|webp|avif|gif|svg)#i', (string)$d, $u);\n    $out[$lang]['upload_urls_count'] = count(array_unique($u[0]));\n}\nrestore_current_blog();\necho json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);\nPHP\ndocker cp tmp/galeria-fingerprint.php concertacao-dev-wordpress:/tmp/\necho \"=== DEV ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp eval-file /tmp/galeria-fingerprint.php --url=https://cambrasmax.local:8484/cultura/ --path=/var/www/html 2>&1 | grep -vE \"Deprecated|Cores ativadas|[│╭╰├╮]|BIT BPO|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress|^\\s*$\" > tmp/galeria-dev-fp.json\ncat tmp/galeria-dev-fp.json\necho \"\"\necho \"=== PROD ===\"\nscp -q tmp/galeria-fingerprint.php concertacaoamazonia.com.br-prod-sa:/tmp/\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval-file /tmp/galeria-fingerprint.php 2>&1\" | grep -vE \"Deprecated\" > tmp/galeria-prod-fp.json\ncat tmp/galeria-prod-fp.json",
  "description": "Comparar fingerprint da Galeria DEV vs PROD"
}
```

> TOOL

tool_result
id: toolu_01UNC7XxSMdCn2Sf1NsTMhwN
```
=== DEV ===
Warning: Array to string conversion in phar:///usr/local/bin/wp/vendor/wp-cli/eval-command/src/EvalFile_Command.php(85) : eval()'d code on line 13
Warning: Array to string conversion in phar:///usr/local/bin/wp/vendor/wp-cli/eval-command/src/EvalFile_Command.php(85) : eval()'d code on line 13
{
    "PT": {
        "id": 26767,
        "status": "publish",
        "modified": "2026-05-13 10:27:06",
        "elementor_len": 28686,
        "elementor_md5": "36644a0101629c5991d4a5b7849862e3",
        "page_settings": "4410ec34d9e6c1a68100ca0ce033fb17",
        "referenced_ids_count": 13,
        "referenced_ids": [
            "17719",
            "17747",
            "17751",
            "28302",
            "45782",
            "92370",
            "92371",
            "92372",
            "92373",
            "92374",
            "92375",
            "92385",
            "92415"
        ],
        "upload_urls_count": 0
    },
    "EN": {
        "id": 26999,
        "status": "publish",
        "modified": "2026-05-13 10:27:07",
        "elementor_len": 28585,
        "elementor_md5": "ff982e41037ab62cbc0b2f9817120eea",
        "page_settings": "4410ec34d9e6c1a68100ca0ce033fb17",
        "referenced_ids_count": 13,
        "referenced_ids": [
            "17719",
            "17747",
            "17751",
            "28302",
            "45782",
            "92370",
            "92371",
            "92372",
            "92373",
            "92374",
            "92375",
            "92385",
            "92415"
        ],
        "upload_urls_count": 0
    }
}

=== PROD ===
Warning: Array to string conversion in phar:///usr/local/bin/wp/vendor/wp-cli/eval-command/src/EvalFile_Command.php(85) : eval()'d code on line 13
Warning: Array to string conversion in phar:///usr/local/bin/wp/vendor/wp-cli/eval-command/src/EvalFile_Command.php(85) : eval()'d code on line 13
{
    "PT": {
        "id": 26767,
        "status": "publish",
        "modified": "2026-05-13 10:27:06",
        "elementor_len": 28737,
        "elementor_md5": "b5abb8cfbb73dac0fe5c262d2ed56c4e",
        "page_settings": "4410ec34d9e6c1a68100ca0ce033fb17",
        "referenced_ids_count": 13,
        "referenced_ids": [
            "17719",
            "17747",
            "17751",
            "28302",
            "45782",
            "92370",
            "92371",
            "92372",
            "92373",
            "92374",
            "92375",
            "92385",
            "92415"
        ],
        "upload_urls_count": 0
    },
    "EN": {
        "id": 26999,
        "status": "publish",
        "modified": "2026-05-13 10:27:07",
        "elementor_len": 28636,
        "elementor_md5": "6e13294cc318560d7d99b4da0119e23c",
        "page_settings": "4410ec34d9e6c1a68100ca0ce033fb17",
        "referenced_ids_count": 13,
        "referenced_ids": [
            "17719",
            "17747",
            "17751",
            "28302",
            "45782",
            "92370",
            "92371",
            "92372", […]

> AGENT

Comparação muito esclarecedora:

| | DEV | PROD | Igual? |
|---|---|---|---|
| **PT (26767)** modified | 2026-05-13 10:27:06 | 2026-05-13 10:27:06 | ✅ mesma data |
| **PT** elementor_md5 | `36644a01...` | `b5abb8cf...` | ❌ **diferente** |
| **PT** elementor_len | 28686 | 28737 (−51 em dev) | diferente |
| **EN (26999)** modified | 2026-05-13 10:27:07 | 2026-05-13 10:27:07 | ✅ mesma data |
| **EN** elementor_md5 | `ff982e41...` | `6e13294c...` | ❌ **diferente** |
| **referenced_ids** (13) | mesmos 13 IDs | mesmos 13 IDs | ✅ **idênticos** |
| **page_settings** | `4410ec34...` | `4410ec34...` | ✅ idêntico |

Pontos críticos:
1. **As datas de modificação são idênticas** (10:27:06/07) — mas os MD5 diferem. Isso é o padrão clássico de **tunnel/URL drift**: o conteúdo é o mesmo, mas as URLs internas diferem (`cambrasmax.local:8484` em dev vs `concertacaoamazonia.com.br` em prod). A diferença de tamanho (~51 chars) é consistente com a diferença de comprimento entre os dois hostnames.
2. **Os 13 attachment IDs referenciados são EXATAMENTE os mesmos** em DEV e prod — ou seja, **nenhum upload novo** foi adicionado. As imagens da galeria já existem em prod.

Isso é importantíssimo: significa que **você pode não ter feito nenhuma […]

> TOOL

tool_use Bash
id: toolu_0158AMfrzaQfypYoNuebyuxn
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\n# Exportar _elementor_data cru de DEV e PROD para diff normalizado\ncat > tmp/galeria-export.php <<'PHP'\n<?php\nswitch_to_blog(2);\n$which = getenv('WHICH'); // 'dev' ou 'prod'\nforeach ([26767 => 'PT', 26999 => 'EN'] as $id => $lang) {\n    $d = get_post_meta($id, '_elementor_data', true);\n    file_put_contents(\"/tmp/galeria_{$which}_{$lang}.json\", $d);\n}\nrestore_current_blog();\necho \"exportado $which\\n\";\nPHP\ndocker cp tmp/galeria-export.php concertacao-dev-wordpress:/tmp/\ndocker exec -u www-data -e WHICH=dev concertacao-dev-wordpress wp eval-file /tmp/galeria-export.php --url=https://cambrasmax.local:8484/cultura/ --path=/var/www/html 2>&1 | grep exportado\ndocker cp concertacao-dev-wordpress:/tmp/galeria_dev_PT.json tmp/\ndocker cp concertacao-dev-wordpress:/tmp/galeria_dev_EN.json tmp/\n\nscp -q tmp/galeria-export.php concertacaoamazonia.com.br-prod-sa:/tmp/\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data WICH=prod; WHICH=prod wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval 'putenv(\\\"WHICH=prod\\\"); switch_to_blog(2); foreach ([26767=>\\\"PT\\\",26999=>\\\"EN\\\"] as \\$id=>\\$lang){ file_put_contents(\\\"/tmp/galeria_prod_\\$lang.json\\\", get_post_meta(\\$id,\\\"_elementor_data\\\",true)); } restore_current_blog(); echo \\\"ok\\\";' 2>&1\" | grep -vE \"Deprecated\"\nscp -q concertacaoamazonia.com.br-prod-sa:/tmp/galeria_prod_PT.json tmp/\nscp -q concertacaoamazonia.com.br-prod-sa:/tmp/galeria_prod_EN.json tmp/\n\necho \"\"\necho \"=== DIFF NORMALIZADO (URLs unificadas) PT: dev vs prod ===\"\npython3 - <<'PY'\nimport re,json\ndef norm(p):\n    s=open(p).read()\n    # normalizar hostnames\n    s=s.replace('cambrasmax.local:8484','HOST').replace('concertacao.bureau-it.com','HOST').replace('concertacaoamazonia.com.br','HOST')\n    s=s.replace('https:\\\\/\\\\/HOST','HOST').replace('http:\\\\/\\\\/HOST','HOST')\n    return s\nfor lang in ['PT','EN']:\n    a=norm(f'tmp/galeria_dev_{lang}.json')\n    b=norm(f'tmp/galeria_prod_{lang}.json')\n    print(f\"[{lang}] após normalizar URLs: dev=={'PROD' if a==b else 'DIFERENTE de prod'}  (len dev={len(a)} prod={len(b)})\")\n    if a!=b:\n        # achar primeiras diferenças\n        import difflib\n        sa=re.split(r'(?<=,)',a); sb=re.split(r'(?<=,)',b)\n        diff=[d for d in difflib.unified_diff(sb,sa,lineterm='',n=0) if d and d[0] in '+-' and not d.startswith('++') and not d.startswith('--')]\n        for d in diff[:20]:\n            print('   ',d[:200])\nPY",
  "description": "Diff normalizado do elementor_data Galeria dev vs prod"
}
```

> TOOL

tool_result ERROR
id: toolu_0158AMfrzaQfypYoNuebyuxn
```
Exit code 1
exportado dev
usage: sudo -h | -K | -k | -V
usage: sudo -v [-ABkNnS] [-g group] [-h host] [-p prompt] [-u user]
usage: sudo -l [-ABkNnS] [-g group] [-h host] [-p prompt] [-U user]
            [-u user] [command [arg ...]]
usage: sudo [-ABbEHkNnPS] [-r role] [-t type] [-C num] [-D directory]
            [-g group] [-h host] [-p prompt] [-R directory] [-T timeout]
            [-u user] [VAR=value] [-i | -s] [command [arg ...]]
usage: sudo -e [-ABkNnS] [-r role] [-t type] [-C num] [-D directory]
            [-g group] [-h host] [-p prompt] [-R directory] [-T timeout]
            [-u user] file ...
PHP Warning:  file_get_contents(/var/www/concertacaoamazonia.com.br/wp-config.php): Failed to open stream: Permission denied in phar:///usr/local/bin/wp/vendor/wp-cli/wp-cli/php/WP_CLI/Runner.php on line 755
Error: Strange wp-config.php file: wp-settings.php is not loaded directly.
scp: /tmp/galeria_prod_PT.json: No such file or directory
scp: /tmp/galeria_prod_EN.json: No such file or directory

=== DIFF NORMALIZADO (URLs unificadas) PT: dev vs prod ===
Traceback (most recent call last):
  File "<stdin>", line 10, in <module>
  File "<stdin>", line 3, in norm
FileNotFoundError: [Errno 2] No such file or directory: 'tmp/galeria_prod_PT.json'
```

> AGENT

Erro de quoting no comando SSH — o `sudo -u www-data WICH=prod;` quebrou. Vou usar o eval-file que já está em prod (mais limpo).

> TOOL

tool_use Bash
id: toolu_01NaVk7YifbVfyzerpUxwgYq
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\n# usar eval-file (já copiado) com env preservado via sudo env\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data env WHICH=prod wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval-file /tmp/galeria-export.php 2>&1\" | grep -vE \"Deprecated\"\nscp -q concertacaoamazonia.com.br-prod-sa:/tmp/galeria_prod_PT.json tmp/\nscp -q concertacaoamazonia.com.br-prod-sa:/tmp/galeria_prod_EN.json tmp/\nls -la tmp/galeria_prod_*.json",
  "description": "Exportar elementor_data de prod via eval-file"
}
```

> TOOL

tool_result
id: toolu_01NaVk7YifbVfyzerpUxwgYq
```
exportado prod
-rw-r--r--@ 1 dcambria  staff  28636  5 jun 18:57 tmp/galeria_prod_EN.json
-rw-r--r--@ 1 dcambria  staff  28737  5 jun 18:57 tmp/galeria_prod_PT.json
```

> TOOL

tool_use Bash
id: toolu_01XEUiUZ1FZgUS1ff7Hd5onc
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\npython3 - <<'PY'\nimport re,difflib\ndef norm(p):\n    s=open(p).read()\n    for h in ['cambrasmax.local:8484','concertacao.bureau-it.com','concertacaoamazonia.com.br']:\n        s=s.replace('https:\\\\/\\\\/'+h,'HOST').replace('http:\\\\/\\\\/'+h,'HOST').replace(h,'HOST')\n    return s\nfor lang in ['PT','EN']:\n    a=norm(f'tmp/galeria_dev_{lang}.json')\n    b=norm(f'tmp/galeria_prod_{lang}.json')\n    same = a==b\n    print(f\"\\n========== [{lang}] dev {'==' if same else '!='} prod  (len dev={len(a)} prod={len(b)}) ==========\")\n    if not same:\n        # split por vírgula para granularidade\n        sa=[x for x in re.split(r'(?<=,)',a)]\n        sb=[x for x in re.split(r'(?<=,)',b)]\n        diff=list(difflib.unified_diff(sb,sa,fromfile='PROD',tofile='DEV',lineterm='',n=0))\n        shown=0\n        for d in diff:\n            if d.startswith('@@') or (d and d[0] in '+-' and not d.startswith('+++') and not d.startswith('---')):\n                print('  ',d[:260])\n                shown+=1\n                if shown>40: print('   ... (truncado)'); break\nPY",
  "description": "Diff normalizado final dev vs prod"
}
```

> TOOL

tool_result
id: toolu_01XEUiUZ1FZgUS1ff7Hd5onc
```
========== [PT] dev != prod  (len dev=27105 prod=27105) ==========
   @@ -794 +794 @@
   -"toggle_label_typography_font_family":"Barlow",
   +"toggle_label_typography_font_family":"Roboto",

========== [EN] dev != prod  (len dev=27004 prod=27004) ==========
   @@ -796 +796 @@
   -"toggle_label_typography_font_family":"Barlow",
   +"toggle_label_typography_font_family":"Roboto",
```

> AGENT

Diagnóstico decisivo. Após normalizar as URLs, a **única diferença** entre DEV e prod é uma:

```
PROD: "toggle_label_typography_font_family":"Barlow"
DEV:  "toggle_label_typography_font_family":"Roboto"
```

Em ambos PT e EN, em apenas **uma linha** cada. Não há nenhuma outra mudança estrutural, nenhum widget novo, nenhum upload novo, nenhuma diferença de conteúdo. A sua alteração na Galeria em DEV foi trocar a **fonte de um label de toggle de "Barlow" para "Roboto"**.

Isso muda completamente a estratégia. Não preciso de share deploy, nem migração de attachments, nem nada pesado. É uma mudança **cirúrgica de uma única propriedade tipográfica** em 2 posts (PT 26767 + EN 26999), blog 2.

Deixa eu confirmar o contexto dessa mudança — quantas ocorrências de "Barlow" existem em cada (para garantir que troco só o que deve) e onde fica esse toggle.

> TOOL

tool_use Bash
id: toolu_016RDQn35CqRwdDW6kQaVyaJ
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\npython3 - <<'PY'\nimport re\nfor env in ['dev','prod']:\n    for lang in ['PT','EN']:\n        s=open(f'tmp/galeria_{env}_{lang}.json').read()\n        barlow=s.count('\"toggle_label_typography_font_family\":\"Barlow\"')\n        roboto=s.count('\"toggle_label_typography_font_family\":\"Roboto\"')\n        any_barlow=s.count('Barlow')\n        any_roboto=s.count('Roboto')\n        print(f\"{env.upper()} {lang}: toggle_label Barlow={barlow} Roboto={roboto} | total 'Barlow'={any_barlow} total 'Roboto'={any_roboto}\")\nPY",
  "description": "Contar ocorrências de Barlow/Roboto no toggle"
}
```

> TOOL

tool_result
id: toolu_016RDQn35CqRwdDW6kQaVyaJ
```
DEV PT: toggle_label Barlow=0 Roboto=1 | total 'Barlow'=0 total 'Roboto'=3
DEV EN: toggle_label Barlow=0 Roboto=1 | total 'Barlow'=0 total 'Roboto'=3
PROD PT: toggle_label Barlow=1 Roboto=0 | total 'Barlow'=1 total 'Roboto'=2
PROD EN: toggle_label Barlow=1 Roboto=0 | total 'Barlow'=1 total 'Roboto'=2
```

> AGENT

Confirmado com total clareza:

- **DEV:** `toggle_label_typography_font_family` = **Roboto** (1×), e "Barlow" não existe mais (0×). Já há 3 ocorrências de "Roboto".
- **PROD:** `toggle_label_typography_font_family` = **Barlow** (1×), com 2 "Roboto" em outros lugares.

A sua mudança foi: **trocar a fonte do label do toggle de "Barlow" → "Roboto"** num único widget, em PT e EN. Em prod, há exatamente **1 ocorrência de `Barlow`** em cada post para trocar.

Isso bate, inclusive, com uma correção conhecida do projeto (remoção de fontes Barlow órfãs — há um `pre-barlow-removal` nos uploads). A estratégia de deploy é simples e cirúrgica: trocar `"toggle_label_typography_font_family":"Barlow"` → `"...":"Roboto"` no `_elementor_data` de prod nos posts 26767 (PT) e 26999 (EN), blog 2.

Vou apresentar o diagnóstico e o plano de deploy.

---

## Diagnóstico — Galeria (blog 2 /cultura/)

**O que mudou em DEV vs PROD** (após normalizar URLs de tunnel):

| Item | Resultado |
|------|-----------|
| Estrutura Elementor | ✅ idêntica (sem widgets novos/removidos) |
| 13 attachment IDs referenciados | ✅ idênticos — **nenhum upload novo** |
| page_settings | ✅ idêntico |
| **Única diferença** | `toggle_label_typography_font_family`: **Barlow** (prod) → **Roboto** (dev) |

Presente em **1 widget**, nos **2 posts**: PT 26767 + EN […]

> TOOL

tool_use AskUserQuestion
id: toolu_011u9MUAJ6fieXbgCXM7w9mh
```json
{
  "questions": [
    {
      "question": "Confirmei que a única alteração na Galeria foi a fonte do label do toggle (Barlow→Roboto), em PT e EN. Aplico esse deploy cirúrgico em prod?",
      "header": "Deploy Galeria",
      "multiSelect": false,
      "options": [
        {
          "label": "Sim, deploy cirúrgico",
          "description": "Troca 'toggle_label_typography_font_family' de Barlow→Roboto no _elementor_data de prod (posts 26767 PT + 26999 EN, blog 2), com backup, regen Elementor CSS, reload php-fpm e invalidação cirúrgica WP Rocket+CloudFront de /cultura/galeria/."
        },
        {
          "label": "Não — fiz mais mudanças",
          "description": "A mudança da fonte não foi a única coisa que alterei. Vou descrever o que mais mudou (ou pedir um share deploy completo da página)."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_011u9MUAJ6fieXbgCXM7w9mh
```
Your questions have been answered: "Confirmei que a única alteração na Galeria foi a fonte do label do toggle (Barlow→Roboto), em PT e EN. Aplico esse deploy cirúrgico em prod?"="pod fazer deploy cirurgico e perceba que alteramos o nome do Miguel Penha". You can now continue with these answers in mind.
```

> AGENT

Você confirmou o deploy cirúrgico **e** apontou algo importante: também alteraram **o nome do "Miguel Penha"**. Mas o meu diff só detectou a mudança Barlow→Roboto — o que significa que a mudança no nome do Miguel Penha **não está no `_elementor_data` da página Galeria**. Provavelmente está em um **attachment** (título/legenda da imagem na galeria via Network Media Library) ou em um post/CPT separado.

Preciso localizar onde está "Miguel Penha" antes de fazer o deploy, porque deployar só o `_elementor_data` deixaria essa correção de fora. Deixa eu investigar em DEV.

> TOOL

tool_use Bash
id: toolu_012r15RUYHkYrCYgHGUyvqiV
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/find-miguel.php <<'PHP'\n<?php\nglobal $wpdb;\n$results = [];\n\n// Buscar \"Miguel Penha\" e variações em ambos os blogs, em posts (título, conteúdo, excerpt) e postmeta\n$patterns = ['%Miguel Penha%', '%Miguel%Penha%'];\n\nforeach ([1, 2] as $blog) {\n    switch_to_blog($blog);\n    $prefix = $wpdb->get_blog_prefix($blog);\n\n    // posts: title, content, excerpt\n    foreach (['post_title','post_content','post_excerpt'] as $col) {\n        $rows = $wpdb->get_results($wpdb->prepare(\n            \"SELECT ID, post_type, post_status, post_title FROM {$prefix}posts WHERE $col LIKE %s LIMIT 30\",\n            '%Miguel Penha%'\n        ), ARRAY_A);\n        foreach ($rows as $r) {\n            $results[] = ['blog'=>$blog,'where'=>\"posts.$col\",'id'=>$r['ID'],'type'=>$r['post_type'],'status'=>$r['post_status'],'title'=>$r['post_title']];\n        }\n    }\n    // postmeta\n    $metas = $wpdb->get_results($wpdb->prepare(\n        \"SELECT post_id, meta_key, LEFT(meta_value,120) AS snippet FROM {$prefix}postmeta WHERE meta_value LIKE %s LIMIT 30\",\n        '%Miguel Penha%'\n    ), ARRAY_A);\n    foreach ($metas as $m) {\n        $p = get_post($m['post_id']);\n        $results[] = ['blog'=>$blog,'where'=>\"postmeta.{$m['meta_key']}\",'id'=>$m['post_id'],'type'=>$p?$p->post_type:'?','status'=>$p?$p->post_status:'?','snippet'=>$m['snippet']];\n    }\n    restore_current_blog();\n}\necho json_encode($results, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);\nPHP\ndocker cp tmp/find-miguel.php concertacao-dev-wordpress:/tmp/\necho \"=== DEV: onde está 'Miguel Penha'? ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp eval-file /tmp/find-miguel.php --path=/var/www/html 2>&1 | grep -vE \"Deprecated|Cores ativadas|[│╭╰├╮]|BIT BPO|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress|^\\s*$\"",
  "description": "Localizar Miguel Penha em DEV"
}
```

> TOOL

tool_result
id: toolu_012r15RUYHkYrCYgHGUyvqiV
```
=== DEV: onde está 'Miguel Penha'? ===
[
    {
        "blog": 1,
        "where": "posts.post_content",
        "id": "91418",
        "type": "plenarias",
        "status": "publish",
        "title": "Prioridades para as Amazônias"
    },
    {
        "blog": 1,
        "where": "posts.post_content",
        "id": "91428",
        "type": "revision",
        "status": "inherit",
        "title": "Prioridades para as Amazônias"
    },
    {
        "blog": 1,
        "where": "posts.post_excerpt",
        "id": "89977",
        "type": "attachment",
        "status": "inherit",
        "title": "A floresta e seus mistérios, óleo sobre tela 110x300 cm 2024, fotografo Taiguara Luciano Grande"
    },
    {
        "blog": 1,
        "where": "posts.post_excerpt",
        "id": "89978",
        "type": "attachment",
        "status": "inherit",
        "title": "Cipó Mariri, óleo sobre tela 150 x 100 cm 2013, fotografo. Taiguara Luciano Grande"
    },
    {
        "blog": 1,
        "where": "posts.post_excerpt",
        "id": "89979",
        "type": "attachment",
        "status": "inherit",
        "title": "Igarapé, acrílica sobre tela 2x6m 2019, fotografo, Nailana Thiely Grande"
    },
    {
        "blog": 1,
        "where": "posts.post_excerpt",
        "id": "89980",
        "type": "attachment",
        "status": "inherit",
        "title": "palmeira acurí na beira do rio, óleo sobre tela 30x40 cm 2024, Foto, Taiguara Luciano Grande"
    },
    {
        "blog": 1,
        "where": "posts.post_excerpt",
        "id": "89981",
        "type": "attachment",
        "status": "inherit",
        "title": "palmeira babaçu, óleo sobre tela 60x45 cm 2024,fotografo, Taiguara Luciano Grande"
    },
    {
        "blog": 1,
        "where": "posts.post_excerpt",
        "id": "89982",
        "type": "attachment",
        "status": "inherit",
        "title": "palmeira buritirana, óleo sobre tela 60x45 cm 2024, fotografo Taiguara Luciano […]

> AGENT

Agora entendo o quadro completo. "Miguel Penha" foi alterado para **"Miguel Penha Chiquitano"** (acréscimo do sobrenome "Chiquitano"). Isso aparece em **vários** posts do blog 2, não na página Galeria em si. Os posts publicados (não-revisão) afetados em DEV são:

**Blog 2 (Cultura) — posts publicados com "Miguel Penha Chiquitano":**
| ID | Tipo | Título |
|----|------|--------|
| 86792 | `artistas` (CPT) | Miguel Penha Chiquitano |
| 92811 | `artistas` (CPT) | Miguel Penha Chiquitano |
| 89378 | `linha-das-artes` | Miguel Penha Chiquitano não pinta a paisagem... (PT) |
| 89451 | `linha-das-artes` | Miguel Penha Chiquitano does not paint... (EN) |
| 90325 | `elementor_library` | Galeria#21 Miguel Penha Chiquitano |

As **revisões** mostram o título antigo ("Miguel Penha" sem Chiquitano) → confirma que a mudança foi **adicionar "Chiquitano"**.

Isto é bem mais do que a página Galeria. O CPT `artistas` é justamente o que alimenta a galeria via JetEngine/listing. Há inclusive uma skill dedicada (`sync-cpt-totem`) e o padrão de sync de CPT. 

Mas espere — preciso entender o escopo real. Você pediu deploy da **página Galeria**. A mudança "Miguel Penha → Miguel Penha Chiquitano" está espalhada por CPTs `artistas`, `linha-das-artes` e um `elementor_library` (template Galeria#21). Preciso […]

> TOOL

tool_use Bash
id: toolu_011A1GdnkMuLEvcjXwq72g8G
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/check-miguel-prod.php <<'PHP'\n<?php\nswitch_to_blog(2);\n$ids = [86792, 92811, 89378, 89451, 90325, 26767, 26999];\n$out = [];\nforeach ($ids as $id) {\n    $p = get_post($id);\n    if (!$p) { $out[$id] = ['MISSING']; continue; }\n    $content = $p->post_content;\n    $data = get_post_meta($id, '_elementor_data', true);\n    $out[$id] = [\n        'type'              => $p->post_type,\n        'status'            => $p->post_status,\n        'title'             => $p->post_title,\n        'has_chiquitano_title'   => strpos($p->post_title, 'Chiquitano') !== false,\n        'content_has_miguel'     => substr_count($content, 'Miguel Penha'),\n        'content_has_chiquitano' => substr_count($content, 'Miguel Penha Chiquitano'),\n        'elementor_has_miguel'      => substr_count((string)$data, 'Miguel Penha'),\n        'elementor_has_chiquitano'  => substr_count((string)$data, 'Miguel Penha Chiquitano'),\n        'modified'          => $p->post_modified,\n    ];\n}\nrestore_current_blog();\necho json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);\nPHP\necho \"=== DEV ===\"\ndocker cp tmp/check-miguel-prod.php concertacao-dev-wordpress:/tmp/\ndocker exec -u www-data concertacao-dev-wordpress wp eval-file /tmp/check-miguel-prod.php --url=https://cambrasmax.local:8484/cultura/ --path=/var/www/html 2>&1 | grep -vE \"Deprecated|Cores ativadas|[│╭╰├╮]|BIT BPO|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress|^\\s*$\"\necho \"\"\necho \"=== PROD ===\"\nscp -q tmp/check-miguel-prod.php concertacaoamazonia.com.br-prod-sa:/tmp/\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval-file /tmp/check-miguel-prod.php 2>&1\" | grep -vE \"Deprecated\"",
  "description": "Comparar estado dos posts Miguel Penha em dev vs prod"
}
```

> TOOL

tool_result
id: toolu_011A1GdnkMuLEvcjXwq72g8G
```
=== DEV ===
{
    "86792": {
        "type": "artistas",
        "status": "publish",
        "title": "Miguel Penha Chiquitano",
        "has_chiquitano_title": true,
        "content_has_miguel": 1,
        "content_has_chiquitano": 1,
        "elementor_has_miguel": 0,
        "elementor_has_chiquitano": 0,
        "modified": "2026-05-28 15:54:15"
    },
    "92811": {
        "type": "artistas",
        "status": "publish",
        "title": "Miguel Penha Chiquitano",
        "has_chiquitano_title": true,
        "content_has_miguel": 1,
        "content_has_chiquitano": 1,
        "elementor_has_miguel": 0,
        "elementor_has_chiquitano": 0,
        "modified": "2026-05-29 16:26:30"
    },
    "89378": {
        "type": "linha-das-artes",
        "status": "publish",
        "title": "Miguel Penha Chiquitano não pinta a paisagem, mas a sensação de estar na floresta",
        "has_chiquitano_title": true,
        "content_has_miguel": 2,
        "content_has_chiquitano": 2,
        "elementor_has_miguel": 0,
        "elementor_has_chiquitano": 0,
        "modified": "2026-03-19 11:42:37"
    },
    "89451": {
        "type": "linha-das-artes",
        "status": "publish",
        "title": "Miguel Penha Chiquitano does not paint landscapes, but the feeling of being in the forest",
        "has_chiquitano_title": true,
        "content_has_miguel": 2,
        "content_has_chiquitano": 2,
        "elementor_has_miguel": 0,
        "elementor_has_chiquitano": 0,
        "modified": "2026-03-19 12:10:08"
    },
    "90325": {
        "type": "elementor_library",
        "status": "publish",
        "title": "Galeria#21 Miguel Penha Chiquitano",
        "has_chiquitano_title": true,
        "content_has_miguel": 12,
        "content_has_chiquitano": 1,
        "elementor_has_miguel": 1,
        "elementor_has_chiquitano": 1,
        "modified": "2026-05-21 11:43:14"
    },
    "26767": {
        "type": "page",
        "status": "publish",
        "title": "Galeria",
        "has_chiquitano_title": false,
        "content_has_miguel": 1,
        "content_has_chiquitano": 1,
        "elementor_has_miguel": 1,
        "elementor_has_chiquitano": 1,
        "modified": "2026-05-13 10:27:06"
    },
    "26999": {
        "type": "page",
        "status": "publish",
        "title": "Gallery",
        "has_chiquitano_title": false,
        "content_has_miguel": 1,
        "content_has_chiquitano": 1,
        "elementor_has_miguel": 1,
        "elementor_has_chiquitano": 1,
        "modified": "2026-05-13 10:27:07"
    }
}

=== PROD === […]

> AGENT

Comparação DEV vs PROD esclarece exatamente o que falta deployar. Atenção a um detalhe crítico de ID:

| ID | DEV | PROD | Ação |
|----|-----|------|------|
| **86792** `artistas` | "Miguel Penha Chiquitano" | "Miguel Penha Chiquitano" | ✅ **já igual** |
| **92811** `artistas` | "Miguel Penha Chiquitano" | **"Rafael Matheus Moreira"** ⚠️ | **ID divergente** — não é o mesmo artista! |
| **89378** `linha-das-artes` PT | Chiquitano | Chiquitano | ✅ já igual |
| **89451** `linha-das-artes` EN | Chiquitano | Chiquitano | ✅ já igual |
| **90325** `elementor_library` (Galeria#21) | "Galeria#21 Miguel Penha **Chiquitano**" | "Galeria#21 Miguel Penha" ❌ | **PRECISA deploy** |
| **26767** Galeria PT | Chiquitano | Chiquitano | ✅ já igual |
| **26999** Gallery EN | Chiquitano | Chiquitano | ✅ já igual |

**Conclusões:**
1. O ID **92811** é um artista **diferente** em prod (Rafael Matheus Moreira) vs dev (Miguel Penha Chiquitano) — os CPTs `artistas` têm IDs que **não correspondem** entre dev e prod. Não posso tratar artistas por ID. Mas o artista 86792 ("Miguel Penha Chiquitano") já está correto em prod, então o CPT do artista já foi atualizado.
2. O **único post que realmente precisa […]

> TOOL

tool_use Bash
id: toolu_015QqzKysab3stLTLs6miaiR
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/inspect-90325.php <<'PHP'\n<?php\nswitch_to_blog(2);\n$id = 90325;\n$p = get_post($id);\n$data = get_post_meta($id, '_elementor_data', true);\necho \"TÍTULO: \" . $p->post_title . \"\\n\";\necho \"post_name: \" . $p->post_name . \"\\n\\n\";\n// Contexto das ocorrências de \"Miguel Penha\" no _elementor_data\necho \"=== _elementor_data: ocorrências de 'Miguel Penha' ===\\n\";\n$pos = 0;\nwhile (($pos = strpos($data, 'Miguel Penha', $pos)) !== false) {\n    echo \"...\" . substr($data, max(0,$pos-50), 130) . \"...\\n\\n\";\n    $pos += 12;\n}\n// \"Chiquitano\" sozinho\necho \"Ocorrências 'Chiquitano' no elementor_data: \" . substr_count($data, 'Chiquitano') . \"\\n\";\necho \"Ocorrências 'Miguel Penha' (total) no elementor_data: \" . substr_count($data, 'Miguel Penha') . \"\\n\";\necho \"Ocorrências 'Miguel Penha Chiquitano' no elementor_data: \" . substr_count($data, 'Miguel Penha Chiquitano') . \"\\n\";\n\n// no post_content (12 'Miguel Penha')\necho \"\\n=== post_content: ocorrências de 'Miguel Penha' (total=\" . substr_count($p->post_content, 'Miguel Penha') . \", chiquitano=\" . substr_count($p->post_content, 'Miguel Penha Chiquitano') . \") ===\\n\";\n$c = $p->post_content; $pos=0; $n=0;\nwhile (($pos = strpos($c, 'Miguel Penha', $pos)) !== false && $n < 15) {\n    echo \"...\" . substr($c, max(0,$pos-30), 90) . \"...\\n\";\n    $pos += 12; $n++;\n}\n\n// É traduzido via WPML? (elementor_library)\n$el_type = apply_filters('wpml_element_type', 'elementor_library');\nglobal $wpdb;\n$row = $wpdb->get_row($wpdb->prepare(\"SELECT trid, language_code, source_language_code FROM {$wpdb->prefix}icl_translations WHERE element_id=%d AND element_type=%s\", $id, $el_type), ARRAY_A);\necho \"\\nWPML: \" . json_encode($row) . \"\\n\";\nif ($row) {\n    $tr = apply_filters('wpml_get_element_translations', [], $row['trid'], […]

> TOOL

tool_result
id: toolu_015QqzKysab3stLTLs6miaiR
```
TÍTULO: Galeria#21 Miguel Penha Chiquitano
post_name: galeria21-miguel-penha
=== _elementor_data: ocorrências de 'Miguel Penha' ===
...:"6cb341f","elType":"widget","settings":{"title":"Miguel Penha Chiquitano","__globals__":{"typography_typography":"globals\/typogr...
Ocorrências 'Chiquitano' no elementor_data: 1
Ocorrências 'Miguel Penha' (total) no elementor_data: 1
Ocorrências 'Miguel Penha Chiquitano' no elementor_data: 1
=== post_content: ocorrências de 'Miguel Penha' (total=12, chiquitano=1) ===
...<h2>Miguel Penha Chiquitano</h2>							
									<a role="button" tabindex="0" data-galler...
...A floresta e seus mistérios. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...ion="Arte 7 – Cipó Mariri. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...ription="Arte 5 – Igarapé. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...meira acurí na beira do rio. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
..."Arte 6 – Palmeira babaçu. Miguel Penha." data-e-action-hash="#elementor-action%3Aactio...
...rte 3– Palmeira buritirana. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...e 10 – Rainha das árvores. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...cription="Arte 2– Samaúma. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...ription="Arte 9 – Sapopema. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...Arte 4 – Tronco de jatobá. Miguel Penha" data-e-action-hash="#elementor-action%3Aaction...
...A floresta e seus mistérios. Miguel Penha." data-e-action-hash="#elementor-action%3Aactio...
WPML: {"trid":"2138568","language_code":"pt-br","source_language_code":null}
  pt-br => id 90325 (Galeria#21 Miguel Penha Chiquitano)
```

> AGENT

Agora tenho clareza total sobre o template 90325. Observações importantes:

1. **No `_elementor_data` de DEV:** só **1 ocorrência** de "Miguel Penha", já como "Miguel Penha Chiquitano" — é o **título do widget** (`"title":"Miguel Penha Chiquitano"`). Essa é a mudança real que precisa ir pra prod.

2. **No `post_content`:** há 12 "Miguel Penha", mas só o `<h2>` virou "Chiquitano". As outras 11 são **legendas das obras** ("A floresta e seus mistérios. Miguel Penha", "Cipó Mariri. Miguel Penha", etc.) — essas **não** foram alteradas (continuam "Miguel Penha" sem Chiquitano). Importante: o `post_content` de um `elementor_library` é **gerado** a partir do `_elementor_data` no save — então o que importa é o `_elementor_data` (o título do widget) + regenerar. As legendas vêm dos `post_excerpt` dos attachments, que já analisamos.

3. **WPML:** o template 90325 **só tem PT-BR** (`source_language_code: null`, sem tradução EN no trid 2138568). É um template Elementor singular, servido para ambos idiomas (ou tem outro mecanismo). Não há par EN para sincronizar — bom.

Mas espere: o `post_content` de prod tem **12 "Miguel Penha" e 0 "Chiquitano"**, enquanto o `_elementor_data` de prod tem 1 "Miguel Penha" e 0 "Chiquitano". Então em prod o widget title ainda é "Miguel Penha" (sem Chiquitano). Preciso […]

> TOOL

tool_use Bash
id: toolu_014Hm8ZVLk3Ex6rLtXvJ52wd
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/inspect-90325-prod.php <<'PHP'\n<?php\nswitch_to_blog(2);\n$id = 90325;\n$p = get_post($id);\n$data = get_post_meta($id, '_elementor_data', true);\necho \"TÍTULO PROD: \" . $p->post_title . \"\\n\";\necho \"=== _elementor_data PROD: contexto 'Miguel Penha' ===\\n\";\n$pos = 0;\nwhile (($pos = strpos($data, 'Miguel Penha', $pos)) !== false) {\n    echo \"...\" . substr($data, max(0,$pos-50), 130) . \"...\\n\";\n    $pos += 12;\n}\necho \"\\nwidget title 'Miguel Penha' (exato, sem Chiquitano): \" . substr_count($data, '\"title\":\"Miguel Penha\"') . \"\\n\";\necho \"widget title 'Miguel Penha Chiquitano': \" . substr_count($data, '\"title\":\"Miguel Penha Chiquitano\"') . \"\\n\";\necho \"post_name: \" . $p->post_name . \"\\n\";\necho \"modified: \" . $p->post_modified . \"\\n\";\nrestore_current_blog();\nPHP\nscp -q tmp/inspect-90325-prod.php concertacaoamazonia.com.br-prod-sa:/tmp/\necho \"=== PROD: template 90325 ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval-file /tmp/inspect-90325-prod.php 2>&1\" | grep -vE \"Deprecated\"",
  "description": "Inspecionar template 90325 em PROD"
}
```

> TOOL

tool_result
id: toolu_014Hm8ZVLk3Ex6rLtXvJ52wd
```
=== PROD: template 90325 ===
TÍTULO PROD: Galeria#21 Miguel Penha
=== _elementor_data PROD: contexto 'Miguel Penha' ===
...:"6cb341f","elType":"widget","settings":{"title":"Miguel Penha","__globals__":{"typography_typography":"globals\/typography?id=pri...

widget title 'Miguel Penha' (exato, sem Chiquitano): 1
widget title 'Miguel Penha Chiquitano': 0
post_name: galeria21-miguel-penha
modified: 2026-04-08 15:38:52
```

> AGENT

Confirmado em prod com precisão cirúrgica. O template 90325 em prod:
- Widget `6cb341f` tem `"title":"Miguel Penha"` (sem Chiquitano) — **1 ocorrência exata**.
- Título do post: "Galeria#21 Miguel Penha".

Agora tenho o escopo completo e exato do deploy. Deixa eu registrar as tasks e apresentar o plano consolidado.

## Resumo do escopo real do deploy

Após diagnóstico WPML + diff dev/prod, o deploy "página Galeria" na verdade envolve **3 alterações cirúrgicas** no blog 2:

| # | Alteração | Posts (PT/EN) | Estado prod |
|---|-----------|---------------|-------------|
| **A** | Fonte do toggle label: `Barlow → Roboto` | 26767 (PT) + 26999 (EN) — página Galeria | precisa deploy |
| **B** | Widget title: `"Miguel Penha" → "Miguel Penha Chiquitano"` no `_elementor_data` | 90325 (template `elementor_library` Galeria#21) | precisa deploy |
| **C** | Título do post: `"Galeria#21 Miguel Penha" → "Galeria#21 Miguel Penha Chiquitano"` | 90325 | precisa deploy |

**Já estão sincronizados em prod (nenhuma ação):** CPT `artistas` 86792, `linha-das-artes` 89378/89451, e o conteúdo "Chiquitano" das páginas 26767/26999.

⚠️ **Importante:** o ID 92811 é um artista **diferente** em prod (Rafael Matheus Moreira) — vou **deixar intocado**. As 11 legendas das obras ("...Miguel Penha") permanecem como estão em […]

> TOOL

tool_use TaskCreate
id: toolu_01NUBJ497cU4sw4z1VPzw7Yf
```json
{
  "subject": "Deploy Galeria /cultura/ para prod (Barlow→Roboto + Miguel Penha Chiquitano)",
  "description": "3 alterações cirúrgicas no blog 2 em prod: (A) toggle font Barlow→Roboto nas páginas 26767 PT + 26999 EN; (B) widget title Miguel Penha→Miguel Penha Chiquitano no _elementor_data do template 90325; (C) post_title do 90325. Backup + regen Elementor CSS + reload php-fpm + invalidação cirúrgica WP Rocket+CloudFront de /cultura/galeria/ PT e EN.",
  "activeForm": "Fazendo deploy da Galeria para prod"
}
```

> TOOL

tool_result
id: toolu_01NUBJ497cU4sw4z1VPzw7Yf
```
Task #3 created successfully: Deploy Galeria /cultura/ para prod (Barlow→Roboto + Miguel Penha Chiquitano)
```

> TOOL

tool_use AskUserQuestion
id: toolu_014jbPafca9PFcyMCYcfrBD5
```json
{
  "questions": [
    {
      "question": "O 'deploy da Galeria' envolve 3 mudanças cirúrgicas no blog 2. Confirma aplicar TODAS em prod?",
      "header": "Escopo deploy",
      "multiSelect": false,
      "options": [
        {
          "label": "Sim, aplicar A+B+C",
          "description": "A) Barlow→Roboto nas páginas Galeria 26767 PT + 26999 EN; B) widget title Miguel Penha→Miguel Penha Chiquitano no template 90325; C) post_title do 90325. Com backup, regen CSS, reload php-fpm e invalidação cirúrgica."
        },
        {
          "label": "Só A (Barlow→Roboto)",
          "description": "Aplicar apenas a mudança de fonte nas páginas Galeria. Deixar o 'Miguel Penha Chiquitano' do template 90325 para depois."
        },
        {
          "label": "Só B+C (Chiquitano)",
          "description": "Aplicar apenas a correção do nome no template 90325. Deixar Barlow→Roboto para depois."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_014jbPafca9PFcyMCYcfrBD5
```
Your questions have been answered: "O 'deploy da Galeria' envolve 3 mudanças cirúrgicas no blog 2. Confirma aplicar TODAS em prod?"="Sim, aplicar A+B+C". You can now continue with these answers in mind.
```

> AGENT

Confirmado A+B+C. Vou aplicar tudo em prod num único eval-file idempotente com backups. Começo pelo dry-run.

> TOOL

tool_use TaskUpdate
id: toolu_019sS1A5Zqc1UT93bdbbNv5S
```json
{
  "taskId": "3",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_019sS1A5Zqc1UT93bdbbNv5S
```
Updated task #3 status
```

> TOOL

tool_use Bash
id: toolu_01GMNxG2QA1pfg8G73za46qy
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\ncat > tmp/prod-deploy-galeria.php <<'PHP'\n<?php\n/**\n * PROD — Deploy Galeria /cultura/ (blog 2). 3 alterações cirúrgicas:\n *   A) toggle_label_typography_font_family: \"Barlow\" -> \"Roboto\"\n *      nas páginas Galeria 26767 (PT) e 26999 (EN)\n *   B) widget title no _elementor_data do template 90325:\n *      \"title\":\"Miguel Penha\" -> \"title\":\"Miguel Penha Chiquitano\"\n *   C) post_title do 90325: \"Galeria#21 Miguel Penha\" -> \"...Chiquitano\"\n *\n * Idempotente. Backups por post. Opera no blog 2.\n *\n * Uso: wp eval-file ...            (dry-run)\n *      APPLY=1 wp eval-file ...     (aplica + regen Elementor CSS)\n */\n\n$apply = getenv('APPLY') === '1';\nswitch_to_blog(2);\n\nfunction bk($id, $key, $val) { // backup once\n    if (!get_post_meta($id, $key, true)) { update_post_meta($id, $key, wp_slash($val)); return true; }\n    return false;\n}\n\n// ---------- A) Barlow -> Roboto (páginas 26767 PT, 26999 EN) ----------\nforeach ([26767 => 'PT', 26999 => 'EN'] as $id => $lang) {\n    $data = get_post_meta($id, '_elementor_data', true);\n    $needle = '\"toggle_label_typography_font_family\":\"Barlow\"';\n    $repl   = '\"toggle_label_typography_font_family\":\"Roboto\"';\n    $count = substr_count((string)$data, $needle);\n    echo \"[A][$id/$lang] toggle Barlow->Roboto: $count ocorrência(s)\\n\";\n    if ($count > 0 && $apply) {\n        bk($id, '_elementor_data_pre_galeria_deploy', $data);\n        $new = str_replace($needle, $repl, $data);\n        update_post_meta($id, '_elementor_data', $new); // _elementor_data: sem wp_slash (já é JSON)\n        if (class_exists('\\Elementor\\Core\\Files\\CSS\\Post')) { (new \\Elementor\\Core\\Files\\CSS\\Post($id))->update(); }\n        clean_post_cache($id);\n        delete_post_meta($id, '_elementor_element_cache');\n        echo \"      APLICADO\\n\";\n    }\n}\n\n// ---------- B + […]

> TOOL

tool_result
id: toolu_01GMNxG2QA1pfg8G73za46qy
```
=== DRY-RUN PROD ===
[A][26767/PT] toggle Barlow->Roboto: 1 ocorrência(s)
[A][26999/EN] toggle Barlow->Roboto: 1 ocorrência(s)
[B][90325] widget title Miguel Penha->Chiquitano: 1 ocorrência(s)
[C][90325] post_title -> Chiquitano: precisa (atual: 'Galeria#21 Miguel Penha')
DRY-RUN (nada gravado)
```

> AGENT

Dry-run perfeito: A (1+1 ocorrências Barlow→Roboto), B (1 widget title), C (post_title precisa). Vou aplicar.

> TOOL

tool_use Bash
id: toolu_01TyFjtofKL1ULptRmkq9TFN
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== APLICANDO EM PROD ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data env APPLY=1 wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval-file /tmp/prod-deploy-galeria.php 2>&1\" | grep -vE \"Deprecated\"",
  "description": "Aplicar deploy completo da Galeria em prod"
}
```

> TOOL

tool_result
id: toolu_01TyFjtofKL1ULptRmkq9TFN
```
=== APLICANDO EM PROD ===
[A][26767/PT] toggle Barlow->Roboto: 1 ocorrência(s)
      APLICADO
[A][26999/EN] toggle Barlow->Roboto: 1 ocorrência(s)
      APLICADO
[B][90325] widget title Miguel Penha->Chiquitano: 1 ocorrência(s)
[C][90325] post_title -> Chiquitano: precisa (atual: 'Galeria#21 Miguel Penha')
      [B] APLICADO
      [C] APLICADO (novo título: 'Galeria#21 Miguel Penha Chiquitano')
DONE (aplicado)
```

> AGENT

Tudo aplicado. Agora o pós-deploy de prod: reload php-fpm + invalidação cirúrgica de cache. A página Galeria é renderizada via o template `elementor_library` 90325, então preciso invalidar tanto a página quanto garantir que o template regenere.

> TOOL

tool_use Bash
id: toolu_014GbS5wd57GViahR5P8ZR7M
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== 1) Reload php-fpm ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo systemctl reload php8.3-fpm && echo 'php8.3-fpm reloaded OK'\" 2>&1 | grep -vE \"Deprecated\"\necho \"\"\necho \"=== 2) WP Rocket — limpar páginas Galeria PT+EN (blog 2) ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval '\nswitch_to_blog(2);\nforeach ([26767, 26999] as \\$id) {\n  if (function_exists(\\\"rocket_clean_post\\\")) { rocket_clean_post(\\$id); echo \\\"WP Rocket limpo \\$id (\\\" . get_permalink(\\$id) . \\\")\\n\\\"; }\n}\n// flush object cache p/ pegar o template 90325 regenerado\nwp_cache_flush();\necho \\\"object cache flushed\\n\\\";\nrestore_current_blog();\n' 2>&1\" | grep -vE \"Deprecated\"",
  "description": "Reload php-fpm e limpar WP Rocket das páginas Galeria"
}
```

> TOOL

tool_result
id: toolu_014GbS5wd57GViahR5P8ZR7M
```
=== 1) Reload php-fpm ===
php8.3-fpm reloaded OK

=== 2) WP Rocket — limpar páginas Galeria PT+EN (blog 2) ===
WP Rocket limpo 26767 (https://concertacaoamazonia.com.br/cultura/galeria/)
WP Rocket limpo 26999 (https://concertacaoamazonia.com.br/cultura/galeria/)
object cache flushed
```

> AGENT

php-fpm recarregado e WP Rocket limpo. Agora a invalidação do CloudFront. Nota: PT e EN compartilham o mesmo path `/cultura/galeria/` (WPML por diretório no blog 2 — o permalink é idêntico, o idioma é negociado). Vou invalidar esse path e também o path EN se houver prefixo `/en/`.

> TOOL

tool_use Bash
id: toolu_015pkikZ7iELyoUTwqdTPfFE
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\n# Descobrir o permalink real do EN em prod (pode ter prefixo /en/ ou /cultura/en/)\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval '\nswitch_to_blog(2);\necho \\\"PT 26767: \\\" . get_permalink(26767) . \\\"\\n\\\";\necho \\\"EN 26999: \\\" . get_permalink(26999) . \\\"\\n\\\";\nrestore_current_blog();\n' 2>&1\" | grep -vE \"Deprecated\"",
  "description": "Descobrir permalinks reais PT e EN em prod"
}
```

> TOOL

tool_result
id: toolu_015pkikZ7iELyoUTwqdTPfFE
```
PT 26767: https://concertacaoamazonia.com.br/cultura/galeria/
EN 26999: https://concertacaoamazonia.com.br/cultura/galeria/
```

> AGENT

Os permalinks de PT e EN são idênticos no banco (`/cultura/galeria/`), mas o WPML serve o EN num path com prefixo de idioma. Pela memória do projeto, o padrão é `/cultura/en/...`. Vou invalidar os paths cobrindo ambas as variações. Vou invalidar com wildcard para cobrir PT, EN e os assets do template.

> TOOL

tool_use Bash
id: toolu_01K78oWgpbjsCiJwxSeT4drG
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=/home/<USER>/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh\necho \"=== CloudFront — invalidar Galeria PT ===\"\n$DD cache-flush --prod --cf-only \"/cultura/galeria/\" 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|^\\s*$|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress\" | tail -8\necho \"\"\necho \"=== CloudFront — invalidar Galeria EN (/cultura/en/galeria/) ===\"\n$DD cache-flush --prod --cf-only \"/cultura/en/galeria/\" 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|^\\s*$|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress\" | tail -8",
  "description": "Invalidar CloudFront Galeria PT e EN"
}
```

> TOOL

tool_result
id: toolu_01K78oWgpbjsCiJwxSeT4drG
```
=== CloudFront — invalidar Galeria PT ===
[38;2;102;217;239m[INFO][0m Target: PROD (alias=concertacaoamazonia.com.br-prod-sa, wp_root=/var/www/concertacaoamazonia.com.br)
[38;2;102;217;239m[INFO][0m WP Rocket: pulando (--cf-only)
[38;2;102;217;239m[INFO][0m CloudFront (E2F1QD7E7YOYEB): invalidando /cultura/galeria/...
[38;2;102;217;239m[INFO][0m Invalidacao IAX4DK6Q027OG3FLEWEHWTDEVM criada — aguardando propagacao...
[38;2;166;226;46m[OK][0m Cache limpo e propagado!
[38;2;102;217;239m[INFO][0m Verificacao: render fresco da origin em /cultura/galeria/ (bypassa WP Rocket + CloudFront)...
[38;2;166;226;46m[OK][0m Verificacao: HTTP 200 em /cultura/galeria/
[38;2;166;226;46m[OK][0m Verificacao: render fresco OK em /cultura/galeria/

=== CloudFront — invalidar Galeria EN (/cultura/en/galeria/) ===
[38;2;102;217;239m[INFO][0m Target: PROD (alias=concertacaoamazonia.com.br-prod-sa, wp_root=/var/www/concertacaoamazonia.com.br)
[38;2;102;217;239m[INFO][0m WP Rocket: pulando (--cf-only)
[38;2;102;217;239m[INFO][0m CloudFront (E2F1QD7E7YOYEB): invalidando /cultura/en/galeria/...
[38;2;102;217;239m[INFO][0m Invalidacao IBNUEL2P0E72GAD6JFKNWLA666 criada — aguardando propagacao...
[38;2;166;226;46m[OK][0m Cache limpo e propagado!
[38;2;102;217;239m[INFO][0m Verificacao: render fresco da origin em /cultura/en/galeria/ (bypassa WP Rocket + CloudFront)...
[38;2;255;152;0m[WARN][0m Verificacao: HTTP 301 (redirect) em /cultura/en/galeria/ — confira trailing slash
[38;2;255;152;0m[WARN][0m Verificacao: render fresco com pendencias em /cultura/en/galeria/ (invalidacao ja aplicada — revise acima)
```

> AGENT

PT invalidado e verificado (HTTP 200). EN deu HTTP 301 redirect em `/cultura/en/galeria/` — preciso descobrir o path EN correto. O WPML deste site usa um padrão de URL específico para o EN. Vou descobrir a URL real seguindo o redirect.

> TOOL

tool_use Bash
id: toolu_015fhGmAwaMXnMwGu51CNETB
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Seguir redirect do EN ===\"\ncurl -sI \"https://concertacaoamazonia.com.br/cultura/en/galeria/\" | grep -iE \"^location|^HTTP\"\necho \"---\"\necho \"=== Testar variações ===\"\nfor url in \"https://concertacaoamazonia.com.br/en/cultura/galeria/\" \"https://concertacaoamazonia.com.br/cultura/galeria/?lang=en\" \"https://concertacaoamazonia.com.br/en/culture/gallery/\"; do\n  code=$(curl -so /dev/null -w \"%{http_code}\" \"$url\")\n  echo \"$code  $url\"\ndone",
  "description": "Descobrir URL EN correta da Galeria"
}
```

> TOOL

tool_result
id: toolu_015fhGmAwaMXnMwGu51CNETB
```
=== Seguir redirect do EN ===
HTTP/2 301 
location: https://concertacaoamazonia.com.br/cultura/en/gallery/
---
=== Testar variações ===
200  https://concertacaoamazonia.com.br/en/cultura/galeria/
200  https://concertacaoamazonia.com.br/cultura/galeria/?lang=en
200  https://concertacaoamazonia.com.br/en/culture/gallery/
```

> AGENT

O path EN real é **`/cultura/en/gallery/`** (o redirect 301 revelou o slug correto: `gallery`, não `galeria`). Vou invalidar esse path correto.

> TOOL

tool_use Bash
id: toolu_01Ft3cBv3iHqGmTNpcZzbyiC
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\nDD=/home/<USER>/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh\necho \"=== CloudFront — invalidar Galeria EN (/cultura/en/gallery/) ===\"\n$DD cache-flush --prod --cf-only \"/cultura/en/gallery/\" 2>&1 | grep -vE \"Cores ativadas|[│╭╰├╮]|BIT BPO|^\\s*$|Docker Devil|docker-dev\\.sh|Versao|Ambiente WordPress\" | tail -8",
  "description": "Invalidar CloudFront Galeria EN no path correto"
}
```

> TOOL

tool_result
id: toolu_01Ft3cBv3iHqGmTNpcZzbyiC
```
=== CloudFront — invalidar Galeria EN (/cultura/en/gallery/) ===
[38;2;102;217;239m[INFO][0m Target: PROD (alias=concertacaoamazonia.com.br-prod-sa, wp_root=/var/www/concertacaoamazonia.com.br)
[38;2;102;217;239m[INFO][0m WP Rocket: pulando (--cf-only)
[38;2;102;217;239m[INFO][0m CloudFront (E2F1QD7E7YOYEB): invalidando /cultura/en/gallery/...
[38;2;102;217;239m[INFO][0m Invalidacao I4EDFFBD1LRHFXXRVDS2X6CZ7E criada — aguardando propagacao...
[38;2;166;226;46m[OK][0m Cache limpo e propagado!
[38;2;102;217;239m[INFO][0m Verificacao: render fresco da origin em /cultura/en/gallery/ (bypassa WP Rocket + CloudFront)...
[38;2;166;226;46m[OK][0m Verificacao: HTTP 200 em /cultura/en/gallery/
[38;2;166;226;46m[OK][0m Verificacao: render fresco OK em /cultura/en/gallery/
```

> AGENT

EN invalidado e verificado (HTTP 200). Agora a validação final no browser em produção real — confirmar as 3 mudanças. Vou usar o navegador para checar: (1) a fonte Roboto no toggle, (2) "Miguel Penha Chiquitano" renderizado.

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_01BgnkeEzAk1sNiyhHHz48sa
```json
{
  "url": "https://concertacaoamazonia.com.br/cultura/galeria/"
}
```

> TOOL

tool_result
id: toolu_01BgnkeEzAk1sNiyhHHz48sa
```
### Ran Playwright code
```js
await page.goto('https://concertacaoamazonia.com.br/cultura/galeria/');
```
### Page
- Page URL: https://concertacaoamazonia.com.br/cultura/galeria/
- Page Title: Galeria – Uma Concertação pela Amazônia: Cultura
### Snapshot
- [Snapshot](.playwright-mcp/page-2026-06-05T22-05-36-316Z.yml)
### Events
- New console entries: .playwright-mcp/console-2026-06-05T22-05-32-920Z.log#L1-L3
```

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_019t7oKTcr6nX6PxyucWBZ56
```json
{
  "function": "() => {\n  const r = {};\n  // 1) \"Miguel Penha Chiquitano\" presente?\n  const bodyHTML = document.body.innerHTML;\n  r.has_chiquitano = bodyHTML.includes('Miguel Penha Chiquitano');\n  r.miguel_penha_count = (bodyHTML.match(/Miguel Penha/g)||[]).length;\n  r.chiquitano_count = (bodyHTML.match(/Miguel Penha Chiquitano/g)||[]).length;\n  // localizar o h2/heading com Miguel Penha\n  const headings = [...document.querySelectorAll('h1,h2,h3,h4')].filter(h=>/Miguel Penha/.test(h.textContent));\n  r.headings_with_miguel = headings.map(h => ({ tag: h.tagName, text: h.textContent.trim(), fontFamily: getComputedStyle(h).fontFamily }));\n  // 2) toggle labels — procurar elementos de toggle e suas fontes\n  const toggles = [...document.querySelectorAll('.elementor-toggle-title, .elementor-tab-title, [class*=\"toggle\"]')].slice(0,6);\n  r.toggle_fonts = toggles.map(t => ({ text: t.textContent.trim().slice(0,40), fontFamily: getComputedStyle(t).fontFamily }));\n  return JSON.stringify(r, null, 2);\n}"
}
```

> TOOL

tool_result
id: toolu_019t7oKTcr6nX6PxyucWBZ56
```
### Result
"{\n  \"has_chiquitano\": true,\n  \"miguel_penha_count\": 1,\n  \"chiquitano_count\": 1,\n  \"headings_with_miguel\": [],\n  \"toggle_fonts\": [\n    {\n      \"text\": \"Sobre nós\\n\\n\\tRede\\n\\t5 Pilares\\n\\tAgenda Inte\",\n      \"fontFamily\": \"-apple-system, \\\"system-ui\\\", \\\"Segoe UI\\\", Roboto, \\\"Helvetica Neue\\\", Arial, \\\"Noto Sans\\\", sans-serif, \\\"Apple Color Emoji\\\", \\\"Segoe UI Emoji\\\", \\\"Segoe UI Symbol\\\", \\\"Noto Color Emoji\\\"\"\n    },\n    {\n      \"text\": \"\",\n      \"fontFamily\": \"-apple-system, \\\"system-ui\\\", \\\"Segoe UI\\\", Roboto, \\\"Helvetica Neue\\\", Arial, \\\"Noto Sans\\\", sans-serif, \\\"Apple Color Emoji\\\", \\\"Segoe UI Emoji\\\", \\\"Segoe UI Symbol\\\", \\\"Noto Color Emoji\\\"\"\n    },\n    {\n      \"text\": \"\",\n      \"fontFamily\": \"-apple-system, \\\"system-ui\\\", \\\"Segoe UI\\\", Roboto, \\\"Helvetica Neue\\\", Arial, \\\"Noto Sans\\\", sans-serif, \\\"Apple Color Emoji\\\", \\\"Segoe UI Emoji\\\", \\\"Segoe UI Symbol\\\", \\\"Noto Color Emoji\\\"\"\n    },\n    {\n      \"text\": \"\",\n      \"fontFamily\": \"-apple-system, \\\"system-ui\\\", \\\"Segoe UI\\\", Roboto, \\\"Helvetica Neue\\\", Arial, \\\"Noto Sans\\\", sans-serif, \\\"Apple Color Emoji\\\", \\\"Segoe UI Emoji\\\", \\\"Segoe UI Symbol\\\", \\\"Noto Color Emoji\\\"\"\n    },\n    {\n      \"text\": \"\",\n      \"fontFamily\": \"-apple-system, \\\"system-ui\\\", \\\"Segoe UI\\\", Roboto, \\\"Helvetica Neue\\\", Arial, \\\"Noto Sans\\\", sans-serif, \\\"Apple Color Emoji\\\", \\\"Segoe UI Emoji\\\", \\\"Segoe UI Symbol\\\", \\\"Noto Color Emoji\\\"\"\n    },\n    {\n      \"text\": \"Sem imagens\",\n      \"fontFamily\": \"\\\"Plus Jakarta Sans\\\", system-ui, sans-serif\"\n    }\n  ]\n}"
### Ran Playwright code
```js
await page.evaluate('() => {\n  const r = {};\n  // 1) "Miguel Penha Chiquitano" presente?\n  const bodyHTML = document.body.innerHTML;\n  r.has_chiquitano = bodyHTML.includes(\'Miguel Penha Chiquitano\');\n […]

> AGENT

A página Galeria carrega via JetEngine listing (renderização dinâmica). O resultado mostra:
- **"Miguel Penha Chiquitano" presente: true** (chiquitano_count=1, e o único "Miguel Penha" já é "Chiquitano") ✅
- O `headings_with_miguel` veio vazio porque o conteúdo da galeria (template 90325) é carregado via **listing/lazy** — o card individual abre num popup/link. O "Miguel Penha Chiquitano" detectado está no HTML.

A galeria mostra cards de artistas que abrem o template. Deixa eu validar o conteúdo do template 90325 renderizado e a fonte do toggle de forma mais direta — abrindo o card do Miguel Penha. Mas primeiro, o mais importante é confirmar via origin (sem cache) que o template 90325 e as páginas estão corretos. Já validei via WP-CLI que o banco está correto. Vou confirmar o estado final no banco de prod e a fonte Roboto aplicada no CSS regenerado.

> TOOL

tool_use Bash
id: toolu_015Kb5zcagCmVGKhXAd6RvbD
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Validação final no banco de PROD ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval-file /tmp/check-miguel-prod.php 2>&1\" | grep -vE \"Deprecated\" | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint('POST | title | barlow→roboto status')\nfor id in ['26767','26999','90325']:\n    p=d[id]\n    print(f\\\"{id} | {p['title'][:45]:45} | chiquitano_in_elementor={p['elementor_has_chiquitano']}\\\")\n\"\necho \"\"\necho \"=== Confirmar Barlow→Roboto no _elementor_data prod ===\"\nssh concertacaoamazonia.com.br-prod-sa \"sudo -u www-data wp --url=https://concertacaoamazonia.com.br/cultura/ --path=/var/www/concertacaoamazonia.com.br eval '\nswitch_to_blog(2);\nforeach ([26767=>\\\"PT\\\",26999=>\\\"EN\\\"] as \\$id=>\\$l) {\n  \\$d=get_post_meta(\\$id,\\\"_elementor_data\\\",true);\n  \\$barlow=substr_count(\\$d,\\\"toggle_label_typography_font_family\\\\\\\":\\\\\\\"Barlow\\\");\n  \\$roboto=substr_count(\\$d,\\\"toggle_label_typography_font_family\\\\\\\":\\\\\\\"Roboto\\\");\n  echo \\\"\\$id/\\$l: toggle Barlow=\\$barlow Roboto=\\$roboto\\n\\\";\n}\necho \\\"90325 título: \\\" . get_the_title(90325) . \\\"\\n\\\";\necho \\\"90325 widget title chiquitano: \\\" . substr_count(get_post_meta(90325,\\\"_elementor_data\\\",true),\\\"Miguel Penha Chiquitano\\\") . \\\"\\n\\\";\nrestore_current_blog();\n' 2>&1\" | grep -vE \"Deprecated\"",
  "description": "Validação final do banco de prod"
}
```

> TOOL

tool_result
id: toolu_015Kb5zcagCmVGKhXAd6RvbD
```
=== Validação final no banco de PROD ===
POST | title | barlow→roboto status
26767 | Galeria                                       | chiquitano_in_elementor=1
26999 | Gallery                                       | chiquitano_in_elementor=1
90325 | Galeria#21 Miguel Penha Chiquitano            | chiquitano_in_elementor=1

=== Confirmar Barlow→Roboto no _elementor_data prod ===
26767/PT: toggle Barlow=0 Roboto=1
26999/EN: toggle Barlow=0 Roboto=1
90325 título: Galeria#21 Miguel Penha Chiquitano
90325 widget title chiquitano: 1
```

> AGENT

Validação final no banco de produção — **tudo correto**:

| Item | Estado em prod |
|------|----------------|
| **26767 (PT)** toggle font | Barlow=0, **Roboto=1** ✅ |
| **26999 (EN)** toggle font | Barlow=0, **Roboto=1** ✅ |
| **90325** post_title | "Galeria#21 Miguel Penha **Chiquitano**" ✅ |
| **90325** widget title no `_elementor_data` | "Miguel Penha Chiquitano" (1×) ✅ |

Vou fazer uma última checagem visual abrindo o card do Miguel Penha na galeria para confirmar a renderização, e tirar um screenshot.

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01TzYZHVHbUz1JcgW24pvSjL
```json
{
  "function": "() => {\n  // localizar e clicar no card/link do Miguel Penha na galeria\n  const candidates = [...document.querySelectorAll('a, [class*=\"listing\"] *')].filter(el => /Miguel Penha/i.test(el.textContent||''));\n  const card = candidates.find(c => c.tagName==='A') || candidates[0];\n  if (card) {\n    card.scrollIntoView({block:'center'});\n    return 'found: ' + card.tagName + ' | ' + (card.textContent||'').trim().slice(0,60);\n  }\n  return 'card Miguel Penha não encontrado no DOM inicial (listing pode carregar via AJAX)';\n}"
}
```

> TOOL

tool_result
id: toolu_01TzYZHVHbUz1JcgW24pvSjL
```
### Result
"card Miguel Penha não encontrado no DOM inicial (listing pode carregar via AJAX)"
### Ran Playwright code
```js
await page.evaluate('() => {\n  // localizar e clicar no card/link do Miguel Penha na galeria\n  const candidates = [...document.querySelectorAll(\'a, [class*="listing"] *\')].filter(el => /Miguel Penha/i.test(el.textContent||\'\'));\n  const card = candidates.find(c => c.tagName===\'A\') || candidates[0];\n  if (card) {\n    card.scrollIntoView({block:\'center\'});\n    return \'found: \' + card.tagName + \' | \' + (card.textContent||\'\').trim().slice(0,60);\n  }\n  return \'card Miguel Penha não encontrado no DOM inicial (listing pode carregar via AJAX)\';\n}');
```
### Events
- New console entries: .playwright-mcp/console-2026-06-05T22-05-32-920Z.log#L6-L20
```

> AGENT

O listing carrega via AJAX. O HTML já confirmou que "Miguel Penha Chiquitano" está presente. Vou aguardar o listing carregar e tirar um screenshot da galeria para registro visual.

> TOOL

tool_use ToolSearch
id: toolu_01BPmmx98hoNsTUx1KVLyDeU
```json
{
  "query": "select:mcp__playwright__browser_wait_for",
  "max_results": 2
}
```

> TOOL

tool_result
id: toolu_01BPmmx98hoNsTUx1KVLyDeU
```
{
  "type": "tool_reference",
  "tool_name": "mcp__playwright__browser_wait_for"
}
```

> TOOL

tool_use mcp__playwright__browser_wait_for
id: toolu_017EsQKhLAqBRZXzAaK6GNL4
```json
{
  "text": "Miguel Penha Chiquitano",
  "time": 8
}
```

> TOOL

tool_result ERROR
id: toolu_017EsQKhLAqBRZXzAaK6GNL4
```
### Error
Error: No open pages available.
```

> AGENT

A página foi fechada. A validação por banco de dados já confirmou tudo definitivamente — não preciso reabrir o browser para isso. O conteúdo está correto na origem, o cache foi invalidado e verificado (HTTP 200 fresco). Vou limpar os temporários e finalizar.

> TOOL

tool_use Bash
id: toolu_01LYaZPWeJKkdgMx4wsTjgfP
```json
{
  "command": "cd /home/<USER>/scripts/server-tools/v2/docker-dev/sites/concertacao\n# Limpar temporários locais\nrm -f tmp/wpml-diag-galeria.php tmp/galeria-fingerprint.php tmp/galeria-export.php tmp/find-miguel.php tmp/check-miguel-prod.php tmp/inspect-90325.php tmp/inspect-90325-prod.php tmp/prod-deploy-galeria.php tmp/galeria_dev_*.json tmp/galeria_prod_*.json tmp/galeria-dev-fp.json tmp/galeria-prod-fp.json\n# Limpar do container\ndocker exec concertacao-dev-wordpress sh -c 'rm -f /tmp/wpml-diag-galeria.php /tmp/galeria-fingerprint.php /tmp/galeria-export.php /tmp/find-miguel.php /tmp/check-miguel-prod.php /tmp/inspect-90325.php /tmp/galeria_dev_*.json' 2>/dev/null\n# Limpar de prod\nssh concertacaoamazonia.com.br-prod-sa \"rm -f /tmp/galeria-fingerprint.php /tmp/galeria-export.php /tmp/check-miguel-prod.php /tmp/inspect-90325-prod.php /tmp/prod-deploy-galeria.php /tmp/galeria_prod_*.json\" 2>/dev/null\necho \"Temporários limpos.\"",
  "description": "Limpar arquivos temporários"
}
```

> TOOL

tool_result
id: toolu_01LYaZPWeJKkdgMx4wsTjgfP
```
Temporários limpos.
```

> TOOL

tool_use TaskUpdate
id: toolu_01TeC8mse94nVLk6bKpTbMUw
```json
{
  "taskId": "3",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01TeC8mse94nVLk6bKpTbMUw
```
Updated task #3 status
```

> AGENT

Deploy concluído e validado em produção.

## Resumo do deploy — Galeria `/cultura/` (blog 2)

Ao investigar, descobri que o "deploy da Galeria" envolvia **3 alterações distintas**, não só a página. Apliquei todas em produção (PT + EN):

**A) Fonte do toggle label: Barlow → Roboto**
- Páginas **26767 (Galeria PT)** e **26999 (Gallery EN)** — `toggle_label_typography_font_family`
- Resultado em prod: Barlow=0, **Roboto=1** em ambas ✅

**B) Widget title: "Miguel Penha" → "Miguel Penha Chiquitano"**
- Template `elementor_library` **90325** (Galeria#21) — no `_elementor_data` ✅

**C) Título do post: "Galeria#21 Miguel Penha" → "Galeria#21 Miguel Penha Chiquitano"**
- Post **90325** ✅

**Procedimento de prod seguido:**
- ✅ Backups por post (`_elementor_data_pre_galeria_deploy`, `_post_title_pre_galeria_deploy`)
- ✅ Regen do Elementor CSS de cada post + limpeza de `_elementor_element_cache`
- ✅ `reload php8.3-fpm`
- ✅ WP Rocket limpo (páginas 26767 + 26999) + object cache flush
- ✅ CloudFront invalidado e verificado HTTP 200 fresco em **3 paths**: `/cultura/galeria/` (PT), `/cultura/en/gallery/` (EN), e descartado o `/cultura/en/galeria/` (era 301)
- ✅ Validação final no banco de prod: todas as 3 mudanças confirmadas

**Pontos que diagnostiquei e deliberadamente NÃO toquei:**
- **ID 92811** é um artista **diferente** em prod (Rafael Matheus Moreira) vs dev (Miguel Penha Chiquitano) […]