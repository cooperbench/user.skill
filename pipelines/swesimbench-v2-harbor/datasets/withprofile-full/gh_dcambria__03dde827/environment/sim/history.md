[DEVELOPER]: https://concertacao.bureau-it.com/atuacao/grupos-de-trabalho/ [Image #1] remova o italico dos textos da colmeia

[AGENT]: Vou primeiro entender a estrutura da página da colmeia (Grupos de Trabalho) para localizar onde está aplicado o itálico nos textos. Pelas memórias do projeto, a "colmeia" é o SVG dos Grupos de Trabalho (hexágonos 6 eixos, posts 26666 PT / 71726 EN, em `/atuacao/grupos-de-trabalho/`). O itálico que você quer remover está nos nomes das instituições facilitadoras (ex: "Instituto de Governança de Terras - IGT", "para Políticas de Saúde - IEPS", "Plataforma Parceiros pela Amazônia - PPA"). Deixa eu localizar a fonte desses textos.

[AGENT]: A imagem da colmeia parece ser composta por logos de instituições (não texto SVG editável). Os títulos com itálico ("Instituto de Governança de Terras - IGT", etc.) provavelmente estão no conteúdo Elementor da página ou em um SVG. Vou verificar o conteúdo real da página `/atuacao/grupos-de-trabalho/`. Primeiro, deixa eu confirmar qual ambiente está rodando e o ID do post.

[AGENT]: A colmeia é um SVG (`gt9_pt_desk.svg`, `gt9_en_desk.svg`, etc.) embutido na página. O itálico está dentro do SVG. Vou descobrir qual SVG está realmente sendo usado na página de produção e como o itálico está aplicado. Deixa eu verificar primeiro qual é o post da página e qual SVG ele referencia, e ao mesmo tempo inspecionar o itálico dentro de um dos SVGs desktop.

[AGENT]: Esses SVGs antigos (2023) não têm itálico, então provavelmente não são os usados atualmente na página em produção. O itálico pode estar: 1. Num SVG diferente/mais recente 2. No texto Elementor (HTML) com `<em>` ou `font-style: italic` no CSS Deixa eu inspecionar a página real em produção para ver exatamente como o itálico está sendo aplicado (no DOM).

[AGENT]: Agora vou inspecionar onde está o itálico — procurar elementos com `font-style: italic` que contenham os textos da colmeia.

[AGENT]: Confirmado: o itálico está em elementos `<tspan>` **dentro de SVGs inline**. Há tanto a versão PT quanto a EN (note "Instituto de Estudos / para Políticas de Saúde - IEPS" e "Parceiros pela Amazônia Platform - PPA"). O itálico vem de `font-style: italic` aplicado via atributo no `<tspan>` ou via classe CSS dentro do `<svg>`. Vou inspecionar como exatamente o itálico está definido nesses tspans (atributo inline `font-style` ou classe CSS) e de qual SVG/`<img>` esses SVGs inline vêm — preciso saber se é SVG inline no DOM (via mu-plugin SVG widget) ou um arquivo `.svg` referenciado.

[AGENT]: Agora está claro. O itálico vem de **`<tspan class="italic">`** dentro de SVGs inline (`<svg class="gtSVG mobile">` e provavelmente `<svg class="gtSVG desktop">`). A classe `.italic` aplica `font-style: italic`. O SVG está inline no DOM — não é um `<img src>`, é o SVG inline. Vou descobrir: 1. Onde a regra `.italic { font-style: italic }` está definida (CSS externo, não no `<style>` do SVG) 2. De onde esses SVGs inline vêm — qual mu-plugin/widget os injeta Vou inspecionar o source HTML cru da página e localizar os SVGs `gtSVG`.

[AGENT]: Diagnóstico completo e empírico: - A colmeia são **dois SVGs inline** (`#mobile` e `#desktop`, classe `gtSVG`) dentro de um **widget Elementor HTML** (`elementor-element-da94e3a`). - O itálico vem de uma regra **`<style>` inline dentro do próprio HTML do widget**: `.gtSVG .italic { font-style: italic; fill: var(--GT-TEXT); }` - Os textos em itálico têm `class="italic"` nos `<tspan>` (10 no mobile, 9 no desktop). A correção mais limpa e cirúrgica: alterar a regra CSS `.gtSVG .italic { font-style: italic; ... }` → `font-style: normal`. Isso remove o itálico de todos os textos de uma vez (PT e EN, mobile e desktop), sem precisar mexer em cada `<tspan>`. Esse SVG+CSS vive dentro do `_elementor_data` do post (widget HTML). Vou confirmar o conteúdo bruto do widget e os post IDs (26666 PT / 71726 EN) no banco para fazer a edição correta.

