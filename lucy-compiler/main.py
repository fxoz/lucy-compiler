import lexer
import parser
import runtime
import generator

from rich import print

with open("test.lucy", "r", encoding="utf8") as f:
    code = f.read()

lexed = lexer.lex(code)
print(lexed)

# parsed = parser.parse(lexed)
# print(parsed)
# assembly = generator.generate(parsed)
# runtime.run(assembly)
