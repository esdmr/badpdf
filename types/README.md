# PDF.js scripting API types

These files are from PDF.js via the TypeScript compiler.

Source: [PDF.js v4.10.38 `/scripting_api/`](https://github.com/mozilla/pdf.js/tree/v4.10.38/src/scripting_api)

```sh
cd scripting_api
tsc --allowJs *.js --declaration --outDir types --emitDeclarationOnly --target es2022 --module esnext --moduleResolution bundler
```
