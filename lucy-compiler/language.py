from types import UnionType

DATA_TYPE: UnionType = int | float | str | bool | None
CODE = list

ALLOCATION_PSEUDO_FUNCTION = "___allocate_last_result"
MAIN_FUNCTION = "___main___"


class IndentationError(Exception):
    pass


class CodeLine:
    def __init__(self, content: str, line_no: int = -1):
        self.line_no = line_no  # 1-based
        self.content = content

    def __repr__(self):
        return f'CodeLine(line_no={self.line_no}, content="{self.content.replace('"', "‌'")}")'


class Parameter:
    def __init__(
        self, name: str, data_type: DATA_TYPE, position: int, default_value=None
    ):
        self.name = name
        self.data_type = data_type
        self.position = position
        assert default_value is None or isinstance(default_value, data_type), (
            f"Default value {default_value} does not match data type {data_type}"
        )
        self.default_value = default_value

    def __repr__(self):
        return f"Parameter(name={self.name}, data_type={self.data_type.__name__}, position={self.position}, default_value={self.default_value})"


class Argument:
    def __init__(self, value: DATA_TYPE, position: int):
        self.value = value
        self.position = position  # 0-based

    def __repr__(self):
        return f"Argument(value={'"' if isinstance(self.value, str) else ''}{self.value}{'"' if isinstance(self.value, str) else ''}, position={self.position})"


class FunctionDefinition:
    def __init__(self, name: str, params: list[Parameter], output_type: DATA_TYPE):
        self.name = name
        self.params = params
        self.output_type = output_type
        self.body: CODE = []

    def set_body(self, body: CODE):
        self.body = body

    def __repr__(self):
        return f"FunctionDefinition(name={self.name}, params={self.params}, output_type={self.output_type}, body={'...' if len(self.body) > 0 else 'None'})"


class FunctionCall:
    def __init__(self, name: str, args: list[Argument]):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall(name={self.name}, args={self.args})"


def to_data_type(type_str: str) -> DATA_TYPE:
    if type_str == "int":
        return int
    elif type_str == "float":
        return float
    elif type_str == "str":
        return str
    elif type_str == "bool":
        return bool
    elif type_str == "any":
        return None
    else:
        raise ValueError(f"Unknown data type: {type_str}")
