# Lucy Syntax

A small VS Code extension that automatically highlights `.lucy` files. No runtime code or language server is needed.

Supports `#` comments, `fun name[parameter type] -> type` declarations, `=>` returns, types (`int`, `float`, `str`, `bool`, `any`), function calls, numbers, strings, escapes, and `{expression}` string interpolation. Also provides comment toggling, bracket matching, and automatic closing pairs.

Because Lucy is evolving, single-quoted strings, interpolation, additional control-flow keywords, `void`, boolean/null spellings, and hexadecimal/binary numbers are provisional highlighting conventions, not a claim that the compiler accepts them. Edit `syntaxes/lucy.tmLanguage.json` to change these rules.

Font ligatures are enabled by default for Lucy files, so a font that supports ligatures can render `->` and `=>` as connected arrows. Your selected editor font must support these ligatures; the extension does not install or change fonts. Explicit language-specific user or workspace settings can override this default.

## Local installation

Run `code --install-extension lucy-syntax-0.1.1.vsix --force`, or use **Extensions: Install from VSIX…** in VS Code. Reload the VS Code window if an already-open Lucy file does not pick up the language.

To rebuild the package, run `npx --yes @vscode/vsce package --allow-missing-repository`. To preview changes without installing, open this folder in VS Code and press F5 (choose VS Code Extension Development if prompted), then open a `.lucy` file in the development window.
