---
session_id: 5add7883-9a20-463b-be39-addad9c1abcf
developer: "gh:dcambria"
split: train
source: entire
repo: Bureau-IT/concertacaoamazonia
start_time: "2026-03-16T06:27:28.820535Z"
n_turns: 17
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Implement the following plan: # Plano: mu-plugin bit-dropdown-btn ## Contexto O componente "Download dropdown" da página /publicacoes/ tem seu CSS embutido na `style.css` do child theme (seção 11, linhas ~285-430). Não há PHP específico para ele em `functions.php` — é puramente CSS + HTML widget do Elementor. O objetivo é isolar esse componente num mu-plugin independente, seguindo o padrão Bureau IT. **CSS variables** usadas pelo componente estão no `:root` do child theme e ficam lá: - `--btn-normal-*` — cores do botão - `--ucpa-icon-download` — SVG data URI do ícone (linha 228 do style.css) - `--e-global-typography-text-font-family` — Elementor Kit ## Arquivos a criar ### 1. `bit-dropdown-btn.php` Caminho: `sites/concertacao/wordpress/wp-content/mu-plugins/bit-dropdown-btn.php` ```php <?php /** * Plugin Name: BIT Dropdown Button * Description: Componente dropdown button para a página de Publicações. * CSS isolado do child theme — depende das variáveis --btn-normal-* * e --ucpa-icon-download definidas no child theme (style.css :root). * HTML via widget HTML Elementor: div.dropdown-btn-wrapper > * div.dropdown-btn-container > button.dropdown-btn-toggle + * div.dropdown-btn-menu. * Version: 1.0.0 * Author: Bureau IT * Network: true */ if ( ! defined( 'ABSPATH' ) ) { exit; } add_action( 'wp_enqueue_scripts', function () { wp_enqueue_style( 'bit-dropdown-btn', WPMU_PLUGIN_URL . '/bit-dropdown-btn.css', [ 'hello-elementor-child' ], filemtime( WPMU_PLUGIN_DIR . '/bit-dropdown-btn.css' ) ); } ); ``` **Notas:** - `Network: true` — padrão de todos os mu-plugins do projeto - Dependência `hello-elementor-child` — garante que as CSS vars do `:root` já estão carregadas - `filemtime()` — cache-busting automático (padrão do projeto) - `WPMU_PLUGIN_URL`/`WPMU_PLUGIN_DIR` — corretos para mu-plugins (não `plugin_dir_url()`) ### 2. `bit-dropdown-btn.css` Caminho: `sites/concertacao/wordpress/wp-content/mu-plugins/bit-dropdown-btn.css` CSS extraído byte-a-byte da seção 11 do child theme (linhas 284-430 do style.css HML): ```css /** * BIT Dropdown Button — Estilos * Versão: 1.0.0 * * Requer variáveis do child theme (style.css :root): * --btn-normal-bg, --btn-normal-txt, --btn-normal-bdr * --btn-normal-bg-hv, --btn-normal-border-hv, --btn-normal-txt-hv * --btn-normal-icn, --btn-normal-icon-hv * --ucpa-icon-download (linha 228 …

> AGENT

Feito. Arquivos criados e copiados para a fonte canônica: - `mu-plugins/bit-dropdown-btn.php` — enqueue do CSS com dependência `hello-elementor-child` e cache-busting via `filemtime()` - `mu-plugins/bit-dropdown-btn.css` — CSS do componente extraído do child theme - Ambos copiados para `docker-dev/common/mu-plugins/` **Próximos passos (fora do escopo):** - Remover a seção 11 (~linhas 284-430) do `style.css` do child theme - Verificar no browser: `/publicacoes/` → hover nos botões DOWNLOADS deve funcionar normalmente

> DEVELOPER

pode seguir. também preciso de revisão no css que dão destaque nos listings das publicações na mesma página. não quero misturar esses códigos customizados no style.css atual, pois está uma bagunça. qual a melhor alternativa? mu-plugin mesmo?

> AGENT

Sim, mu-plugin é a melhor alternativa — exatamente o padrão que já seguimos. Deixa eu ler o CSS relevante primeiro.

> AGENT

O `style.css` tem só 252 linhas — o CSS do listing destaque está em outro lugar. Deixa eu procurar.

> AGENT

O CSS já está em `css/pages/estudos.css` dentro do tema. Deixa eu ver como está sendo carregado e o que vem após esse arquivo.

> AGENT

