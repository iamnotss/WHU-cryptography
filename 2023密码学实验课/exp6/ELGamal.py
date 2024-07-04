# coding=gbk
# -*- coding: UTF-8 -*-
import random


# 求最大公约数
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# 快速幂+取模
def power(a, b, c):
    ans = 1
    while b != 0:
        if b & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a * a) % c
    return ans


# 大素数检测
def Miller_Rabin(n):
    a = random.randint(2,n-2) #随机第选取一个a∈[2,n-2]
    # print("随机选取的a=%lld\n"%a)
    s = 0 #s为d中的因子2的幂次数。
    d = n - 1
    while (d & 1) == 0: #将d中因子2全部提取出来。
        s += 1
        d >>= 1

    x = power(a, d, n)
    for i in range(s): #进行s次二次探测
        newX = power(x, 2, n)
        if newX == 1 and x != 1 and x != n - 1:
            return False #用二次定理的逆否命题，此时n确定为合数。
        x = newX

    if x != 1:  # 用费马小定理的逆否命题判断，此时x=a^(n-1) (mod n)，那么n确定为合数。
        return False

    return True  # 用费马小定理的逆命题判断。能经受住考验至此的数，大概率为素数。


# 扩展的欧几里得算法，ab=1 (mod m), 得到a在模m下的乘法逆元b
def Extended_Eulid(a: int, m: int) -> int:
    def extended_eulid(a: int, m: int):
        if a == 0:  # 边界条件
            return 1, 0, m
        else:
            x, y, gcd = extended_eulid(m % a, a)  # 递归
            x, y = y, (x - (m // a) * y)  # 递推关系，左端为上层
            return x, y, gcd  # 返回第一层的计算结果。
        # 最终返回的y值即为b在模a下的乘法逆元
        # 若y为复数，则y+a为相应的正数逆元

    n = extended_eulid(a, m)
    if n[1] < 0:
        return n[1] + m
    else:
        return n[1]


# 生成域参数p，长度大约为512bits
def Generate_p() -> int:
    a = random.randint(10**150, 10**160)
    while gcd(a, 2) != 1:
        a = random.randint(10**150, 10**160)
    return a


# 生成域参数alpha
def Generate_alpha(p: int) -> int:
    return random.randint(2, p)

#     def is_primitive_root(alpha, p):
#         """
#         检查 alpha 是否是模 p 意义下的本原元
#         """
#         for i in range(2, p - 1):
#             if pow(alpha, i, p) == 1:
#                 return False
#         return True

# def Generate_alpha(p: int) -> int:
#     """
#     生成模 p 意义下的本原元
#     """
#     while True:
#         alpha = random.randint(2, p - 1)
#         if is_primitive_root(alpha, p):
#             return alpha


# 生成一个小于p的素数作为私钥，长度大约为512bits
def Generate_private_key(p: int) -> int:
    pri = random.randint(2, p - 2)
    while gcd(pri, p) != 1:
        pri = random.randint(2, p - 2)
    return pri


# 快速幂
def quick_power(a: int, b: int) -> int:
    ans = 1
    while b != 0:
        if b & 1:
            ans = ans * a
        b >>= 1
        a = a * a
    return ans


def Generate_prime(key_size: int) -> int:
    while True:
        num = random.randrange(quick_power(2, key_size - 1), quick_power(2, key_size))
        if Miller_Rabin(num):
            return num


# 计算签名
def Sign(m, p, alpha, x) -> []:
    k = random.randint(0, p - 2)
    while gcd(k, p - 1) != 1:
        k = random.randint(0, p - 2)
    #验证步骤二
    k = 5
    r = power(alpha, k, p)
    s = (m - x * r) * Extended_Eulid(k, p - 1) % (p - 1)
    return r, s


# 签名验证
def Verify(m, p, alpha, y, r, s):
    v1 = power(alpha, m, p)
    v2 = (power(y, r, p) * power(r, s, p)) % p
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    if v1 == v2:
        return True
    else:
        return False

if __name__ == '__main__':
    #验证步骤二，m=14
    M = int(input("Message:"))
    if type(M) != int:
        raise ValueError("Must be an integer!")

    # 大素数
    p = Generate_prime(512)
    # alpha是模p的本原元
    alpha = Generate_alpha(p)
    # 用户自己的解密钥
    x = Generate_private_key(p)
    # 用户公开的加密钥
    y = power(alpha, x, p)

    #步骤一验证
    p = 19
    alpha = 10
    x = 16
    y = power(alpha, x, p)
    
    r, s = Sign(M, p, alpha, x)
    Valid = Verify(M, p, alpha, y, r, s)

    r_ = random.randint(10 ** 150, 10 ** 160)
    s_ = random.randint(10 ** 150, 10 ** 160)
    x_ = random.randint(10 ** 150, 10 ** 160)

    print("Private Key: ")
    print("x:            ", x)
    print("Public key : ")
    print("p:            ", p)
    print("alpha:        ", alpha)
    print("y:         ", y)
    print("Signature: ")
    print("r:            ", r)
    print("s:            ", s)
    print("Verify (r, s) of M: ")
    if Verify(M, p, alpha, y, r, s):
        print("Signature is valid")
    else:
        print("Signature is invalid")
    print("M' (After attack): ", x_)
    print("Verify (r, s) of M': ")
    if Verify(x_, p, alpha, y, r_, s_):
        print("After attack M,signature is still valid")
    else:
        print("After attack m,signature is invalid")

    print("r' (After attack): ", r_)
    print("s' (After attack): ", s_)
    print("Verify (r', s') of M: ")
    if Verify(M, p, alpha, y, r_, s_):
        print("After attack (r,s),signature is still valid")
    else:
        print("After attack (r,s),signature is invalid")
