# coding=gbk
# -*- coding: UTF-8 -*-
import random


# �����Լ��
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# ������+ȡģ
def power(a, b, c):
    ans = 1
    while b != 0:
        if b & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a * a) % c
    return ans


# ���������
def Miller_Rabin(n):
    a = random.randint(2,n-2) #�����ѡȡһ��a��[2,n-2]
    # print("���ѡȡ��a=%lld\n"%a)
    s = 0 #sΪd�е�����2���ݴ�����
    d = n - 1
    while (d & 1) == 0: #��d������2ȫ����ȡ������
        s += 1
        d >>= 1

    x = power(a, d, n)
    for i in range(s): #����s�ζ���̽��
        newX = power(x, 2, n)
        if newX == 1 and x != 1 and x != n - 1:
            return False #�ö��ζ����������⣬��ʱnȷ��Ϊ������
        x = newX

    if x != 1:  # �÷���С�������������жϣ���ʱx=a^(n-1) (mod n)����ônȷ��Ϊ������
        return False

    return True  # �÷���С������������жϡ��ܾ���ס�������˵����������Ϊ������


# ��չ��ŷ������㷨��ab=1 (mod m), �õ�a��ģm�µĳ˷���Ԫb
def Extended_Eulid(a: int, m: int) -> int:
    def extended_eulid(a: int, m: int):
        if a == 0:  # �߽�����
            return 1, 0, m
        else:
            x, y, gcd = extended_eulid(m % a, a)  # �ݹ�
            x, y = y, (x - (m // a) * y)  # ���ƹ�ϵ�����Ϊ�ϲ�
            return x, y, gcd  # ���ص�һ��ļ�������
        # ���շ��ص�yֵ��Ϊb��ģa�µĳ˷���Ԫ
        # ��yΪ��������y+aΪ��Ӧ��������Ԫ

    n = extended_eulid(a, m)
    if n[1] < 0:
        return n[1] + m
    else:
        return n[1]


# ���������p�����ȴ�ԼΪ512bits
def Generate_p() -> int:
    a = random.randint(10**150, 10**160)
    while gcd(a, 2) != 1:
        a = random.randint(10**150, 10**160)
    return a


# ���������alpha
def Generate_alpha(p: int) -> int:
    return random.randint(2, p)

#     def is_primitive_root(alpha, p):
#         """
#         ��� alpha �Ƿ���ģ p �����µı�ԭԪ
#         """
#         for i in range(2, p - 1):
#             if pow(alpha, i, p) == 1:
#                 return False
#         return True

# def Generate_alpha(p: int) -> int:
#     """
#     ����ģ p �����µı�ԭԪ
#     """
#     while True:
#         alpha = random.randint(2, p - 1)
#         if is_primitive_root(alpha, p):
#             return alpha


# ����һ��С��p��������Ϊ˽Կ�����ȴ�ԼΪ512bits
def Generate_private_key(p: int) -> int:
    pri = random.randint(2, p - 2)
    while gcd(pri, p) != 1:
        pri = random.randint(2, p - 2)
    return pri


# ������
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


# ����ǩ��
def Sign(m, p, alpha, x) -> []:
    k = random.randint(0, p - 2)
    while gcd(k, p - 1) != 1:
        k = random.randint(0, p - 2)
    #��֤�����
    k = 5
    r = power(alpha, k, p)
    s = (m - x * r) * Extended_Eulid(k, p - 1) % (p - 1)
    return r, s


# ǩ����֤
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
    #��֤�������m=14
    M = int(input("Message:"))
    if type(M) != int:
        raise ValueError("Must be an integer!")

    # ������
    p = Generate_prime(512)
    # alpha��ģp�ı�ԭԪ
    alpha = Generate_alpha(p)
    # �û��Լ��Ľ���Կ
    x = Generate_private_key(p)
    # �û������ļ���Կ
    y = power(alpha, x, p)

    #����һ��֤
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
