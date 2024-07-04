# coding=gbk
# description: ECC��Բ���߼����㷨ʵ��

import random

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - (a // b) * y

def get_inverse(z, p):
    """
    ��ȡy����Ԫ
    """
    d, x, y = extended_gcd(z, p)
    if d == 1:
        return (x % p + p) % p
    else:
        return -1

def get_gcd(x, y):
    """
    ��ȡ���Լ��
    """
    if y:
        return get_gcd(y, x % y)
    else:
        return x



def add(x1, y1, x2, y2, a, p):

    flag = 1  # �������λ��+/-��

    # ��� p=q  k=(3x2+a)/2y1mod p
    if x1 == x2 and y1 == y2:
        molecule = 3 * (x1 ** 2) + a  # �������      
        denominator = 2 * y1    # �����ĸ

    # ��P��Q����k=(y2-y1)/(x2-x1) mod p
    else:
        molecule = y2 - y1
        denominator = x2 - x1
        if molecule* denominator < 0:
            flag = 0        # ����0Ϊ-��������
            molecule = abs(molecule)
            denominator = abs(denominator)

    # �����Ӻͷ�ĸ��Ϊ���
    gcd_value = get_gcd(molecule, denominator)     
    molecule = molecule // gcd_value            
    denominator = denominator // gcd_value
    #��molecule / denominator = molecule * inverse_denominator
    inverse_denominator = get_inverse(denominator, p)
    k = (molecule * inverse_denominator)

    if flag == 0:                   # б�ʸ��� flag==0
        k = -k
    k = k % p
    # ����x3,y3 P+Q
    """
        x3��k2-x1-x2(mod p)
        y3��k(x1-x3)-y1(mod p)
    """
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return x3,y3

def get_ng(G_x, G_y, n, a, p):
    """
    ����nG
    """
    temp_x = G_x
    temp_y = G_y
    while n != 1:
        temp_x,temp_y = add(temp_x,temp_y, G_x, G_y, a, p)
        n -= 1
    return temp_x,temp_y

def get_rank(x0, y0, a, b, p):
    """
    ��ȡ��Բ���ߵĽ�:
    ��ȡn*p��ÿ��+p��ֱ��������np=-p

    """
    #p =(x,y) -p = (x,-y) 
    x1 = x0             #-p��x����
    y1 = (-1*y0)%p      #-p��y����
    tempX = x0
    tempY = y0
    n = 1
    while True:
        n += 1
        # ��p+q�ĺͣ��õ�n*p��ֱ�������
        p_x,p_y = add(tempX, tempY, x0, y0, a, p)
        # ��� == -p,��ô����+1������
        if p_x == x1 and p_y == y1:
            return n+1
        tempX = p_x
        tempY = p_y
    
    return n


def get_param(x0, a, b, p):
    """
    ����x����,����p��-p
    """
    y0 = -1
    for i in range(p):
        # ��Բ����Ep(a,b)��pΪ������x,y��[0,p-1]
        #ͨ��ѭ��������ÿ��i������Ƿ�������Բ���ߵķ���
        if i**2%p == (x0**3 + a*x0 + b)%p:
            y0 = i
            break

    # ���y0û�У�����false
    if y0 == -1:
        return False

    # ����-y������ȡģ��
    x1 = x0
    y1 = (-1*y0) % p
    return x0,y0,x1,y1


def get_graph(a, b, p):
    """
    �����Բ����ɢ��ͼ�Լ����н��
    """
    x_y = []
    # ��ʼ����ά����
    for i in range(p):
        x_y.append(['-' for i in range(p)])

    solutions = []  # �洢���н��

    for i in range(p):
        val = get_param(i, a, b, p)  # ��Բ�����ϵĵ�
        if val != False:
            x0, y0, x1, y1 = val
            x_y[x0][y0] = 1
            x_y[x1][y1] = 1
            solutions.append((x0, y0))
            solutions.append((x1, y1))

    print("��Բ���ߵ�ɢ��ͼΪ��")
    for i in range(p):  # i= 0-> p-1
        temp = p - 1 - i  # ����

        # ��ʽ�����1/2λ����y������
        if temp >= 10:
            print(temp, end=" ")
        else:
            print(temp, end="  ")

        # ������������ֵ��һ��
        for j in range(p):
            print(x_y[j][temp], end="  ")
        print("")  # ����

    # ��� x ������
    print("  ", end="")
    for i in range(p):
        if i >= 10:
            print(i, end=" ")
        else:
            print(i, end="  ")
    print('\n')

    print("��Բ�����ϵ����н��Ϊ��", solutions)




def ecc_main():
    while True:
        a = int(input("��������Բ���߲���a(a>0)��ֵ��"))
        b = int(input("��������Բ���߲���b(b>0)��ֵ��"))
        p = int(input("��������Բ���߲���p(pΪ����)��ֵ��"))   #����ģ����

        # ���������ж�
        if (4*(a**3)+27*(b**2))%p == 0:
            print("������Ĳ����������������룡����\n")
        else:
            break

    # �����Բ����ɢ��ͼ
    get_graph(a, b, p)

    # ѡ����ΪG��
    #print("userA������������ϵ��ѡһ��ֵΪG������")
    G_x = int(input("userA��������ѡȡ��x����ֵ��"))
    G_y = int(input("userA��������ѡȡ��y����ֵ��"))

    # ��ȡ��Բ���ߵĽ�
    n = get_rank(G_x, G_y, a, b, p)

    # userA����˽Կ��Сkey
    key = int(input("userA��������˽Կkey��<{}����".format(n)))

    # userA���ɹ�Կ����Q=key G
    Q_x,Q_y = get_ng(G_x, G_y, key, a, p)

    # userB�׶�
    # userB�õ�userA�Ĺ�ԿKEY��Ep(a,b)��n��������Ҫ���ܵ���������
    # ����׼��
    k = random.randint(1, n)  # ����1����n֮����������
    print("�������������K�����ڼ������ݣ�",k)
    #k * G
    k_G_x,k_G_y = get_ng(G_x, G_y, k, a, p)                         # kG
    #k * Q
    k_Q_x,k_Q_y = get_ng(Q_x, Q_y, k, a, p)                     # kQ

    # ����
    plain_text = input("userB����������Ҫ���ܵ��ַ���:")
    plain_text = plain_text.strip()
    c = []
    print("����Ϊ��",end="")
    for char in plain_text:
        #��ȡÿ���ַ���ASCII��ֵ
        intchar = ord(char) 
        #��ASCII��ֵ������Կk_Q_x�ĵõ����� ASCII * r * KEY
        cipher_text = intchar*k_Q_x
        c.append([k_G_x, k_G_y, cipher_text])
        print("({},{}),{}".format(k_G_x, k_G_y, cipher_text),end="-")


    # userA�׶�
    # �õ�userB���ܵ����ݽ��н���
    # ֪�� k_G_x,k_G_y��key����£����k_Q_x,k_Q_y�����׵ģ�Ȼ��plain_text = cipher_text/k_Q_x
    print("\nuserA���ܵõ����ģ�",end="")
    for charArr in c:
        #key * kG = k * (key * G) = k * Q 
        decrypto_text_x,decrypto_text_y = get_ng(charArr[0], charArr[1], key, a, p)
        #m * kQ / kQ
        print(chr(charArr[2]//decrypto_text_x),end="")

      


if __name__ == "__main__":
    print("*************ECC��Բ���߼���*************")
    ecc_main()
