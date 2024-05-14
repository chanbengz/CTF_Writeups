from pwn import *

win_month = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
]

win_day = {
    'January' : 20,
    'February' : 21,
    'March' : 22,
    'April' : 23,
    'May' : 24,
    'June' : 25,
    'July' : 26,
    'August' : 27,
    'September' : 28,
    'October' : 29,
    'November' : 30,
    'December' : 31,
}

p = remote('detroit.sustech.edu.cn', 49393) # URL here
p.recvuntil(b'?')
p.recvline()
p.recvline()
p.recvline()
for i in range(1, 101):
    banner = f'''----------
ROUND {i}
----------'''
    p.recvuntil(banner.encode())
    p.recvline()
    print(f'Round {i} ')
    while True:
        computer = p.recvline().decode().strip('\n')
        p.recvuntil(b'> ')
        print('Computer: ' + computer, end=' ')
        month, daystr = computer.split(" ")
        day = int(daystr, 10)
        ans = ''

        if day > win_day[month]:
            ans = win_month[day - 20] + ' ' + str(day)
        elif day < win_day[month]:
            ans = month + ' ' + str(win_day[month])
        else:
            ans = month + ' ' + str(day + 1)

        print("Me: " + ans)
        p.sendline(ans.encode())
        if ans == 'December 31':
            break
    # END of each turn
    print()
    p.recvuntil(b'You won!\n')

# Success !
p.interactive()