[AGENT]: Confirmado. Ambos os posts (PT 26666 e EN 71726) têm o SVG `gtSVG` com a regra `.italic` no `_elementor_data`. Vou extrair o trecho exato da regra CSS de cada post para fazer a substituição precisa. Preciso ver como `font-style: italic` está escrito dentro do JSON (escapes).

[AGENT]: Perfeito. Cada post tem exatamente **uma** ocorrência de `font-style: italic` dentro da regra `.gtSVG .italic`. A correção é trivial e cirúrgica: trocar `font-style: italic` → `font-style: normal` no `_elementor_data` de ambos os posts. Isso remove o itálico de todos os textos da colmeia (mobile + desktop, PT + EN) de uma vez. Antes de aplicar, preciso esclarecer **escopo e ambiente** com você:

[AGENT]: Vou aplicar em DEV primeiro, você valida, depois deployo para prod. Vou criar uma task list e começar pela edição em DEV.

[AGENT]: Importante: a página que estou inspecionando (`concertacao.bureau-it.com`) é o **tunnel do DEV**, não prod. Então o DOM que vi já é o DEV. Vou aplicar a edição no banco DEV. Vou usar um eval-file PHP para fazer a substituição de forma segura e idempotente, com backup do valor original.

[AGENT]: Vou copiar o script para o container e rodar primeiro em **dry-run** para confirmar.

[AGENT]: Dry-run confirma: 1 ocorrência em cada post. Vou aplicar de fato.

[AGENT]: Aplicado e caches limpos. Agora vou validar no browser (DEV via tunnel) que o itálico foi removido — tanto PT quanto EN.

[AGENT]: Conexão fechou momentaneamente (provavelmente OPcache reset/cache flush reiniciando o pool). Vou tentar de novo sem query string.

[AGENT]: DEV validado: - A regra agora é `.gtSVG .italic { font-style: normal; fill: var(--GT-TEXT); }` - Todos os 19 tspans `.italic` computam `font-style: normal` — **zero itálico**. Vou confirmar visualmente com um screenshot da colmeia em DEV (PT), e também checar a versão EN.

[AGENT]: O screenshot confirma visualmente: os textos das facilitações agora estão **em estilo normal (sem itálico)**. Comparando com a sua imagem original: - **Antes:** "Instituto de Governança de Terras - IGT", "para Políticas de Saúde - IEPS", "Plataforma Parceiros pela Amazônia - PPA" estavam em *itálico*. - **Agora:** todos em romano (reto). DEV está validado — PT e EN (a regra é a mesma em ambos os posts, e confirmei `font-style: normal` nos 19 tspans). Vou marcar a task 1 como concluída.

[AGENT]: ✅ **DEV pronto.** O itálico foi removido da colmeia em Grupos de Trabalho (PT post 26666 + EN post 71726). **O que fiz:** - Diagnóstico empírico via browser: o itálico vinha da regra CSS `.gtSVG .italic { font-style: italic }` embutida no widget Elementor HTML, aplicada aos `<tspan class="italic">` dos SVGs inline da colmeia (mobile + desktop). - Troquei `font-style: italic` → `font-style: normal` no `_elementor_data` de ambos os posts (com backup em `_elementor_data_pre_italic_fix`), regenerei o Elementor CSS e limpei os caches. - Validei: regra agora é `font-style: normal`, os 19 tspans computam `normal`, e o screenshot confirma os textos em romano. A imagem acima é a colmeia em DEV já sem itálico. --- **Você confirma que quer que eu siga para o deploy em produção?** Já confirmou "DEV agora, depois prod" no início — então, se o resultado acima estiver bom para você, eu sigo. O deploy em prod fará: 1. Mesma troca `italic → normal` nos posts PT/EN de produção (com backup) 2. Regen do Elementor CSS de cada post 3. `reload php-fpm` (obrigatório em prod — OPcache do pool FPM) 4. Invalidação **cirúrgica** de cache (WP Rocket + CloudFront) só de `/atuacao/grupos-de-trabalho/` e `/en/...` — sem flush […]