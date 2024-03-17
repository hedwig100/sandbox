.intel_syntax noprefix

.section .data
number_format:
    .ascii "%d\n"

.global main, print_one_integer
.section .text

print_one_integer:
    mov rsi, rdi # Integer
    lea rdi, [rip + number_format]
    call printf
    ret

main:
    mov rsi, 5
    mov rdi, 6
    add rdi, rsi
    call print_one_integer
    ret
