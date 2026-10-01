from language import (
    Argument,
    CodeLine,
    FunctionCall,
    FunctionDefinition,
    ALLOCATION_PSEUDO_FUNCTION,
)
from rich import print

# TODO - Later write fake lines for function calls inside of arguments:
# TODO - i. e. print(add(1, 2)) => _t1 = add(1, 2); print(_t1)

COMMA_ESCAPE_CHAR = "[escaped\u2063comma]"


def escape_commas(args_text: str) -> str:
    # escape commas inside of strings
    in_string = False
    escaped_args_text = ""
    for char in args_text:
        if char in ('"', "'"):
            in_string = not in_string
        escaped_args_text += (
            char if not (in_string and char == ",") else COMMA_ESCAPE_CHAR
        )
    return escaped_args_text


def does_allocate_function_result(line: str) -> bool:
    return "=" in line and line.index("=") < min(
        (line.find(q) for q in ("'", '"') if q in line), default=len(line)
    )


def parse_line(line: CodeLine) -> list[FunctionCall]:
    text = line.content.strip()

    if text.startswith("if "):
        return []  # TODO - Handle if statements

    if text.startswith("=> "):
        return []  # TODO - Handle return statements

    if "(" not in text or ")" not in text:
        raise ValueError(f"No function call found in line {line.line_no}")

    function_name = text.split("(")[0].strip()
    args_text = text.split("(")[1].split(")")[0].strip()

    args = []

    for i, arg in enumerate(escape_commas(args_text).split(",")):
        arg = arg.strip()
        arg = arg.replace(COMMA_ESCAPE_CHAR, ",")
        if (arg.startswith('"') and arg.endswith('"')) or (
            arg.startswith("'") and arg.endswith("'")
        ):
            args.append(Argument(value=arg[1:-1], position=i))
        elif arg.isdigit():
            args.append(Argument(value=int(arg), position=i))
        else:
            raise ValueError(f"Unsupported argument type: {arg}")

    out = []
    out.append(FunctionCall(name=function_name, args=args))

    if does_allocate_function_result(text):
        out.append(
            FunctionCall(
                name=ALLOCATION_PSEUDO_FUNCTION, args=[text.split("=")[0].strip()]
            )
        )

    return out


def parse_function(function_def: FunctionDefinition) -> list[FunctionCall]:
    function_calls = []
    for line in function_def.body:
        if isinstance(line, CodeLine):
            function_calls.append(parse_line(line))
        else:
            raise TypeError(f"Unsupported line type: {line}")
    return function_calls


if __name__ == "__main__":
    print(parse_line(CodeLine('x = add(1, "2", 3)')))
