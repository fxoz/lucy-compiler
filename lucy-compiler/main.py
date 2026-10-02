import generator  # noqa: F401
import lexer
import parser
import runtime  # noqa: F401
from language import FunctionDefinition
from rich import print

with open("test.lucy", "r", encoding="utf8") as f:
    lucy_code = f.read()

function_constructs: list[FunctionDefinition] = lexer.lex(lucy_code)

for fun in function_constructs:
    fun.set_parsed(parser.parse_function(fun))
    # print(fun)

assembly = generator.generate(function_constructs)
open("../debug/out.s", "w", encoding="utf8").write(assembly)

runtime.run(assembly)
