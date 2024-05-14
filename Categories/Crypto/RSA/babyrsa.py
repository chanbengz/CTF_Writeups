import imp
from operator import mod
from Crypto.Util.number import *


n = 228430203128652625114739053365339856393
e = 65537
c = 126721104148692049427127809839057445790
p = 12546190522253739887
q = 18207136478875858439
m = (p-1) * (q-1)

def exgcd(a, b, arr):
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    r = exgcd(b, a%b, arr)
    t = arr[1]
    arr[1] = arr[0] - (a // b) * arr[1]
    arr[0] = t
    return r

def modrev(a,n):
    arr = [0,1,]
    gcd = exgcd(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1
d = modrev(e, m)
print(long_to_bytes(pow(c, d, n)))