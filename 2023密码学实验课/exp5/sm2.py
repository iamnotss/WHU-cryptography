# coding=gbk
# -*- coding: UTF-8 -*-
import random
from math import gcd, ceil, log
from gmssl import sm3


# ��������װ��
# �������ֽڴ���ת�������շǸ�����x���ֽڴ���Ŀ�곤��k��k����2^8k > x������ֵ�ǳ�Ϊk���ֽڴ���k�Ǹ����Ĳ�����
def int_to_bytes(x, k):         # ����˼·���������0��x��Ϊk*8λ16������������ÿ2λ�ϳ�1���ֽ�
    if pow(256, k) <= x:
        raise Exception("�޷�ʵ���������ֽڴ���ת����Ŀ���ֽڴ����ȹ��̣�")
    s = hex(x)[2:].rjust(k*2, '0')          # s��k*2λʮ�����ƴ�
    M = b''
    for i in range(k):
        M = M + bytes([eval('0x' + s[i*2:i*2+2])])
    return M


# �ֽڴ���������ת�������ܳ���Ϊk���ֽڴ�������ֵ������x
def bytes_to_int(M):            # ����˼·�ǴӺ���ǰ����M��ÿ���ֽڵĻ�����2^8��
    k = len(M)          # k���ֽڴ��ĳ���
    x = 0           # x�洢��������
    for i in range(k-1, -1, -1):
        x += pow(256, k-1-i) * M[i]
    return x


# ���ش����ֽڴ���ת�������ճ���Ϊm�ı��ش�s�����س���Ϊk���ֽڴ�M������k = [m/8] ����ȡ����
def bits_to_bytes(s):           # ���ж��ַ��������Ƿ�������ת��Ϊ�ֽڴ����������Ƿ�Ϊ8�ı������������������������Ϊ8�ı�����
    k = ceil(len(s)/8)          # ���ش����ȳ���8����ȡ��
    s = s.rjust(k*8, '0')           # ����������һ���൱��û�У����������൱�ڽ��������Ϊ�����ܱ�8������k
    M = b''         # M�洢Ҫ���ص��ֽڴ�
    for i in range(k):
        M = M + bytes([eval('0b' + s[i*8: i*8+8])])
    return M


# �ֽڴ������ش���ת�������ճ���Ϊk���ֽڴ�M�����س���Ϊm�ı��ش�s������m = 8k���ֽڴ���λ�����ɡ�
def bytes_to_bits(M):           # ����˼·�ǰ�ÿ���ֽڱ�Ϊ8λ���ش������б�洢�������������
    s_list = []
    for i in M:
        s_list.append(bin(i)[2:].rjust(8, '0'))         # ÿ��ѭ���洢1���ֽڡ�����䲹0
    s = ''.join(s_list)
    return s


# ��Ԫ�ص��ֽڴ���ת������Ԫ����������ת�����ֽڴ�Ҫ��ȷ���ȡ��ĵ��涨��Ԫ��ת��Ϊ�ֽڴ��ĳ�����ceil(ceil(log(q, 2)/8))�����յĲ�������Ԫ��a�������ֽڴ�M
def fielde_to_bytes(e):
    q = eval('0x' + '8542D69E 4C044F18 E8B92435 BF6FF7DE 45728391 5C45517D 722EDB8B 08F1DFC3'.replace(' ', ''))
    t = ceil(log(q, 2))
    l = ceil(t / 8)
    return int_to_bytes(e, l)


# �ֽڴ�����Ԫ�ص�ת����ֱ�ӵ���bytes_to_int()�����յĲ������ֽڴ�M��������Ԫ��a
def bytes_to_fielde(M):         # ��Ԫ�ز������
    return bytes_to_int(M)


# ��Ԫ�ص�������ת��
def fielde_to_int(a):           # ֱ�ӷ���
    return a


# �㵽�ֽڴ���ת�������յĲ�������Բ�����ϵĵ�p��Ԫ���ʾ������ֽڴ�S��ѡ��δѹ����ʾ��ʽ
def point_to_bytes(P):
    xp, yp = P[0], P[1]
    x = fielde_to_bytes(xp)
    y = fielde_to_bytes(yp)
    PC = bytes([0x04])
    s = PC + x + y
    return s


