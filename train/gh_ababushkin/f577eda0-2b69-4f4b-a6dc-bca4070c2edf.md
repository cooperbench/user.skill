> DEVELOPER

Brewfile is my main source of truth - i recently installed some extra packages using brew, that are no longer in my Brewfile - is there a way to find what they are and uninstall them

> TOOL

tool_use Bash
id: toolu_01Kv1WQpCN76Pki34fJFFGuC
```json
{
  "command": "brew bundle cleanup --file=/Users/anton/src/dotfiles/Brewfile 2>&1 | head -50",
  "description": "Show packages not in Brewfile"
}
```

> TOOL

tool_result
id: toolu_01Kv1WQpCN76Pki34fJFFGuC
```
Would uninstall casks:
google-chrome
iterm2
Would uninstall formulae:
libvmaf
aom
brotli
libpng
freetype
fontconfig
glib
xorgproto
libxau
libxdmcp
libxcb
libx11
libxext
libxrender
lzo
pixman
cairo
cfitsio
cgif
libomp
fftw
fribidi
fzf
gmp
isl
mpfr
libmpc
gcc
jpeg-turbo
libtiff
gdk-pixbuf
giflib
libidn2
libnghttp2
libtasn1
nettle
p11-kit
unbound
gnutls
libgpg-error
libassuan
libgcrypt
libksba
libusb
npth
pinentry
```

> TOOL

tool_use Bash
id: toolu_01JvwQiNJPEkXivfrHPeLcBq
```json
{
  "command": "brew bundle cleanup --file=/Users/anton/src/dotfiles/Brewfile 2>&1",
  "description": "Full list of packages not in Brewfile"
}
```

> TOOL

tool_result ERROR
id: toolu_01JvwQiNJPEkXivfrHPeLcBq
```
Exit code 1
Would uninstall casks:
google-chrome
iterm2
Would uninstall formulae:
libvmaf
aom
brotli
libpng
freetype
fontconfig
glib
xorgproto
libxau
libxdmcp
libxcb
libx11
libxext
libxrender
lzo
pixman
cairo
cfitsio
cgif
libomp
fftw
fribidi
fzf
gmp
isl
mpfr
libmpc
gcc
jpeg-turbo
libtiff
gdk-pixbuf
giflib
libidn2
libnghttp2
libtasn1
nettle
p11-kit
unbound
gnutls
libgpg-error
libassuan
libgcrypt
libksba
libusb
npth
pinentry
gnupg
gpgme
gpgmepp
graphite2
icu4c@78
harfbuzz
libaec
pkgconf
hdf5
highway
libde265
webp
x265
libheif
m4
libtool
little-cms2
imagemagick
imath
libdeflate
openjph
openexr
jpeg-xl
krb5
libb2
libarchive
libdatrie
uthash
libdicom
libexif
libimagequant
libmatio
libraw
libthai
pango
librsvg
libultrahdr
libxml2
mozjpeg
nspr
nss
openjdk
openjpeg
openslide
poppler
postgresql@16
vips
Run `brew bundle cleanup --force` to make these changes.
```

> AGENT

`brew bundle cleanup` does exactly this. List above = all installed but not in Brewfile.

Few notes:
- **Casks**: `google-chrome`, `iterm2` — probably intentional, just missing from Brewfile
- **Most formulae**: library deps (libpng, freetype, cairo, etc.) — pulled in by something you installed manually
- **Likely the "extra packages"**: `fzf`, `gnupg`, `imagemagick`, `postgresql@16`, `vips`, `openjdk`, `poppler`

Two options:

**Option A** — Add keepers to Brewfile, then purge the rest:
```bash
brew bundle cleanup --force --file=/Users/anton/src/dotfiles/Brewfile
```

**Option B** — Just remove orphaned deps (safer):
```bash
brew autoremove
```

Recommend: scan the list, add anything you want to keep to Brewfile, then run `--force`. The library deps will auto-uninstall once nothing depends on them.

Want me to diff what's there vs add any of those packages to Brewfile?
