from sage.all import *
from Crypto.Util.number import *
from pwn import *

def read_output():
    fi = open('output.txt', 'r').readlines()
    outputs = []
    for line in fi:
        if len(line) <= 1: continue
        A, b = line[1:-2].split('] [')
        A = [int(num[1:-1], 16) for num in A.split(', ')]
        b = [int(num[1:-1], 16) for num in b.split(', ')]
        outputs.append((matrix(n, n, A), vector(b)))

    return outputs

q = 2**142 + 217
n = 69
nseeds = 142

warn("=== Reading output.txt ===")
outputs = read_output()
info("Done!")

warn("=== Finding secret vector s ===")

info("Building basis...")
A, b = outputs[0]
I = identity_matrix(n)
O = 0*I
Q = q*I
mt = (I.augment(A.T)).stack(O.augment(Q)).stack(vector([0]*n + [-x for x in b]))
info("Done!")

info("Running LLL...")
s = mt.LLL()[1][:69]
info("Done!")
warn("secret vector s = " + str(s))

flag = ""
for A, b in outputs:
    e = b - A.change_ring(Zmod(q))*s
    if sum(e) < 7*n:
        flag += "0"
    else:
        flag += "1"

warn("Flag: " + long_to_bytes(int(flag, 2)).decode())
