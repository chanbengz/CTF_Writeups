from pwn import *

#            flag{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx3861}
flag = list('flag{************************************}')
stri = "0123456789abcdef-ghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"

sp = b"LEGEND: "
context.log_level = 'critical'



for i in range(5, 43):
    for j in range(len(stri)):
        p = process(["gdb", "fuck"])
        p.sendline(b"b *0x8052A92")
        p.sendline(b"r")
        tr = [x for x in flag]
        tr[i] = stri[j]
        p.sendline(''.join(tr).encode())
        _ = p.recvuntil(sp)
        print(f'No.{i + 1}, trying {stri[j]}, now flag is {"".join(flag)}')
        for c in range(i-1):
            p.sendline(b'c')
            _ = p.recvuntil(sp)
        p.sendline(b'c')
        r = p.recvall(0.3)
        if sp in r:
            print("hit!!!!")
            flag[i] = stri[j]
            print(''.join(flag))
            p.close()
            break
        else:
            p.close()


print(''.join(flag))
