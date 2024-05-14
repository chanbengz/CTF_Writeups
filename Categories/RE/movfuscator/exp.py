from pwn import *

flag = list('cs315{*************}')
stri = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"
p = process(["gdb", "fuck"])
p.sendline(b"b *0x804c3a9")
sp = b"LEGEND: "  # 注意我用的是pwndbg，使用其他插件可能要更换分割符
# context.log_level='debug' 
for i in range(6, 19):
    for j in range(len(stri)):
        p.sendline(b"r")
        tr = [x for x in flag]
        tr[i] = stri[j]
        p.sendline(''.join(tr).encode())
        _ = p.recvuntil(sp)
        cnt = 0
        print(f'No.{i+1}, trying {stri[j]}, now flag is {"".join(flag)}')
        try:
            while True:
                cnt += 1
                p.sendline(b"c")
                r = p.recvuntil(sp, timeout=0.1)
                if b"Invalid." in r:
                    break
            if cnt == i+1:
                raise Exception
        except:
            print("hit!!!!")
            flag[i] = stri[j]
            print(''.join(flag))
            break

print(''.join(flag))
