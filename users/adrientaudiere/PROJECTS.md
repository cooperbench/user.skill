# Projects: adrientaudiere

## adrientaudiere/MiscMetabar *(dominant — 100% of sessions)*

**What it is:** A large R package for metagenomics and amplicon sequencing analysis built on top of the phyloseq ecosystem. Used in mycology/fungal microbiome research.

**Tech stack:**
- R, phyloseq, ggplot2, dplyr, rlang, magrittr/native pipe
- Testing: testthat (parallel, 4 CPUs), covr → Codecov
- Docs: roxygen2, pkgdown, devtools
- CI/quality: lintr, codefactor, rcmdcheck `--as-cran`, air formatter
- DADA2 pipeline integration (cutadapt, primer removal)

**Recurring work themes:**
- **Visualization functions** with complex parameters: `tax_bar_pq`, `biplot_pq`, `upset_pq`, `hill_pq`, `ridges_pq`, `sankey_pq`, `circle_pq`, `ggaluv_pq`. User iterates heavily on visual behavior (label placement, sort order, log10 transforms, sample-level splitting).
- **Bug fixes triggered by R updates or dplyr API changes.** The `.` magrittr placeholder is being actively removed in favor of native pipe + anonymous functions.
- **Factor-level edge cases.** Recurring TDD effort: functions must handle single-level factors (single-sample phyloseq) gracefully — either returning output or raising informative errors.
- **Package quality maintenance.** Lint count tracked, codefactor grade checked after every build, R CMD check run at `--as-cran` level. NOTEs are fixed, not ignored.
- **Documentation site.** pkgdown site rebuilt on every significant release cycle; README rebuilt from `README.Rmd`.
- **Test coverage.** Codecov integrated with a hardcoded token; coverage by file/function reported and gaps filled with new testthat tests.
- **Claude Code customization.** User wrote and iterates on custom `/r-check`, `/r-build`, `/r-test` command definitions with embedded multi-step instructions.
- **Statusline customization.** Added usage bars (session + week) to Claude Code statusline.

**Test data objects used:** `data_fungi`, `data_fungi_mini`, `GlobalPatterns` (phyloseq built-in), `enterotype` (phyloseq built-in).
