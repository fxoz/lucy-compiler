from language import (
    CODE_LINES,
    CodeLine,
    FunctionDefinition,
    IndentationError,
    Parameter,
    to_data_type,
    MAIN_FUNCTION,
)


def new_function_definition(line: str) -> FunctionDefinition:
    params: list[Parameter] = []
    for i, param in enumerate(line.split("[")[1].split("]")[0].split(", ")):
        if not param:
            continue
        param_name, param_type = param.split()
        params.append(
            Parameter(name=param_name, data_type=to_data_type(param_type), position=i)
        )

    return FunctionDefinition(
        name=line.split()[1].split("[")[0],
        params=params,
        output_type=line.split("-> ")[1].strip(),
    )


def ensure_corrent_indent(indentation_level: int, current_indentation: int, i: int):
    if current_indentation - indentation_level > 1:
        raise IndentationError(
            f"Unexpected indentation at line {i + 1}. Jump from {indentation_level} to {current_indentation} >= 1."
        )


def lex(inp: str) -> list[FunctionDefinition]:
    main_body: CODE_LINES = []
    indentation_level = 0
    current_function_definition = None
    current_function_body: CODE_LINES = []
    functions: list = []

    for i, line in enumerate(inp.splitlines()):
        line = line.replace("\t", "    ")
        line = line.split("#")[0]
        line = line.rstrip()

        if not line.strip():
            continue

        # --- INDENT ---

        current_indentation = (len(line) - len(line.lstrip())) // 4
        ensure_corrent_indent(indentation_level, current_indentation, i)

        # --- END FUNCTION ---
        if current_function_definition and current_indentation == 0:
            indentation_level = 0
            current_function_definition.set_body(current_function_body)
            functions.append(current_function_definition)
            current_function_definition = None
            current_function_body = []

        # --- NEW FUNCTION ---

        if line.startswith("fun "):
            current_function_definition = new_function_definition(line)
            continue

        # --- ADD TO CONTEXT ---

        line = CodeLine(
            content=line.strip(),
            line_no=i + 1,
        )

        if current_function_definition:
            current_function_body.append(line)
        else:
            main_body.append(line)

        indentation_level = current_indentation

    main_function = FunctionDefinition(name=MAIN_FUNCTION, params={}, output_type=None)
    main_function.set_body(main_body)
    functions.append(main_function)

    return functions


if __name__ == "__main__":
    pass
