"""li a0, 1
la a1, msg
li a2, 6
li a7, 64
ecall"""

"""
li a0, 0
li a7, 93
ecall
"""

"""
msg:
    .ascii "Hello\n"
"""


class Code:
    def __init__(self):
        self.data = []
        self.instructions = []

    def render(self):
        return f"""
.section .data
{"\n".join(self.data)}

.section .text
.globl _start

_start:
{"\n".join(self.instructions)}
"""
