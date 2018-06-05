import math
import base64
import binascii
import os

import time

from fractions import gcd
from hmac import compare_digest
from random import SystemRandom

_sysrand = SystemRandom()

def randbelow(exclusive_upper_bound):
    if exclusive_upper_bound <= 0:
        raise ValueError("Upper bound must be positive.")
    while True:
        rands = _sysrand._randbelow(exclusive_upper_bound)
        if rands in ans and rands > 400:
            return rands

def sieve(n):
    nums = [i+1 for i in range(2, n, 2) if (i+1) % 3 != 0 and (i+1) % 5 !=0]
    ans = [2,3,5]
    while nums[0] <= math.sqrt(n):
        for i in range(nums[0]**2, nums[-1]+1, nums[0]):
            if i in nums: nums.remove(i)
        ans.append(nums.pop(0))
    ans += nums
    return ans

def lcm(p, q):
    return (p * q) // gcd(p, q)

def generate_keys(p, q):
    N = p * q
    L = lcm(p - 1, q - 1)
    for i in range(2, L):
        if gcd(i, L) == 1:
            E = i
            break
    for i in range(2, L):
        if (E * i) % L == 1:
            D = i
            break
    return (E, N), (D, N)

def encrypt(plain_text, public_key):
    E, N = public_key
    plain_integers = [ord(char) for char in plain_text]
    encrypted_integers = [i ** E % N for i in plain_integers]
    encrypted_text = ''.join(chr(i) for i in encrypted_integers)

    return encrypted_text


def decrypt(encrypted_text, private_key):
    D, N = private_key
    encrypted_integers = [ord(char) for char in encrypted_text]
    decrypted_intergers = [i ** D % N for i in encrypted_integers]
    decrypted_text = ''.join(chr(i) for i in decrypted_intergers)

    return decrypted_text

def sanitize(encrypted_text):

    return encrypted_text.encode('utf-8', 'replace').decode('utf-8')

if __name__ == '__main__':
    print("素数リストを作成...")
    ans = sieve(2048)
    print("成功\n")

    print("公開鍵、秘密鍵を生成...")
    while True:
        rand1 = randbelow(2048)
        rand2 = randbelow(2048)
        randsum = rand1 + rand2
        if randsum >= 2048 and randsum <= 2200 and abs(rand1 - rand2) > 400:
            break

    public_key, private_key = generate_keys(rand1, rand2)
    rand1 = rand2 = 0
    print("成功\n")
    text = "2fjaewfj34jfd99#$ofaf7htyi97y4568067lo784u5978056i6o56u35685ujhyu549023DHHfi3r299d02$flf43tteru5ie9"
    print("平文: ",text)
    e_text = encrypt(text, public_key)
    print("暗号文: ",sanitize(e_text))
    t1 = time.time()
    d_text = decrypt(e_text, private_key)
    t2 = time.time()
    elapsed_time = t2 - t1
    print("復号文: ",d_text)
    print("復号化に%lf秒かかりました" % elapsed_time)
