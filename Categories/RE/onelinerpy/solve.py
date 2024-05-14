#!/usr/bin/env python3

from z3 import *

conds = open('conds.txt').read().replace('lambda*a:(', '').replace('),', '').splitlines()

a = [Int('a%d'%i) for i in range(16)]
s = Solver()
for var in a:
    s.add(var>0)
    s.add(var<128)

num = 1
while len(conds) > 0:
    cond = conds.pop()
    conds.reverse()
    eqs = cond.split(',')
    bits = '{:04b}'.format(num)
    for i, b in enumerate(bits):
        eq = eqs[i]
        if b == '0':
            eq = eq.replace('==', '!=')
        exec('s.add(%s)'%eq)

    num += 1
    num %= 16

print("Solving...")
print(s)
print(s.check())
print(s.model())

print([s.model()[i] for i in a])

