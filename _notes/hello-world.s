.section .data
msg:
    .ascii "Hello, world!\n"
len = . - msg

.section .text
.globl _start

_start:
    # write(1, msg, len)
    li a0, 1
    la a1, msg
    li a2, len
    li a7, 64
    ecall

    # exit(0)
    li a0, 0
    li a7, 93
    ecall