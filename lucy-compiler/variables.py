from language import (
    DATA_TYPE,
    VAR_SET_FUNCTION,
    VAR_SET_TYPE_FUNCTION,
    Argument,
    FunctionCall,
)


def init_variable(data_type: DATA_TYPE, name: str, value=None) -> list:
    return [
        FunctionCall(
            name=VAR_SET_TYPE_FUNCTION,
            args=[
                Argument(value=name, position=0),
                Argument(value=data_type, position=1),
            ],
        ),
        FunctionCall(
            name=VAR_SET_FUNCTION,
            args=[
                Argument(value=name, position=0),
                Argument(value=value, position=1),
            ],
        ),
    ]
