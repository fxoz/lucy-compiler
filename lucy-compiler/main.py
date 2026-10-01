import lexer
import parser
import runtime
import generator


from language import FunctionDefinition

from rich import print


with open("test.lucy", "r", encoding="utf8") as f:
    code = f.read()


function_constructs: list[FunctionDefinition] = lexer.lex(code)


for fun in function_constructs:
    print(fun)
    for res in parser.parse_function(fun):
        print(res)

# assembly = generator.generate(parsed)

# runtime.run(assembly)
