#define SET_CONTEXT set_context
#define SWITCH_CONTEXT switch_context

.global SET_CONTEXT
.global SWITCH_CONTEXT

.text
.align 4

SET_CONTEXT:
    pop %rbp
    
    // Save callee saved registers
    movq %rbx, (%rdi)
    movq %rdx, 8(%rdi)
    movq %r12, 16(%rdi)
    movq %r13, 24(%rdi)
    movq %r14, 32(%rdi)
    movq %r15, 40(%rdi)

    // Save the stack pointer
    // IDK if this is correct??
    lea 8(%rsp), %rdx
    movq %rdx, 48(%rdi)

    // Save the link pointer (return address)
    // IDK if this is correct??
    push %rbp
    movq (%rsp), %rdx
    movq %rdx, 56(%rdi)

    // Return 0
    xor %eax, %eax
    ret 


.text
.align 4

SWITCH_CONTEXT:
    pop %rsi 

    // Restore callee saved registers
    movq (%rdi), %rbx
    movq 8(%rdi), %rbp
    movq 16(%rdi), %r12
    movq 24(%rdi), %r13
    movq 32(%rdi), %r14
    movq 40(%rdi), %r15

    // Restore the stack pointer
    movq 48(%rdi), %rdx
    movq %rdx, %rsp
    addq $0x8, %rsp

    // Return 1
    xor %eax, %eax
    inc %eax

    // Return to the starting address
    // IDK if this is correct??
    push %rbp
    push %rsi
    movq 56(%rdi), %rdx
    jmpq *%rdx
