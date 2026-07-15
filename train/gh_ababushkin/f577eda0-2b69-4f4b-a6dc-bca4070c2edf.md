> DEVELOPER

Brewfile is my main source of truth - i recently installed some extra packages using brew, that are no longer in my Brewfile - is there a way to find what they are and uninstall them

> AGENT

`brew bundle cleanup` does exactly this. List above = all installed but not in Brewfile. Few notes: - **Casks**: `google-chrome`, `iterm2` — probably intentional, just missing from Brewfile - **Most formulae**: library deps (libpng, freetype, cairo, etc.) — pulled in by something you installed manually - **Likely the "extra packages"**: `fzf`, `gnupg`, `imagemagick`, `postgresql@16`, `vips`, `openjdk`, `poppler` Two options: **Option A** — Add keepers to Brewfile, then purge the rest: ```bash brew bundle cleanup --force --file=/Users/anton/src/dotfiles/Brewfile ``` **Option B** — Just remove orphaned deps (safer): ```bash brew autoremove ``` Recommend: scan the list, add anything you want to keep to Brewfile, then run `--force`. The library deps will auto-uninstall once nothing depends on them. Want me to diff what's there vs add any of those packages to Brewfile?
