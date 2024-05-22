# urllib (Web/Easy)
## 题目描述

是SSRF吗？如是。

是SSRF吗？如是。

是SSRF吗？如是。

## 附件

[server.py](../app/server.py)

## 解题思路

本题改编自`CVE-2023-24329`

据[PoC](CVE-2023-24329-PoC.py)描述，当url开头为空格时，urllib中urlparse函数会无法解析，导致scheme和hostname为`ValueError`，因此黑名单失效，得以绕过。

### payload

```
/?url=%20file://127.0.0.1/flag
```

### 其他解

俺不会