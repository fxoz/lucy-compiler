from types import UnionType

DATA_TYPE: UnionType = int | float | str | bool | None
CODE = list


class IndentationError(Exception):
    pass


class CodeLine:
    def __init__(self, line_no: int, content: str):
        self.line_no = line_no  # 1-based
        self.content = content

    def __repr__(self):
        return f'CodeLine(line_no={self.line_no}, content="{self.content.replace('"', "‌'")}")'


class FunctionDefinition:
    def __init__(self, name: str, params: dict[str, DATA_TYPE], output_type: DATA_TYPE):
        self.name = name
        self.params = params
        self.output_type = output_type
        self.body: CODE = []

    def set_body(self, body: CODE):
        self.body = body

    def __repr__(self):
        return f"FunctionDefinition(name={self.name}, params={self.params}, output_type={self.output_type}"


class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall(name={self.name}, args={self.args})"
