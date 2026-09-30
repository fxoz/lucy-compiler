from language import CODE, DATA_TYPE, CodeLine, FunctionDefinition, IndentationError


def new_function_definition(line: str) -> FunctionDefinition:
    params: dict[str, DATA_TYPE] = {
        param.split()[0]: param.split()[1]
        for param in line.split("[")[1].split("]")[0].split(", ")
    }

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


def lex(inp: str):
    main_body: CODE = []
    indentation_level = 0
    current_function_definition = None
    current_function_body: CODE = []
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

        line = CodeLine(line_no=i + 1, content=line.strip())

        if current_function_definition:
            current_function_body.append(line)
        else:
            main_body.append(line)

        indentation_level = current_indentation

    main_function = FunctionDefinition(name="__main__", params={}, output_type=None)
    main_function.set_body(main_body)
    functions.append(main_function)

    return functions


if __name__ == "__main__":
    pass
