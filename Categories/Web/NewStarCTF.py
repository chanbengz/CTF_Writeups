import requests
from tqdm import tqdm
url = 'http://node4.buuoj.cn:25515/?ctf=1'\

data = {'secret' : 'n3wst4rCTF2023g00000d'}
header = {'User-Agent' : 'NewStarCTF2023', 'Referer' : 'newstarctf.com', 'X-Real-IP' : '127.0.0.1'}
cookie = requests.cookies.RequestsCookieJar()
cookie.set('power', 'ctfer')
res = requests.post(url, data=data, cookies=cookie, headers=header)

print(res.text)
