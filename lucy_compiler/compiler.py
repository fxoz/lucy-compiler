from rich import print  # noqa: F401

from . import generator, lexer, parser, runtime
from .language import FunctionDefinition


def compile(source: str = None, file_path: str = None, *args, **kwargs):
    if source is None:
        with open(file_path, "r", encoding="utf8") as f:
            lucy_code = f.read()
    else:
        lucy_code = source

    function_constructs: list[FunctionDefinition] = lexer.lex(lucy_code)

    for fun in function_constructs:
        fun.set_parsed(parser.parse_function(fun))
        # print(fun)

    assembly = generator.generate(function_constructs)

    # with open("../debug/out.s", "w", encoding="utf8") as f:
    #     f.write(assembly)

    return runtime.run(assembly, *args, **kwargs)


if __name__ == "__main__":
    compile(file_path="test.lucy")
