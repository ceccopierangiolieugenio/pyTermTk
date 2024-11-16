From: https://stackoverflow.com/questions/22656131/find-the-font-used-to-render-a-character-or-containing-the-glyph

To check if one of those symbols are supported:
https://en.wikipedia.org/wiki/Symbols_for_Legacy_Computing

You can use this command:
```
 $ fc-list ':charset=1FB41'

/usr/share/fonts/opentype/3270/3270SemiCondensed-Regular.otf: IBM 3270 Semi\-Condensed:style=Condensed
/usr/share/fonts/opentype/3270/3270-Regular.otf: IBM 3270:style=Regular
/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf: Noto Sans Symbols2:style=Regular
/usr/share/fonts/truetype/unifont/unifont_upper.ttf: Unifont Upper:style=Regular
/usr/share/fonts/opentype/3270/3270Condensed-Regular.otf: IBM 3270 Condensed:style=Condensed

```

Check the font rendering in the browser:
https://typezebra.com
OK: 
* FreeSans Regular
* FreeSerif Regular
* FreeMono Regular

