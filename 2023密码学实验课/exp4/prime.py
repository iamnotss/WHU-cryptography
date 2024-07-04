# coding=gbk
# coding=utf-8
import random
import math
from random import randint

def proBin(w):  # w表示希望产生位数，生成目标位数的伪素数
    list = []
    list.append('1')  #最高位定为1
    for _ in range(w - 2):
        c = random.choice(['0', '1'])
        list.append(c)
    list.append('1') # 最低位定为1
    res = int(''.join(list),2)
    return res

def montgomery_reduction(x,n,r):    
    #计算N'和R'
    n_inv = pow(n,-1,r) * (-1)
    r_inv = pow(r,-1,n)
    #计算m = XN'（modR）
    m = (x * n_inv) % r
    #计算k：
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
    #计算r：
    while r < mod:
        r<<=1
    #预处理： 
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
    
    #计算r'
    r_inv = pow(r, -1, modulus)
    #计算n'
    n_inv = pow(r % modulus,-1,modulus)
    
    #将base转换为Montogomery形式
    x = (base * r) % modulus
    
    #将exponent转化为二进制表示
    bits = bin(exponent)[2:]
    
    #计算x^exponent
    y = r
    for bit in bits:
        y = montgomery_multiply(y,y,modulus,r)
        if bit == '1':
            y = montgomery_multiply(x,y,modulus,r)
            
    return montgomery_multiply(y,1,modulus,r_inv)
    

#幂模运算
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
        result = result % n # 加快连乘的速度
    return result

def MillerRabin(a, p):  #素性测试
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

    # 将 n - 1 表示为 2^k * q 的形式，其中 q 为奇数
    k = 0
    q = n - 1
    while q % 2 == 0:
        q //= 2
        k += 1

    # 进行 t 次测试
    for _ in range(t):
        # 随机选择一个在 [2, n-2] 范围内的整数 a
        a = a = randint(2, n - 2)

        # 计算 a^q % n
        x = X_n_mod_P(a, q, n)

        if x == 1 or x == n - 1:
            continue

        # 进行 k - 1 次平方探测
        for _ in range(k - 1):
            x = (x * x) % n
            if x == n - 1:
                break

        # 如果循环结束仍未找到非平凡平方根，那么 n 是合数
        if x != n - 1:
            return False

    # 通过所有测试，n 可能是素数
    return True

def makeprime1(w):           # 产生w位素数
    while 1:
        d = proBin(w)
        for i in range(50):  # 伪素数附近50个奇数都没有真素数的话，重新再产生一个伪素数
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
        
def makeprime2(w):           # 产生w位素数
    while 1:
        d = proBin(w)
        for i in range(50):  # 伪素数附近50个奇数都没有真素数的话，重新再产生一个伪素数
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

if __name__ == "__main__":   #测试
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

