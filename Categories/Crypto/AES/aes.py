from Crypto.Cipher import AES
from Crypto.Util.number import *

cipher = b'>]\xc1\xe5\x82/\x02\x7ft\xf1B\x8d\n\xc1\x95i'
key_iv = 3657491768215750635844958060963805125333761387746954618540958489914964573229 ^ 1
key_part = key_iv // 2**(8*16)

key = long_to_bytes(key_part) * 2
iv = long_to_bytes((key_iv % 2**(8*16)) ^ key_part)
aes = AES.new(key, AES.MODE_CBC, iv)
message = aes.decrypt(cipher)

print(message)
