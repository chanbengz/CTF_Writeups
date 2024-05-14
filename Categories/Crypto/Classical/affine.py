from sage.all import *

modulus = 256
h = 'dd4388ee428bdddd5865cc66aa5887ffcca966109c66edcca920667a88312064'
cipher = [i for i in bytes.fromhex(h)]

def dec(key1, key2):
    s = ''
    if gcd(key1, modulus) != 1:
        return ''
    for i in cipher:
        a = pow(key1, -1, modulus)
        b = key2
        s += chr((key1*(i - key2)) % modulus)
    return s

for i in range(256):
    for j in range(256):
        res = dec(i, j)
        if 'flag' in res:
            print(res)