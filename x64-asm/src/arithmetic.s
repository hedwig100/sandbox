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
    call print_one_integer # expect 11

    mov rsi, 10
    mov rdi, 9
    sub rdi, rsi
    call print_one_integer # expect -1

    mov rdi, -2
    mov rsi, 4
    imul rdi, rsi
    call print_one_integer # expect -8

    mov rsi, 5
    mov rdi, 4
    xor rdi, rsi
    call print_one_integer # expect 1

    mov rdi, 1
    sal rdi, 4
    call print_one_integer # expect 1<<4 = 16

    ret