# �ֽڴ������ת�������յĲ������ֽڴ�s��������Բ�����ϵĵ�P����P��������Ԫ���ʾ
def bytes_to_point(s):
    if len(s) % 2 == 0:
        raise Exception("�޷�ʵ���ֽڴ������ת���������ֽڴ��Ƿ�Ϊδѹ����ʽ��")
    l = (len(s) - 1) // 2
    PC = s[0]
    if PC != 4:
        raise Exception("�޷�ʵ���ֽڴ������ת��������PC�Ƿ�Ϊb'04'��")
    x = s[1: l+1]
    y = s[l+1: 2*l+1]
    xp = bytes_to_fielde(x)
    yp = bytes_to_fielde(y)
    P = (xp, yp)            # �˴�ȱ�ټ����p�Ƿ�����Բ������
    return P


# ������������ת��
# ��Ԫ�ص����ش�
def fielde_to_bits(a):
    a_bytes = fielde_to_bytes(a)
    a_bits = bytes_to_bits(a_bytes)
    return a_bits


# �㵽���ش�
def point_to_bits(P):
    p_bytes = point_to_bytes(P)
    p_bits = bytes_to_bits(p_bytes)
    return p_bits


# ���������ش�
def int_to_bits(x):
    x_bits = bin(x)[2:]
    k = ceil(len(x_bits)/8)         # 8λ1�飬k��������Ŀ���Ƿ������
    x_bits = x_bits.rjust(k*8, '0')
    return x_bits


# �ֽڴ���ʮ�����ƴ�
def bytes_to_hex(m):
    h_list = []         # h_list�洢ʮ�����ƴ��е�ÿһ����
    for i in m:
        e = hex(i)[2:].rjust(2, '0')            # ���ܰ�0����
        h_list.append(e)
    h = ''.join(h_list)
    return h


# ���ش���ʮ������
def bits_to_hex(s):
    s_bytes = bits_to_bytes(s)
    s_hex = bytes_to_hex(s_bytes)
    return s_hex


# ʮ�����ƴ������ش�
def hex_to_bits(h):
    b_list = []
    for i in h:
        b = bin(eval('0x' + i))[2:].rjust(4, '0')           # ��ǿ��forѭ������i����h
        b_list.append(b)
    b = ''.join(b_list)
    return b


# ʮ�����Ƶ��ֽڴ�
def hex_to_bytes(h):
    h_bits = hex_to_bits(h)
    h_bytes = bits_to_bytes(h_bits)
    return h_bytes


# ��Ԫ�ص�ʮ�����ƴ�
def fielde_to_hex(e):
    h_bytes = fielde_to_bytes(e)
    h = bytes_to_hex(h_bytes)
    return h


