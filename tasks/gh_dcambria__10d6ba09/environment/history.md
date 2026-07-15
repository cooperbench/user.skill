> DEVELOPER

as fontes que estamos usando no projeto estao sem italico, consegue incorporar italico?

> AGENT

Vou primeiro entender o contexto — quais fontes estão em uso no projeto e como estão sendo carregadas — antes de propor a inclusão do itálico. Deixa eu invocar a skill de brainstorming já que isso envolve modificar comportamento/assets visuais, e em paralelo investigar a configuração de fontes.

> TOOL

tool_use Skill
id: toolu_011e7GNHA6BPFZSp5o79w6A6
```json
{
  "skill": "superpowers:brainstorming"
}
```

> TOOL

tool_result
id: toolu_011e7GNHA6BPFZSp5o79w6A6
```
Launching skill: superpowers:brainstorming
```

> AGENT

Vou começar entendendo o contexto. Deixa eu investigar quais fontes estão em uso no projeto e como estão configuradas.

> TOOL

tool_use Agent
id: toolu_01E3ZACqyUTGHwTqgG9pKp5M
```json
{
  "description": "Find font configuration in project",
  "subagent_type": "Explore",
  "prompt": "Investigate how web fonts are configured/loaded in this WordPress project at /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao.\n\nI need to know:\n1. Which font families are used in the project (look in child theme CSS, Elementor global fonts, @font-face declarations, Google Fonts imports, etc.)\n2. How fonts are loaded — are they self-hosted (look for .woff, .woff2, .ttf, .otf files), loaded via Google Fonts, via Elementor's font manager, or via WP Rocket/plugin font hosting?\n3. Specifically look for whether italic font variants/weights are being loaded. The user says \"the fonts we're using in the project are without italic, can you incorporate italic?\" — so I need to find where the non-italic fonts are declared and whether italic faces are missing.\n\nSearch thoroughly:\n- The child theme directory: wordpress/wp-content/themes/hello-elementor-child/ (style.css, functions.php, any css/ folder, any fonts/ folder)\n- Any @font-face declarations across the theme and mu-plugins\n- Any references to \"italic\", \"font-style\", font weights like 400, 700, \"normal\"\n- Any self-hosted font files (find .woff2, .woff, .ttf, .otf)\n- Any Google Fonts URLs (fonts.googleapis.com) and check if they include italic variants (e.g. \"ital,wght@\" or \":ital\")\n- Elementor font settings if stored in DB dump or kit files\n\nReport back:\n- The exact font family […]

> TOOL

tool_result
id: toolu_01E3ZACqyUTGHwTqgG9pKp5M
```
Perfect! Now I have all the information I need. Let me compile a comprehensive report.

## Font Configuration Investigation Report

Based on my thorough search of the WordPress project at `/Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao`, here's the complete font configuration:

---

### 1. **Font Families Used in the Project**

The project uses **three custom font families**:
- **Franie** — Display/heading font
- **Just Sans** — Body/UI font
- **Roboto** — Secondary font for SVG spiral widget
- **Plus Jakarta Sans** — Accessibility panel font (mu-plugin only)

---

### 2. **Font Loading Mechanism**

All fonts are **self-hosted as WOFF2 files**. There are NO Google Fonts imports. The project explicitly disables Google Fonts loading.

**File Locations:**
- Theme fonts: `/wordpress/wp-content/themes/hello-elementor-child/fonts/woff2/`
- A11y font: `/wordpress/wp-content/mu-plugins/bureau-a11y/fonts/`

---

### 3. **Font Declaration Details**

#### **Primary Source: Child Theme Functions.php**
**File:** `/wordpress/wp-content/themes/hello-elementor-child/functions.php` (lines 169–250)

The `bureau_it_custom_fonts_css()` function (line 181) registers all fonts via inline CSS with `@font-face` declarations:

**Franie Font Family:**
- **Line 186-191:** `Franie-Regular.woff2` — weight: 400, style: normal ✓ italic missing for regular weight
- **Line 195-199:** `Franie-Italic.woff2` — weight: 400, style: italic ✓ PRESENT
- **Line 203-207:** `Franie-Bold.woff2` — weight: 700, style: normal ✓ italic missing for bold weight
- **Line 211-215:** `Franie-BoldItalic.woff2` […]

> AGENT

Tenho o contexto completo. Deixa eu confirmar alguns detalhes lendo diretamente os arquivos-chave antes de propor o design.

> TOOL

tool_use Read
id: toolu_01UehH3GTq1pUUz4rpfnmL3a
```json
{
  "file_path": "/Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/wordpress/wp-content/themes/hello-elementor-child/functions.php",
  "offset": 169,
  "limit": 100
}
```

> TOOL

