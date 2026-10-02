from language import (
    ALLOCATE_LAST_RESULT_FUNCTION,
    Argument,
    CodeLine,
    FunctionCall,
    FunctionDefinition,
    VAR_SET_FUNCTION,
    VAR_SET_TYPE_FUNCTION,
    to_data_type,
    RETURN_STATEMENT_FUNCTION,
    ConditionalBlock,
)

import variables

from rich import print

# TODO - Later write fake lines for function calls inside of arguments:
# TODO - i. e. print(add(1, 2)) => _t1 = add(1, 2); print(_t1)

COMMA_ESCAPE_CHAR = "[escaped\u2063comma]"

id_counter = 0


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
    global id_counter

    text = line.content.strip()

    if text.startswith("if "):  # TODO - implement
        return []

    if text.startswith("=> "):
        return [
            FunctionCall(
                name=RETURN_STATEMENT_FUNCTION,
                args=[Argument(value=text[3:].strip(), position=0)],
                code_line=line,
            )
        ]

    if (
        "(" not in text or ")" not in text
    ):  # TODO - incorrect, since "()" can be inside a string
        if " = " in text:  # variable assignment
            var_type = text.split()[0]
            var_type = to_data_type(var_type)
            var_name = text.split()[1]
            var_value = text.split("=", 1)[1].strip()
            return variables.init_variable(var_type, var_name, var_value)

        raise ValueError(f"No function call found in line {line.line_no}")

    function_name = text.split("(")[0].strip()
    args_text = text.split("(")[1].split(")")[0].strip()

    out = []
    args = []

    for i, arg in enumerate(escape_commas(args_text).split(",")):  # process arguments
        arg = arg.strip()
        arg = arg.replace(COMMA_ESCAPE_CHAR, ",")
        if (arg.startswith('"') and arg.endswith('"')) or (
            arg.startswith("'") and arg.endswith("'")
        ):
            temp_var_name = f"___litstr{id_counter}"
            out.extend(
                variables.init_variable(
                    data_type=str, name=temp_var_name, value=arg[1:-1]
                )
            )
            args.append(Argument(value=temp_var_name, position=i))
            id_counter += 1
        elif arg.isdigit():
            temp_var_name = f"___litint{id_counter}"
            out.extend(variables.init_variable(int, temp_var_name, int(arg)))
            args.append(Argument(value=temp_var_name, position=i))
            id_counter += 1
        else:
            raise ValueError(f"Unsupported argument type: {arg}")

    out.append(FunctionCall(name=function_name, args=args, code_line=line))

    if does_allocate_function_result(text):
        out.append(
            FunctionCall(
                name=ALLOCATE_LAST_RESULT_FUNCTION,
                args=[text.split("=")[0].strip()],
                code_line=line,
            )
        )

    return out


def parse_function(function_def: FunctionDefinition) -> list[FunctionCall]:
    function_calls = []
    for line in function_def.body:
        if isinstance(line, CodeLine):
            function_calls.extend(parse_line(line))
        else:
            raise TypeError(f"Unsupported line type: {line}")
    return function_calls


if __name__ == "__main__":
    print(parse_line(CodeLine('x = add(1, "2", 3)')))