# ��Կ��������KDF�����յĲ����Ǳ��ش�Z��Ҫ��õ���Կ���ݵĳ���klen������klen���ȵ���Կ���ݱ��ش�K
def KDF(Z, klen):
    v = 256           # �����Ӵպ�������SM3
    if klen >= (pow(2, 32) - 1) * v:
        raise Exception("��Կ��������KDF��������klen�Ĵ�С��")
    ct = 0x00000001
    if klen % v == 0:
        l = klen // v
    else:
        l = klen // v + 1
    Ha = []
    for i in range(l):         # i��0�� klen/v-1������ȡ����,��l��Ԫ��
        s = Z + int_to_bits(ct).rjust(32, '0')         # s�洢 Z || ct �ı��ش���ʽ # ע�⣬ctҪ���Ϊ32λ
        s_bytes = bits_to_bytes(s)          # s_bytes�洢�ֽڴ���ʽ
        s_list = [i for i in s_bytes]
        hash_hex = sm3.sm3_hash(s_list)
        hash_bin = hex_to_bits(hash_hex)
        Ha.append(hash_bin)
        ct += 1
    if klen % v != 0:
        Ha[-1] = Ha[-1][:klen - v*(klen//v)]
    k = ''.join(Ha)
    return k


# ģ���㷨������Mģm���档�ڽ���ʽģ����ת��Ϊ����ʱ�ã����ӷ�ĸͬʱ���Ϸ�ĸ��ģ�档
def calc_inverse(M, m):
    if gcd(M, m) != 1:
        return None
    u1, u2, u3 = 1, 0, M
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


# ����ʽģ����ת��Ϊ���������� up/down mod m, ���ظ÷�ʽ��ģm�����µ���������ӺͶ���������ʱ����á�
def frac_to_int(up, down, p):
    num = gcd(up, down)
    up //= num
    down //= num         # ���ӷ�ĸԼ��
    return up * calc_inverse(down, p) % p


# ��Բ�����ϵĵ�����㡣���յĲ�����Ԫ��P��Q����ʾ��ӵ������㣬pΪģ�������ض��ߵĵ�Ӻ�
def add_point(P, Q, p):
    if P == 0:
        return Q
    if Q == 0:
        return P
    x1, y1, x2, y2 = P[0], P[1], Q[0], Q[1]
    e = frac_to_int(y2 - y1, x2 - x1, p)            # eΪ��
    x3 = (e*e - x1 - x2) % p            # ע��˴�ҲҪȡģ
    y3 = (e * (x1 - x3) - y1) % p
    ans = (x3, y3)
    return ans


# �������㷨������ֱ���õ���㷨������ᷢ��������󡣽��յĲ����ǵ�P������p����Բ���߲���a������P�Ķ����㡣
def double_point(P, p, a):
    if P == 0:
        return P
    x1, y1 = P[0], P[1]
    e = frac_to_int(3 * x1 * x1 + a, 2 * y1, p)         # e�Ǧ�
    x3 = (e * e - 2 * x1) % p         # ȡģ����������
    y3 = (e * (x1 - x3) - y1) % p
    Q = (x3, y3)
    return Q


# �౶���㷨��ͨ��������չ����ʵ�֡����յĲ���[k]p��Ҫ��Ķ౶�㣬m��ģ����a����Բ���߲�����
def mult_point(P, k, p, a):
    s = bin(k)[2:]          # s��k�Ķ����ƴ���ʽ
    Q = 0
    for i in s:
        Q = double_point(Q, p, a)
        if i == '1':
            Q = add_point(P, Q, p)
    return Q


# ��֤ĳ�����Ƿ�����Բ�����ϡ����յĲ�������Բ����ϵͳ����args��Ҫ��֤�ĵ�P(x, y)��
def on_curve(args, P):
    p, a, b, h, G, n = args
    x, y = P
    if pow(y, 2, p) == ((pow(x, 3, p) + a*x + b) % p):
        return True
    return False


# �����㷨�����յĲ�������Բ����ϵͳ����args(p, a, b, h, G, n)������n�ǻ���G�Ľס�PB��B�Ĺ�Կ��M��������Ϣ��
def encry_sm2(args, PB, M):
    p, a, b, h, G, n = args         # ������Բ���߲���
    M_bytes = bytes(M, encoding='ascii')
    print("Step1�����������k��[1,n-1]")
    k = random.randint(1, n-1)
    k_hex = hex(k)[2:]          # k_hex ��k��ʮ�����ƴ���ʽ
    print("���ɵ�������ǣ�", k_hex)
    print("\nStep2:������Բ���ߵ�C1=[k]G=(x1,y1)����C1����������ת��Ϊ���ش�")
    C1 = mult_point(G, k, p, a)
    print("��Բ���ߵ�C1=[k]G=(x1,y1)��������:", tuple(map(hex, C1)))
    C1_bits = point_to_bits(C1)
    print("��Բ���ߵ�C1=[k]G=(x1,y1)������ı��ش���ʽ��:", C1_bits)
    print("\nStep3��������Բ���ߵ�S = hPB")
    S = mult_point(PB, h, p, a)
    if S == 0:
        raise Exception("����õ���S������Զ��")
    print("��Բ���ߵ�S = [h]PB��������:", tuple(map(hex, S)))
    print("\nStep4��������Բ���ߵ�[k]PB=(x2,y2)��������x2��y2 ����������ת��Ϊ���ش�")
    x2, y2 = mult_point(PB, k, p, a)
    print("��Բ���ߵ�[k]PB=(x2,y2)��������:", tuple(map(hex, (x2, y2))))
    x2_bits = fielde_to_bits(x2)
    print("x2�ı��ش���ʽ�ǣ�", x2_bits)
    y2_bits = fielde_to_bits(y2)
    print("y2�ı��ش���ʽ�ǣ�", y2_bits)
    print("\nStep5������t=KDF(x2 �� y2, klen)����tΪȫ0���ش����򷵻�Step1")
    M_hex = bytes_to_hex(M_bytes)
    klen = 4 * len(M_hex)
    print("������Ϣ�ı��ش�����klen�ǣ�", klen)
    t = KDF(x2_bits + y2_bits, klen)
    print("ͨ��KDF�㷨����õ���t=KDF(x2 �� y2, klen)�ǣ�", t)
    if eval('0b' + t) == 0:
        raise Exception("KDF������ȫ�㴮������KDF�㷨��")
    t_hex = bits_to_hex(t)
    print("t��ʮ�����Ʊ�ʾ��ʽ�ǣ�", t_hex)
    print("\nStep6���������C2 = M �� t")
    C2 = eval('0x' + M_hex + '^' + '0b' + t)
    print("�����C2�ǣ�", hex(C2)[2:])
    print("\nStep7������C3 = Hash(x2 �� M �� y2)")
    x2_bytes = bits_to_bytes(x2_bits)
    y2_bytes = bits_to_bytes(y2_bits)
    hash_list = [i for i in x2_bytes + M_bytes + y2_bytes]
    C3 = sm3.sm3_hash(hash_list)
    print("�����C3 = Hash(x2 �� M �� y2)�ǣ�", C3)
    print("\nStep8���������C = C1 �� C2 �� C3")
    C1_hex = bits_to_hex(C1_bits)
    C2_hex = hex(C2)[2:]
    C3_hex = C3
    C_hex = C1_hex + C2_hex + C3_hex
    print("���ܵõ��������ǣ�", C_hex)
    return C_hex


# �����㷨�����յĲ���Ϊ��Բ����ϵͳ����args(p, a, b, h, G, n)��dB��B��˽Կ��C��������Ϣ��
def decry_sm2(args, dB, C):
    p, a, b, h, G, n = args
    print("Step1����C��ȡ�����ش�C1����C1����������ת��Ϊ��Բ�����ϵĵ㣬��֤C1�Ƿ�������Բ���߷��̣����������򱨴��˳���")
    l = ceil(log(p, 2)/8)         # l��һ����Ԫ�أ�����һ����ĺ����꣩ת��Ϊ�ֽڴ�����ֽڳ���.��δѹ������ʽ�����ĵ�һ����C1����Ϊ2l+1
    bytes_l1 = 2*l+1
    print("����õ���C1���ֽڴ������ǣ�", bytes_l1)
    hex_l1 = bytes_l1 * 2            # hex_l1�����ĵ�һ����C1��ʮ�����ƴ��ĳ���
    C_bytes = hex_to_bytes(C)
    print("��ʮ���������Ĵ�ת��Ϊ�ֽڴ��ǣ�", C_bytes)
    C1_bytes = C_bytes[0:2*l+1]
    print("�������ֽڴ���ȡ����C1���ֽڴ��ǣ�", C1_bytes)
    C1 = bytes_to_point(C1_bytes)
    print("��C1�ֽڴ�ת��Ϊ��Բ�����ϵĵ��ǣ�", C1)
    if not on_curve(args, C1):          # ����C1�Ƿ�����Բ������
        raise Exception("�ڽ����㷨Step1�У�ȡ�õ�C1������Բ������")
    x1, y1 = C1[0], C1[1]
    x1_hex, y1_hex = fielde_to_hex(x1), fielde_to_hex(y1)
    print("C1�����õ�ʮ��������ʽ��ʾ�ǣ�", (x1_hex, y1_hex))
    print("\nStep2��������Բ���ߵ�S=hC1����S������Զ�㣬�򱨴��˳���")
    S = mult_point(C1, h, p, a)
    print("����õ���S�ǣ�", S)
    if S == 0:
        raise Exception("�ڽ����㷨Step2�У�S������Զ��")
    xS, yS = S[0], S[1]
    xS_hex, yS_hex = fielde_to_hex(xS), fielde_to_hex(yS)
    print("S��������ʮ�����ƴ���ʽ��ʾ�ǣ�", (xS_hex, yS_hex))
    print("\nStep3������dC1=(x2,y2)��������x2��y2����������ת��Ϊ���ش���")
    temp = mult_point(C1, dB, p, a)
    x2, y2 = temp[0], temp[1]
    x2_hex, y2_hex = fielde_to_hex(x2), fielde_to_hex(y2)
    print("���ܵõ���dC1=(x2,y2)��ʮ�����ƴ���ʽ�ǣ�", (x2_hex, y2_hex))
    print("\nStep4:����t=KDF(x2 �� y2, klen)����tΪȫ0���ش����򱨴��˳���")
    hex_l3 = 64           # hex_l3�����ĵ�������C3��ʮ�����ƴ��ĳ��ȡ�C3��ͨ��SM3�õ���hashֵ����64λʮ�����ƴ���
    hex_l2 = len(C) - hex_l1 - hex_l3           # hex_l2�����ĵڶ�����C2��ʮ�����ƴ��ĳ��ȡ�
    klen = hex_l2 * 4           # klen������C2�б��ش��ĳ���
    print("�����C2�ı��ش�����klen�ǣ�", klen)
    x2_bits, y2_bits = hex_to_bits(x2_hex), hex_to_bits(y2_hex)
    t = KDF(x2_bits + y2_bits, klen)
    print("�����t=KDF(x2 �� y2, klen)�ǣ�", t)
    if eval('0b' + t) == 0:
        raise Exception("�ڽ����㷨Step4�У��õ���t��ȫ0��")
    t_hex = bits_to_hex(t)
    print("t��ʮ�����ƴ���ʽ�ǣ�", t_hex)
    print("\nStep5����C��ȡ�����ش�C2������M�� = C2 �� t��")
    C2_hex = C[hex_l1: -hex_l3]
    print("C2��ʮ�����ƴ���ʽ�ǣ�", C2_hex)
    M1 = eval('0x' + C2_hex + '^' + '0x' + t_hex)           # M1��M'��M�� = C2 �� t
    M1_hex = hex(M1)[2:].rjust(hex_l2, '0')         # ע��λ��Ҫһ��
    print("�����M�� = C2 �� t�ǣ�", M1_hex)
    print("\nStep6������u = Hash(x2 �� M�� �� y2)����C��ȡ�����ش�C3����u != C3���򱨴��˳���")
    M1_bits = hex_to_bits(M1_hex)
    cmp_bits = x2_bits + M1_bits + y2_bits          # cmp_bits�洢���ڼ����ϣֵ�ԶԱ�C3�Ķ����ƴ�
    cmp_bytes = bits_to_bytes(cmp_bits)
    cmp_list = [i for i in cmp_bytes]
    u = sm3.sm3_hash(cmp_list)          # u�д洢
    print("�����u = Hash(x2 �� M�� �� y2)�ǣ�", u)
    C3_hex = C[-hex_l3:]
    print("��C��ȡ����C3��ʮ��������ʽ�ǣ�", C3_hex)
    if u != C3_hex:
        raise Exception("�ڽ����㷨Step6�У������u��C3��ͬ")
    print("\nStep7���������M��")
    M_bytes = hex_to_bytes(M1_hex)
    M = str(M_bytes, encoding='ascii')
    print("���ܳ��������ǣ�", M)
    return M


# ��Բ����ϵͳ����args(p, a, b, h, G, n)�Ļ�ȡ��
def get_args():
    p = eval('0x' + '8542D69E 4C044F18 E8B92435 BF6FF7DE 45728391 5C45517D 722EDB8B 08F1DFC3'.replace(' ', ''))
    a = eval('0x' + '787968B4 FA32C3FD 2417842E 73BBFEFF 2F3C848B 6831D7E0 EC65228B 3937E498'.replace(' ', ''))
    b = eval('0x' + '63E4C6D3 B23B0C84 9CF84241 484BFE48 F61D59A5 B16BA06E 6E12D1DA 27C5249A'.replace(' ', ''))
    h = 1
    xG = eval('0x' + '421DEBD6 1B62EAB6 746434EB C3CC315E 32220B3B ADD50BDC 4C4E6C14 7FEDD43D'.replace(' ', ''))
    yG = eval('0x' + '0680512B CBB42C07 D47349D2 153B70C4 E5D7FDFC BFA36EA1 A85841B9 E46E09A2'.replace(' ', ''))
    G = (xG, yG)            # G �ǻ���
    n = eval('0x' + '8542D69E 4C044F18 E8B92435 BF6FF7DD 29772063 0485628D 5AE74EE7 C32E79B7'.replace(' ', ''))
    args = (p, a, b, h, G, n)           # args�Ǵ洢��Բ���߲�����Ԫ�顣
    return args


# ��Կ��ȡ������������Ҫ����Ϣ���շ�B�Ĺ�˽Կ�Ļ�ȡ��
def get_key():
    xB = eval('0x' + '435B39CC A8F3B508 C1488AFC 67BE491A 0F7BA07E 581A0E48 49A5CF70 628A7E0A'.replace(' ', ''))
    yB = eval('0x' + '75DDBA78 F15FEECB 4C7895E2 C1CDF5FE 01DEBB2C DBADF453 99CCF77B BA076A42'.replace(' ', ''))
    PB = (xB, yB)           # PB��B�Ĺ�Կ
    dB = eval('0x' + '1649AB77 A00637BD 5E2EFE28 3FBF3535 34AA7F7C B89463F2 08DDBC29 20BB0DA0'.replace(' ', ''))
    # dB��B��˽Կ
    key_B = (PB, dB)
    return key_B


print("SM2��Բ���߹�Կ�����㷨".center(100, '='))
print("���㷨����256λ�������ϵ���Բ���ߡ���Բ���߷���Ϊ��")
print("y^2 = x^3 + ax + b")

print("��Ϊ�㷨��1���֣���ȡ�������".center(100, '='))
# ������Ϊ�����ӽ����㷨��������Ԫ��args��key_B��ascii�ַ���������ϢM����Ϊ���ɱ����С�����һ�����������ʱ����ı���ֵ
print("�����ȡ��Բ����ϵͳ����")
args = get_args()           # ��ȡ��Բ����ϵͳ����
p, a, b, h, G, n = args         # ���н��
p, a, b, h, xG, yG, n = tuple(map(lambda a: hex(a)[2:], (p, a, b, h, G[0], G[1], n)))   # ������ת��Ϊʮ�����ƴ��������
print("��Բ����ϵͳ���������p�ǣ�", p)
print("��Բ����ϵͳ�Ĳ���a�ǣ�", a)
print("��Բ����ϵͳ�Ĳ���b�ǣ�", b)
print("��Բ����ϵͳ��������h�ǣ�", h)
print("��Բ����ϵͳ�Ļ���G�ĺ�����xG�ǣ�", xG)
print("��Բ����ϵͳ�Ļ���G��������yG�ǣ�", yG)

print("�����ȡ���շ�B�Ĺ�˽Կ")
key_B = get_key()           # ������Ϣ���շ��Ĺ�˽Կ
PB, dB = key_B          # ���н����PB�ǹ�Կ������Ԫ����ʽ�洢�ĵ�(xB, yB), dB��˽Կ��������
xB, yB, dB = tuple(map(lambda a: hex(a)[2:], (PB[0], PB[1], dB)))
print("���շ�B�Ĺ�ԿPB�ĺ�����xB�ǣ�", xB)
print("���շ�B�Ĺ�ԿPB��������yB�ǣ�", yB)
print("���շ�B��˽ԿdB�ǣ�", dB)
print("�����ȡ����")
M = input('������Ҫ���ܵ�����(����ӦΪascii�ַ���ɵ��ַ���)��')
print("��ȡ��ascii�ַ��������ǣ�", M)
print("��Ϊ�㷨��2���֣����ܲ���".center(100, '='))
C = encry_sm2(args, key_B[0], M)            # �����㷨�Ĳ�������Բϵͳ������B�Ĺ�ԿPB��ascii�ַ�����ʽ��������ϢM������ʮ�����ƴ���ʽ��������Ϣ

print("��Ϊ�㷨��3���֣����ܲ���".center(100, '='))
de_M = decry_sm2(args, key_B[1], C)           # �����㷨�Ĳ�������Բ����ϵͳ������B��˽ԿdB��ʮ�����ƴ���ʽ��������Ϣ������ascii�ַ�����ʽ��������ϢM

print("��Ϊ�㷨��4���֣���֤����".center(100, '='))
print("ԭʼ�����ǣ�", M)
print("���ܵõ��������ǣ�", de_M)
if M == de_M:
    print("��ϲ�������ܳɹ���")
else:
    print("����ʧ�ܣ������㷨��")
