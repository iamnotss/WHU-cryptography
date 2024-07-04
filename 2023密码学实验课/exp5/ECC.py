# coding=gbk
# description: ECC椭圆曲线加密算法实现

import random

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - (a // b) * y

def get_inverse(z, p):
    """
    获取y的逆元
    """
    d, x, y = extended_gcd(z, p)
    if d == 1:
        return (x % p + p) % p
    else:
        return -1

def get_gcd(x, y):
    """
    获取最大公约数
    """
    if y:
        return get_gcd(y, x % y)
    else:
        return x



def add(x1, y1, x2, y2, a, p):

    flag = 1  # 定义符号位（+/-）

    # 如果 p=q  k=(3x2+a)/2y1mod p
    if x1 == x2 and y1 == y2:
        molecule = 3 * (x1 ** 2) + a  # 计算分子      
        denominator = 2 * y1    # 计算分母

    # 若P≠Q，则k=(y2-y1)/(x2-x1) mod p
    else:
        molecule = y2 - y1
        denominator = x2 - x1
        if molecule* denominator < 0:
            flag = 0        # 符号0为-（负数）
            molecule = abs(molecule)
            denominator = abs(denominator)

    # 将分子和分母化为最简
    gcd_value = get_gcd(molecule, denominator)     
    molecule = molecule // gcd_value            
    denominator = denominator // gcd_value
    #求molecule / denominator = molecule * inverse_denominator
    inverse_denominator = get_inverse(denominator, p)
    k = (molecule * inverse_denominator)

    if flag == 0:                   # 斜率负数 flag==0
        k = -k
    k = k % p
    # 计算x3,y3 P+Q
    """
        x3≡k2-x1-x2(mod p)
        y3≡k(x1-x3)-y1(mod p)
    """
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return x3,y3

def get_ng(G_x, G_y, n, a, p):
    """
    计算nG
    """
    temp_x = G_x
    temp_y = G_y
    while n != 1:
        temp_x,temp_y = add(temp_x,temp_y, G_x, G_y, a, p)
        n -= 1
    return temp_x,temp_y

def get_rank(x0, y0, a, b, p):
    """
    获取椭圆曲线的阶:
    获取n*p，每次+p，直到求解阶数np=-p

    """
    #p =(x,y) -p = (x,-y) 
    x1 = x0             #-p的x坐标
    y1 = (-1*y0)%p      #-p的y坐标
    tempX = x0
    tempY = y0
    n = 1
    while True:
        n += 1
        # 求p+q的和，得到n*p，直到求出阶
        p_x,p_y = add(tempX, tempY, x0, y0, a, p)
        # 如果 == -p,那么阶数+1，返回
        if p_x == x1 and p_y == y1:
            return n+1
        tempX = p_x
        tempY = p_y
    
    return n


def get_param(x0, a, b, p):
    """
    给定x坐标,计算p与-p
    """
    y0 = -1
    for i in range(p):
        # 椭圆曲线Ep(a,b)，p为质数，x,y∈[0,p-1]
        #通过循环，尝试每个i，检查是否满足椭圆曲线的方程
        if i**2%p == (x0**3 + a*x0 + b)%p:
            y0 = i
            break

    # 如果y0没有，返回false
    if y0 == -1:
        return False

    # 计算-y（负数取模）
    x1 = x0
    y1 = (-1*y0) % p
    return x0,y0,x1,y1


def get_graph(a, b, p):
    """
    输出椭圆曲线散点图以及所有解点
    """
    x_y = []
    # 初始化二维数组
    for i in range(p):
        x_y.append(['-' for i in range(p)])

    solutions = []  # 存储所有解点

    for i in range(p):
        val = get_param(i, a, b, p)  # 椭圆曲线上的点
        if val != False:
            x0, y0, x1, y1 = val
            x_y[x0][y0] = 1
            x_y[x1][y1] = 1
            solutions.append((x0, y0))
            solutions.append((x1, y1))

    print("椭圆曲线的散列图为：")
    for i in range(p):  # i= 0-> p-1
        temp = p - 1 - i  # 倒序

        # 格式化输出1/2位数，y坐标轴
        if temp >= 10:
            print(temp, end=" ")
        else:
            print(temp, end="  ")

        # 输出具体坐标的值，一行
        for j in range(p):
            print(x_y[j][temp], end="  ")
        print("")  # 换行

    # 输出 x 坐标轴
    print("  ", end="")
    for i in range(p):
        if i >= 10:
            print(i, end=" ")
        else:
            print(i, end="  ")
    print('\n')

    print("椭圆曲线上的所有解点为：", solutions)




def ecc_main():
    while True:
        a = int(input("请输入椭圆曲线参数a(a>0)的值："))
        b = int(input("请输入椭圆曲线参数b(b>0)的值："))
        p = int(input("请输入椭圆曲线参数p(p为素数)的值："))   #用作模运算

        # 条件满足判断
        if (4*(a**3)+27*(b**2))%p == 0:
            print("您输入的参数有误，请重新输入！！！\n")
        else:
            break

    # 输出椭圆曲线散点图
    get_graph(a, b, p)

    # 选点作为G点
    #print("userA：在如上坐标系中选一个值为G的坐标")
    G_x = int(input("userA：请输入选取的x坐标值："))
    G_y = int(input("userA：请输入选取的y坐标值："))

    # 获取椭圆曲线的阶
    n = get_rank(G_x, G_y, a, b, p)

    # userA生成私钥，小key
    key = int(input("userA：请输入私钥key（<{}）：".format(n)))

    # userA生成公钥，大Q=key G
    Q_x,Q_y = get_ng(G_x, G_y, key, a, p)

    # userB阶段
    # userB拿到userA的公钥KEY，Ep(a,b)阶n，加密需要加密的明文数据
    # 加密准备
    k = random.randint(1, n)  # 生成1到阶n之间的随机整数
    print("随机产生的整数K，用于加密数据：",k)
    #k * G
    k_G_x,k_G_y = get_ng(G_x, G_y, k, a, p)                         # kG
    #k * Q
    k_Q_x,k_Q_y = get_ng(Q_x, Q_y, k, a, p)                     # kQ

    # 加密
    plain_text = input("userB：请输入需要加密的字符串:")
    plain_text = plain_text.strip()
    c = []
    print("密文为：",end="")
    for char in plain_text:
        #获取每个字符的ASCII码值
        intchar = ord(char) 
        #将ASCII码值乘以密钥k_Q_x的得到密文 ASCII * r * KEY
        cipher_text = intchar*k_Q_x
        c.append([k_G_x, k_G_y, cipher_text])
        print("({},{}),{}".format(k_G_x, k_G_y, cipher_text),end="-")


    # userA阶段
    # 拿到userB加密的数据进行解密
    # 知道 k_G_x,k_G_y，key情况下，求解k_Q_x,k_Q_y是容易的，然后plain_text = cipher_text/k_Q_x
    print("\nuserA解密得到明文：",end="")
    for charArr in c:
        #key * kG = k * (key * G) = k * Q 
        decrypto_text_x,decrypto_text_y = get_ng(charArr[0], charArr[1], key, a, p)
        #m * kQ / kQ
        print(chr(charArr[2]//decrypto_text_x),end="")

      


if __name__ == "__main__":
    print("*************ECC椭圆曲线加密*************")
    ecc_main()
