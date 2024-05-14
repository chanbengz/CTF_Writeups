h = 'e9e3eee8f4f7bffdd0bebad0fcf6e2e2bcfbfdf6d0eee1ebd0eabbf5f6aeaeaeaeaeaef2'
cipher = [i for i in bytes.fromhex(h)]

for i in range(256):
    text = ''
    for j in cipher:
        text += chr(i ^ j)
    if 'flag' in text:
        print(text)