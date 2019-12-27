push   rbp
 mov    rbp,rsp
 sub    rsp,0x2100
 mov    rax,QWORD PTR fs:0x28
 mov    QWORD PTR [rbp-0x8],rax
 xor    eax,eax
 lea    rax,[rbp-0x20f0]
 mov    edx,0x20d0
 mov    esi,0x0
 mov    rdi,rax
 call   6a0
 movabs rax,0x772f2f3a70747468
 mov    QWORD PTR [rbp-0x20f0],rax
 movabs rax,0x6f2e6d63612e7777
 mov    QWORD PTR [rbp-0x20e8],rax
 mov    QWORD PTR [rbp-0x20e0],0x2f6772
 lea    rdx,[rbp-0x20d8]
 mov    eax,0x0
 mov    ecx,0x7
 mov    rdi,rdx
 rep stos QWORD PTR es:[rdi],rax
 mov    DWORD PTR [rbp-0x20f4],0x0
 mov    eax,DWORD PTR [rbp-0x20f4]
 mov    DWORD PTR [rbp-0x20f8],eax
 jmp    a15 
 lea    rax,[rbp-0x12]
 lea    rsi,[rip+0x237]      
 mov    rdi,rax
 call   6b0
 test   eax,eax
 je     a38 
 lea    rax,[rbp-0x12]
 lea    rsi,[rip+0x221]      
 mov    rdi,rax
 call   6b0 
 test   eax,eax
 jne    951 
 mov    eax,DWORD PTR [rbp-0x20f4]
 mov    DWORD PTR [rbp-0x20f8],eax
 add    DWORD PTR [rbp-0x20f8],0x1
 mov    eax,DWORD PTR [rbp-0x20f8]
 mov    DWORD PTR [rbp-0x20f4],eax
 lea    rcx,[rbp-0x20f0]
 mov    eax,DWORD PTR [rbp-0x20f8]
 movsxd rdx,eax
 mov    rax,rdx
 shl    rax,0x2
 add    rax,rdx
 shl    rax,0x4
 add    rax,rcx
 mov    rsi,rax
 lea    rdi,[rip+0x1d1]
 mov    eax,0x0
 call   6c0 
 lea    rcx,[rbp-0x20f0]
 mov    eax,DWORD PTR [rbp-0x20f8]
 movsxd rdx,eax
 mov    rax,rdx
 shl    rax,0x2
 add    rax,rdx
 shl    rax,0x4
 add    rax,rcx
 mov    rdi,rax
 call   680
 lea    rax,[rbp-0x12]
 lea    rsi,[rip+0x196] 
 mov    rdi,rax
 call   6b0
 test   eax,eax
 jne    9af
 cmp    DWORD PTR [rbp-0x20f4],0x0
 jle    9a3
 sub    DWORD PTR [rbp-0x20f4],0x1
 lea    rcx,[rbp-0x20f0]
 mov    eax,DWORD PTR [rbp-0x20f4]
 movsxd rdx,eax
 mov    rax,rdx
 shl    rax,0x2
 add    rax,rdx
 shl    rax,0x4
 add    rax,rcx
 mov    rdi,rax
 call   680
 jmp    9af <main+0x19f>
 lea    rdi,[rip+0x14d]      
 call   680
 lea    rax,[rbp-0x12]
 lea    rsi,[rip+0x145] 
 mov    rdi,rax
 call   6b0
 test   eax,eax
 jne    a15
 mov    eax,DWORD PTR [rbp-0x20f4]
 add    eax,0x1
 cmp    eax,DWORD PTR [rbp-0x20f8]
 jg     a09
 add    DWORD PTR [rbp-0x20f4],0x1
 lea    rcx,[rbp-0x20f0]
 mov    eax,DWORD PTR [rbp-0x20f4]
 movsxd rdx,eax
 mov    rax,rdx
 shl    rax,0x2
 add    rax,rdx
 shl    rax,0x4
 add    rax,rcx
 mov    rdi,rax
 call   680
 jmp    a15 
 lea    rdi,[rip+0xe7]  
 call   680 <puts@plt>
 lea    rax,[rbp-0x12]
 mov    rsi,rax
 lea    rdi,[rip+0xcc]     
 mov    eax,0x0
 call   6c0 
 cmp    eax,0xffffffff
 jne    8a2 
 jmp    a39 
 nop
 mov    eax,0x0
 mov    rsi,QWORD PTR [rbp-0x8]
 xor    rsi,QWORD PTR fs:0x28
 je     a52
 call   690 
 leave  
 ret    
 nop    WORD PTR cs:[rax+rax*1+0x0]
 xchg   ax,ax