Entendi o cenário completo. Tenho duas observações antes de recomendar: **1. O CSS de `.listing_destaque` já existe em `css/pages/estudos.css`** — mas o `functions.php` só o carrega em `is_page('estudos')`, não em `/publicacoes/`. O CSS que aparece inline no DevTools (fonte `publicacoes/`) vem do **campo "Custom CSS" do Elementor** da página, não de um arquivo. **2. Mu-plugin vs. `css/pages/publicacoes.css`:** | Critério | `css/pages/publicacoes.css` no tema | Mu-plugin | |---|---|---| | Padrão já estabelecido no projeto | ✅ (home, artistas, estudos) | — | | CSS acoplado ao tema (usa `--ucpa-color-sage`, IDs Elementor) | ✅ melhor aqui | ❌ mu-plugins são componentes reutilizáveis | | Carregamento condicional | ✅ via `functions.php` | ✅ mas requer `is_page()` dentro do plugin | | Isolamento do `style.css` | ✅ | ✅ | **Minha recomendação:** `css/pages/publicacoes.css` no child theme, seguindo o padrão dos outros `css/pages/`. Mu-plugin fica reservado para componentes reutilizáveis (como o `bit-dropdown-btn`). O que você quer que eu faça: 1. Criar `css/pages/publicacoes.css` com o CSS dos listings + adicionar `is_page('publicacoes')` no `functions.php` 2. Você remove o CSS do campo Custom CSS do Elementor na página Confirma essa abordagem? Também: o CSS atual tem só o `.listing_destaque` com `has(a[href*="uma-agenda"])`, ou tem mais regras inline que preciso extrair? Posso buscar o Custom CSS via WP-CLI se quiser.

> DEVELOPER

ok, gostei. prossiga

> AGENT

Vou buscar o CSS completo do campo Custom CSS do Elementor antes de criar o arquivo.

> AGENT

O Custom CSS da página está vazio. O CSS inline deve vir do Elementor Kit ou Customizer. Vou verificar.

> AGENT

O CSS está no `_elementor_data` como classe CSS no container (não como custom CSS). Vou confirmar o que está no `estudos.css` e verificar se há CSS inline no `_elementor_data` da página.

> AGENT

Encontrei o CSS. Está em `css/pages/estudos.css` (já existe no tema, mas a condição de carregamento não cobre `/publicacoes/`). O CSS inline no DevTools vem do Elementor compilado — as regras estão no arquivo mas sendo carregadas pelo mecanismo do Elementor. Vou criar `css/pages/publicacoes.css` com o CSS revisado e atualizar `functions.php`. **Revisão que farei antes de criar:** - Regra duplicada: `.listing_destaque .jet-listing-grid__item:has(a[href*="uma-agenda"]) { order: 1 }` — redundante (a regra acima já cobre todos os itens) - `--ucpa-color-sage` — alias legado de `--color-extra-2`, substituir pelo alias moderno `--ucpa-color-3` que já é o padrão no projeto - Separar os dois media queries `max-width: 1024px` e `max-width: 767px` que são idênticos em um único

> AGENT

Agora adiciono o enqueue condicional no `functions.php`:

> AGENT

Feito. Resumo do que foi criado e das revisões aplicadas: **`css/pages/publicacoes.css`** — novo arquivo, limpo e documentado: - Removida regra duplicada: `has(a[href*="uma-agenda"]) { order: 1 }` (o `order: 1` global já cobre) - `--ucpa-color-sage` → `--ucpa-color-3` (alias moderno, mesmo valor) - `max-width: 1024px` e `max-width: 767px` eram idênticos → mantive ambos (breakpoints distintos) mas o 1024 já cobre o 767 — você pode revisar se quer só um - Comentário sobre `.elementor-element-540275a` alertando que é um ID frágil **`functions.php`** — novo bloco #11 com `is_page('publicacoes') || is_page('publications')` (cobre PT e EN). **Próximo passo para você:** - Verificar se o `estudos.css` ainda precisa das regras de `.listing_destaque` — se a página `/estudos/` não usa listagem com destaque, pode remover a seção `8.4` de lá

> DEVELOPER

ok, verifique o css de estudos de uma passagem geral no functions .php e me diga quais os códigos "gerais" e quais podem ficar separados para páginas específicas.

> AGENT

Tenho tudo que preciso. Vou escrever o plano agora.

> AGENT

Resumo do plano para sua revisão: **3 mudanças concretas + 1 documentação:** | # | O que | Arquivo | Ação | |---|---|---|---| | 1 | Remover `listing_destaque` duplicado | `css/pages/estudos.css` | Apagar seção 8.4 inteira (já existe em `publicacoes.css`) | | 2 | Mover seletor WPML | `style.css` → `css/header-menu.css` | `style.css` deve ter só `:root` variáveis | | 3 | TODO no jetengine.css | `css/plugins/jetengine.css` | Documentar que template-id 4360 é específico de `/participantes/` | **O que NÃO muda:** - `tec.css` e `jetengine.css` continuam globais (risco/benefício não justifica restringir agora) - `complianz.css` condicional no `class_exists` está correto (cookie banner é global) - `estudos.css` mantém o `.listing_container_thumb_bg` (duplicação de 3 linhas aceitável) Quer prosseguir?
