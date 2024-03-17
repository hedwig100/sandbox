.intel_syntax noprefix

# Data
.section .data
msg1:
    .ascii "Hello World!\n"
    msg1len = . - msg1

# Functions
.global print, main
.section .text

# print function that takes (ptr, len) as argument (rdi, rsi)
print:
    mov rdx, rsi # move the length to rdx
    mov rsi, rdi # move the pointer (rdi) to rsi
    mov rax, 0x01 # write syscall on x64 linux
    mov rdi, 0x01 # STDOUT file descriptor
    syscall
    ret

main:
    lea rdi, [rip + msg1]
    mov rsi, OFFSET msg1len
    call print
    ret
