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
    mov r8, 5
    mov r9, 4
    lea rdi, [r8]
    call print_one_integer # expect 5

    mov r8, 5
    mov r9, 4
    lea rdi, [r8 + r9]
    call print_one_integer # expect 9

    mov r8, 5
    mov r9, 4
    lea rdi, [r8 + r9 - 2]
    call print_one_integer # expect 7

    mov r8, 5
    mov r9, 4
    lea rdi, [r8 + 2*r9 + 3]
    call print_one_integer # expect 5 + 2*4 + 3 = 16

    ret