tool_result
id: toolu_01UehH3GTq1pUUz4rpfnmL3a
```
169	 * ============================================================================
170	 * CUSTOM FONTS: Franie, Just Sans, Roboto (local, no Google Fonts)
171	 * Roboto: subset Latin, wght 100-900 (42 KB vs 204 KB Variable Font original)
172	 * ============================================================================
173	 *
174	 * @since 1.6.0
175	 */
176	
177	/**
178	 * Register @font-face declarations via inline CSS
179	 */
180	add_action('wp_enqueue_scripts', 'bureau_it_custom_fonts_css');
181	function bureau_it_custom_fonts_css() {
182	    $fonts_woff = get_stylesheet_directory_uri() . '/fonts/woff2';
183	
184	    $css = "
185	@font-face {
186	    font-family: 'Franie';
187	    src: url('{$fonts_woff}/Franie-Regular.woff2') format('woff2');
188	    font-weight: 400;
189	    font-style: normal;
190	    font-display: swap;
191	}
192	
193	@font-face {
194	    font-family: 'Franie';
195	    src: url('{$fonts_woff}/Franie-Italic.woff2') format('woff2');
196	    font-weight: 400;
197	    font-style: italic;
198	    font-display: swap;
199	}
200	
201	@font-face {
202	    font-family: 'Franie';
203	    src: url('{$fonts_woff}/Franie-Bold.woff2') format('woff2');
204	    font-weight: 700;
205	    font-style: normal;
206	    font-display: swap;
207	}
208	
209	@font-face {
210	    font-family: 'Franie';
211	    src: url('{$fonts_woff}/Franie-BoldItalic.woff2') format('woff2');
212	    font-weight: 700;
213	    font-style: italic;
214	    font-display: swap;
215	}
216	
217	@font-face {
218	    font-family: 'Just Sans';
219	    src: url('{$fonts_woff}/JustSans-Regular.woff2') format('woff2');
220	    font-weight: 400;
221	    font-style: normal;
222	    font-display: swap;
223	}
224	
225	@font-face {
226	    font-family: 'Just Sans';
227	    src: url('{$fonts_woff}/JustSans-ExBold.woff2') format('woff2');
228	    font-weight: […]

> TOOL

tool_use Bash
id: toolu_01LK2JA98RqUaQachkKK9E9Y
```json
{
  "command": "ls -la /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/wordpress/wp-content/themes/hello-elementor-child/fonts/woff2/",
  "description": "List font files in child theme"
}
```

> TOOL

tool_result
id: toolu_01LK2JA98RqUaQachkKK9E9Y
```
total 584
drwxr-xr-x@ 10 dcambria  staff    320 18 mai 21:56 ./
drwxr-xr-x@  9 dcambria  staff    288  2 mai 16:03 ../
-rwxr-xr-x@  1 dcambria  staff  32824 16 mar 01:38 Franie-Bold.woff2
-rwxr-xr-x@  1 dcambria  staff  35412 16 mar 01:38 Franie-BoldItalic.woff2
-rwxr-xr-x@  1 dcambria  staff  35508 16 mar 01:38 Franie-Italic.woff2
-rwxr-xr-x@  1 dcambria  staff  32284 16 mar 01:38 Franie-Regular.woff2
-rwxr-xr-x@  1 dcambria  staff  40104 16 mar 01:38 JustSans-ExBold.woff2
-rwxr-xr-x@  1 dcambria  staff  37976 16 mar 01:38 JustSans-Regular.woff2
-rwxr-xr-x@  1 dcambria  staff  27272  2 mai 01:21 PlusJakartaSans-latin-w400-700.woff2
-rw-r--r--@  1 dcambria  staff  43136 18 mai 21:55 Roboto-latin-w100-900.woff2
```

> AGENT

Tenho tudo que preciso. O contexto está claro. Deixa eu confirmar com você o escopo antes de propor a solução, porque "incorporar itálico" pode significar coisas diferentes.

A situação atual é esta:

| Família | Uso no site | Regular | Itálico | Bold | Bold Itálico |
|---------|-------------|:---:|:---:|:---:|:---:|
| **Franie** | Títulos/display | ✓ | ✓ | ✓ | ✓ |
| **Just Sans** | Corpo/UI | ✓ | ✗ | ✓ (800) | ✗ |
| **Roboto** | SVG da espiral | ✓ | ✗ | — | — |

E o tema tem `font-synthesis: none` no `base.css`, ou seja: o navegador **não fabrica** itálico falso. Quando algum texto pede itálico em **Just Sans**, ele não inclina — cai para uma fonte de sistema ou simplesmente fica reto.

A **Franie já tem itálico completo**. O problema real é a **Just Sans** (a fonte do corpo do texto), que é onde quase todo itálico de conteúdo acontece (citações, ênfases, nomes de obras/publicações etc.).

Uma questão importante que muda totalmente a abordagem:

> TOOL

tool_use AskUserQuestion
id: toolu_01MwrRqTvx13qzUvKFJCoUrh
```json
{
  "questions": [
    {
      "question": "Você tem os arquivos de fonte itálica da Just Sans (ex.: JustSans-Italic.woff2 / JustSans-ExBoldItalic), ou só temos os arquivos que já estão no tema?",
      "header": "Arquivos itálicos",
      "multiSelect": false,
      "options": [
        {
          "label": "Tenho os arquivos itálicos",
          "description": "Você consegue me passar os .woff2/.ttf/.otf da Just Sans Italic (e ExBold Italic). Esse é o caminho ideal — itálico verdadeiro, desenhado pela fundição, com font-synthesis: none mantido."
        },
        {
          "label": "Não tenho / não sei",
          "description": "Só temos JustSans-Regular e JustSans-ExBold (sem itálico). Eu avalio alternativas: permitir o itálico sintético (oblíquo) só para a Just Sans, ou usar Franie itálico como par estilístico onde houver ênfase."
        },
        {
          "label": "Quero que você procure",
          "description": "Verificar se há licença/fonte disponível para baixar os arquivos itálicos da Just Sans antes de decidir."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01MwrRqTvx13qzUvKFJCoUrh
```
Your questions have been answered: "Você tem os arquivos de fonte itálica da Just Sans (ex.: JustSans-Italic.woff2 / JustSans-ExBoldItalic), ou só temos os arquivos que já estão no tema?"="Quero que você procure". You can now continue with these answers in mind.
```

> AGENT

Vou verificar a licença/disponibilidade da Just Sans. A "Just Sans" é uma fonte comercial da fundição **pangrampublishing / atipo / Latinotype** — preciso confirmar quem é a fundição e se há versão itálica disponível. Deixa eu pesquisar.

> TOOL

tool_use ToolSearch
id: toolu_016NFmngNZQHafNdV3PUDGH4
```json
{
  "query": "select:WebSearch,WebFetch",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_016NFmngNZQHafNdV3PUDGH4
```
{
  "type": "tool_reference",
  "tool_name": "WebSearch"
}
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
```

> TOOL

tool_use WebSearch
id: toolu_01Y29XPuxTp9ZYtGyGTcjM4w
```json
{
  "query": "\"Just Sans\" font foundry italic oblique webfont license"
}
```

> TOOL

tool_result
id: toolu_01Y29XPuxTp9ZYtGyGTcjM4w
```
Web search results for query: ""Just Sans" font foundry italic oblique webfont license"

Links: [{"title":"Just Sans Font | Webfont & Desktop | MyFonts","url":"https://www.myfonts.com/collections/just-sans-font-just-creative/"},{"title":"Foundry Form Sans Font | Webfont & Desktop | MyFonts","url":"https://www.myfonts.com/collections/foundry-form-sans-font-the-foundry/"},{"title":"Foundry Sans Font | Webfont & Desktop | MyFonts","url":"https://www.myfonts.com/collections/foundry-sans-font-the-foundry/"},{"title":"JUST Sans Outline Font | Webfont & Desktop | MyFonts","url":"https://www.myfonts.com/collections/just-sans-outline-font-just-creative/"},{"title":"Foundry Sans: download for free and install for your website or Photoshop.","url":"https://en.bestfonts.pro/font/foundry-sans"},{"title":"Obliqua Sans | Adobe Fonts","url":"https://fonts.adobe.com/fonts/obliqua-sans"},{"title":"JUST Sans Font Family | Download Free Fonts for Desktop & Webfonts","url":"https://www.cufonfonts.com/font/just-sans"},{"title":"Source Sans | Adobe Fonts","url":"https://fonts.adobe.com/fonts/source-sans"},{"title":"Foundry Sans W04 Demi 1.1 Fonts Free Download - OnlineWebFonts.COM","url":"https://www.onlinewebfonts.com/download/5ed3b781ae836bd96075f7da49fe2a3d"},{"title":"JUST Sans Font Family Download | Free Font.Download","url":"https://font.download/font/just-sans"}]

Based on the web search results, I found information about "Just Sans" (also referred to as "JUST Sans") from the font foundry Just Creative. Here's what I found regarding italic, oblique, and webfont licensing:

## Just Sans Font - Licensing Information

Just Sans offers webfonts that allow you to embed the font into a webpage using the @font-face rule, so paragraphs and headings of text can be styled as the webfont. Most foundries on MyFonts offer their webfonts with the Annual license model.

The font is available through MyFonts with multiple license types including:

- **Desktop licenses**: Desktop licenses are based […]

> AGENT

Vou checar a página oficial do MyFonts para ver exatamente quais estilos a família Just Sans tem (se há itálico/oblíquo).

> TOOL

tool_use WebFetch
id: toolu_013J2y68ei5LVMQhtzvUbxiV
```json
{
  "url": "https://www.myfonts.com/collections/just-sans-font-just-creative/",
  "prompt": "List ALL the font styles/weights available in the Just Sans family by Just Creative. Specifically: does it include any Italic or Oblique styles? List every named style (e.g. Thin, Light, Regular, Medium, Bold, ExtraBold, and whether each has an italic counterpart). Report exactly what styles exist and whether italics are offered at all."
}
```

> TOOL

tool_result
id: toolu_013J2y68ei5LVMQhtzvUbxiV
```
# Just Sans Font Styles Available

Based on the webpage content, the Just Sans family includes **8 styles**:

1. Just Sans Extra Light
2. Just Sans Light
3. Just Sans Regular
4. Just Sans Medium
5. Just Sans Semi Bold
6. Just Sans Bold
7. Just Sans Extra Bold
8. Just Sans Variable

## Italic/Oblique Styles

**No italic or oblique variants are mentioned anywhere on the page.** The listing presents only the upright weights listed above. There is no reference to italic counterparts for any of the weights, and the family description emphasizes "7 weights" (excluding the variable font) without mentioning any slanted versions.

The typeface is described as offering "maximum versatility" through its variable version and weight range, but italics are not part of the available offerings for this family.
```

> AGENT

Confirmado — informação decisiva. A fundição **Just Creative não desenha itálico para a Just Sans**. A família tem 8 estilos, todos verticais. Não existe "JustSans-Italic" para comprar nem baixar. Isso elimina a opção de itálico verdadeiro para a fonte do corpo.

Agora o quadro está completo:

- **Franie** (títulos): já tem itálico verdadeiro completo (Regular/Bold + Italic/BoldItalic). ✓ Nada a fazer aqui.
- **Just Sans** (corpo): a fundição **não oferece** itálico. Não tem como obter arquivo verdadeiro.
- **Roboto** (só no SVG da espiral): tem itálico oficial disponível, mas a Roboto não é usada em texto corrido — só em labels da espiral, onde itálico não faz sentido.

Então o "itálico que falta" no projeto é, na prática, o **itálico da Just Sans no corpo do texto** — e ele não existe como fonte desenhada. Com `font-synthesis: none`, hoje o navegador simplesmente não inclina nada.

Restam duas saídas reais. Deixa eu te mostrar a diferença visual, que é o ponto que decide:

> TOOL

tool_use AskUserQuestion
id: toolu_01KK6Aka1WLe92Y2WyWESfYz
```json
{
  "questions": [
    {
      "question": "A Just Sans (fonte do corpo) não tem itálico desenhado pela fundição — não existe arquivo para comprar/baixar. Como você quer resolver o itálico do texto?",
      "header": "Estratégia itálico",
      "multiSelect": false,
      "options": [
        {
          "label": "Oblíquo sintético p/ Just Sans",
          "description": "Permitir que o navegador incline a própria Just Sans (~12°) só quando font-style:italic for pedido. Mantém a mesma fonte/identidade, sem novos arquivos. É oblíquo (reto inclinado), não itálico cursivo verdadeiro — mas a Just Sans nem tem desenho cursivo, então é a aproximação legítima.",
          "preview": "font-synthesis hoje:  texto reto (itálico ignorado)\n\nCom oblíquo sintético:\n  normal  ->  Em 2025, o estudo SINISA\n  italic  ->  /Em 2025, o estudo SINISA/   (inclinado ~12 graus)\n\nMesma fonte Just Sans, só inclinada pelo browser.\nFunciona em todo texto do corpo, automático."
        },
        {
          "label": "Franie itálico p/ ênfase",
          "description": "Onde houver ênfase/citação, trocar a fonte para Franie Italic (que é itálico verdadeiro). Vira um par editorial: corpo Just Sans reto + ênfase em Franie itálico. Mais sofisticado tipograficamente, mas muda a fonte do trecho enfatizado.",
          "preview": "Corpo em Just Sans (reto):\n  Em 2025, o estudo SINISA revelou que\n  /a cobertura/ caiu pela metade.\n             ^^^^^^^^^^^^\n             este trecho em […]

> TOOL

tool_result
id: toolu_01KK6Aka1WLe92Y2WyWESfYz
```
Your questions have been answered: "A Just Sans (fonte do corpo) não tem itálico desenhado pela fundição — não existe arquivo para comprar/baixar. Como você quer resolver o itálico do texto?"="Os dois (recomendado)". You can now continue with these answers in mind.
```

> AGENT

Boa. Então o plano combina os dois caminhos. Deixa eu fechar o último ponto de escopo — onde exatamente o oblíquo sintético deve valer — porque o `font-synthesis: none` hoje é global e tem uma razão de ser (a Franie já tem itálico verdadeiro, e não queremos que o navegador fabrique itálico falso *dela*).

A abordagem técnica correta é **cirúrgica**: manter `font-synthesis: none` no geral (protege a Franie e as variáveis), e **reabilitar a síntese só para a `Just Sans`**. Assim:

- `Just Sans` em itálico → navegador inclina (oblíquo) ✓
- `Franie` em itálico → continua usando o arquivo desenhado verdadeiro ✓
- `Roboto` na espiral → intocada ✓

Uma decisão final sobre o **peso bold em itálico**:

> TOOL

tool_use AskUserQuestion
id: toolu_014FWdPhmHGF8cQDgiJqFRJA
```json
{
  "questions": [
    {
      "question": "Para a Just Sans, o itálico deve valer só no peso normal (400) ou também no negrito (ExBold 800)? Texto em negrito-itálico (ex.: <strong><em>) usaria qual base?",
      "header": "Itálico no bold",
      "multiSelect": false,
      "options": [
        {
          "label": "Ambos os pesos (recomendado)",
          "description": "Oblíquo sintético funciona tanto no Regular (400) quanto no ExBold (800). Negrito-itálico fica negrito inclinado. Cobertura completa, comportamento previsível para qualquer combinação do editor."
        },
        {
          "label": "Só peso normal (400)",
          "description": "Itálico só no corpo regular. Negrito-itálico cairia em negrito reto (sem inclinação). Mais restrito — só faço isso se você não quiser bold inclinado por algum motivo de design."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_014FWdPhmHGF8cQDgiJqFRJA
```
Your questions have been answered: "Para a Just Sans, o itálico deve valer só no peso normal (400) ou também no negrito (ExBold 800)? Texto em negrito-itálico (ex.: <strong><em>) usaria qual base?"="Ambos os pesos (recomendado)". You can now continue with these answers in mind.
```

> AGENT

Tenho tudo. Vou apresentar o design completo.

---

## Design: Incorporar itálico às fontes do Concertação

### Diagnóstico (o que está acontecendo)

O tema declara `font-synthesis: none` em `css/base.css`, o que impede o navegador de fabricar itálico. Combinado com fontes que não têm arquivo itálico, o resultado é que **`font-style: italic` é simplesmente ignorado** no corpo do texto.

| Família | Uso | Itálico hoje | Itálico desenhado existe? |
|---------|-----|:---:|:---:|
| **Franie** | Títulos | ✓ já funciona | ✓ sim (arquivos já no tema) |
| **Just Sans** | Corpo do texto | ✗ ignorado | ✗ **a fundição não desenha** |
| **Roboto** | SVG da espiral | n/a | (irrelevante — labels) |

A "Just Sans" da Just Creative tem 8 estilos, **nenhum itálico** ([confirmado no MyFonts](https://www.myfonts.com/collections/just-sans-font-just-creative/)). Não há arquivo para comprar nem baixar. Logo, itálico verdadeiro para o corpo é tecnicamente impossível — a solução correta é **oblíquo sintético** (o navegador inclina a própria Just Sans).

### Solução (2 camadas, conforme aprovado)

**Camada 1 — Oblíquo sintético cirúrgico para a Just Sans (base universal)**

Em vez de remover o `font-synthesis: none` global (que protege a Franie e variáveis de itálico/bold falsos), reabilito a síntese **apenas […]

> DEVELOPER

sim, dev

> AGENT

Perfeito. Vou registrar o spec, depois implementar e validar em dev. Deixa eu fechar o ciclo de brainstorming escrevendo o design doc e criar as tasks de execução.

> TOOL

tool_use ToolSearch
id: toolu_017bRSP4fqkiZrJJSPPYrmCk
```json
{
  "query": "select:TaskCreate,TaskUpdate",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_017bRSP4fqkiZrJJSPPYrmCk
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

> AGENT

Vou primeiro ler o `base.css` para conhecer o contexto exato onde a regra vai entrar, e ver como o Elementor aplica a Just Sans (preciso checar o kit/global typography para a regra cirúrgica casar certo).

> TOOL

tool_use Read
id: toolu_01Vorz4v9hGHHkQ5PBhnGtpc
```json
{
  "file_path": "/Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/wordpress/wp-content/themes/hello-elementor-child/css/base.css"
}
```

> TOOL

tool_result
id: toolu_01Vorz4v9hGHHkQ5PBhnGtpc
```
1	/*
2	 * base.css — Estilos globais e componentes base do tema
3	 * Extraído de: style.css
4	 * Tema: hello-elementor-child
5	 */
6	
7	/* ==========================================================================
8	   2. ESTILOS GLOBAIS
9	   ========================================================================== */
10	
11	/* --- 2.0 Proibir síntese de pesos/itálicos (fake-bold / fake-italic) ---
12	 * Just Sans só tem fonts reais para 400 e 800. Franie só para 400/700.
13	 * Sem essa regra, o browser sintetiza algoritmicamente pesos como 300, 500,
14	 * 600, 700 (Just Sans) ou 900 (Just Sans) — degrada legibilidade e quebra a
15	 * identidade tipográfica oficial (Manual de Marca §3.9). Com font-synthesis:none,
16	 * o browser cai no peso real mais próximo. Widgets Elementor que solicitam
17	 * pesos inexistentes precisam ser ajustados para valores reais (400/700/800).
18	 */
19	* {
20	    font-synthesis: none;
21	}
22	
23	/* --- 2.1 HTML & Body --- */
24	html {
25	    font-size         : 16px;
26	    scrollbar-gutter  : stable;
27	    scroll-behavior   : smooth;
28	    scrollbar-color   : var(--e-global-color-bbe749d, #C02975) var(--e-global-color-e03d05f, #DEDDD1);
29	    scrollbar-width   : thin;
30	}
31	
32	@media (prefers-reduced-motion: no-preference) {
33	    :has(:target) {
34	        scroll-behavior   : smooth;
35	        scroll-padding-top: 3rem;
36	    }
37 […]

> AGENT

O comentário no `base.css` (linhas 11–18) é muito esclarecedor: o `font-synthesis: none` foi posto deliberadamente para impedir síntese de **pesos** (fake-bold) — o foco era peso, não itálico. Isso reforça que reabilitar **só `style` (itálico) só na Just Sans** é cirúrgico e alinhado à intenção original (continua proibindo fake-bold).

Agora preciso ver exatamente como a Just Sans é aplicada pelo Elementor, para a regra casar. Deixa eu inspecionar o kit global de tipografia.

> TOOL

tool_use Bash
id: toolu_01RESkQXg9YTFMSD8uyU9Qqv
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Onde 'Just Sans' aparece no child theme ===\"\ngrep -rn \"Just Sans\" wordpress/wp-content/themes/hello-elementor-child/ 2>/dev/null | grep -v \"/fonts/\" | head -40\necho\necho \"=== Global typography do kit no DB (qual var usa Just Sans) ===\"\n/Users/dcambria/scripts/server-tools/v2/docker-dev/common/bin/docker-dev.sh wp option get elementor_active_kit 2>/dev/null"
}
```

> TOOL

tool_result
id: toolu_01RESkQXg9YTFMSD8uyU9Qqv
```
=== Onde 'Just Sans' aparece no child theme ===
wordpress/wp-content/themes/hello-elementor-child/functions.php:170: * CUSTOM FONTS: Franie, Just Sans, Roboto (local, no Google Fonts)
wordpress/wp-content/themes/hello-elementor-child/functions.php:218:    font-family: 'Just Sans';
wordpress/wp-content/themes/hello-elementor-child/functions.php:226:    font-family: 'Just Sans';
wordpress/wp-content/themes/hello-elementor-child/functions.php:338:    $additional_fonts['Just Sans'] = 'custom';
wordpress/wp-content/themes/hello-elementor-child/svg/espiral-do-conhecimento.svg:29:                --spiral2026-foreignobject-fontfamily: "Just Sans", Sans-serif;
wordpress/wp-content/themes/hello-elementor-child/svg/espiral-do-conhecimento.svg:160:                font-family: var(--spiral2026-foreignobject-fontfamily, "Just Sans", Sans-serif);
wordpress/wp-content/themes/hello-elementor-child/css/base.css:12: * Just Sans só tem fonts reais para 400 e 800. Franie só para 400/700.
wordpress/wp-content/themes/hello-elementor-child/css/base.css:14: * 600, 700 (Just Sans) ou 900 (Just Sans) — degrada legibilidade e quebra a

=== Global typography do kit no DB (qual var usa Just Sans) ===
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

2553
```

> AGENT

O kit ativo é o `2553` (bate com `.elementor-kit-2553` no CSS). A Just Sans é registrada no Elementor como fonte custom. Deixa eu ver como o Elementor materializa isso no CSS gerado — preciso saber se ele aplica via `font-family` inline ou via variável global de tipografia, para a regra cirúrgica casar. Vou checar o CSS do kit gerado e como widgets recebem a fonte.

> TOOL

tool_use Bash
id: toolu_01CZ56TnwFzxffvm74tU73YR
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Quais containers estão de pé? ===\"\ndocker ps --format '{{.Names}}' 2>/dev/null | grep -i concertacao\necho\necho \"=== Como 'Just Sans' aparece no CSS gerado do Elementor (kit + post css) ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'grep -rl \"Just Sans\" /var/www/html/wp-content/uploads/elementor/css/ 2>/dev/null | head -5'\necho \"---- amostra de ocorrências ----\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'grep -rho \"font-family:[^;}]*Just Sans[^;}]*\" /var/www/html/wp-content/uploads/elementor/css/ 2>/dev/null | sort -u | head -20'"
}
```

> TOOL

tool_result
id: toolu_01CZ56TnwFzxffvm74tU73YR
```
=== Quais containers estão de pé? ===
concertacao-dev-wordpress
totem-concertacao-dev-tileserver
totem-concertacao-dev-nginx
totem-concertacao-dev-wordpress
totem-concertacao-dev-mysql
totem-concertacao-dev-redis
concertacao-dev-nginx
concertacao-dev-redis
concertacao-dev-mysql
concertacao-dev-tileserver
www-concertacao-dev-nginx
www-concertacao-dev-wordpress
www-concertacao-dev-mysql
www-concertacao-dev-redis

=== Como 'Just Sans' aparece no CSS gerado do Elementor (kit + post css) ===
---- amostra de ocorrências ----
```

> AGENT

Não há CSS gerado com "Just Sans" literal — o que significa que o Elementor provavelmente aplica a Just Sans via **variável de tipografia global** (`--e-global-typography-*-font-family`). Deixa eu confirmar como ela é referenciada no CSS gerado e no kit.

> TOOL

tool_use Bash
id: toolu_01NbZ76Kb64FwUrsyqvPmhie
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Definição das vars de typography global no kit ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'grep -rho \"\\-\\-e-global-typography-[a-z0-9_]*-font-family:[^;]*\" /var/www/html/wp-content/uploads/elementor/css/ 2>/dev/null | sort -u'\necho\necho \"=== body / global font-family no kit gerado ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'grep -rho \"font-family:[^;}]*\" /var/www/html/wp-content/uploads/elementor/css/post-2553.css 2>/dev/null | sort -u | head -30'\necho\necho \"=== arquivos css do elementor existentes ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'ls /var/www/html/wp-content/uploads/elementor/css/ 2>/dev/null | head'"
}
```

> TOOL

tool_result
id: toolu_01NbZ76Kb64FwUrsyqvPmhie
```
=== Definição das vars de typography global no kit ===

=== body / global font-family no kit gerado ===

=== arquivos css do elementor existentes ===
```

> AGENT

O diretório de CSS do Elementor está vazio (cache não gerado neste dev, ou caminho diferente). Deixa eu verificar o método de print de CSS e localizar onde o kit guarda a tipografia. Vou checar o post_content/meta do kit 2553 direto no banco.

> TOOL

tool_use Bash
id: toolu_012ULzipzoL5th1Mh7Lg8DAN
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Método de print de CSS do Elementor ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp option get elementor_css_print_method --path=/var/www/html 2>/dev/null\necho\necho \"=== Onde está o CSS do Elementor (procura no FS todo) ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'find /var/www/html/wp-content -type d -name css -path \"*elementor*\" 2>/dev/null'\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'find /var/www/html/wp-content/uploads -name \"post-2553.css\" 2>/dev/null'\necho\necho \"=== Typography global do kit 2553 (system_typography no _elementor_page_settings) ===\"\ndocker exec -u www-data concertacao-dev-wordpress wp eval '\n$kit_id = 2553;\n$s = get_post_meta($kit_id, \"_elementor_page_settings\", true);\nif (is_array($s) && !empty($s[\"system_typography\"])) {\n  foreach ($s[\"system_typography\"] as $t) {\n    $fam = isset($t[\"typography_font_family\"]) ? $t[\"typography_font_family\"] : \"(herda)\";\n    printf(\"%-12s => %s\\n\", $t[\"_id\"], $fam);\n  }\n} else { echo \"system_typography vazio ou formato inesperado\\n\"; }\necho \"----- custom_typography -----\\n\";\nif (is_array($s) && !empty($s[\"custom_typography\"])) {\n  foreach ($s[\"custom_typography\"] as $t) {\n    $fam = isset($t[\"typography_font_family\"]) ? $t[\"typography_font_family\"] : \"(herda)\";\n    printf(\"%-24s => %s\\n\", $t[\"title\"] ?? $t[\"_id\"], $fam);\n  }\n}\n' --path=/var/www/html 2>/dev/null"
}
```

> TOOL

tool_result
id: toolu_012ULzipzoL5th1Mh7Lg8DAN
```
=== Método de print de CSS do Elementor ===
external

=== Onde está o CSS do Elementor (procura no FS todo) ===
/var/www/html/wp-content/cache/min/1/wp-content/plugins/elementor-pro/assets/css
/var/www/html/wp-content/cache/min/1/wp-content/plugins/elementor/assets/css
/var/www/html/wp-content/cache/min/1/wp-content/plugins/elementor/assets/lib/swiper/v8/css
/var/www/html/wp-content/cache/min/1/wp-content/elementor-cache/elementor/css
/var/www/html/wp-content/cache/min/1/wp-content/themes/hello-elementor/assets/css
/var/www/html/wp-content/cache/min/1/wp-content/themes/hello-elementor-child/css
/var/www/html/wp-content/cache/min/2/cultura/wp-content/plugins/elementor-pro/assets/css
/var/www/html/wp-content/cache/min/2/cultura/wp-content/plugins/elementor/assets/css
/var/www/html/wp-content/cache/min/2/cultura/wp-content/plugins/elementor/assets/lib/swiper/v8/css
/var/www/html/wp-content/cache/min/2/cultura/wp-content/elementor-cache/sites/2/elementor/css
/var/www/html/wp-content/cache/min/2/cultura/wp-content/themes/hello-elementor/assets/css
/var/www/html/wp-content/cache/min/2/cultura/wp-content/themes/hello-elementor-child/css
/var/www/html/wp-content/plugins/complianz-gdpr/integrations/plugins/elementor-pro/assets/css
/var/www/html/wp-content/plugins/elementor-pro/modules/loop-builder/files/css
/var/www/html/wp-content/plugins/elementor-pro/assets/css
/var/www/html/wp-content/plugins/elementor/core/files/css
/var/www/html/wp-content/plugins/elementor/assets/css
/var/www/html/wp-content/plugins/elementor/assets/lib/swiper/v8/css
/var/www/html/wp-content/plugins/elementor/assets/lib/e-select2/css
/var/www/html/wp-content/plugins/elementor/assets/lib/eicons/css
/var/www/html/wp-content/plugins/elementor/assets/lib/font-awesome/css
/var/www/html/wp-content/plugins/elementor/assets/lib/e-gallery/css
/var/www/html/wp-content/plugins/jet-menu/integration/plugins/header-footer-elementor/assets/css
/var/www/html/wp-content/plugins/jet-menu/integration/themes/hello-elementor/assets/css
/var/www/html/wp-content/plugins/jet-menu/includes/elementor/assets/editor/css
/var/www/html/wp-content/plugins/events-widgets-for-elementor-and-the-events-calendar/admin/events-addon-page/assets/css
/var/www/html/wp-content/plugins/events-widgets-for-elementor-and-the-events-calendar/admin/cpfm-feedback/css
/var/www/html/wp-content/plugins/events-widgets-for-elementor-and-the-events-calendar/admin/feedback/css
/var/www/html/wp-content/plugins/events-widgets-for-elementor-and-the-events-calendar/admin/feedback-notice/css
/var/www/html/wp-content/plugins/events-widgets-for-elementor-and-the-events-calendar/assets/css
/var/www/html/wp-content/plugins/events-widgets-for-elementor-and-the-events-calendar/assets/lib/css
/var/www/html/wp-content/uploads/elementor/google-fonts/css
/var/www/html/wp-content/uploads/sites/2/elementor/css
/var/www/html/wp-content/elementor/google-fonts/css
/var/www/html/wp-content/elementor-cache/elementor/css
/var/www/html/wp-content/elementor-cache/sites/2/elementor/css
/var/www/html/wp-content/themes/hello-elementor/assets/css
/var/www/html/wp-content/themes/hello-elementor-child/css

=== Typography global do kit 2553 (system_typography no _elementor_page_settings) ===
primary      => Franie
secondary    => Roboto
text         => Just Sans
accent       => Roboto
----- custom_typography -----
Condensado               => Roboto
Just Sans                => Just Sans
Roboto                   => Roboto
Roboto                   => Roboto
Filtro                   => Roboto
Leia também             => Franie
Listing Notícias Excerpt => Roboto
Single Excerpt           => Roboto
Single Título           => Franie
Single Data              => Roboto
Single Texto             => Roboto
Single Frases            => Roboto
```

> AGENT

Informação crucial. A Just Sans é a tipografia **`text`** global do Elementor — ou seja, é a fonte do corpo, aplicada via `--e-global-typography-text-font-family`. Deixa eu confirmar o valor exato dessa variável no CSS gerado, para a regra cirúrgica casar pela variável (mais robusto que casar por `font-family` literal).

> TOOL

tool_use Bash
id: toolu_017epEKTtDcMYbkG6SQEh9CY
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Valor das typography vars no CSS gerado (cache/min) ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'grep -rho \"\\-\\-e-global-typography-text-font-family:[^;]*\" /var/www/html/wp-content/cache/min/ 2>/dev/null | sort -u'\necho\necho \"=== Onde a var text-font-family é APLICADA (quais seletores usam) ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'grep -rho \"font-family:var(\\-\\-e-global-typography-text-font-family[^;)]*)\" /var/www/html/wp-content/cache/min/ 2>/dev/null | sort -u | head'\necho\necho \"=== O kit aplica a text font ao body? (busca no post-2553 / global) ===\"\ndocker exec -u www-data concertacao-dev-wordpress sh -c 'grep -rl \"e-global-typography-text-font-family\" /var/www/html/wp-content/cache/min/ 2>/dev/null | head -5'"
}
```

> TOOL

tool_result
id: toolu_017epEKTtDcMYbkG6SQEh9CY
```
=== Valor das typography vars no CSS gerado (cache/min) ===
--e-global-typography-text-font-family:"Just Sans"

=== Onde a var text-font-family é APLICADA (quais seletores usam) ===
font-family:var(--e-global-typography-text-font-family)

=== O kit aplica a text font ao body? (busca no post-2553 / global) ===
/var/www/html/wp-content/cache/min/1/wp-content/elementor-cache/elementor/css/post-72921.css
/var/www/html/wp-content/cache/min/1/wp-content/elementor-cache/elementor/css/post-75718.css
/var/www/html/wp-content/cache/min/1/wp-content/elementor-cache/elementor/css/post-2553.css
/var/www/html/wp-content/cache/min/1/wp-content/elementor-cache/elementor/css/post-74762.css
/var/www/html/wp-content/cache/min/1/wp-content/elementor-cache/elementor/css/post-52767.css
```

> AGENT

Confirmado de ponta a ponta. A Just Sans é aplicada exclusivamente via `font-family: var(--e-global-typography-text-font-family)`, onde a variável vale `"Just Sans"`. Isso me dá uma âncora **robusta e precisa** para a regra cirúrgica: posso casar elementos cuja `font-family` resolve para essa variável, e também cobrir `<em>/<i>/<cite>` no corpo.

Tenho contexto técnico completo. Vou escrever o spec, depois implementar. Deixa eu criar as tasks e gravar o design doc.

> TOOL

tool_use TaskCreate
id: toolu_01MLiFkmsEKWNaaKCokdGYwe
```json
{
  "subject": "Escrever spec do itálico (Just Sans oblíquo + Franie ênfase)",
  "description": "Gravar docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md e commitar.",
  "activeForm": "Escrevendo o spec do itálico"
}
```

> TOOL

tool_result
id: toolu_01MLiFkmsEKWNaaKCokdGYwe
```
Task #1 created successfully: Escrever spec do itálico (Just Sans oblíquo + Franie ênfase)
```

> TOOL

tool_use TaskCreate
id: toolu_01EjviK4cZGgY4CXdsSEaTaK
```json
{
  "subject": "Implementar regras CSS de itálico no child theme",
  "description": "Em css/base.css: reabilitar font-synthesis:style cirúrgico para Just Sans (via var --e-global-typography-text-font-family + em/i/cite no corpo), nos pesos 400 e 800; manter font-synthesis:none global (protege Franie/fake-bold). Adicionar classe utilitária .bit-emphasis-serif (Franie Italic verdadeiro). Bump de versão no style.css.",
  "activeForm": "Implementando as regras CSS de itálico"
}
```

> TOOL

tool_result
id: toolu_01EjviK4cZGgY4CXdsSEaTaK
```
Task #2 created successfully: Implementar regras CSS de itálico no child theme
```

> TOOL

tool_use TaskCreate
id: toolu_01T4TcGGG7vdgvqFdao3BaXP
```json
{
  "subject": "Validar itálico em dev com Playwright",
  "description": "Flush de cache dev; abrir cambrasmax.local:8484; inserir/usar trecho <em> em Just Sans e confirmar inclinação real (getComputedStyle fontStyle + bounding/screenshot antes-depois). Confirmar que Franie itálico segue usando arquivo verdadeiro (não sintético) e que fake-bold continua proibido.",
  "activeForm": "Validando o itálico em dev"
}
```

> TOOL

tool_result
id: toolu_01T4TcGGG7vdgvqFdao3BaXP
```
Task #3 created successfully: Validar itálico em dev com Playwright
```

> TOOL

tool_use TaskUpdate
id: toolu_01FYHuVwCQ8FeVRSyUMhKAYk
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01FYHuVwCQ8FeVRSyUMhKAYk
```
Updated task #1 status
```

> TOOL

tool_use Write
id: toolu_01Lcs1HBSfwiztsKtBGNgHQN
```json
{
  "file_path": "/Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md",
  "content": "# Incorporar itálico às fontes do site — Design\n\n- **Data:** 2026-06-09\n- **Autor:** Daniel Cambría\n- **Site:** Concertação Amazônica (concertacaoamazonia.com.br)\n- **Ambiente de aplicação inicial:** DEV (`cambrasmax.local:8484`) — **prod só após validação**\n- **Tema:** `hello-elementor-child`\n\n## Problema\n\nTextos que pedem itálico (`<em>`, `<i>`, `<cite>`, itálico configurado no\neditor) aparecem **retos** no corpo do site. A causa é a combinação de dois\nfatores:\n\n1. O child theme declara `font-synthesis: none` em `css/base.css` (regra `* {}`,\n   linhas 19–21). Isso impede o navegador de **fabricar** itálico/oblíquo e\n   negrito. A regra foi posta deliberadamente para impedir **fake-bold** de\n   pesos inexistentes da Just Sans (300/500/600/700/900) — ver comentário\n   2.0 no `base.css`.\n2. A fonte do corpo — **Just Sans** — **não possui itálico desenhado**. A\n   fundição Just Creative oferece 8 estilos da família, **todos verticais**\n   (confirmado em MyFonts, 2026-06-09). Não existe `JustSans-Italic` para\n   comprar ou baixar.\n\nResultado: `font-style: italic` no corpo é silenciosamente ignorado.\n\n### Estado atual das famílias\n\n| Família | Papel | Aplicada via | Itálico desenhado |\n|---------|-------|--------------|:---:|\n| **Franie** | Títulos/display (`primary`) | `--e-global-typography-primary-font-family` | ✓ sim (Regular/Bold + Italic/BoldItalic, arquivos já no tema) |\n| **Just Sans** | Corpo do texto (`text`) | `--e-global-typography-text-font-family` (vale `\"Just Sans\"`) | ✗ **não existe** |\n| **Roboto** | Labels do SVG […]

> TOOL

tool_result
id: toolu_01Lcs1HBSfwiztsKtBGNgHQN
```
File created successfully at: /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md (file state is current in your context — no need to Read it back)
```

> AGENT

Spec self-review: sem placeholders, internamente consistente (escopo, arquivos e validação batem), escopo focado num único plano de implementação, sem ambiguidades. Vou commitar o spec.

> TOOL

tool_use Bash
id: toolu_01LC9HUrpkjrr85x5uDn2C2k
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\ngit add docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md\ngit commit -q -m \"docs(spec): incorporar itálico às fontes (Just Sans oblíquo + Franie ênfase)\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\" && echo \"commitado: $(git rev-parse --short HEAD)\""
}
```

> TOOL

tool_result
id: toolu_01LC9HUrpkjrr85x5uDn2C2k
```
Command running in background with ID: b3n2fu5j4. Output is being written to: /private/tmp/claude-501/-Users-dcambria-scripts-server-tools-v2-docker-dev-sites-concertacao/e2b142ca-5d4d-4a6b-b99f-525ac919d698/tasks/b3n2fu5j4.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> TOOL

tool_use Bash
id: toolu_01HkAvcyH5ogsaE1cYe6CvVJ
```json
{
  "command": "cat /private/tmp/claude-501/-Users-dcambria-scripts-server-tools-v2-docker-dev-sites-concertacao/e2b142ca-5d4d-4a6b-b99f-525ac919d698/tasks/b3n2fu5j4.output 2>/dev/null",
  "description": "Read commit output"
}
```

> TOOL

tool_result
id: toolu_01HkAvcyH5ogsaE1cYe6CvVJ
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01D2XENNRK4A79F7fPxQNQWi
```json
{
  "command": "git log --oneline -1 -- docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md",
  "description": "Confirm spec commit"
}
```

> TOOL

tool_result
id: toolu_01D2XENNRK4A79F7fPxQNQWi
```
(Bash completed with no output)
```

> AGENT

O `git log` retornou vazio — o commit pode não ter ocorrido. Deixa eu verificar o estado.

> TOOL

tool_use Bash
id: toolu_012ZW24yxUht4JECqpqcKw3M
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\ngit log --oneline -3\necho \"--- status do spec ---\"\ngit status --short docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md"
}
```

> TOOL

tool_result
id: toolu_012ZW24yxUht4JECqpqcKw3M
```
47cad4919a docs(mapa-plataformas): formato contador = intervalo [start-item]–[end-item]
1dd998c931 docs(mapa-plataformas): registra fix real custom_query=yes (não use_custom_query)
9ed6056fe1 docs(plan): Mapa de Plataformas — plano de implementação query+contador
--- status do spec ---
A  docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md
```

> AGENT

O spec está apenas **staged** (`A`), não commitado — o commit em background não rodou (provavelmente o `cd` separado dele). Vou commitar diretamente.

> TOOL

tool_use Bash
id: toolu_01Fyo9BJhketsDi49fUsWG4o
```json
{
  "command": "git commit -q -m \"docs(spec): incorporar itálico às fontes (Just Sans oblíquo + Franie ênfase)\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\" -- docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md; git log --oneline -1"
}
```

> TOOL

tool_result
id: toolu_01Fyo9BJhketsDi49fUsWG4o
```
Command running in background with ID: bhzk5edmz. Output is being written to: /private/tmp/claude-501/-Users-dcambria-scripts-server-tools-v2-docker-dev-sites-concertacao/e2b142ca-5d4d-4a6b-b99f-525ac919d698/tasks/bhzk5edmz.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

The commit ran (exit 0). Let me confirm the final state — both background commits may have raced.

> TOOL

tool_use Bash
id: toolu_01XVQ67QgA4LhngNRRcx5tc3
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\ngit log --oneline -2\necho \"--- spec ainda staged? ---\"\ngit status --short docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md || echo \"(limpo)\""
}
```

> TOOL

tool_result
id: toolu_01XVQ67QgA4LhngNRRcx5tc3
```
f879721237 docs(spec): incorporar itálico às fontes (Just Sans oblíquo + Franie ênfase)
47cad4919a docs(mapa-plataformas): formato contador = intervalo [start-item]–[end-item]
--- spec ainda staged? ---
```

> AGENT

Spec commitado (`f879721237`), working tree limpo. Task 1 concluída.

Agora, conforme o fluxo de brainstorming, o próximo passo formal é o **gate de revisão do spec** por você antes de eu partir para a implementação.

> TOOL

tool_use TaskUpdate
id: toolu_01Viyv6bRZPTyNee7xCVtiPp
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_01Viyv6bRZPTyNee7xCVtiPp
```
Updated task #1 status
```

> AGENT

Spec escrito e commitado em `docs/superpowers/specs/2026-06-09-incorporar-italico-fontes-design.md` (commit `f879721237`).

**Resumo do que ficou definido:**

- **Just Sans** (corpo): não tem itálico desenhado pela fundição → oblíquo sintético cirúrgico (`font-synthesis: style`, só itálico, ambos os pesos 400/800), mantendo `font-synthesis: none` global para continuar barrando fake-bold.
- **Franie** (títulos): já funciona, intocada — e exposta via classe `.bit-emphasis-serif` para ênfase editorial com itálico verdadeiro.
- Aplicação só no **child theme CSS**, validada em **dev** antes de qualquer prod.

Dá uma olhada no spec e me diz se quer ajustar algo antes de eu escrever o plano de implementação. Se estiver de acordo, sigo para o plano e depois para a implementação + validação em dev.

> AGENT

O segundo commit em background terminou sem efeito (o spec já tinha sido commitado pelo primeiro — `git log` mostrou que não havia nada a commitar). Estado final confirmado: spec commitado em `f879721237`, working tree limpo. Sem duplicação.

Aguardo sua revisão do spec para seguir ao plano de implementação. Se preferir que eu já avance direto para a implementação em dev (o spec é curto e você já aprovou a abordagem nas perguntas), é só dizer.

> DEVELOPER

abra na tela pra eu verificar

> AGENT

Vou subir o ambiente (se necessário), abrir o site em dev no navegador e te mostrar o estado atual do itálico — assim você verifica o problema antes de eu aplicar o fix. Deixa eu primeiro confirmar que o container está acessível e preparar uma página com texto em itálico para comparação.

> TOOL

tool_use Bash
id: toolu_01Gg3Nr4KeGJLnVWSp3oMSB1
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\necho \"=== Container WP up? ===\"\ndocker ps --format '{{.Names}} {{.Status}}' | grep '^concertacao-dev-wordpress'\necho\necho \"=== Site responde em dev? ===\"\ncurl -sk -o /dev/null -w \"HTTP %{http_code} em %{time_total}s\\n\" https://cambrasmax.local:8484/ 2>&1 | head -1"
}
```

> TOOL

tool_result
id: toolu_01Gg3Nr4KeGJLnVWSp3oMSB1
```
=== Container WP up? ===
concertacao-dev-wordpress Up 6 days (healthy)

=== Site responde em dev? ===
HTTP 200 em 2.591931s
```

> AGENT

Container saudável, site respondendo. Vou abrir o navegador e montar uma comparação ao vivo: a mesma frase em Just Sans, uma versão normal e uma com `<em>` (itálico). Hoje, com `font-synthesis: none`, o itálico deve aparecer **reto** — é exatamente o problema que você relatou. Deixa eu carregar o site e injetar esse comparativo na própria página para você ver com a fonte real do tema.

> TOOL

tool_use ToolSearch
id: toolu_01VWfrnHpxUDLJZVLxiCjPLL
```json
{
  "query": "select:mcp__playwright__browser_navigate,mcp__playwright__browser_evaluate,mcp__playwright__browser_take_screenshot,mcp__playwright__browser_resize",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_01VWfrnHpxUDLJZVLxiCjPLL
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
  "tool_name": "mcp__playwright__browser_take_screenshot"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__playwright__browser_resize"
}
```

> TOOL

tool_use mcp__playwright__browser_navigate
id: toolu_015QdMthbmmuFpfq4NZazvGR
```json
{
  "url": "https://cambrasmax.local:8484/"
}
```

> TOOL

tool_result
id: toolu_015QdMthbmmuFpfq4NZazvGR
```
### Ran Playwright code
```js
await page.goto('https://cambrasmax.local:8484/');
```
### Page
- Page URL: https://cambrasmax.local:8484/
- Page Title: Uma Concertação pela Amazônia
- Console: 4 errors, 1 warnings
### Snapshot
- [Snapshot](.playwright-mcp/page-2026-06-10T01-03-58-568Z.yml)
### Events
- New console entries: .playwright-mcp/console-2026-06-10T01-03-54-061Z.log#L1-L7
```

> AGENT

Página carregada. Agora vou injetar um painel comparativo no topo da página, usando a fonte real do tema (Just Sans via a variável global), mostrando lado a lado: normal vs. itálico (estado atual, antes do fix), e também como ficaria a Franie em itálico. Vou medir e exibir o `font-style` computado de cada um para evidenciar o problema.

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01TBmSrQyHNeTZpccfdQhthg
```json
{
  "function": "() => {\n  // Remove painel anterior se existir\n  const prev = document.getElementById('bit-italic-demo');\n  if (prev) prev.remove();\n\n  const panel = document.createElement('div');\n  panel.id = 'bit-italic-demo';\n  panel.style.cssText = [\n    'position:fixed','top:0','left:0','right:0','z-index:999999',\n    'background:#1d1f21','color:#f5f5f0','padding:20px 28px',\n    'font-family:var(--e-global-typography-text-font-family,\"Just Sans\"),sans-serif',\n    'font-size:18px','line-height:1.6','box-shadow:0 6px 24px rgba(0,0,0,.4)',\n    'max-height:100vh','overflow:auto'\n  ].join(';');\n\n  panel.innerHTML = `\n    <div style=\"font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#e7dd6d;margin-bottom:14px\">\n      Estado ATUAL do itálico (antes do fix) — fonte do corpo: Just Sans\n    </div>\n\n    <div style=\"display:grid;grid-template-columns:170px 1fr;gap:6px 18px;align-items:baseline\">\n      <div style=\"color:#9aa\">Just Sans normal:</div>\n      <div class=\"demo-justsans-normal\">Em 2025, o estudo SINISA revelou dados sobre saneamento.</div>\n\n      <div style=\"color:#9aa\">Just Sans &lt;em&gt;:</div>\n      <div><em class=\"demo-justsans-em\">Em 2025, o estudo SINISA revelou dados sobre saneamento.</em></div>\n\n      <div style=\"color:#9aa\">Just Sans &lt;strong&gt;&lt;em&gt;:</div>\n      <div><strong><em class=\"demo-justsans-bolditalic\">Em 2025, o estudo SINISA revelou dados.</em></strong></div>\n\n      <div style=\"grid-column:1/-1;height:1px;background:#444;margin:8px 0\"></div>\n\n      <div style=\"color:#9aa\">Franie normal:</div>\n      <div style=\"font-family:'Franie',serif\" class=\"demo-franie-normal\">Uma Concertação pela Amazônia</div>\n\n      <div style=\"color:#9aa\">Franie itálico:</div>\n      <div style=\"font-family:'Franie',serif;font-style:italic\" class=\"demo-franie-italic\">Uma Concertação pela Amazônia</div>\n    </div>\n\n    <div id=\"bit-italic-readout\" style=\"margin-top:16px;font-family:monospace;font-size:13px;color:#7fd17f;white-space:pre\"></div>\n  `;\n  document.body.prepend(panel);\n\n  // Leitura do estado computado\n  const read = (sel) => {\n    const el = panel.querySelector(sel);\n    const cs = getComputedStyle(el);\n    return { fontStyle: cs.fontStyle, fontFamily: cs.fontFamily.split(',')[0].replace(/[\"']/g,''), synthesis: cs.fontSynthesis || cs.fontSynthesisStyle || '(n/a)' };\n  };\n\n  const r = {\n    justsans_em: read('.demo-justsans-em'),\n    justsans_bolditalic: read('.demo-justsans-bolditalic'),\n    franie_italic: read('.demo-franie-italic'),\n  };\n\n  const out = panel.querySelector('#bit-italic-readout');\n  out.textContent =\n    `Just Sans <em>          -> font-style: ${r.justsans_em.fontStyle.padEnd(8)} | font: ${r.justsans_em.fontFamily} | font-synthesis: ${r.justsans_em.synthesis}\\n` +\n    `Just Sans <strong><em> […]

> TOOL

tool_result
id: toolu_01TBmSrQyHNeTZpccfdQhthg
```
### Result
{
  "justsans_em": {
    "fontStyle": "italic",
    "fontFamily": "Just Sans",
    "synthesis": "none"
  },
  "justsans_bolditalic": {
    "fontStyle": "italic",
    "fontFamily": "Just Sans",
    "synthesis": "none"
  },
  "franie_italic": {
    "fontStyle": "italic",
    "fontFamily": "Franie",
    "synthesis": "none"
  }
}
### Ran Playwright code
```js
await page.evaluate('() => {\n  // Remove painel anterior se existir\n  const prev = document.getElementById(\'bit-italic-demo\');\n  if (prev) prev.remove();\n\n  const panel = document.createElement(\'div\');\n  panel.id = \'bit-italic-demo\';\n  panel.style.cssText = [\n    \'position:fixed\',\'top:0\',\'left:0\',\'right:0\',\'z-index:999999\',\n    \'background:#1d1f21\',\'color:#f5f5f0\',\'padding:20px 28px\',\n    \'font-family:var(--e-global-typography-text-font-family,"Just Sans"),sans-serif\',\n    \'font-size:18px\',\'line-height:1.6\',\'box-shadow:0 6px 24px rgba(0,0,0,.4)\',\n    \'max-height:100vh\',\'overflow:auto\'\n  ].join(\';\');\n\n  panel.innerHTML = `\n    <div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#e7dd6d;margin-bottom:14px">\n      Estado ATUAL do itálico (antes do fix) — fonte do corpo: Just Sans\n    </div>\n\n    <div style="display:grid;grid-template-columns:170px 1fr;gap:6px 18px;align-items:baseline">\n      <div style="color:#9aa">Just Sans normal:</div>\n      <div class="demo-justsans-normal">Em 2025, o estudo SINISA revelou dados sobre saneamento.</div>\n\n      <div style="color:#9aa">Just Sans &lt;em&gt;:</div>\n      <div><em class="demo-justsans-em">Em 2025, o estudo SINISA revelou dados sobre saneamento.</em></div>\n\n      <div style="color:#9aa">Just Sans &lt;strong&gt;&lt;em&gt;:</div>\n      <div><strong><em class="demo-justsans-bolditalic">Em 2025, o estudo SINISA revelou dados.</em></strong></div>\n\n      <div style="grid-column:1/-1;height:1px;background:#444;margin:8px 0"></div>\n\n      <div style="color:#9aa">Franie normal:</div>\n      <div style="font-family:\'Franie\',serif" class="demo-franie-normal">Uma Concertação pela Amazônia</div>\n\n      <div style="color:#9aa">Franie itálico:</div>\n      <div style="font-family:\'Franie\',serif;font-style:italic" class="demo-franie-italic">Uma Concertação pela Amazônia</div>\n    </div>\n\n    <div id="bit-italic-readout" style="margin-top:16px;font-family:monospace;font-size:13px;color:#7fd17f;white-space:pre"></div>\n  `;\n  document.body.prepend(panel);\n\n  // Leitura do estado computado\n  const read = (sel) => {\n    const el = panel.querySelector(sel);\n    const cs = getComputedStyle(el);\n    return { fontStyle: cs.fontStyle, fontFamily: cs.fontFamily.split(\',\')[0].replace(/["\']/g,\'\'), synthesis: cs.fontSynthesis || cs.fontSynthesisStyle || […]

> AGENT

O painel está montado. O readout confirma o diagnóstico: a Just Sans em `<em>` tem `font-style: italic` **pedido**, mas `font-synthesis: none` → o navegador não inclina. Vou tirar o screenshot pra você ver visualmente que o itálico da Just Sans aparece **reto**, enquanto a Franie itálico (que tem arquivo real) inclina de verdade.

> TOOL

tool_use mcp__playwright__browser_take_screenshot
id: toolu_011vHXi6eWZ4aihnwhUJkabU
```json
{
  "type": "png",
  "element": "Painel de demonstração do itálico no topo",
  "target": "#bit-italic-demo",
  "filename": "italico-antes.png"
}
```

> TOOL

tool_result
id: toolu_011vHXi6eWZ4aihnwhUJkabU
```
### Result
- [Screenshot of Painel de demonstração do itálico no topo](./italico-antes.png)
### Ran Playwright code
```js
// Screenshot Painel de demonstração do itálico no topo and save it as ./italico-antes.png
await page.locator('#bit-italic-demo').screenshot({
  path: './italico-antes.png',
  scale: 'css',
  type: 'png'
});
```
### Page
- Page URL: https://cambrasmax.local:8484/
- Page Title: Uma Concertação pela Amazônia
- Console: 4 errors, 4 warnings
### Events
- New console entries: .playwright-mcp/console-2026-06-10T01-03-54-061Z.log#L9-L10
```

> AGENT

Deixa eu ver o screenshot.

> TOOL

tool_use Read
id: toolu_01NRerdv2jY6xLBbFcZHG84i
```json
{
  "file_path": "/Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/.playwright-mcp/italico-antes.png"
}
```

> TOOL

tool_result ERROR
id: toolu_01NRerdv2jY6xLBbFcZHG84i
```
File does not exist. Note: your current working directory is /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao.
```

> TOOL

tool_use Bash
id: toolu_013zz22Dcp4Ghqgxvn1C66dA
```json
{
  "command": "cd /Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao\nfind . -name \"italico-antes.png\" 2>/dev/null; ls -la .playwright-mcp/ 2>/dev/null | tail -5"
}
```

> TOOL

tool_result
id: toolu_013zz22Dcp4Ghqgxvn1C66dA
```
./italico-antes.png
-rw-r--r--@    1 dcambria  staff    783896  1 dez  2025 sobre-nos-final.png
-rw-r--r--@    1 dcambria  staff     83402  3 fev 00:35 sobre-nos-full.png
-rw-r--r--@    1 dcambria  staff    100281  1 dez  2025 sobre-nos.png
-rw-r--r--@    1 dcambria  staff      1822 23 mai 02:18 uma-concertacao-pela-amazonia-2a981d5c2e0.ics
-rw-r--r--@    1 dcambria  staff   2538514 27 mai 19:18 Versao-Final-de-Estudo-da-GO-Associados-Ranking-do-Saneamento-de-2025-Rio-Corrigido-V4.pdf
```

> TOOL

tool_use Read
id: toolu_01DLwxGkiARgxSfCr8WgJX2E
```json
{
  "file_path": "/Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/italico-antes.png"
}
```

> TOOL

tool_result
id: toolu_01DLwxGkiARgxSfCr8WgJX2E
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "iVBORw0KGgoAAAANSUhEUgAABLAAAAF3CAIAAAA6liUzAAAQAElEQVR4nOydB1wURwPFl16lg6CiIGIXsffee+8l9liSqClqorElMZrYe4k1tthb7L33rgh2BQFFEFApCnzvbmRz3h3n0RQ/3j/3M3tbZmdnZo9586YYS51rS4QQQgghhBBCsh+GEiGEEEIIIYSQbAkFISGEEEIIIYRkUygICSGEEEIIISSbQkFICCGEEEIIIdkUCkJCCCGEEEIIyaZQEBJCCCGEEEJINoWCkBBCCCGEEEKyKRSEhBBCCCGEEJJNoSAkhBBCCCGEkGwKBSEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTaEgJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJplAQEkIIIYQQQkg2hYKQEEIIIYQQQrIpFISEEEIIIYQQkk2hICSEEEIIIYSQbAoFISGEEEIIIYRkUygICSGEEEIIISSbQkFICCGEEEIIIdkUCkJCCCGEEEIIyaYYSSU8pSxMzSIlPZxde9RoiO0HYaHyTnmbEEIIIYQQQkjaMJayNmPafAH5h43DNy+LPfh6aNRUxR6/K7V+/VYihBBCCCGEEJImslCXUSi9pFUH8BF6L7XXSoQQQgghhBBCUkMWEoRw/PCRPqTuahb1FRtHlCcLYCRCSY5t84VECCGEEEIIIUQ/PrEgTEnCyZpQVfWpodqJVJw/pnV3akJCCCGEEEII0ZNPKQjh6UHCqe4Zt3G52jmy6pOpkawVDydrRdkzHLdpxViNEAghhBBCCCGEaOVTCkLoN/x7aNRU2daTNd4YDaPv8PtWobj23cnJqlJVDXJUISGEEEIIIYTo5lMKQqHfoNxUfUJVpSdp6EBJQ+nJYlL1QuyEzkzD5DSEEEIIIYQQkn34xGMIZRX3n0mo7CMqDwtMCdkMFGISulHeg6DETnmBCkIIIYQQQgghmnxUQQippjbpC1Sc8ABlk1Cea1RG9atQiZoyUnXwoWpQaV6oUFWOsvcpIYQQQggh5P+SjycIIatqKHuHqmlCWbOpqbsxes8XCn0oi0bZEsTO9CxbP0ZFuyJMWRNSHBJCCCGEEEL+bzCWPhYK6+/Xb0V/TjFTqCzYsAHRhf2Hb14WDqGqK3jE74qqDFPtHSrMQNXOorKFqDbBTM2ivumcgFSWhfJiicKBlHuoHlbG06BLHYkQQgghhBBCPgc+9hhCqDKoNTFEUHVyUdELdIyKSSiLQFwiqyy1XqC4SrX7qBBmampQTDCDQ+k39xAyYoJwjiijIZ4CIYv9OpZMJIQQQgghhJAsyCeYVEZoQun9deTFYEJ5Lhk1kzClHpu4Ss0tVFODQgq+OyEda9arRkYRN6WT+d8e5UQ4mksmEkIIIYQQQkhW5mN0GVXMJfN+d03xFVJNtc/nu46jbb44rPQAUzsCUIhM+UYK7y65B6kkTMjUdBnFyWM0psDRikLHFvVV3FH5LyGEEEIIIeRzxMrMvGKBoiXz5vdyze1m62BtboGdL2NjgiPD74YEXXl07/Sdm6/iYqX/L4ykEp5SZiJ6choYGGjOHXrE70qP6g0U4+6Sjz58FoLzsf9BWCj2ezi7YgP7l/YfvvzoHmz0qNFQnInTNAOU9+Do0i+H4XKxv+eCPyAXRVB6gpM9nV1rKOOAy8VXERo2HjwLUcSwqO8RZWdXbHxRvYGIrYgnIYQQQggh5HPB08WtV/WGo1p2NTCQbgQ92Hn5zN8n9i0+vPPv4/t2Xjl7M/AhBEuFAkV+aNrB2cY2JDLixauX0v8LBlLn2lJmIkw2uT/nu53vj/ETw/DEToXSS+6QCcNQDNWDWSemb5Gv1XQd1QKUkl3BwxzaRwghhBBCCEmBfrWbNixZbsOZo9svnYqOea3jzBwWls1KVWpbofruK+cWHtwh/V+Q6V1G3+m3jcuh08TkoqIb539TgyZ3H5WSxwSqun9aZ4IRolHHHWso533RVIwZMt0oSTOqE/+IDU7KSgghhBBCPhWezq7fN+1wN/TJF/Mn6ZaCApyz+uSB7RdP9a3dZE7PwZN3/HP/WYj0mZPpDqEasiSQ3p8ABlJN+IFiahlhCYpFBeHyYQPKIWnVAYVhWNQXek+MMBSXfPCmQgfWSJ6xRtxFIh8d5KDqV7U5YwkhhBBCCPloFHf3HN+mx9KjuyHwpNTTrHSlntUbjt647Prj+9LnTKaPIVRDrDBhYGAgJhSFTnuoHI+HD/aLIYLY7lG9AfT68qN7ICAfKscT4kwP5Z6lXw5bfmwvToMaPPL+ZKSa4MKl/YeL9QnFkEKAQFI1npBkCMgCZOURZT/eh8r0xwYzghBCCCGEfHygNSZ26Dtr7+Y9V89LaSIgOPBp1IsRzTqdvXvrxevPeEjhx1uYXhW5a2gNpTEoW4WHb16GiaRYXVDpCoouprKjKCXP5CmfJo8nlN4fl/juLipupCC1xqBwFMV6FWKZwZS6mwpXU2xrPVPuMSsphZDq/Ddiv9pwR9VbizB1BKiGOFnzBBExeYimjhDU7iisWq29cPWMrZQ8648iU5Sn6RjeqZaYaot8EEIIIYQQkk6+b9oB3uCh9K0bh8utzS0Q1KClM6TPlkzsMirPFiOlrKOk5P6cOFPuLyokYg2VNQmlZDEjj0IUvQ3FLVLqAiqCEodSO7uM2qoVqqgtdSgp9dIHz1RVp6pdJVWH1Wk9OaUAU7qpHH5Kgcjh6AhBNZKq4WgmdaoSSlLpNaq1v6jIMinlOEuEEEIIIYSkj361m0LITd25XsoIvm3c7mVszOc7x0wmOoQwdqDfhJYQylBoPLHghGz7vDOOhD4R4i15xhEphfF+wtqCtBCiIiWlh/1pnrNEVZYImSp/VV07UXp/XJyIiXwyzpSHO6pSMzkdJG2oSUe1ACWd6lpPEA7S/4iGISmpmKjyUVVVKa8SKaN/QknJXq58R7VEUFOwmfTshBBCCCEkO+Pp4tawZLkv5k2SMohFh/5d3n/4vusX7j8Nlj5DMlMQQumpiAdF7f/m5ZpKV6pmslBU9Q81Ta2UxJ7oDylOQFBCH2Zg30JZt6guXCE7mZJSnKj2VpU0lriQHyQl7aeprNQulN5/fHm/0HKqAX5wjhzt4Sin7ZHPkWWtmnxVlXCSxqSv+ieUVtQSQVUGa01MzWcnhBBCCCEkVbQqW2XDmaPRsR+eU1RPomNeI8BWZapM3bVB+gz5eGMIRT0elp0QFWI0oKTsBSoGBEpKU1HswTnYo6PqD5lRU3mh9KH1BuXbyePlROC6hIqKJFONPz5yR1Yh87SeKaKHZxHumVbtp9sklJRS+T33TGVxjpTEpD4gnJT6kepGnvRVNdr6JJTqTLDy+pBScgr8F7FkbamZNWIdER29W0nWxNHapkmpinkdXW49eXTy9o0nEc8/eMmXdZrO7zXUuleTV3GxUkZQJHfeCl5Ftl889fxllLzTztK6ZdkqB29cevT8qerJS/r9ULd4mcpjvw4MfyZlbSoXLNa+Qs0hf8+RPiJIzOHNOgUEP56zb+u3jdo9CAtZemS3lIWxNDWrXsSnZF4vlL1Tt2/eCQ2S0kHfWk0W9vk2owpn8Tye5bwKZfEE/MgUzpW3kndR5xy25+75n7nj9zo+7oOXnBo3KzA8rN2McdL/I2lIEEKIPliZmTf0Kd9mxlgpQ9l+6dTGwWMXHNyRUXWYj8knmFRG7imqtl9t/NgHOwfq2SM0pRFuKSGfLDSqGlCeklK6QGHKmlbrmSktpSh3iNWq62SJpWWOHOUe1bUc34WvEpOUrv3v0Psz33wQWcL9JwKTo61nQh1RMfrkWwuvWFKRlzV05hFCq5myuiZZkOalK/898MfYN/F+QQ/71W6ay96x719TPn71FwJvZvev1pw82HnOb/LO3A5OS78c1nraGFVB2MCnXPMylauNH5z11SBY3Pd7VBbXnDqIaqK8094qx9BGbVafPAgFLmUCy74cfvHB7UJu7s8XbIl4FV113GApC1PC3XP94DHuji6XH9xxtXPI7+KWpcYhd6xUa0Dd5iuO7U1ITJQymW8bt/ULerTrylkpq2JoYDC+bc8fW3R+GBYaHPEcv/NPIyNq//Zdqpb2al2uWk5b+3n7t0mfPxmSIGqU8ijQqmzVCVtX42c5o84k5DOlYoGiJwKu67PkYKpAgAgWgR+4cVH63Pg0s4xqRQwIFNNL6i/hxMwoYlyipDKFpoysJfRETVxpRvKwynwwkk7kMXWqjyOGVtZM/qR0odb9qrWZMfLGh2ZS1TpNiz4VIzX1KB5H9jb1Tyi1eL73FBoCT2vE2E308wLOzMpBP+67dqHjrF/fJLzFnmFNO0DDXH98H03d0kenU+Xa0E66lxgKfxlVacxXt0PSZSJ9HCDJoAYhJHrVaKgqCO0srX5u1e3C/duZJAiHrpx79u6ttwkJQ/6e+zI2RuRs1sTMxGTbd78GRYRVGfuNMIe7Vq27ov+I2yGBq04ckLIAo9Yv+XXLyo+gBsHghm02nTuWlQVh39pNRjTv1H3e7yJ3bCwsD46csmfEHwW/S0V/lhZlKvvkzf//IQgzJEHU8M1XAL8PU3au/6DM0/9MQj5TSubNj/ZNKRNAsAicgvA9hJw4nDyXq9xRUFOfyHJOMbVMKnsGimGEOgSDppGop9o8/KFZaHGC7u6XR96fZEVG1e/SOrNLZqPV09NETcKlx6ZT7REqNtTkpZ7hsOPoZ0GR3PlymFv+fXyfrBmm7do4sF6LqoVKCEGI9m8055f3Khz+Knr3lXOXH95RvdzGwqpH9QZeOXNdfXQP9SERCKp69UuUXX3ywBfVGjyLfvHXoZ3YWSBn7jblqzlY20AXbT5/PCkpSWt88AM9v9fQo7euRr5+pfWEqoWK1ylW2sTIGG17qvVmAwODlmWqVC5YDBfiVT3mf03KAvSs0TAgOHDarg2TOvUb+vdc0ZEMlmwDn7LY+L5Je1c7+wUHdqCZHw+FWp1IFpi0nSvXQQKKvru2llZdq9T1ds0DC2LbxZN3Q5/I4bvZOaJujUNXH93dfulU+Mtosf9G4IMvazfVeomdpXW7CjWK5M6LncgIfboHZyq9azbO55Sz0R8/yl2FVx7f/02D1h0q1pIFodZMh8vau2YjpFLJvF5o84qJj1tyeJeqkwyp2b5iTZTGh89CFx36V7VfEAJsVLJC3Nt4NIWcun1T3o+T4T875bA9dfvGjkunoaixs1qhEiXy5p+7b6ukXNfY1NgEbwFeCmTTUb+rSEMXG7uOlWrD2ESyLzu6R36V8O4gqct7FYGVveX8cWEZpRRtUQbyOroMadgmKDwMb41YJiulAv9JwBONbf3FutOH5ayJink9esOyf3+YUNrDGy/voHotLj+8i6iKo23LV8e/G84elUNA2uIXo3u1+pKy/O+5eu7aQhOa+wAAEABJREFU4/spXSXSCilcr3gZD2fXEWsXScpfkrYVqsNgvBn48J/Th6Iy2jdIFR9MECnlN65JqYoWJqbHA653rFgLT3f6zs1/Th/GLwBSA7/AkjJ9UDh3Xj4jpfAjoPXMrPaCE5JOvFxz/6ss21rZO+KP3A5OMcq/rfjNrDvhB+y59zS4/5JpkvKvgN+fy/IP6aL1Wvx1bliyvPQZkomCUJ4IRFLW/seIboQqy0gIxaVu6CX3qNRTJ7yTnalxkHSfLMu8lGSPvCifrBhT6u5YQ2XqTlU/TfTA1HQIP/gUspZWHbP3wUllhN6W1Z2e/aZU/U/VmVSlZFUmJ1RKj681trhETUWLdD6i4qbqHlopkSzPndCg+Ldvu1WtB7En2phRnfUY3FkchX+444cJqKruvXoemvCXtj2/XTVv1p7N8uWnx8/GT2r82zcD6jaHsVP/92GJSUkVvIr82flL1OnfJibA7pCU1eg1X406f88fqhKVGFS1O876RWt8BiyZjtI4pcuAPosmax6d2LHvd43b7bt+Ie7Nm28bt91y/kSXuROEiFo9aGTTUhXxZ6N4HqvxbXuMXLfk922rpU+KkaFh92r15u3fjnrejO5ftSlfHcIb+wu45iqbvxA2yuYvCCEnKSr9JZBi0I0JymeBQMJX1I9RmUP198TYmc+jo44HXENoeCXrTxwG9w+nlfEsuHPY7zh04X4AfgRGtuxaZ8J3j58/03EJ7Mpdw37HPU74X2/oU35c2x4tp/583P+69Omo4FXY78kjNae0x/xJUA5iO6VMd8phg1RC0YVYuh54Hz9uX9VvCVtGVsWHR02LeBWNz8C6LZqXqVz7t+/E/l/a9RzWtOOOS6fQPPFzy26D/54jxB7U+4LeQ1GxDn4R3q92E7RKtJsxDm9HY98KfWo1FuegUo58fPAsBJrQXSneFh/eheYPfEV2f92gVX2fsmKYnKmxMXLHxz0/Yl7fpwxyoeGkEaj0pxRtKBxkqIghNkRR0VHgPwkoma52DpAZqjvRvt5g4vDQyAhsj2/bc+7+rbK0g3smvS8I8ZOi+pgoujquEmk1rGkHfL0R9BD/IvHXfDXyRMCNe0+fjGnTfXDD1tXGD0EWS5+IDyaIjjeuc+XaELrRsTFoR4Dew7MUcnPH381SHt5Fc+fDCWU9C4W8CJeUGljrG615ZhZ8wQlJJ262Dk9e6GrXaD9zPF4i1T2ocqC16IMrFiJYBC59hmSiIFRMi6JtTsiUzCVZZkhCNuhnQ4n1KvDRvXB8GtBqRo1NHpF4RCnqdNhc8pla5Y3stmlqwg8GmFrkGXd067dU8d4gRp2xFRJOh5WqJi+15vsHe+eSLAX8NEivRX2+uz11BZwZGBdosJePftekfbn8hcqM6g/Vh68jW3aZ0qX/7itn5e6aE7etEf2+GpUsj+ovqmvrzxwRh7BfSDLUdf7q+z0sGlhkUnLXg4UHdxy8cUkzPmjVHvnP4mndBq49dXD/9fc6clQv7DO8WcfOc35bc/KgpPRtjvw8DQ7D8mN7PZ1dO1aq1WXOBMQfh35r3/unFp2n7FyH2rz06UDTo6utw8rj+1BhhfzoVbORqOVP3blh87nj96av6jjr160XTugOBJVjyI9q4wfjWRQSYtLiXjUaCXU3t+fgm0EPIcKh4WHzXpwwH0bB4BVzdFwyp8c30OQ1fhn6MjbG2Mho23e/Luk3rNiwXp+wTykqu4/fnzEI3FTW/iWdmS5O8HRxte/bIiExEebeld8XNStVST606sT+SdvXYgNtEzO6D0LdHe4KPOSRLbq0mjZGpDx+ryZ27LP6xAETY+OZ3b/6Y/s/o9YvkZQTyVyZuKiJb0W1ur6k1PlIwKCIMGzvGjYRFlaHWb/AI8LX0a27jWvTAxYNGqq/a9webShIW0h02NcHfpr8R+d+1ccP0RFtNMogemhDEW/KB5/941PANTf+xROp7oRY3XvtvJ4hwAvtNPtXNCHhwbGhzyWwZJ37txZFFKoJ3ulA5YrSyNAHM1bDbF976pD0ifhgguh+45xt7NBMIIzETUPHwTvFX2H8IEMbL+n3Q8fZv4iOEim90ZpnZsEXnJB0Ym1ukdoBhEPQzNdzcJmR/ROSdHX1R7AIXPoMMZQyjbF6rAUvFo0Qik5SWZPw3XIUOmWA7LDBgFIsWbFxuZoalEULDC5xCwT4QVmlOoGKWu9W1TUh1O41Rhmy6q3lM7VO36J6F1XGqaw7n1KAaXPJxqosC6GPvlK9nern3VHINr8rql9Vw1RLqPdWp9AWmqqe1IyejmQnWRaolOLDe2+9cBLVjqsT/zozfo7chN+lSp01pw4KNQim/LsedZ12FWqoXis2dl05i9NglciHZu19ZyTWLlrKxcZu8o514ivKDyqFdYqVTik+M/dsgksDjWplZq66v3PlOhCionIMjvlfO3DjUpcqdSVlNy3UeOoUL+VobYOvP69foqxBJkiflF41GsLKEB0FkVA1Cvvkd3GTUsnwNQsrjB6EiiAcs9wOToHhz1CTxn53R2fojdl7t4iqXnTsa5irZ+7c0nEJrIzaxUohE1FZxNe3CQm/bVnl7Zq7nFch6dNhaWamY/iTjkwXjFq3VIzuu/roHsKBaycfmrvv3RA1IYaRYvi3Q8Wad58+kXX48qN7oKWRAg19yqFmMC15CnJ4d6hth0VHqsUnh4Ul/hVqEMCxwb/CBgenbyuGieZ1UsQBLRT/nDospAI8PRSAqgWLm5mYfDDa+j/7x8fSVPFKfuThahO2rpL1DBQ11KChgYGbnSNk9uv4OFG2PxW6E0T3GwdpJyk7yYuTUUq1FgMp5Tc6Vbcj5P+VFQNGHBs9A5++tZqIPTAMV5048FuH3tL/KZ9mUhmFvFEx0FQXjRDaQHWVP4WKS3mikXfnpHCCLC1UJ3eButDdzVIssSAEJ8Sk2grpkookUz0TH9WVLeQzU9IwWme7EZJJ7m2rWHnv/YGImgEiJce8H8iR5ARM6Y4fXNBPxyIQqjPiyIthqD6+ZkLJyaK2OIescoUrKK9sIT+4lEKyk8+CO6FBXy2bCV8Cze2/tOt5bPR0uIL+Tx57ueRacGCHfBrqPfeeBhd0c9cayP1nwaIqLJA7thXJnRf/Bs7+R/XkPA5OUgokJiX1XvTnpd8W/t6hz4KD/929oFsevycPVc+8GfSgRZkq2Hj+Mqr9zPEzu3/9dH7DU7dvbDhzdP6B7Z+wZ52kHCvVuly1xYd3QbbhK6QF6q+wWHsvnJyqcMxNTP/o1O+L6g0MDBS6N7e90+k7ijFv+V1ySUpDVT5TNlRTuqSgax78q5qGwojD/pMBN6RPRGhkhL1VjpSO6sh0wb2n/6UAasCw7+Svicltw0JOGBka4d8iufLBk1TrWp/HwTmvows8FtUlT7ROtGusDEQGdXTc9G1y00PyjSBYDFBlx6dPrcaq5+eyc/xgtPV/9o+P6AZpb2UtfURuBP2XCJ7OrtO6DWxUsgI0T8ybOEtTMwPJQPp06E4Q3W8c3lPVk9+8fau1GEgpv9Gpup1EyOcJXna0xOkwCbvPm6jWZRS/wBO3rzkxZma5/LpaQxCsaD357PgEglDucqm2eKBY0Fx0GX1PFqYgqORzhO+nVeHI16otZPdB61JWepK2dSNUo6QwJ1WWoddxphpyj1OtcZY9MbVoawaofz/S99Smzh65soTTvJ3a1DKqiwRqfXzZyNWUc5p9buXoSalMTJKlKJ7H083eYd+1C5KyOrvj0mkYEcFz1n9RrcGItYvgO+WweK9DBX5AX7x6KX9VFV1WZhZPoyI0bwFTEf+WHvnlWxXLTkyYkRJ+QY/Gb17xS7teN4IeqF5iZ/lexQvejhzOlvMntl04WdqzYLNSlX5q0bl9xZqVx34tfTq6Kp2c3jUb4SPv7FWjUd9FUxI/pFSFdSD4s/OXrcpVxW+XcBL++fpnobqjYhQ9xGCvaV6e0iUirZBo8pk5lL1ldOdFZgMTrG356pBQqsnyZZ2m7g4uo9Yv0Z3pILWiP+7tG1Ti6/3+g+pOOH4o8BZQFwYGutsRIl5FC79RNwgEbxMKpNpvKW6UzymnntH+4LN/fG6HKDoLFM6VV3VwDoypCe17z9u/TXNe4volyl56cEdKJTqu2vb9r08jX3gO6SzmSgmdt1H6pOhOEN1vHH5dz+s3k3NKb7QaWfMFJySdBEeGoynNP5W9RlHf6LXwz5UDf9RxDoJF4NJnyMcQhELpQTaIiVg01yEUhqHsa71ThilrNrmHoTAP5atSOl8WEqkaiiaUnqSijlQnxdEavurwPDW5K1abULtQXqxPM0DFSn3KREspQB0LCcorcNRIQW3W0Ji+5bDGZKfy1K9qaHZ2lRNKtvXUEkrXJDEq6zq+k/dKha/jwUnWp0YRn1lffJ3rq/ZiTgIQEx+Hqrmp8bvuTPWKlx2/6W9xCJaFh1NO1QmgXWzsRJdIa3ML33xeM3Zv0rzFFeW8KQ5WNvLkzmjw/mCvsz92/NOuQo0/On0p77l4//bwZh3FAC18NTYyql2slBiIWKuob6fKtQevmIMKFj6XH97ZNHSct2vuT7g0Ra+ajbZdPNl2+jh5T+WCxQ6Pmlq3eBl5fJFBsrchZsVwsLZ5FvVCUk62oTyqOIxn3Hv1vJzmELqiEolHQxpWKVhcbvsf3LC1jYXVL5v/TumSgOBAtIbWK1Hm6K2r4lB9n7LI68sP70qfjo1nj35VvyWML3m0HsoefqA2nVN81ZHpaePKw7vVC/tAmMlzz4jSePXRPdy3rGdBWdUs7PPt7ivn5O6gqQW6Maetg+qIXNxIn0GtsuWV4c+efuCg4m9N31pNFh7cIa/DAT0P8+rHf/6SlCXZ4X2/NyU1YmDwn7On51XONnZowPpixyShBtFugt8f6ZOiO0HgOafnjZNLQkpvtNqZWfMFJySd3A0JQt3DP/hxSies+2a06iyj8n7YhmtPHfqyTrOULkSwdz+H9as0yVxBKFtnhzX8QIHcd1T2f4QalLuMqplC8h5ZzMDHEx0R9ZqSNJUWk/7nf/BMzXX5Utr53yGdT5S2O6Z0oWpnTh2x0jxZDnNs8gKSaoJfd2haj9IJ/NxZf+bId03a7/zhd1Rfrj++72bv+F3jdmbGJhvPKurB4zauOPLztIkd+87Zt8U5h92ivt8FhATKg5rAxiHjvl4+C/W58W17mJmYLDr0r+YtDty4dCLg+uJ+3/deOBnisJJ30Xm9hvRc8IewJVNCNO+dHa+YXUPUHWfv3QLNs/brUd+unIca/OjW3d3sHCdsVcxbExIZ3rN6Q9S2J2xdZWxoBCWJ1veg8DDpEwFFV8Ld8+f1S1XnckDF8U5oEIQiBGHwi3A8IOTc+XsBgeHPLtwPgKcEY3PqzvU+eb2mdh0gJbuvUBRNS1VsWLIcfC0xWT+EgaTsRTNn39aRLbqgFnjq9o06xUv/1r63mIwkpUuQaBO3r8ElEJN7rkA/21kAABAASURBVJ4r71UYObvs6O4H6VhBO/3ghwWia/mA4bbLrZBE7o4uUEGmxiZiVk8dmZ42Zu7ZNKh+i/XfjEHzAcpt6/LVRrXsWmxYL7RWoJL9V9/v+yyaDLk4oG7zHtUbaG3g0BP8odw74g9k5fRdGy3NzPEUEDPVxg/WfdWjsKelPb3zOrqERkVk+LNnCD+sXnBs9Iz1g8f8sf2f5y8j0SD4R6d+Cw5sF50nIafblK++/Nje13FxnavUlpK70arx6PnT5mUqF8mdF9IOqknPq8KiI9Fu1b9OM9Tz0AKF9wU7zU1NpU+K7gRJ2xuHYiApdeAx/2toJErpjdY8Mwu+4ISkkyuP7lUtVDyl1YnrTxymY8+k7WvF1GJaKe3h/ZnOwZu5glCYVDocHrEYgzyiT+hDoTdk7Sc2hNKQV6qADjysvKqmcqCgVgnxbv30lKf6JBkLKivvuo+mfqFC8v/E06gXeIt/bddr23e/ClcQla0208eKKeBRyWg+ZdTsHt+gjg4Bc/DmpWaTR8p1tdfxcSuO7d0zYpKVmTnCaT1tzMOwUM1bQNi0mPLz3J6Ddw77Hbd4FRcL2XPg+oeXgr304A58QlHtk5SNf1XHDV7Wf9i1SYsNDQz8gh7V+u1bSCxJ2cW06eSRM7t/NbBuc6hH1IdaTR0jFv37JPSq0RDWwU6NpZP+Pr7vp+ZdHKxzwJ5acHDH903a96rRyPHLloj/T+sWQ1QPadgGhyb/uw6HhAwevGI26ppQ7NiGklx98gDMNHgjyIURaxchHf4eOCKHuSXSH/pTCHIdl/yulBMzug+C74SMWHpk9/er50ufmg6zfoGandylv6O1DYQu5EGNX4aK4U86Mj1tIKEQ+KI+312duAgpDDX+1bKZYvKYJn/+tPTLYSfGzkRaQWY3mDhcbVxKqkB7R7sZ46Z2HTi0UVtJaRj2+2vqB69Cy8vKgT89nLnGZ0QfyICMffYMAblTeezXC3oPPT5mhpGhIeKD4jom+c/6T//8tfW7X8+MnwNjav/1C/gB0TrGD2USuu7mH0u/WTF71p7Nel6FX5JW08as+Wrk+V/noTDP278tp629WHfhE6I7QdL2xqGJB8FuHDIWbSX4NdbxRqudmTVfcELSw+k7N1ED0T2MMA0gQLTJ4m2VPkMMpM61payBsBPFIvKyTyjLOVkWSslrM8jSUXeA4uR305bSeso0xOw78nBBJjWRlDNh5LJ3jHj1UusYa2cbO8UsDtokFqqqrnYO+ix/jBoMKnBPIsIS0zfdC8wBCEu5y58qqAah7VxzcsisibOyw5voJiopuxRCEckzWKpia2mF2rDWNbj71GqMP5a1f/tObe57HZcYKCZpdIDbIHdyyyLAAXsapT1WOjI9bSBANGQIG0cVGN02FlZypqQf5HLcm3j9109HxOytrAPDw+TRjBn+7BmCpakZ3DmtscIPQtTrV7pbZPCe5nFwho0vNzDpc5UAPyNwdz/tojKa6EiQtL1x7o7Oqj/IOt5otTOz7AtOSNr4tlHbkMgIsaxURtG5ch1XO/upOzdInyGfRhBqTg0qxJssJOSOoPJsMap71HqN6kZt5rcPLuNO0oY83pJD/gj53EE1+sfmnfI55Ww5dbRECCGE/H/h6eI2pUv/L+ZPyiiTMIe55fIBw79bNf/+02DpM+RjzzIqhJ+mKhPTqMhTxcjTmdRIXttApkbyjJR6qg7ViSsl9h3NNGgJEvJ/Q34XtxLu+cVsh4QQQsj/GZBtu6+c61urydSd66WMoG/tJgjwM1WDUqYuTK8GZB7MOsg5gy51DqcwfaXYUJ1hsqbGtm6LT+sqDrij6DKasQvZfXCNe0nvVeD1AR7poVFTdURGIoSQjMDEyFgxUcqymRIhhBDy/8jCgzu8cuZqVrqSlG4QCIJaqLLK8WeHkVTCU8pkIIruz1gtBvL1XPCH5tEH708asfzoHnmOGWyLow+fhehj7uFkhU7TWLVCLKKw7OgeST9waw9nV3x61GgoByXvFFGCPBPRE/vFhtqziAfHrcV+caYIE9ty4PJ+8Qia95KUi+fi63LlI4gbvRdC8iPLOzUjQwgh+vAwLPTWk8fpHJZJCCGEZGX8gh4Ob9bpadSL9EycW6uo75e1m43duOyzXp/zY3QZFQuOS9p6FQpfKyWl9946fnp39cRdINVkx0y+aao6i0JfyavqwdiEx6g2RY3q2oZi/yENA/O/KXCUag1fFZOjKjf+WwkweYSkuEoMpMTOMcmrOIh7yd6gGEuJAOWgxDOKAOXIiJGTYoYeQgghhBBCiCr3n4WM3rhsfJse1uYWKa1CoRt4gz2rN0Qg9z/ztVg+0hhCrQPMNKeWSRuaC0tAMkEvyf0503YLBCimsRFB1VAOXDySLNtUw5T1odoENpBtqupOjps8RapCv8HPVI6HlO8lJa/OJ6eP2FCNjHxTEZScCPLEPEJ8SoQQQgghhBBtXH98/7tV875v2sHbNc+ig/9Gx+o7x0wOC8u+tZp45cyFyz93NSh9zDGEakDkaE4YkzaEBae2c1xyyArxlu7xdarhH3l/PpsaKQ8jxK3xERJOx2hDsbiiGiJ9hAhUO0HtYVVDlpdqJIQQQgghhOgGcm7Q0hkvY2OWDxjeuXIdKD3d5+MEnLa8/3Bcggv/D9Sg9PFnGRXIc42q7pTXHtQnBLU1J6CC5HUp3u1R9lMV/SfTJjvFfDBiUlNh6+EWUIM1lGMC5dPGJffnVFOGigUzkn0/4eONSzkaqvc6olx08Z3XJ7rU3rysFpmUJO4RZe9TsUC8RAghhBBCCPkQCw/u2Hf9QquyVTYOHnsi4PrFB7cDggOfvHgu1qWACMxl51jQLU9pD+8qBYvvvnL2811hQisfY1IZNaBYelRvANGiNsXL0v7D1aacUZ0WRW2KFLUJV7CBMD2dXdWGHRoYGGhOY6MPwoV7GBaKD4QcwscHoUnKOW9EzPF1mXJSGXk/TpYfCiHIM+IgqjjnwbMQnIBY4as8zYzwG5Ea4nzFCTcvizPfPYVykKF8ghwmzsEGghJhInyxFIeIDHYe0XtlDkIIIYQQQrIzL169PHX75qZzxxKTkormztfIt0K3KvV612zcrWq9Jr4Virl7oIZ97p7/lJ3rjt66ipOl/yM+wcL0mkP+pBSWqlf9qnaVPAxP9QRhjkkZMS5RtccmIYQQQgghhPxf8gm6jGraVgp1p+whqbpTd6dHMaunasdR4Y/Ja9CnUxNymXVCCCGEEELI/z2fbFIZVcZom25UbRaWmkV91SZT0TqXDCGEEEIIIYQQPfn0glDMwKlmD4oZWdTOVPMMj6j4gYJxG5eLeVzo7xFCCCGEEELIB/n0glDMmKIm4fSZJFOsr6C63qBQg5xJhRBCCCGEEEL0IUt0GdU09Gq+v7SDvPO9r8r+omKxCokQQgghhBBCSCr5NOsQfhDN6T2FZ6i62KBiPQblkgwSIYQQQgghhJDU8wmWnUgDqt4gFSAhhBBCCCGEZAhZ1CFUgyKQEEIIIYQQQjKcLDGGkBBCCCGEEELIx4eCkBBCCCGEEEKyKRSEhBBCCCGEEJJNoSAkhBBCCCGEkGwKBSEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTaEgJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJplAQEkIIIYQQQkg2hYKQEEIIIYQQQrIpFISEEEIIIYQQkk2hICSEEEIIIYSQbAoFISGEEEIIIYRkUygICSGEEEIIISSbQkFICCGEEEIIIdkUCkJCCCGEEEIIyaZQEBJCCCGEEEJINoWCkBBCCCGEEEKyKRSEhBBCCCGEEJJNoSAkhBBCCCGEkGwKBSEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTTFwz+cpEUIIIYQQQgjJftAhJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJplAQEkIIIYQQQkg2hYKQEEIIIYQQQrIpFISEEEIIIYQQkk2hICSEEEIIIYSQbAoFISGEEEIIIYRkU4xs7eyl/1cMDHLY2iYlJSUmJEiEqGBiYpIrl5uhoWFsbJyO02xtbS0tLWJjY9MZDkkDFhYWudxc8f7GxcdLH4WPf0dCCCGEkE+OsfSx6Nb/S1sH+9kTJkrpxtzCIiEh4U3KlTZrmxw1GzYoXqqUsbFxYmJiSFDQXf+Ao3v3oaonZXkMDA2trKxeRkdL2Yx9e7a7u+fReujhw0cNGrWQMoKWLZt169KpaNHCBgYG+Prq1at/d+5ZuGhJYGCQfI6jo+OPw78rV65Mzpwu+PrsWdj5Cxd/nzj56dNn+oczbeqkRg3ra0bg+vWbbdt3kbIY5cuXNTU1xcbp02ffvn0rpYPrV8/hvcPGwkVLp06bKaUSGxubnj26tm3TytnZSex5/vw50nbuvIUvXkTiq5ur66GDu8Sh6TPmzF/wl+qesLDnDRu3ePnylfi6Y/vGAl75sbF374Fvhnyvea0+d5RBA8HJ4weMjIzE1+jol5Wr1n7z5o2UlVj59+KyZUpj49y5C92+6CNlPqVKlVyzapnY7tNv0PHjJ6XUk85iQwghhJA081l2GW3bvVvZypVSOorqWuc+fYr5+p4/cfKfJcs2/r3qyePAanVq12vWVPoccM+Xb9CPwyWSCYz8adjECeOLFSsiVByA9m7frjWqs5AKYk/p0r7bt65v2rSRUIMAOgHSDjsrVCinfzi2NjbSZwJ8zqWL5/+1cA4+OXJYS58OJOOypQsG9O8razNJqc+7d+u8Yd0q1Z0p4eTkOGjAl5LepOqOtWpVl9UgQFpVTC4ShBBCCCGfKZ+lIHRxc9VxNJe7O044eejw/h3/3vbz879+fffmLft2/JszVy5bOzspy6P76bIDEREvDh46ovo5dfqslG68vQt069pJbD969Hja9NmbN28TX1Hv7969s6RsTfhl/GgHh3f9qENDnwaHhIhtuEO/jh8N7aRPOOJ8sQG76f79B/LnyZNgKYuRP7+Hqs75hDRuVL9okcJi+9ChI6PH/rpz1x7xNU+e3F9018tZ7datk1d+T0k/UnXHenVriw3ZgZT3EEIIIYR8pny8LqOqVK5Vs2jJkstmz5E7p8Fp6T34G4i3Y/sP4KuJqWnNBvUL+5QwMzN7ePfelfPnA27cxP4egwaamJpYWlmVr1YVHiD2rF2y5GXUe70rExIUYSa83+3tzNFj+MhfEYJv+XIFChd2zZ07MiL84ukz50+eEh1KK9WsUbSkz+KZs0uVL4dznFwoW12VAAAQAElEQVRcQoOD927dFhL0RFybUtw+gIFBgUKFhFLFtzKVKparUtnGzj44KPD2Tb/TR45ip0+ZMniuHDY2JsbGfYYMxp6AmzeP7t3nUcCrbtOmO9ZvwB2r1KmVz8tr2rhfYmNicELBYkXLVanilid3dFTU/YDbh3btljuwte7aBefs3rK1VsMGhYoVM7e0eHDnzu7NW1+/eleXNTA0rFm/XhEfH1Nzswe37xzYuatwieIly5ZdOmu2haVlherVLpw89SIiQvro+N3yHzhoiOb+KlUqffftN2K7+xd9GtSv17Fj2zy5cx87fmLC73++eBHZqWO7tm1a5c3rfvbc+dGjf3keHq56+e3bd2rVblTCp1hJnxLbtv/r738bpa527RpCuRUqVBD/tmzRTNYSy1es+n3iZGx8O/Sbfn17YsPdPU+7tq1Wr1n3wXAkRUfEHGJj0h/TcJqUekqWLNG3T8/ChQoiZET+6LETfy1ellJ/TviZg78ZWKJ4sdy5c92///DkqdNz5i6QRzbmyuXWv1/vihXLu7g433/w8OrVa/v3Hzp2/KRrzpxz5063tv7PFVy+dOHbhIQxY34NDApa/Nc8sXPBgsV79u7HxqiRw+GgYuPu3Xs/DBuJDUNDQ9y3SeOG2MA5k6dM1xq9li2bNW/WpFAh76TEpFu3/Ddu2rpr917N09zz/NdnePGSFecvXFy/ftPly1cDA4Ou37ip2mVXB8bGxiNHDu/Vu78+J+t/RwsLiyrJHRNmz5k/Yvh32KhTp+bY8RMSExM1Q541Y3LuPLmx8e+/u1et/ufnUcPr16tbrkI17DEzM4UnWalihQIF8uMWV65enzFzTnCwoukBha1qVcVdnoY+7T9Q8SMAHxKZIim96GnTZh1Tdshs3apFs2aNUTbi4+P9/G79tXg5Yi6ljI6yVK1q5aFDvxanfTP4e9HnGV63mbkZNrZt+3fZ8pVqodnY2Iwd81PFCuVDQkPXrFl35+49zTsir/v27lmqVEm0kjx/Ho6mkBV/rz585N2PcIYUGwSOhypatHAOa2v8aFy5cm3zlu137tyVCCGEEJIaPo0gtLGzc82dS+5uJ8CekKB3468atGwOZXLl3PmnISGFihdr063r0llzcDQ8LMzS2gpe3+uXr54/U9TVEhPUq2LwdGJev65er+6b+PirFy7GacwIApOn24AvHZ2c7t+5e/H0ae8iRRq0bGFqZnbi4CEctc6Rwy1PHki+0hUr3PMPMDU1zevp2a3/l7N/n4RgdcQtpYc1MzeHsCxTqZKDk6OQjiXKlG7UutW9gNsXz5x1y527btMmkK/nTpxE+HgoCytLSFPxdK+UIwkRNyROPq/8VWrXev3y5e2bNxMTFdPklKtapUHzZpGRkf43btjY2kFMehQosHT2HDG60sHJCRe26NgB1wY+euhVsBBEeA5b2+Vz3tXyW3bqWMy3ZHjY8zu3bjk6O3fu0ysy4gVOxt2hFSvWqI4PxCoidv/2bekjYmVlWaRwIdU9qHFC6GK/bOb8POrHFs2biG1UGVEjPHzk+JjRP4k9dWrXxPlDhg5TCxl2Hz579x4QX8uVKyP7eKEhofjX19dHfI2NjZ05611CzZ23AFJT9KXECRCEHwxHUjiE77qMenl5opZfpowvJOvp02dxeYIesxx1aN929M8/Ghm98/Ahw/CB/OjWvY/mJDc+JYovWjhbjkOxYkXwqV27ZqdOX0RFRzs6OKxetRTaTxxF2uLTvl2b4SN+vnz5ipykgoIFvSVlR0rIKvmQvf07ax2SWOxEBV3s+eH7IT17dBPb2LC3szMwUO938MekX5FH8teqVSvjU7Zs6V9+VR9RfO/+fXl73twZmzZvPX785Lr1m3TM66OVypUq1KtXZ9++A0napFra7litWmVzpUYKCnqyadPWYT8MhZhxdHQs5VvywsVLmiF7eOSDmYyNkJBQ/Oa0ad1S6EabHDlWrVwiDgFPTytPTw80KPTpM/Dqtev3HzwQrQ9IZyQ73HIfnxJFixbBHlx+XfkD8ucfvzVr2li+EdoCqlevisRcs3a91mfUXZZsbG3kjDY1NREbRYoUMjc3x8aZ0+fUQsPv9tLF81HAsA0vHY76xk1b1M5B+Ev+midCAG5urvhUrlxx0p9Tly79W8qIYlOubOmlSxaIYYegbJnS+HTs0LZ9h253792XCCGEEKI3n0YQfpCCRYtCL8ETw/aFU6fbdO3ilNMFomvbP+scXZzh7F2/dOnU4SNar0Wz95bVa1t16QSZV6dpE8ins8dOPH7w4L/AixV1zplzz5atkDr4Cmfsm5E/wmcTglBU2mASLpgy9VX0S2xXr18P8rJkubLCx0spbpoxwV3KVqnsU6Y0TEVE4Ni+fTevXlOGUAQy9Z+ly4SN+TI6OoeyKn/bzw+f1l07WxYtunnVajkcIXrrNG50cNduEQdJKVxrN2oY+PDR6r/+io9TKEDEsFn7dhWrVxMuKx4EEjT0yZMFU6YlJiQYGRl16NUzf0Fv2InBgUH4F2oQDufqvxaLaEADV61bR1wYHRk5Z+IfkMQIE8kV9vTp+RMnr164IG6U2cB527xpreqeeg2aPX4cmPD2Px0lq0FBrVo18Hnvkrq1UQNOSEhRD0Ag/TLuZ/mrMPE88uUVXx88fPQq2UqFzwbZgFhhO1/yCbrDQaVZtt2+7NdbPgql2rRpo67deuueiQSmyvBhQ+UavAwMwN69us+Zu1B1J+6F6r5Qg3BsTpw4VbdOLXyF1fnVV/3hnUJsCDWI2v+wEaMaNqjXoH7dW7cCXF1dpPQBbYMquOoeWDpq5yBfVKv1Ml06d9i9e++58+/5WgcPHoFjBhtTUjpjX3Tvgg/Sf/eefTNmzJG77+oADpKYy+fH4d8dO3Y8Pv4DM77of8f6yrcDnDp9FjL75s1bxYsXxdd69WprFYRvk2V/mdK+qkMNBwzoK9RgTEzMnr0HfEuWgHRESo4dO7Jtuy6HDx9FoRVZ7+tb8tChI6VL+YoLL166DH2I9BRqEA03hw4ftbayKl++LKQpBOqhQ0dRANSikaqypA+VKlUQalAGWlftnG++HiDUIBpBzpw9h0cQozGHDv5q5cq1Fubm6S827du3EWrwln/A7Nnzv/5qgLt77uvXb+bNl5eCkBBCCEkVWXQM4auXL51zukDPSMrOn+uWLb+urcqVEnf9/WdNmHh4z154ZUV8fL4YNKBz397wvsTRG5evLJ4x6/zJU+IrPISbl69Y2+QwNVPMsigE4bF9+4UaBDiKf+Gh6R83uIJd+/f78vtvi5fyvXL+wsKp0+DLXbt4SUivVy9fmZmZeXh5iZMP/Lvz4M5dOh5HRCk4KEhWg6Cob0nozAM7d8oiDaZlcGAg3MjkqxT10X3btotVN+BK+V+/Lj8IRDX+vXzunNy3FuIWdUy589uL8HDEauavEzatXI2kaNiq5eBRIytUryZ9OlSNtdu37wz9dviVK9fkPagLwhJE7VB8hQB2ckpxDpLcuXOt/HuxrO42b94mhinKVtjLly9Vz3+VPGbM3t5en3DgWKKOrvXWEJa9e30h6QQ1fktLS7E9ZerMNu06P3r0WHzt2KGd2smonQtlAgZ9NXTkqHG/TfhTfG3ZQjGRkmzFw+4u4JV/2bKVZcpVRZgLFy0NehJcq06j2XPmy6G1at0Re6A9JD3wKVnCwsJCbMOOa9Sk1ZatO9TO6dC+jdiA/unbb9BXX38r93rVfBYILTyC6oyvAL4cHmTrln/y5/eQPsS+fQeFPMuVy61vn17xH1pAQs87wuKrUeNd4T99RpHFp06fEV9TGkYot18oFy+xVDj5AYrexXKCzJw9b8SPP/fqM0A0W8Cm8/b2guS7dPld4pcuVVJSdowUXw8cPCyppOeRI8cGDhryRc9+Dx8+kpQ9WiFNNaORqrKkDxUrlJe3Z8yc27xle7x6aueMG//7jyPHrFu3Edk9eMgPI0eNFftRApGkGVJsDKR3pdrJ0RGv7ffDfipbvhpSAxJaIoQQQkhqyKIO4alDR5p3aDdw2A+Bjx5Bbl0+ey61U+HDgju+/wBcRNhxPmXKeBct4pYnz8Kp0+F94ejzZ08r1qju7uFh7+SIlmxLKytJMaxFMa+GkE/BySMGAfwxhAZHTv+4IUzoPYirk4ePXDh5Soz3k4HbBtuwU59e4WFhfleuwqjUvciEiNLD9wfqQNfBInjyOFB1Z9Cjx2UrVTQ2MXn75g18xdevXkVF/jdvfqCy4milfBB7R0dcfveWv3w0Oioq5MkTJ5f3XCNosJtXroSHPavbtKlHAS9P7wKqQzEzifv3H6xc/Y/qngjlUMa3KoJw2fJV8IJQrSxZsoTYs/CvJXv3HsiZ0+XHEd+LPajEaw0fNe8F82fJE0jiqlGjx4vtwKAnBQoohLrz+2LSSan/wZMnT/QJJy4+btz4CcWKFYVaO3bs5Nat26HZJvw2Xhg1NWtUEwsepET+5HGMcCmXLF0OwYCHFU4jbmdtbSVPaqI42fPdycjQGdMUUtDI+N0MMTY2Noj5iZOnYXlB5ECjfvP1QHxgfM2du3DT5q3I3+DgkMjIKDk0WEzQJJJ+uOb8r7T8tWQ5Mg7PJVSo5rPA1RHj365duyFEjqdnPs0wr12/0aRZ67p1a9evV6dSxfI2yZO1YmPkj8N69x0o6cTExPj3iZPX/7MS0qtP7x4RLz48CFafO8Lik+dfjYuL9/X1kRMNjQIoCTf9bqkFq9p+sXTZ35OnTEc+wqqV5VnPL7p16dRBufmu/y3kur//7QMHDot1I5BKKDAlfYqLowf2K7owyOmJo/v3KnSUPAdSgQL5NZ/ug2VJSiWysfz69euFi5bgMddt2CQ3SQhQEmBd+pQo/u3Qr52cnexs/5txF7+NGVJsII9htkvKd/OX8aOxceXqtanTZp05c04ihBBCSGr4iILQQOdBpZ1iYPjupKsXLjwJDKxau1bhEsXz5MtXtW6dTStXPUp9RyDYX35Xr+FTumKFxm1aw6+DRIR912fIN1BEUHqP7z94FR2d1yt/Xk9PYekkKqeWeft+jz5F3S45/vrEDTLsn6XLylWpUqtB/Wp1at+4cuXi6TNBSj0mKRXm7N8nwW0rVaF8lTq1K9SoDpPw3PETKT1FYpLCQHjx/hQpaGuH4FQbjaYYPWhgYCIEYVKiWr9EISyFX4SjBsqpHVRPUC7b+N9SjQinmK9v6UoVc7nngaaFFDx/Mi0rjKWW4JDQVavWau5XnSjocaBCCUerCOnHj8Sel5JOqlSpNHP6n1ZW7+rBS5aumDxlhuyLPk4W2DD9PDzyPXjwUFJ6TUIlgkcPH+sTDjSDGNAld1u9e+9+61YtxMIVmv1O1ZD9k+iXL8Xlqgvi4aiqIJRPRs7mUc5iogrKSVDQkz59Bw4f/m2J4sXETjdXV9ShS5fyhY0j6YHc/VXuUmuoVLYwuuVzhIx88eI/MSnUr2VyyCbDUgAAEABJREFU9ORD8oYsjdRA6h04cOjff3cjhEqVKk76fbyjo0KQlylTSm3gsSYotDCstu/Y2bxZEzMzU3nkpG503xFKW9UGnDVjstrlEJOagvBtwrviijIJoSLy0cLSQj5B9FN9L/LKpSARk+HDvpUUvTqLFy1SRJSxO3fuPlIWTjk9bZWoXm5qYipp8MGypHqytZUio9GqIg//M9ToaypnOp5L/P6otiAYKX9SWrZs9vtv40Rm4XYQz7LMhnWfIcUGstbKyvLrrwbIy8PAe1++dOGIn0Zv2bJdIoQQQojeZFaXUTt7e0ml6mZoZOSaK9fL5Db1OKVj5qhiRtk7OEjJHp0gLDR0y5q1U8aM27J6DYRKgxbNJf0wMjYuXKKE8fvu0NXzF5ISE4X9BRkGNbhz46b5f075d8PGw3v2ioln3qkjPRav/2DcUIO8fdNv9aK/5k2ecunsuSIlSvT8alDfoUOK+LybswTe3aFdu6eN+2XFvPnhz8LqN2tqkULlWBmc4h817fc8LAxVK5FuMnjAmNevxeQ3ks7niHgerpj4VGVCETsHB6fk2jNq1Q1athgyelTT9m1huSCtZvzy277tOxRXfTr0yJkP0KpV84XzZ8kqbveefXDPKlWqAHUnPJljx/6T5VP+/B0KChbftCmTZOV87MQpfcIpU7rUsB+Grl659MK5k9CBuNwrv2eJEu/0WFCy/6zmq8gIISopBygWLlQQVeRqVSuLPfB5nj0Le+/kh+9ORnW/Zq2GhYuW8i1dsWmzNkWLl8G2WOXi/IWL7dp37dy158xZcx8mN0y0aNFUzJKiOtAuZ/JbqdqaUKtWdTxs3Tq1ZClrohy+FRr6VD6nTu2a+Ld2rZryHjHE637ys5QvXxZVeZscOcQ8paqPKQMhMWP6n4cP7T6wfyf8KzzR8eMnryX3SIRKgQaQdGLwbjbO2fIMq7rR547Ivjp1auoIpL62vppJyeUVCS4npmIobPKL/N33I5BB+LRo1d7HtwI2hJKB8BNTZULQyquYiP6ikkp6/rNug7i8QaMW5StUx4ZWef/BsqSa0Y0a1UeR6N6ts7xHnrVFRs50KLGiRRVLcdZRGb4rzh/89UCREbNmz6tUpRaMRPkE/GplVLHZsHFL/YbN+g8cvOLv1VHJbUMd2ytGJ0LotmvbqlHD+prxJ4QQQogamfLHEjKjY88ee7Ztl12vfPnzw5d7mjxDg1jMIH9Bb3kulnJVq0jJbcPQcpVr1Xz+7NmNS5dRWbl+6bJ30aIFi72rOr9RVl5NVdqY1SjqU6JFp47XL16CZlONEkxIYbIpViNMSvK7+m74mYubq1chxZyWhnosxaY7bpo8f/psz5at0H4ly5YtW6VSyXJl/K5exba9owOEKKqMsBZhu8G9xB4h5OLj49HKDlmboLOX7N1bt2rWrwebcffmd1P8QQ16FS50Q7/RX7euXRMzqSIdFHrYwKBijeryUUsrq7KVKvrfuHnuxImH2uaUz1QqVSx/49p51T0PHz5u3LSVlG5+GvGD6oJ7DRvUw0dsBwYG1a3f9OixExcuXoKck5Rj89ave2/C/Rs3/PbvP6hPOO7uuXv17C72TPht7M+jhqtaMefOX5CU8/JvWLfq3r0HW7ZtX758ZZzKhD1Hjx4fOKCvqFKv++fvkNCned3frY5w+MhxtYe6du3G8+fP4Wjh9Rkz+seVq/9p07pF40YN4CLu23cAIgG2ZIP6dX1LloBL+fPoX27fuSc8LuicHDlyQDgJu1Uwf/7M52HhXbv3hrETExMjoo0EOX3ykGoXXPH4/gG3FXPSKuMJU6t1q+by5JnAWHnO4cNHy5VViGQIkn17thkZGcu+1qHD6t2PHeztEVWxvWnDmhMnTjk6OVat8m6xByglPFQO6xzShwgOCVm6bMWA/n0/eKY+d8TjC8MQXLx4OTK5G3bu3LnEpKwwkCGVZaWtRoxKj/G3b98eP3GqRvWq2B448EskPlJsyOBBih+T6zehbUTg+w8cEqa0PJvofmV/UUklPXEIlyB6MHuhWu/ffzhq9DhET+3uHyxLqgtj9uzRrWuXjqoZbWys/qt461aAvP3PmuUo8J6eHvIeI+S6kaHs2pUpUxphduvWST4BTQkZUmzatG5ZoUJZ35I+K1etnfTHFIQmVge1s1OchjcODTHYmDZ99oKFiyVCCCGEpEymCMI7frduXb9ep0ljF1fXB3fvunt4lChdCjWhU4cPixP8r9+o16xp1Tp1bOzsoDcKFi3i4OQEB0/4MDjTu0iRyjVroF7y6P79nG65vIsUfvL4XVe9qBcvQoKeFPMt+fj+fUdn54tnzqoJJ4i0EmXKFC9dCqLxtp9fZMQLKM/ipUrFxsRcUy7VpQjKwKBxm1aXz56HDKtevx4iDFGX0iwgquiOW0rEx8VBWZ07edJROTINEhRCDvoTUbW0sixdsSJOCEte8Szgxk3fcuWq1an9+OHDpMSkewEBWsMMDgy6euFi2cqVTM1MA2742djZVq1T++2bN9CZkh5AqZ45egwicOCwH4IePXJ0cX718uVdf393D8XQHRiYs36fFPVC37FkGQvqdmrrpGvOkZh5jB03Yf7cGbmTpyCSCQkN/XnML0n62ZT/7tzTqFEDUe+X3u+YB9kwa7ZiEpdqykaQ/Pk9YJIsXLhE9fIrV69t3LS1bRvF5I2KhU+Sa/DR0S81V2x7/fr1pD+mTZr4C9JNdbZVWD1r1ynmwjU1MenUsR2Ows+BcJWr+9eu3xBm45Ur17AhBkOi/o1PhfJlDx85dvDgkSZNGoqTcRXuHhERkTevu5Rs48DvOnLkWM2a75oSUK2H5kRsxS2MTRTnwL2BoVrASzG8TZZVknISoA0bN6k9y5q166tVq4IWAUk5wk118snExMTffpsk6c2iv5a1a9taHvyZEvrcUZ6sBf5h/wHfyGZUqVIl16xaJrbr16uz6K+lkh5MnDSlfLkyKBIwjefMniZ2IsX27jsgS80DBw73/7KPfMnTp8+uJy92qkjPls0gF+GbibFzAhjFly5d0bzdB8uSv/9tWNZygUdMkIm5c7mJXqOaDtvOXbu//26wGLiIkz09Pfxu+cvrxEDvIZVu3fIXS2VUrlQBH9zCzdVVnIBXO0OKTb687mIa0p9+/OGH74fIpVpYqfLUrLKvSAghhJCUyKx69vZ1Gy6eOp03v2erzp0gWl6ER6xcsFDucAi9sWnl6jfx8TjUslMHmIerFi2Kjo5+12U0KWntkiWwp2o1agi50qh1S8jL7WvXyYEf3bcP/3bu2wcn5HRzU7t1kuLypQf+3WlialK/RfPOfXtDfT0LDV25YJFwJq9dunzh1OnCJUp06tOrcu1aR/fuO31UMXunoT6q40Nx032tWF3wwM5dJw8dRgT6fTukY6+eL6Oi1i1dDk0ozrp7yx+uXaWaNTr17uVbvqyO8Lav33B8/wEI1Lbdu9Zt2gQa76/pMyP1Xkp+/45/t65Z+/jBfSTUtYuX/lmyTJ6wFH7Fp1KDn5zbt++0at1x0+at8pIDoaFPt23/t2WrDjdv+ukZCBJw4KAhqPrfv/9A3onq/tKlf7fv2P210gqWe+5NnqxlVe6fR4//9bdJYrFySekyHTx0pHmLdvIeVRC9nr363/IPkLsjQnZ+/8NPYhbWY8dPDhg4+NChI3gQUW9G9HDJAOW655Ky6+CQocNkgwv3slPOtjrpz6lixk68Uwi8S7decsdFWSeM+Gn0yVNnkpTAnurevY/cow+ujrhX+w7doLvkoWvh4RHLlq/s2r2X5qIguHWfvgMn/TFVdXlxeOZwbrt173Pk6HFJb5DI02fM/uBp+txRHkB47dr1KJVhq1evXpfHrNatW0vSDxSJ5i3bI3x5qUMUjLnzFi1d9rd8DuSfar9KZL3cEqFIz47dV69ZJ6cn9vz77+7hI0al1Fqhuyzh8u+H/SRKO7ZRTjp1+uJe8qBokYmqwNXs3WeAGNCIhNq4aUufvoPko+L8kaPGieKEAonigbyWe/CKzvzpLzbTZszG+3XmzDlkgSjVSMb5C/6aOm2WpJjFZyXuiMxa/f70VIQQQgjRxMA9n6eUmeSwsYmLi5PVzvs3N7C1tUVl9G3Ka7LBQoyOjNRa0bFzcICU0j37KFw4WzvbqMgoze6XJqamirng0yF7dMRNT6ysrZE4Wh/f3MICLeUvo6L1CcfWzk53MmoF1qKBgWGcygLcA4Z9b2RsPHvCRIkosbe3MzQwfB6erpGT8IJcXJwjIl5ERf03mSfK3plTh1GRPXz4aP9kYaYVa2srGxsb1N31KWmwgNzcXJXTeERqPQFmCwzDp8+eal2hEX4aYhsSEqo6rgxeELwy1ZlINLHJkcPA0DClm8rAgktMSNQzPeFQId2g654/D09K//jRrHdHQ0PDXLncIAshdeTpiFIF0hNFSG0coA50lCUYyK6uOeEA6zn2UlJOioMcj0thbVJFgDlzRkZFieYPrWRIscGNFMkYExseEaH6XHjY+Pg3H1x3hBBCCCGZLghJ1sTSyqr/D98FBwauXbxU1KI8Cnh1/bLfjctXNq9aLZFMpmrVyn8tnAMZALNI1ZsihBBCCCHkY0JBmH0p4lOiTdcu0dHRj+8/sHOwz+Xu/vrVq8XTZ0Zm186iH5kCXvm9vPLv2btfIoQQQggh5BNBQZityZkrF4zBfPnzJyUlhj4JPnv8RKzKjIiEEEIIIYSQ/28oCAkhhBBCCCEkm/LxZvMnhBBCCCGEEJKloCAkhBBCCCGEkGwKBSEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTaEgJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJphhLHwUTE5PipUvFvI65de0avppbWNRu3MjDy8vS2io4MOjQrl1PHgeKMyvVrFG0pM+SmbOr169XvJRvUpLkf/36wZ27jI2N6zRt4l2ksKGR0fWLlw7t3pOYkODp7e3smvPKufNxsbGaN23Stk0+L6+V8xdERUZKhBBCCCGEEELex8jWzl7KTOwdHarWqd2yc0fIvMCHD4MePbK0sur59Vd583sG3LwZFvq0QJHCpSuUf3jvXmTEC5xfpESJwiVK2NrbeRUq9OTRY7c8eTwKeCUlJpatUtktdy6oR9fcufJ55YcCRGi58+Vt2rZNuSpVbOzsXoRHvH71SvXWEIQI517A7YjnzyVCCCGEEEIIIe+TaYLQwCB/wYL1mzdr0LJFbnf3O7du7dmy9caVqzhSs2EDGH3/LFl25tix2zf9Lp46XaZSRQi/S2fO4qindwF3D4+kxKTFM2f5Xb168fSZ8lWrIKhX0S+XzZnrd/Xa1fMXsMfG1vbCqdPPQkLuBgSYmpmWKCC94BYAABAASURBVF0aO909PSEUw8PCRBQe3bsf9PDRrevXJfiMhBBCCCGEEELeJ1O6jELdwRJ0dHaOjIg4smfv5bPnXkZHy0d9y5cLe/r0rr+/+Brz+vXNK1dLV6xgbmERGxOTmJiIndcuXkx4+1Ycffzggae3N3SgOBQVGRny5Imjs4u4HJIPn33bdviULVOmYsX2Pb7ATXes33D/9p0njx/jIxFCCCGEEEII0UamCELnnDmhBl+9fHng310w6BITEuRDVjmszczNX0ZFt+zUUd5p66BwKR2cnKDfxMn3/APko0+DQyAI7wX8tyc0OBia08DAICnZ+oNuPHvsePizsIatWtja27vmzg1BKBFCCCGEEEIISZlMEYR+166ZmJqUrVK5ddfOr6JfXj579tKZsy8iInDI1NRUcVdTExt7O/l86LpH9++/VVqCiUqNJ7blo2p7pPd7gFrb5PAtX75UhfK2dnYRz8P3bd9x5dx5iRBCCCGEEEKITjJFEL6Jj79w6jQ+HgW8ylWpXLlWzcq1a8HiO7Rrd2hwSEJCwovn4X/PX6D94hTG+yVp2+/g7FS7UaOCxYoaGhjcDbi9a9Pmu7f8kzhikBBCCCGEEEL0IHOXnXhw5y4+tvb2ZSpVhIPn6e0dEvTknn+Ad5HC9o4OcPPEafWaNX0RHn7uxEkpleTJm8/Tu8CFU6dwbfizMLWjRkZG5pYWsCglQgghhBBCCCEafIx1CCMjIg7u3HV07z6rHDnw9cDOXVBx7Xv2OLJnb2xMTDFfX2jFPVu2Sqnn/p07M36dEB8Xp/Voz68H5XRzWzxzFlSoRAghhBBCCCHkfT7SwvSSchBgpHIYYVho6JJZs5u2a9umaxcDQ0M4e0f27kuDPQiida44n6REIoQQQgghhBCiDQP3fJ7SJ8LE1NTMzEx1RYqMBWoT4cOElAghhBBCCCGEaPDxHEJN3sTH4yNlGkmJiVSDhBBCCCGEEJIShhIhhBBCCCGEkGwJBSEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTaEgJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJplAQEkIIIYQQQkg2hYKQEEIIIYQQQrIpFISEEEIIIYQQkk2hICSEEEIIIYSQbAoFISGEEEIIIYRkUygICSGEEEIIISSbQkFICCGEEEIIIdkUYykTKOTtJRFCCCGEEEIIyTj8b9+VMhoD93yeEiGEEEIIIYSQ7Ae7jBJCCCGEEEJINoWCkBBCCCGEEEKyKRSEhBBCCCGEEJJNoSAkhBBCCCGEkGwKBSEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTaEgJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJplAQEkIIIYQQQkg2hYKQEEIIIYQQQrIpFISEEEIIIYQQkk0xsrWzlwgh5FNgZmbq4uIcGxubmJhoa2trbW0dExMjkc+BqlUrN2pY/9mzsMjIKIkQQgghny0UhCSrULNGtfIVyj0PC3/56pXaIXNzs9atW3oX8LrlHyB9aoyMjAoV9K5SpWKzpo1LlvRxcLB/9fK1Zpw/X0qWLFGjRrWEtwlhz59LmYyzk9OhA7uMjY0aN6z/x6Rfe3zRJSYm9vKVq1JWJVcut0aNGjjY2z969FjKOKytrVq2bF6saBGU8KSkJCnLU6VKpQXzZpb0KdGgft2du/a8fp0WGZ9JiUkIIYSQVGEs/b9gZm4eHx+flJgokc+THj26VqxQvnffgSGhoWqHrKysx48d9eJF5JatO6RPik+J4r/+MrpgQW/VnW/fvl2zdv3ceQsjIl5Inz8N69fr2bPblKkzP4L8Rl5v277zy369X758tXzFKk9Pj149u2Mjy4qiIoULoSgePnLs2PGTUsbRulWLn378ARvR0S937d4rZW2KFy86a8ZkJMKvv05as3rZX4vmduveGzGXUkkmJSYhhBBCUkVmCcKm7dv6liunud/v6tWNf6+SMhrX3Ll6fjUoNDhkycxZ0v8XXb/sZ+/kOOu33yXyqYFW+f67wYaGhmfOnDtw8LB/wG1LS0u4Ot26duzWtVPtWjXad+z+PPNdtf8zho8YNWfugqdPn8bGxllZWTk62BsaGiQkfAYuWUZhYGDQqWM7sd2lS4esLwhDQkJbtuoQEvoUbXAtWnWws7VJm4C/6Xdr1M/jgkNCJUIIIYR8OjLXIdy3fYdaRSE8LEzKBBISEt+8eRMXy9FH2YJy5cqMGPbdhYuXVq9Z9/Wg/uXLl42MjDx56szs2fOjoqNLlizRrUsn7ExITLh44fKfk6erWY7u7nn69e0FlyOvex5//9uXr1xduuxvOzu7iRPG3713b9jwUVpvWrRoke++/QblefTYX9et2yjvP3ToyIoVq2bOnAx7c97c6bBK4uLi5aPe3gV69uhauFBBT0+P4OBQ/4CALVu2Hzl6XD4BkvLv5X/FxsV27da7fbs2NWtULVO29NPQp+fOX5wxcw5MUbVo1Ktbu2nTRgjQ2dnpwYOH167fmD9/cXBIiNppdna2eEYfn+IwM6Mio27evIWbbty0RfWcyX9MQKygx3LY5GjbpmVkZFSBAl6ODg6uri442rVLx4YN6t2//+D7YT/JUf2yX6+yZUsX9PYOCQm5dOnKxk1br1y9tnb1chMTky7dekLRpTaeWvMif/78mnlhZGQE1V25csVCBb3Nzc0CAu7g5EWLliLHpRSQ07ZL114oFW1atyxdqmTOnDmRC+fOXVi4aKnmeEU5vzw88gUGBt244bd56/azZ89LOklVymhSqWJ5ZMSJE6dsbG3KlildqJA3kkL1hHQWeH2i5+jouHB+iq1pf0yehkYQ+WtJnxLNmjVGRuTM6XLv3gM4yUuWLofHqxlhxLBbt05VKldCObx7996Bg4cWL1mRkJAgTgsODtmwcUvGJiYhhBBCUkvmCsIzx45LH6Xr17OQkCljx7O/aDbBJkeOYsWKGBoZ1q9fx87WLiwsLH9+T4gZnxLFZ82ZP2vGZFNT0yfBIbncXJs0aVitehW4GU+eBItrWzRvMmb0T6h0Yjss7HmRIoVKl/Zt1LD+7DkLEKaOm/7+2zhokiVLV6iqQQEq5V99/e3mjWsRgQb1623b/q/YP2hgvwH9+xobG0NGoo6eN2+e/Pk9cK8dO3aNGj0+NjZWUugcQ9wXyuTboV/37dPz1atXEGZeXvnxONBUPXp9eefOXREa3DPEAY+MbTR/hD1H5AtDprZo3mzcLxM2b94mx6dWrRq//jIa0g7bT58+s7W1xVX41KtX+6eRY8LDI8RpXgXyFylcqHr1qkOHfIWq9voNmwsWLOCaM6c4iro+PgaGBuIrIjlj2p958uSWlN0aoR/at2/TokWzYcNHIhpmZqaGhkapjaf+eYF0mzJ5ImKLbSRRbFwcJAc+rVo2//Gn0Sl1OJTTtnGjBhN/H49SgWeHHQfRhU+Txg0HD/nB75a/fP7AAX0HDuiH/EIDU2hoaL58+SBjWrRo+tfi5RDnsoxRQ/+USYnOnTvg31Wr/7G1s0XSdenUAY0Oqiekp8DrGT1TExMd5R8REBvI3Am/jW1Qv66UnLm4Cnq+ebPGs2bPX/TXUtUI472YM3sasgmZGxcfB+GKT926tbt/0UeIOlk3Tvj9z4xKTEIIIYSklk8zhtCjgFfdpk13rN9gZmZWpU6tfF5e08b9EhsT4+zq6lOmdIEihXPY2DwLCT22/8C9gHejmFp37YITdm/ZWqthg0LFiplbWjy4c2f35q2vkyfz6PX1V3f8/I7s3Se+OuXMWath/dx58yUmJT66d3/f9u2vtA1xqVSzRtGSPotnzi5Vvpxv+XJOLi6hwcF7t24LCXoin2Nmbl67cSPE2dLKKjgw8NTho/dv31a7vHSF8qUrVjQwkBZNm5H8dOsdnJwr1qhua2/34Padvdu2v3r5El+Llypl52D/8O7dnRs3Y48IR8eDq9KkbRuk1cr5C6IiI6VsD+TB2n82oCoZHx+fN6/7siULfH19Fi+ae/TYie9/+CkqKgou2exZU1H1H/bD0CFDh+ES1KF/+3UsavyQJVOnz3r2LMzQ0BBX/TJ+9C/jf9Zxr9y5c8G3gRRBrVfrCbBHVq5a++OI71u2bCYEIUTI118NQKV5ytSZMHZwLURXndo1R//8I6yz5+Hhv0+cLF9uYWHRsUM76JO9+w5APcJVQzyrV6vy6/jRnbr0EDb7D98PgR5AnMeO+w1239u3b62trfr17d23T49fxv386OFjVKxxGirTUyf/jgC3bN0xddpMCELshNAaN2ZkzRrVJvw6tv/Awaox//67wVeuXJs1e9716zd//W0i9NK3Q7/p3q3zjJlzly5bkZiouDUcuWlT/0DIMGrGjPnVP+A2ooSvI3/8Yfq0P9SSQs946p8XOGf61D+gzWAz4u6QcLi7m6vrDz8MQSIjAk2btdX0HmXMzc2nTP794KEjKCpBQU/wgDAAx4//uUTxYtOmTmresj3KD06DEP3m64GILfLr75WroVigJ5s0bjRq1PB+fXtGvIhYuvRvbYGnImW04ubmWqtmDei3I0eP4UlHDPu2efMmk6fM0HQ+01Dg9Y8eGix8S1d8/4YGSDeU2Dt3751J9kiRuVCDEHjI3MNHjonMRWmBkIZ/fu/e/QMHD8vXw/nEta1adxSqGwk++c8JELGDBn6JRJaSdeOz5G4j6U9MQgghhKSBT7MOoamZmWvuXPm88rfp3tXG1vb2zZuJiQkQRT2/Gli6YoXQoCc3r1x1cHbq1KeXu4eHuMTBycmjQIEWHTsULFY08NHDpMSkoiVLtuvRXQ4TAdo6vJsx1d3TA/owl7v79UuXQp88Ke5bsu+QIeYWFpoxsc6Rwy1PnpoN6tdq1DAi7HnUixd5PT279f/SQulaAGz0Hvw1YvUiPOK2nx8i2blv75Llyqpe7lO6dKNWLd++eXP/9h356SpUr16/RbPnT5+izlSslG/zjh2gBvGBmfn2zdtCxYs3a/9u1JDuB1fFu2gRBydHnC8R2MLPwn75daKozT969Hjd+k1i/48/jUHlGBsvXkQuWLBYUlZMxaFRI4ehzg2l9OPIMbgcexITEy9evNy5S0/NzpmqFFLOIhMQcEfHogj/rNvYoWP3adMU/e7geo0aORwb43/5HbbJK2WzBcTh7j37+vQdCAOqW9dOwu+S+XPK9D179wvth7ihQq+oo/v6+PgUl5Sd9Dq0b4Oy1KNnP9S5sSEpVSgk3/wFf+GhoEVFOD+PGgFyamAVAAAQAElEQVQ1uGv33hE//izUIMAz9u47EP5YzZrVK1Yor3pfOJBdu/c+eeoMFEhcXDyEUMJbhRWGW2BbJG+vnt3zuud5+PBRt+595GkwAwODBgwacvrMOUgsOTT946l/XvTs0Q1q8NHjwK7det30uyXuDgX47Xcj9u07AM/qp59+kFIG0Tt16sygr4YGKVt5cDn0CYJCgB4e+Xp80UVSCnIIP2z8NuEP5Jfwr5BN0PZCWcHphdzSDFz/lEmJjh3aQnmuXbcBt0P6b9q0DQq2desWmmemocDrHz0cwlOrfoYMHgQ1iCLUt98gET78PTlz9x84JGfu3HmLJk6agu2xY0bCxJPDxBMNUfFgoeeHfjscN0Lhh/jPjMQkhBBCSBrIXEFYskwZn7LvfQyU9YDEBEXfzjqNG508dHj+5KkbVqyMj4svV6WysYnJinkLtqxZu3Pjpr/nLVB07qpcSQSFyiK0EKoRC6ZM27Z23czfJtwLuA3V5KbsXPQeBgYNWjTH/2HW7d/x7z9Llq1cuMjaJkeV2rU0Y5io7GUKl2/BlKm4LwI/um8/LEFZ8lWtUxtadOPfK9f8tRj3XTB56tPg4LpNm+Ac+fIGLZv/PX/hsjlzcTv56Yr4lFgyY9bWtf/MmfjH4wcPvAoVRFCLpk7Hnlm/T0Qg8ANhOeJM3Q+uyrqly3es23Dv9m2JKOTZbdVefKihSsqeh6rTupw4efr169e2SiA/YJ5g57Tp6mOlIiMjlyxdoeNeBby98O/de/d1nBMbGwtnA7VebBctUtjBQTGZvuYQKUiaXbv2oCRXqlRBdf/evftVvyLax4+fkpK1aOXK8J8NIJ8047Dor2WQqcWLF4WXYmRkJMQA6uhqp6Fmv3mLortmyxZNVfev+Ht1Sp0hZSpVVER19pwFQo2oIgSwjJ7xTFVeVKmicK7mzJmvOjhTMFlpNFWuVEG3WpiqcRcENXfeQsWjVVIEjvxydHBAyVm3Xr0/8MmTp5Gn8LJq1aqhGbL+KaMVmMZt27bCtRs2bBZ71vyzHkKoc6f2mk+U2gKfnuj1+KIrPtHRL/t+OSg4+J37WkWZuVu37YDvp3Y+PHBIdDjb3t4F5J337t1TOxOF/3FgEBSvu3sezZumMzEJIYQQkjYyt8tosw7t1PbAAXubmCh0VHBQ0OkjR+VDu7dsvXj6NAw98TXs6dOQoCcOzs7iKyxE/Ltv2/ZEZZUIFSP/69fzF/R2dHYODgxSvUVONzfX3LkvnDot9yZ9cOfu82fPIMkO/LtTLT4iJsf27Zc7lN68fKV6vbqOyff1LV8Ovt+ta9fF19iYmMO793bo1aNw8eJXzp8Xl+Nej+7fVwvznn+A6NiJCN+95Q/tGnDjpugjmvD2LdSsi5ubrb0dIqn7wVV58vgxPhJR8kZpUMgI7+5twns7kRfw5bBhbGSUP78ndAhqz6GhTzVDu3HjppQy4c/D8a+9vZ2kH4UKKVTcjZt+WmdfxP6mTRsVKlRQ3gMxqWlRBgcrhoHlzp0L/xYuXDClSEIA1G/YHNICBqCnRz5TU4VFs2DezHeKQvyj3LZQtmK45HRRvfze/QfShyhYsIAy2lruDicHRhA8LvFVz3imKi8KFVSEef26ljDhJsGhsra2gsh8/DhQ0obit8L/tra7+MmPJvLL2jrHvj071NLNQDKwsVGMoMvp4qIZiP4po5WGDepBiMKHlAd2ohHhxIlTVatWrla18tFjJ1RPTm2BT3P0GjWsP3zYtwjnq2++VU06UWK1ZgTue8vP383VFZkln/AkWEs/3uAnwbABUaqRd2qH0pmYhBBCCEkbmSsI4dGpVYhFLyMh6h6+33iMnTGvY+o0aazo/GlnDwvO0sryWfJ0ebDdoJ1Ux84FKusTVsmzHcgILeeU06Vlp47yTtTr7J2cJA1ETIJVRgxCj8XFxlorg7XKYY1oBD16r+Iivjq6OOt4EPx71/+/ySqeKgc4qQ4LDFXW9d/ZjDofPPsQo1zbGoJB85CpcqeO7pr6YGqqCCQ+/o3WoyntF4hqsar7oUnhQgVH//wjRM7Xg783MzPDnrgUpkMU08kIeSbQqhvFTgOlNBEBxsZpD1B0uZSUXR8lpQR6rS2toJ2ehT1XS0ZNN0YNvDsiU7QmUULCW3yMjExVI/DBeOqfF7i76IWYUphx8XHWkpW5SmKq8ebNW60WaJwyF8xMzeRoIym0plu0sh1HM49SlTJa6aKcTqZO7Zonjh+Qd1oqI9O5cwc1QZha0ha9cmVLT5r4CzZG/Piz6syiknI0ppRyRoj95hYfKtVSkpTcQpH+2BJCCCEk/WSuIFTIHm11gsQkhYf2IjxcdWcu9zzdBw4wNDSECXY3wD/m1etSFcobJA81wSWi5fu/QJSVPM2KhXBILCwsVQ+9jI6OjozSFhNF9N6+H7Ki+mjwX1Bq932jrECbKA+Jy9UeRDzdW5Xm/CTlzByqe1STRfeDZx9u375bq1aN/J4ehw8fVTvkmd8D/wYoh2immTt37sHHcHXNCUNJdYp8gbeyU2iKcbtzF9kHZwPV5XPnL2o9p337NqVL+65atVaOqnA8NBHr2vsHpGLZ9wD/2zVrVCuoTZGilH41qL+JsfHipcsRT6VBbdCp8xeaC4W7u+eBzRUeES6lBlTrEWxJnxLQw4Hvu/EgX7684jUR3L1zr3q1KrrjuWTZCv3zQnH323dLliyBRAtSabgRwF7DB2/ovZR785qbm8E/hPOmcRdFJG8rcyogQCH44Vm1bd9FM4SiRQpbWlo+fKTuaKUqZbQG6+vr80bBWyOVyTPj4uIhjZCMyK+UbE99SEP0CnjlnzNnOvZP+nPqvzv3qB1Fs0iN6lULeusq1QH+qSjV6YwtIYQQQjKET6Q6lGpIrdm+Wr26RoaGC6dOXzZ77p4t244dOGhqZvbf3AN6r17xPEwxkcata9dWzJ2v+vl7/gJtMdEV7ouIF4ik0/tdxRyVX8OF16G8XN1/SCHIlG71gQfPNlxXdhVr2aKpsbF6O0XbNi2l5D5+aQa+HHQamgl6qsxFJED9u3u3LrqvXbBwCTbGjBkJgaF5QoUK5dq3a41K7dZtinGkN2/6oZpftGgReXoPGRcX52ZNG2Pj0uWrkt5cvqI4uXWr5g7JMyfJDBrYr1/fng0a1H3+PFw8o5GRYds2rdROc3Z2+mfNipV/Ly7l6yulkqtXFV2me/Xsrnmod68vVL+ev3BRdzwbN24gx1PPvLh0+Yq4u2brT+/eirtfv35T9zDIPu9HUlI2JPXqpbj1VWVv8Js3bynzq3Dx4kXVzqxcueLGDav/XvGXhbZZqfRPGU06dWovKUZRzq5YuabaZ/6CxfgF6NyxvZQ+UhU9lMxFi+bY5MixbPlKrVOqXlZmhNbMRWuFV37P2Ni4W2kVhFL6EpMQQgghaSYLqQ5bO7tnoU/DkrtKlq5Q3szcPA2rToUEBsEP9ClXVkquPiKclp075S9YMLVBJSUm3vMPKOJTAnGTd1asXg3mBqw8KYPQ/8GNjIysclhL/6fs33/oytVr8BkmThifI/kx8ciwlRo3gop4jnqqlD7++GMq/oUsUZ20w9bWdurk3/MrTUgdzF/w152792ChbNqwVlU2QH11aN929syp0LEzZ80TAiM8PGLOXMWcJZMm/qo6qyeMjjmzp8EWO3ToyMmTpyW9Oag8H1GdO3t6HpWJlODY9OndAxuLl64QPfQm/P4nNr779ps2rVvKz4j7Tp08EfX4J0+Cd2iMpP0g8+f/FRkZCXd0/NhRcudMPPjAAX1bt3pvPswDBw/DQdURz0V/LRWDbPXPC6Q8cl9x93E/WyZP/wu91LNHty+6d0lISFRdwEMr7dq1/rJfb3kEGqQdgipTuhQeasFCxbScz8PDcReEOWvmFOyXbwHL989JvyJ6u3bv1fQYU5UyatjY2DRr2kgxrejmrZpHN2zYjOdq06aF1tYH/dE/eiiTixbMcXN13blrzyRl1miiKISnzmhmbtWqlX/7dQw2ZsyaE61tdZ8Mjy0hhBBCMpBPsw6hVp48DvQtX65Gg/qP79/P5+VVqkL5R/fu22o0RX8QtPQf2rW7Wft27bp3O3/ypKmZeflqVXLnzXvm6DEp9RzYuauPd4EeXw08eejwy+iXRUuWKOLjc+74ifDk0VDpR/8H7/n1oJxubotnzgrR6Dv3fwB0wsiRY5csnt+0aaPqNarCD4yLjS1WrCisrdevX/80cqyY+z49oDq7eMlyuA2jf/6xb5+eN/1uwQ+BL2RkZLxw4ZJ+/XrpuBblqv+Abyb8OrZ8+bIb1q0KDg7xu+WPamuhggUcHR0R+b9Xrpk3/7+5PaF8fEuWqFmz+tIl8+/eu3/v7n23XK6FCxWEAwZhOWbcb1IqGTV6/JK/5vn6+uzcsQm3DgkJ9fTIJ/rprf1ng+iqCs6ePT9n7oKBA/qhjv7VoC/9/QM8PPLhIymXJejTb6DmXJ0fBHrp5zG//DHxt/bt2zRsWO/6Db/4+PjixYo6OTlCR8HSUe3ON3LkmHnzZmqN58ZNW1Ymx1P/vEC0R/w4euqUSe3atoIRCvc1NiYW7iscLRiDk6dOv5o855NW4EauXrNu6JCvunbpeOOmn5mZWbGihaHHsH/U6F/k2VzgAPv6lqxWtfKqlUsCAm4HBT0pWdJHWGFopxg5alz6U0YV+GwoPPCTta53EhIaeuTosdq1asBMXp88AWka0D96aNQQM+sULVJ46+Z/1MJZs3Y9PtgY9fM4uRDCDAwJDi2ANhKlgN+378Dy5aukdJDmxCSEEEJIeshCgvDgzl32jo7V6tbB9rOQkPXLVnh4FyhTsWIagrpy7nx8XFydpk269OsLly84KGjL6jXBgWkZjQPjbsms2U3bta3fvJmBoeHrV68Qz5OHj0gZh/4PnqRE+v8FSqlJs9bffze4bp1aorMlDIf9Bw7BAgrKIA385+TpZ86cGzLkq4LeBeq41YyJibl69bpiWYIkSbcglJRLon3Rs1/7dm1aNG+C2nNt5ToEqNAfPnx0+ow5ap3loFX6DxyMCn3fPj3y5/dEtRl59zgwaOvW7QsXLVUbmKoPMPdatGoPpde0SaOSPiXwgYkEdQQrUnU1cEk5cf/xE6eQjMWKFoEilZTTyWzdtgN6NSzsuZQm9u49EBBwZ+RPw8qU9q1cqQKe7tatgGnTZ0PjqXX7fPQ4sG27Lt98PaBe3dpyPK9fvwmFvOf9pTX0z4tjx082btpq+A/fVqpcQTiur169OnX67J9/ToOS1B1zJPsff0578OBhxw5toffgOaN9AQH+NuEP7JRPe/v2bd9+g1q1at6rRzcvr/xCwUKYQeSsXvOPDhWtf8rIwHLs1FExA/OatetSCnbt2vUoYJ07d0iPINQ/ekbG77okiLYDNRwdHcQGCmHzlu0H9O+Dgl2ieDGfEsVRklHyFyxYDBNVSjdpSExCCCGEpBMD93yeUlZCwiWDgAAAEABJREFULM0nrxiR/tBQpRDTCaYTE1NTCwsL1WlOMxZ9HhyKFP5GbPom2/xccHRwMDM3QwVUyhzgNri5uQYGBiYo141MLajT586dK+Z1zPPwD8/RYmxsnCdP7tDQpzEZlHfW1lZOTk4QybqFpaGhYZ7cuV7HxKRZB6YU5tNnYbF6vFZjx4ysX69Og0bNdfckTFVewI81VxaMDzaO5Mhhfe7MMaR5qTKVxR68ws5OjoFBT0S31ZSAi4v8evbsmeaENzpIVcp8fDI8elZWVnDv0Ury9v31MDKELJ6YhBBCyP8TWU4QEkL+b1izapmrW876DZqnwRFNP5qCkBBCCCGEqMF1fgkhmQJsTPh4isXKlYPTCCGEEEJIFiQLjSEkhPw/UatmjTp1aq5es+769ZvSpwC25Lp1G+M/hTlJCCGEEPK5wC6jhJBMwdjYODNGlxFCCCGEkAyEDiEhJFOgGiSEEEIIyfpwDCEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTaEgJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJplAQEkIIIYQQQkg2hYKQEEIIIYQQQrIpFISEkE+MtbWVm5ur2HZzdbW0tJTIZ0LbNi379etlYWEhEUIIIeTzxMjWzl4iJMvQpnXLEiWK+fvfTkxMVDuUO3euRo3q29vbP3r0WPrUQLQUL160erUqTZs0Kly4oE2OHM+fP4+PfyP9v1Cnds1y5cqEhj59/TpGymTatW29ZPH8R48CR4z4fuRPwzp2aHvy5OlnYWFSVsWnRPEaNaslJSZlbCTzuudp0LCee548d+7ek7I8xsbGE34d26vXF5Uqlre3tzty5JiUJmrXqlGufNmnT5+9fv1aIoQQQshHx1j6f8HM3Dw+Pj5JQ0V8EHMLi9gYvaq8BoaGjs7O2AgPC0tMSMjAOBCBa86cv/06BiJk3bqNmkcbN2rw3bffLF369/HjJ6VPh4mJSbeunfr37wMRqLo/LOz5bxP+2LV7r/T5Y2BgMOG3sba2tgf2H5Iyn+s3bkZHv5w08Zfz5y/+8uvE0T//WKxYkZt+t6SsCjyxunVqDRk6LAMjaWho+OefE0r6lIiNjdu3/2CCtl+YrAMaRGZO/7NkSZ8+fQdWqVJxQP++Bw4eTtuL+duvY6Enqxw4LBFCCCHkU5BZgrBp+7a+5cpp7ve7enXj36ukjMY1d66eXw0KDQ5ZMnNWqi5s061L4RIl1i1bfvumn9gDfYiq2Jv4eM2Ti/mWbNmp441LlzevXiPvHPnHxGsXL25buy7NcSAyJXyK49+rV69pPeqjPHolhaMfB2/vAnNnT3N3zxMTE7Nq9T83bvg9fPjI1S1n/Xp1GtSvO23qJDMz0y1bd0ifOR4e+aAGHz0OfB4eLmU+V65cq1O3sZW1VXBwCL5CV7x4ESllYeAQShldFDt1ag81iA1zc7OC3gX8bvlLWRhDQ4Pxv/we/fJlRMSLy1eubt687XVMWpxkU1PTKVNnvHnzBga7RAghhJBPQeY6hPu270hKSlLdE5453cASEhJRpYiLTXWNJDYm9u2bNwlv/2uMb9u9211//1OHj6idCc+kWp06wYGB29dvkDI0DkSm5DvJd13rUVELv3pNcTRXLrdZM6aEhIZO+mPqV4O+rFihfGRk5OEjx2bOmodcqFChXLs2rcqVK5MkJZ07d2HixClqwsbR0bFP7y9Q/4bACw4OPn/h0oq/Vz97FrZi2aKY2Jiu3XprjYCLi/PCBbPcXF3//Xf3pD+nPn36TD6EPf369vx26Dc/jvj+6LET4eER8qHcuXP1+KJrkSKFUMt/9fq1/62A3Xv2qYnGvxbOsbe3HzBocJ3aNdu1a+3pkQ82KWI1ecp0TWlUrmzptm1bFyxYwCNf3uDgUCiHuXMX3L13X+00eDjdu3UuU6YU7otqN1y4U6fOLFu+UrUv7tAhX1WtUnnmrLlIyZYtmrm4uERFRSGdc+SwVqSSg/3G9atj42KRIOJFRjhdunSoUqli4cKF3rx9c+H8pc1bt584cWrKn79DQw4fMUq1r6Oe8dSaFwmJibi1Wl7AQ2verHHtWjW9vb1y5nS5d+8BHmruvIWqGaHJ4kVz7ezs+vX/2s0tZ9s2rXxKFMuXLy/ieeHCpdlzFmh2U0TR6tmjW9Gihb0LeEVFReMWyFxYdvIJuDVKAgSMkK+CVKWMJgjz2yFfxcfHnz17vmrVyiVKFFMThOks8PpEz8bGZuni+SnFcNqM2bIBiIyAQaqZEarn16tXp3+/3ocOH922/d+vv+pfoXw5CwuLW7f8V69Zp+qi45E3bNyidq+0vZ6EEEIISRuZKwjPHDsuvS8IM4lnISFTxo5PQ1/Nfzds3Llps+qFLm6uEISaZ+Ixls6eA+cwpa5caY4DkREOiZB8aqDeiQ9q4U+eBOOrb0mfYsWKmJqarF651Nra+tWrl6g74oPtS5euTPhtLM5BfR3V6GZNG5cu5duwcUvUm0VQnTq2g3ITmgf15jx5chcs6F27do3pM+YgzIsXL2uNG6y/hQtmQw1Cy4348WfNExYvWdG+XRuEhrqvqPIaGRl+8/XAHl90w7WQYaFPn7o4o3y51qxZHTJs2IhRQpuh+gsNACU2aGC/Du3bRke/fBEZiWo6PlUqV2zdthNMGHELRweH0aN/hBWJbTxOWNhzD4+8+fN71Ktb64dhI/fs3S9HpknjBiOGf+/s7CQp+7IiJtWqVsanfPmy3343QlZB9erWweWFCnnPnDEFkVy5am3TJo3s7GzFUSsrK5EgQg1C4P3269i8ed2xjRBiYg2aNm3UsGG9wUN+qF+/DkTC48DA1MZT/7zA11/G/Vy0aBFsR0VHx8e/KV68KD7wZr8Z/P35Cxe15pqTk2OVKpUgqqEkv/v2G2NjY2xDbaKk4VOjRrU+fQfKug6p9PVXA3r26P4uv0KfOjk5NWxQD585cxfOmj1PnOajLKWqzRb6p0xK/DxqBFIbyjww8AkKQ/Hixdat36R6QnoKvJ7RgwOPW6QUw6CgJ6nKCBRdnHnL33/N6mX2dnZ4bSE4IVnxQSQXL1kuTuvVs3uTxg2Xr1gF3Sj2pO31JIQQQkia+TRjCD0KeNVt2nTH+g1mZmZV6tTK5+U1bdwvsTExzq6uPmVKFyhSOIeNzbOQ0GP7D9wLCBCXtO7aBSfs3rK1VsMGhYoVM7e0eHDnzu7NW1+/eiVO6PX1V3f8/I7s3Se+OuXMWath/dx58yUmJT66d3/f9u2vol9qxqRUhfJlKlX6Z8nS6KioHoMGmpiaWFpZla9WtZivL46uXbLkZVQ0Kkwly5UtULhwPq/8Ma9jbt+8eXTffq3DDtXiYGZuXrtxIzysmZn5nVu3rl+69ODOXflkJxeXmg0b5M6XFxoy8OHDgzt3v0hu1G/Stg3SZOX8BVGRWbrjXMaC6jgqfKiIX79+U/OoWi0cFgr+LVDAC8bF0qV/JyYmQNtMn/YHapMdO7Rdt37j5CkzoKygvjZsWKWYjaZhfVHjbNum5ZjRP+Euq1atXfTXMlguyN8K5ctOmTxxwq9jpRTkKIAqKFyo4LXrN0b9PE7rCWgpQPRQf4XyEXt++nFYl84d4Gz8OXn63n0HYmNjzc3NOnVs//13g1Ej37PvwL59B6TkrrCK6nLZst179IVHhK9e+T3nz5vp7p4HTzR33iJJ0ZPQfP78mSWKFwsIuD3pz2lnzpx7+/atTY4cY8eObNyoweifR5w8dTpaWcihxCb/+Tvis3DRUlS1RWc8eErTpk6qWaMa0mfJ0hXYgzq3p2c+bAz+ZtDmLXC+N/n734YniT0rVyxBFf+Lnv2uXLkK6xt78OwL5s+C63jy5Gk8jn+AYtYfaIypkyfOmjkFaXjT71ZcXHyq4ql/Xnh6eiz5a56tre2/O/dANT18+Egk0Z9//AZlAjXVolV7rZlSQukqQ+L+8P0QOFHzF/wFZQK3H9FDaUEIA/r3HT3ml3f5NeKHLl06Irl+nzh/y9btsbFxiE+nTu1H/TQMWv3Q4SOiZPooy97V5KKof8qkRL26tWG4waNDIqD8yMX7/QdJY4HXP3qnTp32LV1R9abVqlWd8ucEuIt/LV52//6DVGWESKXWrVqgsCHZETe84F8N6o8E7/9ln7X/bHil/OmuVasG3nrZ403z60kIIYSQNPNplp0wNTNzzZ0L+qpN9642traQWKjfQA32/Gpg6YoVQoOe3Lxy1cHZqVOfXu4eHuISBycnjwIFWnTsULBY0cBHD5MSk4qWLNmuR3c5TARo6/BuxlR3Tw9os1zu7tBgoU+eFPct2XfIEHNtE6Nb58iBC42MFcI4PCwMshAbr1++ev7sGT6Jyqpwk3ZtoNBs7OwunTkbHRlZvmqVVl06a30u1ThYWFr2Hvw1HudFeMTjBw+KlfLt0q9vEaWqAXk88vX65itP7wKP7z948vixd5EifYZ8kzNXLnHUu2gRBydHJIiUnfDy8kK19e7de1onGyz5bnjhu+qgEFGopy5cuAROCETL7j37hPI5cPDwmLG/CckRHBLid1Mx7YeDMl98ShQfO2Yk/K4h3w775bdJqG5iJ2qfp06f/ePPqah64uu1FGqc7dq1xr/QV5A3UgpATXXo2F10B0VNHWoQEWjZuiOq5lCD2AmNsXTZ3xuVfeRwwrtnUVadUSf+ouc7NQju3rs/b/5f2IDfKPb8PmEcZMzpM2dbt+184sQpEQ1YNBMnTcETKWzGKpWxp0jhQn9M+g1pMnDQkKnTZspDs3Dh7LkLsAEtKvYUL1YU0ggb43+ZCJV75cq1WAVxSMyCBQso9O2Vq/iKoKytrebNnYHc+Xvlml59Bvjd8hfe5qNHjwcP/UEEIqebnvHUPy9wX0gaiJCp02d99/0IIUJEEg0cNBSxhcNZurSv1hzxSVZWI34cDeEn7GXcFLriZ6UObN6sCRQsNuDNQg3CB+vYuQfkCh5cxAfKZN8+RX9ReKfJYf7XdTlVKaMVhDBq5HBE6efR45HUDx48RNEt6F0AbQfvPUiaCnyqoocw8dTyp1bNGtOmTIQaRCmC2kxVRsBiha2HjTlzF0CFirjhhJmz5iGF0RJRtEghSdkGVFy0Ad24IaXv9SSEEEJImslch7BkGcWYFtU91y5egiEmhFadxo0O7tp9+shRcahclcrGJiaLZ8yChMPXs8eO9//hu7KVK0FNScpqATQSDi2YMi0xIcHIyKhDr575C3q75ckdHBj03l0NDBq0aI7/L5o2Q/iH8Oi6ftmvSu1aB/7dqSO22/5Z5+jiDCcQMlIeQ5jD1tandOlb165tWLFS7IFXWbSkD/Rq+DNd4yGr1qkNEbthxd+3lDUYRP7L776t06TxrdsPl2wAABAASURBVOs3UONBDFFRXjZnrgjExc0N/mS9Zk1XLlCMw1m3dLmLq+u927el7ISou39gAKFyGg+Fl1i0CJIR8kz1nIiIF9Aby5atVN35XDmcT4jMnj27GRsbo1a9d+8BtfBPnDwtNq5eu6F5dzgqZcuUjoqK0rxQleDgENH/EJXXfv16YWPot8M1Z8s4ePho+/Zt5ElKxaMtXrL82fslKiREEZTo+OfhkQ+ez4sXkd98872aIoWShJbz9fURS/n16qXo8QhP5uixE2r3vXz5iqTwc/KLr2IKHyi3f9a9NywWnhJkAMSDEEWgWdPGCPzy5asTJ01WCxP1ewgDRO/q1Rupiqf+edG0ScO87nmOHz8JLaR2JjTDrVv+sJjUZnyVEWm7es06uUeizOnTZ/CrAt2Fh42Pj+//pWJkGlTZ48fq3TsvXblSv34dLy9FuiFn4Z2i7F1Xxk3/lEmJoYO/ypnTBTG8dEmRO4qQb9ysVLF84cKFEKw4J80FPs3Ra9+uNbQZNiA15eKhf0YUKVIYmRseHjF/wWLV0/AIoaFPYWDGK0s12oAsLCygJ1++VPxQp/n1JIQQQkh6yFxB2KxDO7U9sP7eJiaKVurgoCBZDYLdW7ZePH1aqEEQ9vRpSNATB+UyD5JCECpG7u3btl2s9wD7wv/6dQhCR2dnNUGYEzWg3LkvnDot9yZ9cOcu7D6vQgV1C0KtwBKcM+nP+Lg4eQ/kIgSho5OzbkHoW77c/dt3biW3Z4eHPd+y5p+XUVHQw3AC3fLkObxnrxzC0+BgPHvFGtXt7O1fRETAM8RHymb4pDyAUOEkKGvh164rqoPeBeCfmMNLCQv7T2uhWo/aLeST2tyPMLvw702/W/b2dnXr1ELZW7lyreYtzMwUhgyUjKYeAHlyK8zbwMCg+Hhdff9kqlWt7ObqevOmn1ynV8VE6UjHxSsKlaL7olIJ79y1R+00JyfFCMDwCEX9vl3bVvh367YdsNo0A+w/8Bu4Ny+jX9rY2NSvpxi516Z1S3hfCgtIYQJJwgsyNlLc9+nTp+IqIZY050QVZtQ1FWUu7v73qjWi+6gaIulExukZz1TlhfBmV61ZJ2nDWCSmyhsqI6ct/DHNoyYmJsJ0io+Pq1K5In42UMB+/WWMSCvVdLNUdi4Q6ZY/v6eVldX9+w/EA+qfMlop6VOiU6f20Ehw4eSdSHkIQriscuFJW4FPc/R69ew+7Ieh0PPDR4z6d+d/xVL/jBBFa//+g5p2upNyXGuEUrWWVClp6Xk9CSGEEJIeMlcQwqNTm2VU1A+EqHv4/rR72BnzOgYemqLjpZ29mbm5pZXlM2WvIeXRRAg81TF1gcoOS1YazoBYKtApp0vLTh3lnajY2Sur12kgMiKimG9JOIdOOXNaoG5oaYmdhkZGOi6xymGN+Ac9eqS60+/qVdUYBj1876g42dHF5UVEhJQtKaB0YG75aZnRB24JhATquKLvWQltXmKRwoVQJYVilOfSkJJn8IeK8/e/XblSBWgABBKSXKhUKV6sqJRy3R2Vb/wrfIyUQPhfDep/587d0WN/LV++LPacOXNe65l4HPwbEHAH/7q754GKg6/4TKN9QTymGLcmAjx16ozWAFFRFpORVq9WBfZgTExMpLLzs5YzIyP9kpfOg+TAv+fPX9S473tzvUKKiBlEtK487uzs5OLiAj/qrvJ1Fh1cPxjPGtWr6pkXuLuI55kz5zTPRKnImzcP1I7m5KWSnLYhIWL8m8ZdFMFCYMAIrVBBEW1ob61rJyDfnz4Lu3VLMZ45ed6jG6lNGU1QXH8Z/zNEqZ2d3Z7d2+T95krxozqMMG0FPm3RGzJ4UP8v+yBNvhn8narJnKqMEBG+fEV9WQ5bW1t4jHDaHyl1XQmVzrfQkGl+PQkhhBCSHjJXEIYGB2udZTQxSdFc/eL9idFzuefpPnAAqkcwx+4G+Me8el2qQnkDQ0P5EtV6j5SsKt8156sg6u7QbaqHXkZHR0dqryJ/ELFW4cuo6Id376I+a22Tw6dMGUNDAx2XiDioRVjj6Hte05t4xckmykPZExNTEym5q5saYvjWtm3vev2p1iNlRB302vs9yooUKWxkZHTjph/yQiR7dFS01ru3V7ofV1PosCrcj9y5c0kpgIr4uLGjoEAWLFT0kROGRoxy3KAacDtbtWyGjfUbNks6F1cUh8Rjmikj/+qVFkWKanrjRg2ehYUtWbpCPCMSoXuPvppn+vr6wCQMCFB0RXZxcc6Z0yUi4kWgWo/r98fIScnFFdaNVj3culULPNGNG37C9keLie54hj1/vnjJcv3zQqSkpBh+qSUxmzRuYGFhcejQEa0rT4gEfJWCjBd+15at2+VnXLNm3ew5C9ROQ/jFlLLqwsVLyjDFjDLXpFSmjCa9enYrWNAb6j0uLt7I8L8GJtFqJnJBkLYCb6E0NvWPHn4wR40c3qVzBzS79B/wjXhemVRlhGoHb1V83o+zauFPz+tJCCGEkPTwaWYZFeMK1dZvqFavrpGh4YKp08OULcSQghWqV/uvh57eq1c8D1PUSG5du3Z0334p3bjlyQ01qLoYfcUa1SXlUCIdV72IeIGnQwu86s4cNjZQOwlv34oY4mjgg4fyUUcXhW0YHqZrRbX/b0TFtFDhgmorthUo4IXqICyL7dvf9fh9p5Te9x+0V5qL/1cBFeUtf35P1IPVetB17dKxcmXF/IrXr2sfoXTm7DnkHQRhubKlz2lYarCh5ihXqz985NiRo8flZymjbaaTH0f8kCuX28WLl2/e9JP+qzqr13QhQWEBIc7C0EtQBohnVLu7h0e+hQtm29vb/ThyDL6+VT6je948UAVq79fwH77t2bPbgwcPm7dsL2moPhkx9eh7xlGSYtgvCjwsXLWsQSAD+iuU57XkdBM9BnXE8+fR46XU5EWSEmgVJKZamHnzun//3WBJ0SVSSydD+RlxGh4q+v1JhiFgmjdrjEK1abPCmhMrkXp6eqqFAJGDaCPTt2zdIRZUKKGaX6lJGTVglA0c8CUigOxQ6waJhz1z+ki+fHnlaKetwKcqeigwv08Y17xZk+fh4X37DrqZbCPL6J8ReB0QeTQK3NMwZt/1Rr7+zl/1LlAAYhhmppS+15MQQggh6eHTzDKqFVs7u2ehT8OS+wuVrlDezNzc0NAoteGEBAbBD/QpV1ZKdggRTsvOnfIXLPjBa4VNZ2r23/x+NnaKyfr8rr2ripmYmJRVzpGou8soKmL3/AOK+JTAQ4k9RsbGXfr1GfDDd6joixiWq1JZDsTYxKRMpUoRz8PDlO3rqJxZKZfhylZsVQ5mGzr4KyhAeWflShUWzp9lZWU1avQ4sda2qEeipeCWf4Dq5cJ8uP6+YSIkgZiZ8PiJUwjB2dnpm68Hyu6xpaXld99+A5EmvqbUJw318s1K5TB9+p8lS5aQ9yOnWrZounH9KmiGk6fODBk67N2zbFM8S4UK5Tp3+m85BDs721/Gj0btNjgkZPDQHzRjqErhwoqZXfwDboslAcScKD2+6FqokLd8Dmr/yhXt7eDMbNmicLpOnDgFi8bN1fXboV+jYi1Og479edQIqEEk2qifx4tGlpQ8HDH1qKpxFBUdfVjZ53DE8O+QEWInZEbbNi0XLZwtJsOUBe2uXXt1x3Pjpq2pyouoqCjR4/HHEd/D0pTDrFWrxvKlC21tbafPmHMyecYRNcQzIhlH/jRceLyScgLM/l/2+X3CeNx35KgxYhKgzUqfsGGDenXr1BKn4WjRIoWFGsQ5YlIWPGyhgt5y2UtVyqgxduwonDB33gLNQXHQXUh/RED0k0xzgdc/ekiTWTOnQA3iSbt07aWpBlOVEXJXZ01rVFVOw3dFEb11y184oul5PQkhhBCSHj6RQ6iNJ48DfcuXq9Gg/uP79/N5eZWqUP7RvfvyKg768+bNm0O7djdr365d927nT540NTMvX61K7rx5zxw99sFro168CAl6Usy3JOLg6Ox88czZ0CdPUK2pWqeOgQLDKrVrhgY9sbO31+0QggM7d/XxLtDjq4EnDx2Oi43zKVvGKWfOzatWi9qPiGG3/v0unj5jaGAIkeng6LDh75WiH2zPrwfldHNbPHNWSPJi0NmBDRu3tG3bCrXwTRtW37x5C8LGq0B+r/yesA5Q19yxY5c4TdQjr9/wV+2RCy8FHpSmKfHOkVBWmlGlnjVr3pjRP33Zr3eTxg39bvlDosCFMzMz27R5a7u2rYKCnoSHpziAc9ac+YqV4qtU+mfNikePA/1v+aMYFPT2QlUYJQQhjB03QTa0UaFHhJs2bTT65x+hjvz9A5ydnaHxULm/e+/+4CE/iBGDChuwSGH4Iddv+KndTk0orl+/qV2b1vnze6z/ZyUSJ/TpU0+PfGJmf9xoxE+jxWBdpMnUaTN/+3Vs715fNG7UALVtWC6wayTlQLiBXw2R1w0v4aPdmSzho8V3mjdvUflyZatWrXxg379waRKTkpBNTk6OuHXNmtWtra3k89et39SkScPChQpqxnPX7r3Dho8SIiFVeTFn7sIyZUoXLVpk984tSCgoE6iyPHlyi4UW5y/4S9KGSFsky+8TJ0PDVKlcETGHwChSpBAsLCTUpD+nyjOmBATcRsxhRM+eNRWGVXBwsI9PCbFyA/Krd+8BYuhjUUXZM7p+46Zc9vRPGVVaNG+Clg7cdPGSFVojjxKrmFemRLFTp8+mucDrH72+fXrVrlVDUjZwzJz+p1pk/lq8XLRH6JkRKZnPaod83i9p6Xw9CSGEEJJmspAgPLhzl72jY7W6dbD9LCRk/bIVHt4FylSsmIagrpw7Hx8XV6dpky79+sKsCw4K2rJ6TXCgXtPTHd23r27TJp379kEIQY8Us33u3LCpfotmbbp1jYuNvXH5yp4tW0dM+NXI6APWJazOJbNmN23Xtn7zZgaGhhCW+3f8e0M5779qDFt07CAp5yBdu2TZnVvvGuZF7ywpm4EaYcdOX8AhhI7y9fWRlBrm2PGTk6dMF53KBGpVXoHwtaBAVE0J1Pvz5nVHIHKlee0/G+CB/PD9EMgkVGTh+125cg1qE5IJNU7d/gMkQd8vv+rT+4uGDet7F/DK655HUs62f/jIcVSFNact+X7YTwiwa9dO7u55EA00BOCctes2rl27Xu7MCaUEcwbCIEZjLpNkQfjuMfEUbdp1/nH4d3Xq1hKJA+cQamHhwsX4V/XCLVt3PHj46Kcff4Aqq6Ws5UdEvIB/uGTZCnneGtl90pzEX2sX1mvXb+Du48eO8vUtCXUBZYL6+uSpM06dOoPMgrEj1vcDkZGR3br3/uH7obDaRDxjY2NPnzkLwaDm4+mfF7h7qzYdIRVKlyoJv05SrKwQvnfvgekzZ9+790BKgYLeBZC2OGHF36tj4+K6dOpQo0Y1tOPANzt46Mifk6erZdnoMb9AfkNIe3t7wd7EC/jo0WNcu2HjZnn5DbVMSVXKyMAoHjFeRkFqAAAQAElEQVT8e4Q/euyvat16VYOVkvt/pqfA6xk9eRVHFxdnFxdntcjIj6BnRgjrUrNowamGxsYrI+ZKFUaiaklLz+tJCCGEkDRj4J7PU8pKWCq7Nr1+9UrKCBAaqlxx2mZB0I2dg8PLqCh5znRDIyMbW9vIFy+SUpgfQgcmpqamZqav3h/CpBpDVA1j3p9JBQIS7eKx2iY8zCag4ggzTbMynVFYWFg4Ozk+DgxKm/CG+wSZBw/zlR4F1crKytnZKTAwSMeK9qkCoaFMoeqcqLM0os0CkYQajFSZmzedIEzU1JEvKU2YJAP36ejhvWvWrp86bVZKskegf15AAkFUvH79Wh+nqEP7tuPGjoQShn0q9tjAVsth/cFChfi4ueV88iQkNjW/G/qnzCchY6OXqoxIA+l8PQkhhBCSKrKQQyjIKCmYztDUZkBNTEhQ26M/b+Lj36S8eJ3WGEJ2Zmc1CDK7bxgcuUfpWNBM2H16nvxKiZRxPNO5AKYMZNgDlVmLMgSE+fD95VJSonmzJpaWlkFBT3SrQSk1eQF5oDknakqI6UAvX/lvHUh4g1pXR9SMjw7jMSX0T5lPQsZGL1UZkQbS+XoSQgghJFVkOUFICPncgYFZsuS7fq3SJyKl6VsJIYQQQogqFISEkAymbZuWtWpVX7rs742btkifAkNDw/MXLl28dNk/4LZECCGEEEJSJsuNISSEfO4YGxtn1IBJQgghhBCSqdAhJIRkMFSDhBBCCCGfC1loYXpCCCGEEEIIIR8TCkJCCCGEEEIIyaZQEBJCCCGEEEJINoWCkBBCCCGEEEKyKRSEhBBCCCGEEJJNoSAkhBBCCCGEkGwKBSEhhBBCCCGEZFMoCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsikUhIQQQgghhBCSTaEgJIQQQgghhJBsCgUhIYQQQgghhGRTKAgJIYQQQgghJJtCQUgIIYQQQggh2RQKQkIIIYQQQgjJplAQEkIIIYQQQkg2hYKQEEIIIYQQQrIpFISEEEIIIYQQkk2hICSEEEIIIYSQbIqRrZ299P+FoZFBDjebt3FvkxKSJJJdMcth5lXd083H9emtZ9JnQs4iLt51vFyL5zQyNYoOiZYyB++6BWIjYt7EvpXShFfN/PkquCOSMS9i4qLj1I7mLpXLzNr0dXiM9BHxqJTXzMbs1bNXep7/OZaNjCWHaw4pSUp4kyB9RIq3LPry2as3MW/0PP//J5sMFM8eGRiZEJ8xCZ7OV5gQQghRw1jKNKoPqVKgtpfYXtV5bdzLeClNlOpUMuRGaPDVkA+eiQpEma6l8lZ0T3yTaG5jdmO734W/L0kk++GQ36HRL/UenQ2Mf53GUgc8q3qY25r5/esvpQMDQ4Ma31Y9s/h8TMSHNVISSEjKV8kd8ibo0hMpcyjfs8yB4OjXKvGxz2dfuFHBU/PP6HN5UkIiIlm8VdGIhxGRQVFqRws18A5/EBF257n0EclbwT3i0YvQm0/1OTnrlA1U66t9U1lsH/j98MNTj6Q0kYrIGEgl25bAz7KxmZGZtRmyaedPe6SPRdFmRUJuPH39/LU+J2edbEr/TQ0MDMr3Kvv4XGCa/wiqofkKE0IIIekhEwXhsRknj8086VzQqekfjaR0AM/hdfhrfQRhhT7lrBwtNw7Y8ub1GxMLEwfP/zfzk+iJZ9V8qF4fn31KSgcoP9Yu1ukVhAYG+at7Xlx9RR9BCCcEH+uc1lJmsrbnBrSYqO6xtDfPV9FdT0F479gDSSFmvLQePTz5GHStlIXJOmXj9oE7dw7exUb3dZ2ldKB/ZArWKQCrauvQHS+fvkJTRa6SblJWJetkUxa8qeYrTAghhKSHTBSEcDsk/Jf4X+0QleOWM5vu++XQy6cv8RWt47BBRP0yh2uOMl19FZ3lTIyCr4ce/P2wpBR4UIM5clpb5/Qt1rwo9mz79t+3cSn2k7HNbfPo7GOoQWy/iXkjOwYF63sXb1HUytkqLiru4amH51dcSniTgMi0mt38yvprJVoXM7U09dt569qmG+J83LRYiyLO3k4JbxNvbve7uuG6pB9O3k4F63pFh7y8tvmGsZlxme6lPCrlQ2N84IWgU/PPoqnbrYSrT9vilo6WhoYGdw7fK9qkcMD+O7AxK/WvgKO399+NehIlERVSmzJFmxYu3KiQpYMFCp5LERfs2TRoq6R06mA1e9fxMjY3CbkeemreadG+Dvvu2e3necvncfCwv3/i4YUVl3A7SDjfDj7mtuZGxoat57TAaRBLwdd0NUloLTNNJjWED4ONBmPrJLxJfPHoxcFJR2zcctT5qea/I/bEv1LYBbC1G09osO+Xg+Kl0Iq1s1XFfuVzFnV5G5fgvyfg8rqrUvJbhfjDSzn8x1FYZNKHqDKokrO3IzZQzxYmHiJTd1RtY3Njc1sL8aRQKeJF0PrW6Ai8UIOCRRoVxIbfrgBEUt6PV7tC77IuhZ2RBU+uhhyadET6RHyEslGsWZGCDbyvb75x+8DdD0coSfkj+T7VhlQJPBeI22G7SONCSL2zS85Lip7whvg9zOXrZmFnHhUcfWDCoVdhr1NbUG1y2zy/Fw41qLh5YpLsQiN3yvcua+duC5kR6vcMgaANLqUUSCkyUgaRUjbhTan0ZflcvrkS3ybcO/rg/IqLiW8TU/oZT8MrDAPTq4anbR6b2BexpxeeC7wYhMDxbl5ae+XJlWBxTt1Rte4euoekSEPZwPtba3gNtb81rsVylutZxi6P7avnr88vv4i/XylFRuzXfIV1Z4f+BdKlkHPZHqXvH3tQonXx2KjYS2uuwNKUUvl2YL/WP3wSIYSQrE0mCkItGCg6pxmZvJvJBnUdMxszsY2/o7FRcev7bUYlCapJ7Dy39AL+6jf6rT7+BkM4YY/uMRj3jz9AOCbmJg9OPlTttBYTHnNw4uHIwCibXKiL14p7FX957VVEBhWgArW9ID6tnKwa/loPd8GfOlQCKg+oAJG2b9xBU2tTu7y20ofAn2Gvmvm96xaAmr17+J6QuFAyOVyt947bD4FaoW951FcurLwE39Lew37LN9vr/FjTqYDT1iE72i1qfWPrzVu7AgrWK9Dk9wZRIdG399+5f/yh/iNt/r9Jbcrc2uXvv/d25YEV37yKP7f8ory/UH1vKJxj00+gwlS5f4VqQ6vuGb0P+9GWn7NoziPTjqGQ1B9TJ/RGKLIPBenh6UelO/tCiR2dcQKn6W6PT6nM7B61z9DYsNs/nfb/djgqOEo0jiACEIcFauW/ueMWvmLjTewbHWoQITQYXw9V0k1fbUNBRT0MLqJcQ8VLZJ/XzsjUSNKDM4vPoXrXflFrVNrEHqQq/KJcPm5Vvq6EDUnZI1Qc0v7WpAzMrnvH7tcYWtXC3lzeCamJ9xd14n9H7FYKGA/p0/ERyoa5vTmyw9zGXEorNvhVzPHuVxHSAncR25AHTt6OO4btin8Z71zQSfwSpragPjjxED9E1YdUuXvkfvDVkMTkvIbUP7fswjP/MFMrU0iLGt9V3TVyb0opkFJkMoqUsgm/qFZOljt/3I2/GtUHV4mLjoMOTOlnPLUpg/eodJeS27/bGRkUhW2IGUnZpvk04FnhxoXE64aWl9y+uY5OOyGlqWx4VvNUiyRaMBuMr3t64Vlcm8vHtfrQKv/03oi/F1ojI9B8hSWd2aF/gcSrmrOIC9oLtn33b6F63qKPq5TKt0NK4Q+fRAghJGvzcQVhyqAOZGhkgD9y+DMvt4Yq6isJinZ0bOhT57ix1Q9/tIo1L1K8VbGwO2FocEWLJvY/Ph+IKrujlwP+Tr94/MLB00G+BFYGLsEH7g38SfxJMzAyQK0IVTFDE0NEJvSGroFJOK3q12iydXpw8tGJWaee+r+b/ADCz7u218U1l+HASIqugE8Rq4urL2P7ZejL2MjYyCdRr569Qp0gJjLWwt4i4mHEmb/OwQpAhcOrpmfZ7qXRtnpsxsmkrN37LgNBK4B9Pju1nWjVTm3KJCYkSQkJkF7YUC0zntU8YLwIS+TGNr/6Y+uYWZuKIT2o94hcDrz4xLWEK8oALse1KHWJie8FklIkUZ/WWmawX4hAbKiGc2unP+xEIQhR2bqebBdoRZjkqG+5FHLC12f+z1BFkwUhRJq5rVl06EtJD95qzkKRpGhkgeWCyq/aK6bjrdGK4hnfJMgaQ+BeLo+lg+WZReeEHRqw74706cjUsiF4cPxh5OPIzBhCCRWkHPhnigIm/87ojowmiBhkRvGWRWv/WFMhqNZdE17u87vhklIUOXjYRQdH5ymdS75EMwVSikxGoTWboII8KufFi//icSS+wpJCrikEoRLNn/GUUgbtL3hVVW8H3XL74F1TKxMjYyO8wghEdT4n/90B8PrQ5BfzIhYyCSGLkiylvmxoRhKmenTIS4QMNSgpm4og7dAEllJkJK2vsM7sSFWBxPuOIoE/T7f2BMDls7S3wF+oVL0dKf3hU+0oRAghJAuSVQQh2qdLdyrZcWlbWBbXNt0QQ2tSC0TCozOP8cGf0tKdS1YbXGV9303YX7hhQbRTht+PQL3ZwtZCtdNpxMN3He3iouOFXZn4NvHwlGO+7XzK9Szz1O8ZWjd1zHFnbGpk42bzOjwmMigySuUvN1pP0XRt5WglegxKirb8h7AuRfiSsuVYNB7DkIGv+C7+iUkQimgVdinsbJPLRspOWDpaamotmGNiI/0pA1nyQNkNDzy/91zcUVRrIh5FiP2oTqE1XUp9JGFa6l9mJOUwvPK9y6ItX0Ts3vEHOk6GGkSJdS7k/C6SL+NRY5OPyq0nGY6Ot0Z/EPnw++FyHTprkiFlI/nycHykTCBg7x3Es+mfjfGLAQMNWihtvhy0weHJx/Cb41Urf9VBlVDRhzvtVMCx5vfVXj57FfHohYWtOcwi+XytKZBRkdEfxMrQyPD53XfCBomMZpH/IqnxM54S+PWAulPdE6ucKReSGG5k1a8rI+sfnnx4YeXlV2GKjrWQZPC3vesUuLHdDw1Se8bs/++mqSwbmpG0zmmdlJgo94gJvflUlLqUIpMSOrIjVQUSrZPit0XMHoxWWgjCVL0dKf3hY69RQgjJ4mS6IMQfD+i0NzGK2iQ2UK1EI6I4pDp5RmRg5KE/jxqZGqGJtNrgysFXg+VREEkJSWgellID/qpdXnetcKNCtrltUJ317VTy4O+HRR299ogaQpi9Q5vRFHTxCT5QlaU6law+pMqG/ltSuhGqUJsGbUXN3rtugTZzWzwLCLt75P7D04/ECJzH5x4/Ohso6YG5jRkaYr1q5Icbc+fwvb3jDmjO3/j/zd3D9/DR3J9RKYMiYZvnXU9O29y2Ys+7Yyk0XkOFGr5f8FKKpJRymREjadUKMN4CNHnAH8DhO4fuqlWmE+Lfwh+Qv6K5Aa/MpTVXtMoqBw97E0uT8Hvh6ZmDHoaGM1U0igAAEABJREFUgeF7S5JC5ep6a/AI8QmGJh/up4rIix6tmS0Y0kOGlA2BtYuVlZMVfnP0nEtTUla7kT5i5DN4E/tG1mM5VH4hUaWGT3526XnXYjlrD6+BH0z81OiOjA7g5Qbsve3TpjjMwFu7A3zalYDRLQy3ok0K56uU979TtaWAjshkErFRcXiV7PLYCocQP+yqzSIpzWOkmTIXV11O6RY3t/vhg5JQ9atKvh18Tsx5N58N0qdcjzKvnr9++fQVfuFVQpf0vGlKkcSfiRwu1mf+OifpHRmt6MiO1BVIbcmYqrcjtX/4CCGEZBEyZWF62DgeVfKhEox2aPdyeaKCot51JEuSQv2eYY+k7EsmD48RlxgYGKDWGHwt9G3s2wSVoReht566FXc10qP2WbC+t2J9LUlCBQv+BsLBX3EEi6ZlMeICyi1P6dy6AzG1NLXPp5ieFH/2wgLChJTVDWoJJ+eeXttzA9SCdx0vVLPQYgp54F3X28LeQsRHbgbWSqUBFfGMl9dd/af3xvPLL2Y3NaiDjEoZOGl5yuRWDMgxN/auVwCt5jEvYnVfAq/PqaCTmbXpBwPXUWZQO3x2Oyx3qVzS+1VE1DIhdPHx3x2gFlrQpWA3H1doS/H1yeVg1IaLNi0syjD8Dfg58smVB1ZsMrGhXGNLG3CN8JgO+f/rFPrBtwbOUr4K7h8cuxh4IQjSsWTbEiZKkYPXXMp6ZGDZKNSwILLDq7qn7suRGiXbl1CknoGUr6I7CsmLwEhxKPTGU5QWCHLEJ7dKsjt6OSiyI0kxFS38GdUypn9BzVM2d07lNC24Lx7Zxi2HuK+c19APBep4fTAcHZHJJPAXJPhqiFctL7xrVk6W+SrmDbz44XVZ9E8ZpLb4rYaainoS9Tb2v4HKj88+NjY1Kt+zjOpUSRly03tH7jt42ucunQuvG76i6QTprzsyWtGRHXoWSB2k6u1I7R8+QgghWYRMcQgT3yZW6F0WPgnMPfwhV8xEn4zfDr9K/SsUaVL46a2nqt3qyvcqi0Zf/KXBn5CLq6+otv7e3n+nbPfSHZa0wfa6vpvexuqaZbRSv/JvYt6gOvXs9vODk46Iky+uvFTj26oQmWgXR0O4GN6QEiaWxg1/qYdHwMm4XEzxpw9Qs2iXxcfQSPHX/eiME9W+qazoBBscbWlvce/YfR1z3B2ZfFQxcoZokFEpc2Orn6OXY5t5LVE84l/GHVBOY6ubJ1eDg68Et5jezNjM6MjU4zoWBtRdZi6vvVqidbFSHX1Ql9r98z6xE0bH87vPUREXjsd7970S/PhcYOvZzWEMru2xHjW8/b8exNuEhobXETGoaJ5bdiENo9Sg6+r8WBMbptamtX+smfgmwX/vbRiPknIY1YW/L9UYWsXSwdLvX/+Lqy/jQXS/NTit7Belu6zs8OLxi23f7cSe9ovbwBiB3wU9U7hBwYhHL/aM2Y8X+cBvh+D5F2tRJC4aVdU3m7/eJmUxMrVsaAWWrEelfKU6+eJ2ptZmF1Zekg2c+yceQiJ2WtE+9kXM4/OBpsn9KTyrehRpXOjls1coAGgjeHTucRoigxJVfXAVIzNj5D78LnhTYpT11Q3Xqn5d2atWfijVG9v8NPtFq6EjMpkHGt3q/FSr/ZLWxqbG+C29vPbKBy/RP2UcPOyqDakSExELZRUVHIWT5UP4/QnYd6d4q6J3D+vlgup/U/wFPD7rZM3vqycqBxuD/b8dQr6kFJmUXuFMzY7Uvh2p+sNHCCEki2Dgni/tbYc6A1aMzIGt9+rZS7UKPfQS6kDvdfhRgqqkqaWJntNjpASkoJWTFepSaj3oYFdaOljoPzc6GqER7Zh0r/yLGpi4b9qGYJGMxdTKFGUMNScpE0htmWk9p8W1zTdu79d3nhV4g6ggvgp79dHaDlL71ugAVUMDI0PdQ6HSDNQy9Oc1nXPzfJBMLRtawS+euY0Z7qjZnxY/nqL3nSqwaLD/ZWh0egoAzChLRws0Xmj6PPjlhC7VcyKrNEQGTQYHJx4Jux0mpQNLR0sklxjklrGgdcbK2Qp/mDTnMa48oCLU3dHpJ6TMwECydrZGjqjmuI7IaCVDyoYOUvt28A8fIYR8XmTaGMIkKaVBC/iLpakGJWVvk/T/mcefVbVp2d5FJzEpVfXajFpWC3/OI4O4gERWIf5VfOZNcKJ/mclZxMWzuoeplcm9o6kYefXBfowZTmrfGh28TnfbSmaTqWVDKzp+8TTVoKScYTL965RC76WUp6mS6xkSmTSg/+DM1JKYoOVvh20e29wl3QrUzr/zxz1SJpEkaa46ozUyOsjs7Ejt28E/fIQQ8nmRVWYZJST7kL+Gp5Gx4e6f92XlqVYIIW4lcroUdTk46UhmLCVCCCGEZBEyrcsoIYR8FIzNjBVLwL2hus7SmFiawMjiknSEEEJIVoMOISHk84bjlD4L5KU1CCGEEJKlyJRlJwghhBBCCCGEZH0oCAkhhBBCCCEkm0JBSAghhBBCCCHZFApCQgghhBBCCMmmUBASQgghhBBCSDaFgpAQQgghhBBCsilGtnb20v8XhkYGOdxs3sa9TUrgglfZF7McZl7VPd18XJ/eeiZ9JuQs4uJdx8u1eE4jU6PokGgpc/CuWyA2IuZNbBqXavCqmT9fBXdEMuZFTFx0nNrR3KVymVmbvg6PkT4iHpXymtmYvXr2Ss/zP8eykbHkcM0hJUlcuZEQQgghUqauQ1h9SJUCtb3E9qrOa+NexktpolSnkiE3QoOvhnzwTNTzynQtlbeie+KbRHMbsxvb/S78fUnKetjnsy/cqOCp+Wckkjk45Hdo9Eu9R2cD41+nsdQBz6oe5rZmfv/6S+nAwNCgxrdVzyw+HxPxYY2UBBKS8lVyh7wJuvREyhzK9yxzIDj6tUp8UlUgkxISEcnirYpGPIyIDIpSO1qogXf4g4iwO8+lj0jeCu4Rj16E3nyqz8lZp2xAmVf7prLYPvD74YenHklpIhWRMZBKti2Bn2VjMyMzazNk086f9kiEEEIIyd5koiA8NuPksZknnQs6Nf2jkZQO4Dm8Dn+tjyCs0KeclaPlxgFb3rx+Y2Jh4uCZRc1PS3vzfBXdKQgzD8+q+VC9Pj77lJQOUH6sXazTKwgNDPJX97y4+oo+ghCGFT7WOa2lzGRtzw1oMVHdk6oCee/YA0khZry0Hj08+Rh0rZSFyTpl4/aBO3cO3sVG93WdpXSgf2QK1ilQvGXRrUN3vHz6Ck0VuUq6SYQQQgjJ9mSiIITbIeG/xP9qh6gct5zZdN8vh14+fYmvaB2HDSLqlzlcc5Tp6qvoLGdiFHw99ODvhyWlwIMazJHT2jqnb7HmRbFn27f/vo1LsaubbW6bR2cfQw1i+03MG9kxKFjfu3iLolbOVnFRcQ9PPTy/4lLCmwREptXs5lfWXyvRupippanfzlvXNt0Q5+OmxVoUcfZ2SnibeHO739UN1yX9cPJ2KljXKzrk5bXNNwyNDBH/XL5uFnbmUcHRByYcehX22sYtR91RtY3Njc1tLVrPaSEpK4XyfZtPbXJhxUU8ac5iLgjk3+G73sS+9aiSr3RnXysnyxePI88sOvfUX9HJzaWQc9kepe8fe1CidfHYqNhLa648PheI/UamRhX7lsclr5+/RshuJVz3/XIQj5+zsHPAgTuhN1K0UAyNDPKUyQPL4sa2myHXQ62drSr2K5+zqMvbuAT/PQGX111FVtYeUQNnIkz/PbdFTh2bcQKZXK5H6dv778ByyYweaJX6V4CTc3v/3agnUfqcX7Rp4cKNClk6WKDguRRxwZ5Ng7ZKSqcOVrN3HS9jcxM84Kl5p4VFBvvu2e3necvncfCwv3/i4YUVl3A7SDjfDj7mtuZGxoYimyCWgq/papLQWmaaTGoIHwYbDcbWSXiT+OLRi4OTjqAM1Pmp5r8j9sS/UjhUsLUbT2iAbBIvhVa0ZocA8YfldfiPo7DIpA9RZVAlZ29HbEAOCRNPR4HU+tboCLxQg4JFGhXEht+uAERS3o9Xu0Lvsi6FnZEFT66GHJp0RPpEfISyUaxZkYINvK9vvnH7wN0PRyhJ+SP5PtWGVAk8F4jbYbtI40JIvbNLzkuKN1TL70lqC6pNbpvn98KhBhU3T0ySXWjkTvneZe3cbdFSEOr3DIGgDS6lFEgpMhIhhBBCPk8yURBqwUDROc3I5N1MNqjrmNmYiW1Ua2Kj4tb324xKEiSH2Hlu6YXzKy42+q3+3UP3AvbfwZ6EeF1V0vvHHyAcE3OTBycfqnZaiwmPOTjxcGRglE0u1MVrxb2Kv7z2KiKDClCB2l4Qn1ZOVg1/rYe7oCIIoVh5QIULf1/aN+6gqbWpXV5b6UOgVuRVMz/UFDTS3cP3hMT1quHp5O24Y9iu+JfxsElFzKNCotE8n8vHrcrXlbAhKTvgyeHY5rEt17MsKtPHZ52097RHVRExrPVDddTP8EQl2hSvN7r2uj6boHVRg89ZxAV1u23f/Vuonnf5XmWFIPSq7gmptnfsftT2an5fDTVd7Hx89rG5jVnlARURPWFKqNbe7PPaIeaILeKGyD+/89zQ2LDB+HpPrgRv+mobUgaVQthW+Ir8unf0PjKi/ug6UOaojKLuizxCTRH17EoDKt47dh/K8PndcCnjuLUroGC9Ak1+b4DoIfD7xx/i8XWe7++/93blgRXfvIo/t/yivL9QfW8onGPTT6D+Wrl/hWpDq+4ZvQ/7Ya3kLJrzyLRjKCT1x9QJvRGK7ENBenj6EXQ4lNjRGSdwmpqlpkZKZWb3qH1IzG7/dNr/2+Go4CjROIIIQBwWqJX/5o5b+IqNN7FvdKjBlLJDHEWmIAfRECDpwZnF51Ak2i9qbWz27sXXUSC1vzUpg3KFAlBjaFULe3N5Jwoq3l9IlH9H7FYKGA/p0/ERyoa5vTmyw9zGXEorNvhVzPHuVxFKD3cR21p/T1JbUB+ceIj2r+pDqtw9cj/4akhicl5D6p9bduGZf5iplSmUXo3vqu4auTelFEgpMoQQQgj5TPm4gjBlUAeCSYV6alx0XODFILFTUV9JULSjY0OfOseNrX6o0hVrXqR4q2Jhd8LOL7+I9n7sf3w+EFV2Ry8HVJtePH7h4OkgXwL1hUvwgXsDKYXqjoGRAWpFqIoZmhgiMjpcNUlZY6v6NVwXpwcnH52YdUrYd++eyMZMOVDHFIH8tz9JoWkT3ybAGtD6RKjo++1UdP0SHgW8vujQl7d2K/yWy2uuwLFBq7wYa4QnurLuWmxk7K09AWW6l7K0t8AlecrmhmZ7FhCGEx6ceuRZJR82Yl7EwrDCxzG/A4Rrsz8bw006Ofe0hb1Fxb7lTCxNoQN3DN8tz2LiXi4PXFlU/lwKOeHrM/9nqDELBRJ+PwJGJZ4i7O5zew9797K58RTQafjAw4RERF0TngdUYmqHwKEVwD6fndpO2CwRDyPO/HUOJklu31xeNT3Ldi8deCHo2IyTSSn0S0eK35MAABAASURBVExMQBInQHphQzWFPat5wHgRsbqxza/+2DqKrFGOa4WWFrkcePGJawlXlAFcrsimhMTExPcCSSmSqE9rLTPYL0QgNlTDubXTH3aiEISQIteTLWKtCJNca3YAiDRzWzMUEkkP3mpOJJNygdTx1mhF8YxvEhIT3hMkKEuWDpZwtoUdGrDvjvTpyNSyIXhw/GHk48jMGEKp9fdEd2Q0QcS2f7ezeMuitX+siXDwAyK8XNGIg8YFBw+76ODoPKVzyZdopkBKkSGEEELIZ0pWEYRony7dqWTHpW1hWVzbdEMMrUktEAmPzjzGB1Xz0p1LVhtcZX3fTdhfuGFBtItDzKDebGFrodrpNOLhu452cdHxwq5MfJt4eMox33Y+5XqWeer37MLKSzqmIjQ2NbJxs3kdHhMZFBn1/rSQAXvvoCrc9M/GsFzgS1xZf02fGpuajrJytIQNKLbfxL6NehJl5WApvsZExkINKmOumOkRihqC0KWw870j9+VHE4JQBjZUZFDUy2evbNxyQHvDy7JytoZ6jHwSJXqICSA/kETOhZzfpczLeHEjkTgQD4pKf5JiW9WYguxE4DCUoKtli0N/LB0tNbUWzDGxgYovIonw8YA2uWyk1IO8eKDshgee33su7igq/RGPIsR+pCTsHSn1kYRpqX+ZkZTD8Mr3LgtrRUTs3vEHOk7WkR2SopoeJGUOOt4a/UHkw++HCzWYZcmQspF8ebj8wmYsafs90QSa8PDkY0YmRl618lcdVAk/OPhZcCrgWPP7avhlQFORha05fF35fK0pkFGRIYQQQkhWINMFIapW0GlvYhS1SWygWmliYSIOqU6eERkYeejPoxAYXjU8qw2uHHw1WO7WmJSQJLo+6g9qzJfXXSvcqJBtbhtUZ307lTz4+2FRR689ooaJucl/p2ozmoIuPsEHqrJUp5KwvDb035LSjVCF2jRoK2r23nULtJnbAuLq7pH7D08/ghUT/zoevtbZpeddi+WsPbwGHvBuslRDc76BofYVIMUASBmoLEggsQ3hgRSLiYrVEfNn/mF2UCxKC1HuuIhUhVHjVSO/azGXR+cCz6+4GHIjFIoOlb9/em5wL5cbka/cvwIO3T10L/haCPQt8ujSmit61eMNpJxFXRC4R+V8z+88Dzhw58jU42kYTAiXEh/N/eY2ZjBwED58qjuH7+0dd0BzZkt9QJGwzfMuQWxz24o9746lMAcKVKjh+wUvpUhKKZcZMZJWrQDjLUCTR6EGBXH4zqG7apXphPi3Rsb/KW3d2eHgYW9iaRJ+LzzNy0hI2gokCpuutwaPEJ9gaPLhfqqIvOjRmpUFQ4aUDYG1i5WVkxV+c14/13dMHVpPkD7yi/8m9o2sx3Ko/ELq+D1JKTI6wBsasPe2T5viMANv7Q7waVcCRjd0HQ4VbVI4X6W8/52qLQV0RIYQQgghnx2ZsjA9NIxHlXyoBKMdGlIkKijqXUeyJCnU7xn2SMq+ZPLwGHGJgYEBao3B10KhphJURsKE3nrqVtzVSI/aZ8H63or1tZQSCP4Gwnn1/DWCNTQyFIOmoNzylM6tOxBTS1P7fIrpSVEpDAsIE1JWN9CBJ+eeXttzA9SCdx0vVLOw09HLQXHTJMXUkXAbVMNBI72ZtalDfocPhgyNYZfXTjGo0kAqWM8boYlOsCnx+EJQ/mqeiL+du22+Cu9qdUiKYs2KPD77eF3vjcemn1CEkFzJQ748PP14/6+HNg7cGvEgokLfcrjXk8vBsVFxRZsWFolmYWcOAyGlOzp4OlT7uvKrZ6+2Dtm+Z+z++8ceZOzUMpUGVETuX1539Z/eG88vv5g2NSgpnbQ8ZXKjeKC27V2vAGwciG3dl8DrcyrohJz6UNi6ygwq689uh+UulUt6v8aOWjiELj7+uwPUQgu6FOzm4wptKb7qzo7KAys2mdhQ1jNpQ7NAfvCtgbOUr4L7B8cuBl4IgnQs2baEiVLkyK0bWYoMLBuFGhZEdnhV99R9OVKjZPsSitQzkPJVdEcheREYKQ6F3niK0gJBjvjkVkl2Hb8n+hfUPGVz51TOpoP74pFt3HKI+8p5DUFboI7XB8PRERlCCCGEfHZkikOY+DaxQu+yiuFkCUmQHIqZ6JPx2+FXqX+FIk0KP731VLVbXfleZeHmoR6GStLF1VdUO8Xd3n+nbPfSHZa0wfa6vpvexuqaZbRSv/JvYt6gOvXs9vODk46Iky+uvFTj26oQmdAqaAhHNUhKGRNL44a/1MMj4GRcLqb40weoWTST42NopKj7e1b1KNK4ECxEVNRQp3907rF8JtyAC39fqjG0iqWDpd+//hdXX04pzFC/p5dWX2kwvl78yzikzLEZJ3SvXgBFCkXXfErjV2Gv7p94mLeCO3b6/XvrxjY/SSdI8OtbbuKDyCcmJO3/9SCyD8r2dUQM4n9u2YWUhkW9eBihw0FNP0cmH1UM/Uo3N7b6OXo5tpnXEsUDiXlAOY2tbp5cDQ6+EtxiejNjMyPYnjpGReouM5fXXi3Rulipjj5QGrt/3id2vngc+fzuc1TEFWMy1e57JfjxucDWs5vDGFzbYz0q3Ppnhw6g6+r8WBMbptamtX+smfgmwX/vbRiPkrYCiQfR/dbgtLJflO6yssOLxy+2fbcTe9ovbgOfCn4X9EzhBgXhP+8Zsx/l6sBvh+D5F2tRJC4ayuHN5q+3SVmMTC0bWoEl61EpX6lOvridqbXZhZWXZEcRry0kYqcV7WNfxDw+H2ia3J9Cx+9JKgqqhUn1wVWMzIyR+y+fvjrz1znRwHR1w7WqX1f2qpUfShW/FZr9otXQERlCCCGEfHYYuOfzlDIDA8XIHNh6r569VKvQQ3KgDqQq+QSoSppamug5PUZKQApaOVmhLqXWgw52paWDhf5zo1s5WSLa+qwdpwMYDkiEl6HR6ZQ0kIIIRzMlUwL2TlJSUukuviaWJmcWnZPSCswo+ADQlhkiybICplamKGOoyEqZQGrLTOs5La5tvnF7v77zrHz87EjtW6MDS3sLAyNDRF7KBKCWoT+v6Zyb54NkatnQCn7xzG3McEfN/rR431WH9Qoy5PcEPw6WjhZovNB0QfHLCV2apN8ykhn140YIIYSQT06mCULyKbB2tkLjffC1ELu8dhCEx6af0L16Hvkk5Czi4lndw6NS3vX9NnM2jvSTIYKQEEIIISR7klVmGSUZwtu4t7a5bdzL54l/FX9x5SWqwaxJ/hqeRsaGu3/eRzVICCGEEEI+LXQICSGfN8ZmxooV+d5QXRNCCCGEpBo6hISQz5u0rZFICCGEEEKkTFp2ghBCCCGEEEJI1oeCkBBCCCGEEEKyKRSEhBBCCCGEEJJNoSAkhBBCCCGEkGwKBSEhhBBCCCGEZFMoCAkhhBBCCCEkm2Jka2cvfbZ41y0QGxHzJjZdk87b57NzKeQcGRQlpQkrJ8tizYq4Fs9pm8fm+d1wtaNmOcy863iF3XkukY8LUt6ruqebj+vTW8+kz4ScRVxQWlCWjEyNokOipcwhnW+NV838+Sq4I5IxL2LiouPUjuYulcvM2vR1eIz0EfGolNfMxuzVs1d6nv85lo208UmygxBCCCGfF5m1DmGZ/7F372FRnXcewM9wHYYBHOSuiIDcRVFRFBG8BMGN0QaTJu5u07rpbtOmaWvS3aZ52m2um6btpumTZLttNumapI0xiVndYESRi+CVm6LIHeR+v98ZZuh3PEhGBoYRBsXO9/Pwx5l3Zl7OzPueed7f+3vPOd9YtfLhUO2SDx79SNmvFIxq3b41pxp6+jtmNdxxX+7mFbmk+mKNduGqvSsbC5oa8hunffvoqDCqGnX0USyN9CpOKp3wrMzRJvKJ9UVflgh0Bzn6OO54Kbb6Yu1w/7AwU95RS6UO1oWJxcIsSMwkMU9HXXg3e8CAXjoKqlGvDZ4Ib+ry6oW5oXvUKLwUgTv8z/33BUPePqpSYyeXPxjcUdWhO40SEOfXfr3jDs+ALInw7KjubLrWbMiL50nfWBTmHvdirHZJ8supE36FZu+uNAcRERHdW+bwxvSYfU989vj4w1H1qGBsB/d9qlaqhdkp/LK4KGliwIaZ9f72fkMCwv62/sufXvGN8Q5NcNB9FuPUAw//WaA7yzvKq+pcdeZb54RZcPRWyF3ksw0IJRKfaO/cv1w2JCDEIYM/uatcmEu6R41MIfVa72lgQFiRcV3QpBl9J3027TcZmjmSeWz+9A04sOfPatVYW4zOwfc2/5uDiIiI7ro5DAg16Y7JgsBdr9+f835uyK5g1xCXnsbexJ98qRwcWf+ddV4RnlZyzbqvq0eulZzQpNpcApzDv7W6MuN6aMLywe7BvI8u12TVipVsfHKDs99CbGBgpz3/jURHyANBsoWytor2s/91vrOmS88eLvR13PRUJDZaStvOvD02QIz49lpEg3aucrlrGHYSJUefThwZGrG2s47ZH+Xk72RmIUG1F9/Nnna92e43dkrwPQjCkR99oV3usdJ99T+GLfB0GBkcKThaeOVwAQodlyo2fCcCmUZEDvmfXi1JLhNIEDY8EYFMTmlyeXe9QWt6g3cGBu4IQGIWfc8lyAUlh588ItzI1CHr67fN10Jq2Xi16dzvz4spMqTv0PpL1i3G9195pirn/Tz8O4RwYY+skDpIzS3MEt7ejZchWGq4om92AH0mZHeQs5+TakR97f8L0YIovP+1eGu5NTbint+mUqo7qztTXku3d7fb9tzmxGeThvs0GSr0q7/7j7iTL6X0NvdOVbnc2Xb9v6xzDXYZGVIVJ5VcOpQv3DywsP9IeaX96jSmHoTp6B412Jn7frbVQmohdbARP2npqTKxQ/pv91u+O9jW2Xaoe6jqXFX2+3kqpUpP5QFx/kE7/AXNDEtJsdYMi52bXcTj4S6BzmiC+vzG1NfShbvkDvQN/Pj4x/ld/byg9FS5Ibs0qlbr/khGfjeivbJDsVSz6EA9ok75ZVpLSeukzYHphgff2nX5kyuhCSFWMqvCY0Vi2wlTN4dbiOvafWsWLHboa+vPPpBr9JwkERER3XPmMCB08LDHiErcbi5uGZ9Nd1jssHZfOMYomW+eVXgrxNFQa0lr/qErA12DLkHOO16O667rbixowjjVNcgFod3RZxIDYv3W/VP4eEB44d0sDOO+/k6ChfVXH8Fvq++qR1emv56JwW7IrqCN39+Q+JPjevYQo67E55IC4/wXhy8aL8z6U072+7k7XtlenlohRmWq4bFxcGlKeeqvT2MAFxDvH/fCfQe/+Yn+E7GOPZek8Fyw81c7tAuRW9j+/H05H+Qmv1SG/JHHCjcUmlmYYVxel1eX8lqaR5jHph9EdtZ2/c2f4GSIoi9L/GOX3f9qXHdjT2lyWWVmlXJAqff1xcUnSiO/t17ZN5x1IHe8PGC7H4bUGW+c6W7oiXwiYtP+qKR/P4ly5Hlcg13Tf5sx0D6w/RfbmgqakAGrzLzssdE4AAAKfUlEQVRedb569d+HIRI7/bszeJn+RDTG5RjE53yQd/KFFCu51YIlY7ni4z87iZb9xsd7k19J627oFof+2AEEh8u2+Fz7oggPsaEcVOqJBlFD3Iux9ZcbDn//qK2TLY4pdAw8FJ9FuKVYssDcylwwgO5Rg2/1yP4vPFa4b3xqAzaEGytCxafwhSAU6arttvdABLtlqG/40sF8PZWXpZRXZFRi0sRGIR0vxCGMQwnxUuKzx/ta+32ilwp3zx3oG1KFFM0htZcauEubfrhR3BjuU577w1iGFq28JMITkyCYLMMXqLpR/+TNIREwr7Rsq2/Kq2l4V/zLsfjVEqPZSZvDYZF93Iv3nf/jRXwQ/PJE79/48eOfGX0lPxEREd1b5jAgxMAdQZ24jZGW9lMYzhYe08SH4ycylaVWYFCL2WtruVVPYw+iJvG9GGpfPnRlsGuwKKlkzWOrZAob8S0jk0ViQTsDG681W9pYuIe6ImES+mAIRkt6koQYoGMwNB7viTQruFSavB42tJ8a6hnCWFBqb+3s74wkHgZqcle7jqoOQc830K/EWH9CYWB8QHtl+/hEvrgAD7lQuYtt3sH8gc7B8rQKpDJ8Ni01qYDQPdRN4bVgQiHSLPiGL/xP1sX3sheFefhu9g5/bHVtTl3G785Otb5OrRoVVCq0LDa0m89709LarFrxxDxkZbc/vw09bahXk6PDLENTgeb0s9rcerdQN7QI3o73ogOo1bdUMtVOIldjZWuFrJGZpRn6iVgboFwMArGhXU/RsWKkE8WAEKHI1ZudYVJivhrRiEuAEx62FLcggBkPCBEVSB2se5p6BQNMctSMauY71CMqJPQnHAg12bU4+pBFR+TTWdPp6O2ov3LNZ1SqxhdAijzXLpY5yi68kyWmQ0tO3s2895z2DdH1zKqumi7Dz9lrKmwWewhyv9rlAx2DOR/maZfoaQ5MruEHFn9IQbstdxV/UiZtDqQNexp78SMjzkPhLb4x3jzDmYiIyMTNYUCIyE33Iisi3QtmRP0gEkFRS2nrUPeQuaUZwi2xHDlDRIPCjXhMuLG+Ts8lZDBuxovdlruJD5EN0M4fzhKquv+X8RhgtZW3aUZvo4KldCaVYyd1Fx/KFsqw5/1t/eLDtvJ2lAimBJ9XN9ZCckzcwKC5q767q67bJdDZ3sNeuH0IS66fqRK32yraxP8oDvo7qseievQxpHeE299JzH2k/WdG2MMr1u5b01zYgqG8/mAeQ/Z1j4c7+zuJO1aReV3Pi9FhRoZGnAOcx3ayd1g8IkS1uXXC3AiM9w9NCEEWHdGmjYMN9kG4fdh5TH+I0eC8ZZS+cfPt7fgTDFZyolQTpuqozZvYrHqao6Oq8+ZODlvbWwtTk7vKR9VqzGuID5uuNYsfk4iIiEzZHAaEekxYpOS4VOEV4Xno24cxsMYs+LItPl89dztXROhvH9Cc3fdetjBro6pRiZlEu8Q/dtlgz5C4lgxRwfKvBWs/OzKsQhxrSM397f3Ofk4TCjHEl9pLEe6Kca/DYvuu2hneBuMehbwo/nTLkZJFAsc3xgeJkbK0ihMvnJrZDULwDTssHlvJ6bDIQSwZe26KLoYo1OzWPjDVTkJdbj3+kCRctXdl9I82fvrE/41VorkKrTChL2E0X5ZSjnQNni5LLZ+QaFINj5hbfLUEFL3a0sYy76PLk4ZVOHYsZZbtFe2zufkKkl0Ss1t6L6LcsL0rU15NEyPbrc/GWEotb/kIwyozy+nXqWLnxRWtusm0+cMofUOEPL+tky1itvHJnZmZ8As5TXMY/COJHx87FzlS7gIRERHRTfPixvQScwlGPGbmEoybA+L9MKoWZqQ8vcJrvedYDkeiuXYL6hRmpKmo2X25m7nWkBd7iJAPe4jxd8ju4Amvb8hvxOz7Qh/HaWsuT690CXJZss5TEyRINItFBc1VbVqHeoeQBEChk58Tckdzl/m5t2z47no0xKVD+R8//ln2gdwZ3y4S3+fiNYvs3OyQfPaLXYY0zkDnoP63INfn5O9kLbearm7BSmal8NLczxOBRGtJq3Lgq9gMkQMad9EqD+HWnlh0vASBLv6Kj09csFeX1+C+wm38KKi/1DDYPRS8M1BMd9sskDotWzj+4sjvrUfiejyemZnWsjZ8TEet3ot5GTNzM/E/ojcuXr1IZyfrMYkz7bmLtTl1CB1XPhQqptOR4BXmHyP2jYB4fzSHb7S3YFTTNoeBKtIrHb0Vi1Z7oEI8RKyOCFYgIiIi03Z3MoQTtJW3V5y+/tAfHlSNqFtLW8fPj5oKhkTbfroZG1Zyq60/3axWqopPlCKFcvXzazYO0t1vPNDX0qu5YGlz79EfH5tykl8QtvxrtGuwC0aBGNc++qeHUPLZk0fEufnS5LLwx1Y/8t4ebB/658MjgyOlp8oRxe098LDE3Kzg6LUJCRlkby68k7Xl36KRH0j99enqCzUhDwSFJoRoFj1KBLHyjDfPIomET3f+jxdjnolCDUgyVJ6pai5uwT9N/21mzP6okF1B1vbWBUcKUYNAgpD+m9OTrqm7XfhKF/ou3PP7ryELPdw7dOrVtGnfUp/f0HC5Ad3Jwto8/fVMPTcGtJRZxL8Uqx5Rq5QqdJUJOepLB/PRE1Y9ugKRxvGfnxQLkcpuK2/DKF/3HFf0kJqs2oS3diExePBbnwz1Die/nIKs44o9y/s7BhCEZP1vzgzuLDfVUSPcyEflfJAXs3+jzFFWmFic+5dL+CC5H+bFPB2lUmo+FDq/vbuddm14Wfg3V//Dh4901nQefQZHmfD1d/egPyPLjeg3MM6/o7oz6RfJiJBPvZK66YeRIbuDhnqG8eV//tRRYZ6Z075hFNM2h65JmwMJxsw3z27+cbT6xtmtkPxKam9zn0BEREQmTOLpZeTJ7BnD8Bfhk7hmcjZQidxFjnpmX5Uu5GeGda5DMwOYoUdGUdk/jOTPhMKBjoGZna9F07KytbKSWfa2zMkI2NZJhtjVkPsNihLe3n3l84JSg+8vgr6HHFFfa59RImRDIF8tc7Tpa53V6keRTGGDmRTsvDAHEC0j4Lmi99o805rTvmEURmsOiSB3lmP+or/dCC1LRERE97p5kSEU6b+dgOEw0DHwnnUzMO1aMgNhbr6nsceQQjIiJHLn7gInho/UXYNcvKOXWtlaVpyuFAxmrL5nOCSRjBINClrXE5635rRvGIXRmmNU0HObEyIiIjI18yggJDIRPjHe5hZmx39+cj5faoWIiIiITME8WjJKRDQDFtYWmtsDKhldExEREd02ZgiJ6N7Gc26JiIiIZmxe3HaCiIiIiIiI7jwGhERERERERCaKASEREREREZGJYkBIRERERERkohgQEhERERERmSgGhERERERERCaKASEREREREZGJYkBIRERERERkohgQEhERERERmSgGhERERERERCaKASEREREREZGJYkBIRERERERkohgQEhERERERmSgGhERERERERCaKASEREREREZGJYkBIRERERERkohgQEhERERERmSgGhERERERERCaKASEREREREZGJYkBIRERERERkohgQEhERERERmai/AgAA//90pgQJAAAABklEQVQDADwEwEi4a5pHAAAAAElFTkSuQmCC",
    "media_type": "image/png"
  }
}
```

> AGENT

O screenshot capturou só a parte de baixo (o painel é mais alto que o recorte do elemento por causa do header sobreposto). Mas o que aparece já é a evidência do problema, e dá pra comparar claramente:

**O que está na tela confirma o diagnóstico:**

- **`Just Sans <strong><em>`** → "Em 2025, o estudo SINISA revelou dados." aparece em **negrito, mas perfeitamente reto** — o itálico foi ignorado.
- **Franie normal** vs **Franie itálico** → aqui dá pra ver a diferença real: a linha "Franie itálico" está **claramente inclinada/cursiva** (porque a Franie tem arquivo itálico verdadeiro).
- O readout (verde, monospace) prova: as três linhas pedem `font-style: italic`, mas a Just Sans está com `font-synthesis: none` → não inclina. Só a Franie inclina.

Ou seja: **a Franie já funciona; a Just Sans (corpo do texto) é a que está "sem itálico"** — exatamente o que você relatou.

Deixa eu rolar pro topo e tirar a página inteira do painel, pra você ver também as linhas da Just Sans normal vs `<em>` lado a lado (que ficaram cobertas pelo header).

> TOOL

tool_use mcp__playwright__browser_evaluate
id: toolu_01N4mUWjoYZATPtZ1y1Ywtn9
```json
{
  "function": "() => { window.scrollTo(0,0); const p=document.getElementById('bit-italic-demo'); if(p){p.style.position='static';} return true; }"
}
```

> TOOL

tool_result
id: toolu_01N4mUWjoYZATPtZ1y1Ywtn9
```
### Result
true
### Ran Playwright code
```js
await page.evaluate('() => { window.scrollTo(0,0); const p=document.getElementById(\'bit-italic-demo\'); if(p){p.style.position=\'static\';} return true; }');
```
### Page
- Page URL: https://cambrasmax.local:8484/
- Page Title: Uma Concertação pela Amazônia
- Console: 4 errors, 6 warnings
### Events
- New console entries: .playwright-mcp/console-2026-06-10T01-03-54-061Z.log#L11-L12
```

> TOOL

tool_use mcp__playwright__browser_take_screenshot
id: toolu_01Nw7HobRpm36DAuW7Ky1WPb
```json
{
  "type": "png",
  "element": "Painel de demonstração do itálico",
  "target": "#bit-italic-demo",
  "filename": "italico-antes-completo.png"
}
```

> TOOL

tool_result
id: toolu_01Nw7HobRpm36DAuW7Ky1WPb
```
### Result
- [Screenshot of Painel de demonstração do itálico](./italico-antes-completo.png)
### Ran Playwright code
```js
// Screenshot Painel de demonstração do itálico and save it as ./italico-antes-completo.png
await page.locator('#bit-italic-demo').screenshot({
  path: './italico-antes-completo.png',
  scale: 'css',
  type: 'png'
});
```
```

> TOOL

tool_use Read
id: toolu_01L9fxsS1E173te9nVDw5mtW
```json
{
  "file_path": "/Users/dcambria/scripts/server-tools/v2/docker-dev/sites/concertacao/italico-antes-completo.png"
}
```

> TOOL

tool_result
id: toolu_01L9fxsS1E173te9nVDw5mtW
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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",
    "media_type": "image/png"
  }
}
```

> AGENT

Agora está completo e visível. Esta é a foto do **estado atual (antes do fix)**:

**Just Sans (corpo do texto):**
- `normal` e `<em>` são **visualmente idênticos** — as duas linhas "Em 2025, o estudo SINISA…" estão igualmente retas. O `<em>` não inclina nada.
- `<strong><em>` fica negrito, mas também **reto**.

**Franie (títulos):**
- `normal` vs `itálico` — aqui a diferença é nítida: a segunda linha está **cursiva/inclinada de verdade**, porque a Franie tem arquivo itálico real.

O readout confirma a mecânica: os três casos da Just Sans pedem `font-style: italic`, mas com `font-synthesis: none` o navegador não fabrica a inclinação → fica reto. Só a Franie tem itálico de arquivo.

**Conclusão visual:** o "itálico que falta" é mesmo o da **Just Sans no corpo**. Esse é exatamente o problema que o fix (Camada 1 — oblíquo sintético cirúrgico) vai resolver, fazendo a linha `<em>` inclinar como a Franie já faz, sem tocar na proteção de fake-bold.

Quer que eu agora **aplique o fix** e te mostre o "depois" lado a lado nessa mesma tela pra comparar? Ou prefere primeiro revisar o spec/ajustar algo na abordagem?