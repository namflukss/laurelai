# OpenFonts

The templates are designed for **Lato** (with **Raleway** as an optional display pairing) — both
SIL Open Font License, free to redistribute.

## You don't need to add anything to compile

`cover.cls` and `presskit/main_example.tex` use the TeX Live **`lato`** package *if it's installed*,
and fall back to the default font otherwise. On a standard TeX Live install:

```bash
tlmgr install lato        # optional — nicer typography; templates work without it
pdflatex example.tex
```

## Bundling the .ttf/.otf (optional, for XeLaTeX/LuaLaTeX)

If you'd rather embed the fonts directly (e.g. to match the web app's Lato exactly), drop the font
files here:

```
OpenFonts/
├── Lato-Regular.ttf  Lato-Bold.ttf  Lato-Italic.ttf  Lato-BoldItalic.ttf
└── Raleway-Regular.ttf  Raleway-Bold.ttf
```

…then switch the class to `fontspec` and compile with `xelatex`/`lualatex`:

```latex
\usepackage{fontspec}
\setmainfont{Lato}[Path=OpenFonts/, Extension=.ttf,
  UprightFont=*-Regular, BoldFont=*-Bold, ItalicFont=*-Italic, BoldItalicFont=*-BoldItalic]
```

Download: Lato — https://fonts.google.com/specimen/Lato · Raleway — https://fonts.google.com/specimen/Raleway

> Font binaries are intentionally **not** committed here. Add them locally if you need embedded fonts.
