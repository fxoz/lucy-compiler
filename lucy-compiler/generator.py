from language import (
    FunctionDefinition,
    FunctionCall,
    ConditionalBlock,
    Argument,
    Parameter,
    DATA_TYPE,
    MAIN_FUNCTION,
    VAR_SET_FUNCTION,
    VAR_SET_TYPE_FUNCTION,
)

from rich import print


class Code:
    def __init__(self):
        self.instructions = []
        self.id_counter = 0
        self.string_literals = {}  # name -> value
        self.exit_code = 0
        self.data = []

    def render_string_literals(self):
        for name, value in self.string_literals.items():
            if isinstance(value, str):
                self.data.append(
                    f'{name}:\n\t.ascii "{value}"\n{name}__len = . - {name}\n'
                )
            elif isinstance(value, int):
                self.data.append(f"{name}: .word {value}")
            else:
                raise TypeError(f"Unsupported string literal type: {type(value)}")

    def render(self):
        self.render_string_literals()
        return f"""
.section .data
{"\n".join(self.data)}  

.section .text
.globl _start

_start:
{"\n".join(self.instructions)}

li a0, {self.exit_code}
li a7, 93
ecall
""".replace("\t", "    ")


def generate_function_call(call: FunctionCall, code: Code) -> None:
    if call.name == VAR_SET_TYPE_FUNCTION:
        code.string_literals[call.args[0].value] = (
            "" if call.args[1].value == str else 0
        )  # TODO - handle other types

    elif call.name == VAR_SET_FUNCTION:
        code.string_literals[call.args[0].value] = call.args[1].value

    elif call.name == "print":
        code.instructions.append(f"""\tli a0, 1
    la a1, {call.args[0].value}
    li a2, {call.args[0].value}__len
    li a7, 64
    ecall
""")


def generate(functions: list[FunctionDefinition]) -> str:
    code = Code()

    for fun in functions:
        if fun.name != MAIN_FUNCTION:  # TODO handle non-main
            continue

        statements = fun.parsed

        for statement in statements:
            print(statement.show())
            if not isinstance(statement, FunctionCall):  # TODO
                continue

            generate_function_call(statement, code)

    return code.render()
