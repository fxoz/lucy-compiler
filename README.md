# `lucy-compiler` [VERY EARLY VERSION. WORK IN PROGRESS]

My attempt at writing a language (Lucy), compiler and runtime. Translates to RISC-V-32.

This is a learning project, with zero AI generated base code.*

*This excludes the syntax highlighting extension `syntax-highlighter-vscode` for VSCode, written by GPT-6.1-Sol. This was done to make temporary debugging easier.

## Roadmap

- [ ] Language concept
  - [x] Functions
    - [x] Function definition
    - [x] Return values/statements
    - [x] Type hinting
    - [x] Function calls
  - [x] Operators
  - [ ] Control flow (if, while, for)
  - [ ] Data structures (lists, dicts, etc.)
  - [ ] ...
- [ ] Lexer
    - [x] Tokenization
    - [x] Indentation handling
    - [x] Source locations / line numbers
- [ ] Parser
  - [x] Statements
  - [ ] Expressions
  - [ ] Error reporting
- [ ] AST
  - [ ] Define node types
  - [ ] AST printer / debug output
- [ ] Semantic Analysis
  - [ ] Name resolution
  - [ ] Type checking
  - [ ] Scope checking
- [ ] Code Generation
- [ ] Runtime
  - [x] Basic functionality
  - [ ] ...
- [ ] Testing
- [ ] Documentation
