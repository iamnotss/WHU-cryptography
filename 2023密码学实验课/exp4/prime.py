# coding=gbk
# coding=utf-8
import random
import math
from random import randint

def proBin(w):  # w��ʾϣ������λ��������Ŀ��λ����α����
    list = []
    list.append('1')  #���λ��Ϊ1
    for _ in range(w - 2):
        c = random.choice(['0', '1'])
        list.append(c)
    list.append('1') # ���λ��Ϊ1
    res = int(''.join(list),2)
    return res

def montgomery_reduction(x,n,r):    
    #����N'��R'
    n_inv = pow(n,-1,r) * (-1)
    r_inv = pow(r,-1,n)
    #����m = XN'��modR��
    m = (x * n_inv) % r
    #����k��
    k = 0
    while r < n:
        r <<= 1
        k += 1
    
    y = x + m * n
    y >>= k
    
    if y > n:
        return y-n
    else:
        return y

def mod_exp(base,exp,mod):
    #����r��
    while r < mod:
        r<<=1
    #Ԥ���� 
    base = base * r % mod
    result = 1
    
    while exp > 0:
        if exp & 1 :
            result = montgomery_reduction(result * base,mod,r)
        
        base = montgomery_reduction(base * base, mod, r)
        exp >>=1
    
    return montgomery_reduction(result,mod,r)

def montgomery_multiply(a,b,n,r):
    t = a * b
    t = t % r
    t = (t * n) % r
    
    u = (t + a * b) / r
    if u >= n:
        return u -n
    else:
        return u
    
def montgomery_powmod(base,exponent,modulus):
    r = 1
    while r < modulus:
        r <<= 1
    
    #����r'
    r_inv = pow(r, -1, modulus)
    #����n'
    n_inv = pow(r % modulus,-1,modulus)
    
    #��baseת��ΪMontogomery��ʽ
    x = (base * r) % modulus
    
    #��exponentת��Ϊ�����Ʊ�ʾ
    bits = bin(exponent)[2:]
    
    #����x^exponent
    y = r
    for bit in bits:
        y = montgomery_multiply(y,y,modulus,r)
        if bit == '1':
            y = montgomery_multiply(x,y,modulus,r)
            
    return montgomery_multiply(y,1,modulus,r_inv)
    

#��ģ����
def X_n_mod_P(base, exponent, n):
    bin_array = bin(exponent)[2:][::-1]
    r = len(bin_array)
    base_array = []
    
    pre_base = base
    base_array.append(pre_base)
    
    for _ in range(r - 1):
        next_base = (pre_base * pre_base) % n 
        base_array.append(next_base)
        pre_base = next_base
        
    a_w_b = __multi(base_array, bin_array, n)
    return a_w_b % n


def __multi(array, bin_array, n):
    result = 1
    for index in range(len(array)):
        a = array[index]
        if not int(bin_array[index]):
            continue
        result *= a
        result = result % n # �ӿ����˵��ٶ�
    return result

def MillerRabin(a, p):  #���Բ���
    if X_n_mod_P(a, p - 1, p) == 1:
        u = (p-1) >> 1
        while (u & 1) == 0:
            t = X_n_mod_P(a, u, p)
            if t == 1:
                u = u >> 1
            else:
                if t == p - 1:
                    return True
                else:
                    return False
        else:
            t = X_n_mod_P(a, u, p)
            if t == 1 or t == p - 1:
                return True
            else:
                return False
    else:
        return False


def judge_prime(number):
    temp = int(math.sqrt(number))
    for i in range(2, temp + 1):
        if number % i == 0:
            return False
    return True

def testMillerRabin(n, t):
    if n <= 1:
        return False
    if n <= 3:
        return True

    # �� n - 1 ��ʾΪ 2^k * q ����ʽ������ q Ϊ����
    k = 0
    q = n - 1
    while q % 2 == 0:
        q //= 2
        k += 1

    # ���� t �β���
    for _ in range(t):
        # ���ѡ��һ���� [2, n-2] ��Χ�ڵ����� a
        a = a = randint(2, n - 2)

        # ���� a^q % n
        x = X_n_mod_P(a, q, n)

        if x == 1 or x == n - 1:
            continue

        # ���� k - 1 ��ƽ��̽��
        for _ in range(k - 1):
            x = (x * x) % n
            if x == n - 1:
                break

        # ���ѭ��������δ�ҵ���ƽ��ƽ��������ô n �Ǻ���
        if x != n - 1:
            return False

    # ͨ�����в��ԣ�n ����������
    return True

def makeprime1(w):           # ����wλ����
    while 1:
        d = proBin(w)
        for i in range(50):  # α��������50��������û���������Ļ��������ٲ���һ��α����
            u = testMillerRabin(d+2*(i), 5)
            if u:
                b = d + 2*(i)
                break
            else:
                continue
        if u:
            return b
        else:
            continue
        
def makeprime2(w):           # ����wλ����
    while 1:
        d = proBin(w)
        for i in range(50):  # α��������50��������û���������Ļ��������ٲ���һ��α����
            u = judge_prime(d+2*(i))
            if u:
                b = d + 2*(i)
                break
            else:
                continue
        if u:
            return b
        else:
            continue

if __name__ == "__main__":   #����
    #print(makeprime1(256))
    #print(makeprime2(50))
    if(judge_prime(makeprime1(50))):
        print("yes")
    else: 
        print("no")
    
    #if(judge_prime(1000000000000002493)):
        #print("yes")
    #else: 
        #print("no")

