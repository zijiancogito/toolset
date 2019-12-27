push rbp ; mov rbp , rsp ; sub rsp , 0x30
mov QWORD PTR [ rbp - 0x28 ] , 0x3
mov QWORD PTR [ rbp - 0x20 ] , 0x0
mov QWORD PTR [ rbp - 0x18 ] , 0x2
mov rax , QWORD PTR [ rbp - 0x18 ] ; sub rax , 0x1 ; imul rax , QWORD PTR [ rbp - 0x18 ] ; mov rdx , rax ; shr rdx , 0x3f ; add rax , rdx ; sar rax , 1 ; mov QWORD PTR [ rbp - 0x10 ] , rax
mov rax , QWORD PTR [ rbp - 0x28 ] ; add rax , 0x1 ; imul rax , QWORD PTR [ rbp - 0x28 ] ; mov rdx , rax ; mov rax , QWORD PTR [ rbp - 0x18 ] ; add rax , 0x1 ; imul rax , QWORD PTR [ rbp - 0x18 ] ; sub rdx , rax ; mov rax , rdx ; mov rdx , rax ; shr rdx , 0x3f ; add rax , rdx ; sar rax , 1 ; mov QWORD PTR [ rbp - 0x8 ] , rax
mov rax , QWORD PTR [ rbp - 0x28 ] ; mov DWORD PTR [ rbp - 0x30 ] , eax
mov rax , QWORD PTR [ rbp - 0x18 ] ; mov DWORD PTR [ rbp - 0x2c ] , eax
mov rax , QWORD PTR [ rbp - 0x8 ] ; cmp rax , QWORD PTR [ rbp - 0x10 ] ; jne 758 ; mov edx , DWORD PTR [ rbp - 0x30 ] ; mov eax , DWORD PTR [ rbp - 0x2c ] ; mov esi , eax ; lea rdi , [ rip+0xbb ] ; mov eax , 0x0 ; call 560 ; add QWORD PTR [ rbp - 0x20 ] , 0x1
add QWORD PTR [ rbp - 0x28 ] , 0x1
mov rax , QWORD PTR [ rbp - 0x8 ] ; cmp rax , QWORD PTR [ rbp - 0x10 ] ; jle 76c
add QWORD PTR [ rbp - 0x18 ] , 0x1
cmp QWORD PTR [ rbp - 0x20 ] , 0x9 ; jle 6d0 ; mov eax , 0x0 ; leave ; ret
