# Reverse Engineering Instagram

This repository documents how Instagram encrypts passwords and generates certain headers and payload parameters for authentication and requests.  
The examples are for **research and educational purposes only**.

---

## 1. Password Encryption (`pwd_encoder.js`)

Instagram uses dynamic encryption for passwords. The **Key ID** and **Public Key** are not static—they are periodically updated and must be extracted from Instagram's HTML.

### Required Parameters
- **Instagram Encryption Key ID**
- **Instagram Encryption Public Key**
- **Password** to encrypt
- **Timestamp** (10-digit Unix time)
- **Instagram Encryption Version** (usually `10`)

### Using Node.js
```sh
node pwd_encoder.js \
  158 \
  '425cffed5f79336b65c68c19da3e72b1c08545253057db6dce39885f7dca1c6e' \
  'your-password-here' \
  '1742679434' \
  10
Using Python
python
Copy code
import time
import subprocess

result = subprocess.run([
    'node',
    'pwd_encoder.js',
    '158',
    '425cffed5f79336b65c68c19da3e72b1c08545253057db6dce39885f7dca1c6e',
    'PASSWORD HERE',
    str(round(time.time())),
    '10'
], capture_output=True, text=True)

print(result.stdout.strip())
Sample Output
bash
Copy code
#PWD_INSTAGRAM_BROWSER:10:1742679434:AZ1QAC1dEJegrbNAYcDn7aPPzXcnIfO5x2mhi9Ad0Ax45eYKn45W88XlhGm95iwIt10Y5bvdd+ceEjSj4etqaILHLpraxojNY4nIn13Sdggc7oYjv5y5n/9KIzrNgThBBZ9BxTEN7r1ZuWhXrOd6p4yvKbT8dQ==
Note: The key ID and public key are dynamic and must be scraped from Instagram's HTML source.

2. Instagram Headers and Payload Values (reversed.py)
Instagram uses custom headers and payload values to identify and verify sessions.

2.1 X-Mid Header Generation
python
Copy code
import math
import random
import functools

def random_uint32():
    return math.floor(random.random() * 4294967296)

def to_string(n):
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''
    while n:
        n, r = divmod(n, 36)
        result = chars[r] + result
    return result or '0'

def machine_id():
    return functools.reduce(
        lambda a, _: a + to_string(random_uint32()),
        [0] * 8,
        ''
    )

print(machine_id())
# Example output:
# 1olgdc41oa6xbd5hetz5agulv79tei931on7kdg1i9jnzz1pgez3y
2.2 X-Web-Session-ID
python
Copy code
import math
import random

def to_string(n):
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''
    while n:
        n, r = divmod(n, 36)
        result = chars[r] + result
    return result or '0'

def web_session_id(extra=False, c=None):
    def _p(j=6):
        a = math.floor(random.random() * 2176782336)
        a = to_string(a)
        return '0' * (j - len(a)) + a

    if extra:
        a = _p()
        b = _p()
    else:
        a = ''  # webstorage (empty if no browser data)
        b = ''  # webstorage (empty if no browser data)
    if c is None:
        c = _p()
    return a + ':' + b + ':' + c

sid = web_session_id()  # browser without stored session
print(sid)
# Example output:
# ::1p7dm3

print(web_session_id(extra=True, c=sid.split(':')[2]))
# Example output:
# lejnny:v14jyj:1p7dm3
2.3 Jazoest Payload Parameter
This parameter converts a string into a numeric representation used by Instagram.

python
Copy code
def get_numeric_value(string):
    c = 0
    sprinkle_version = '2'
    for x in range(len(string)):
        c += ord(string[x])
    return sprinkle_version + str(c)

jazoest = get_numeric_value('csrf_token')
print(jazoest)
# Example output:
# 21070
Disclaimer
This repository is for educational and research purposes only.
Do not use these methods to bypass Instagram security, violate terms of service, or perform unauthorized actions.

License
MIT License — use freely for research or learning.

yaml
Copy code

---

Do you also want me to **add file structure (showing pwd_encoder.js and reversed.py locations) and example directory
