# coding=gbk
# coding=utf-8
N = 40

def a_n(s_N, a, b):
    s = sum(a_i * b_i for a_i, b_i in zip(a, b))
    return s % 2

def print_array(arr):
    print(''.join(map(str, arr)))

def print_poly(poly):
    print('f =', end=' ')
    terms = []
    for i, coef in enumerate(poly[::-1]):
        if coef == 1:
            if i == 0:
                terms.append('1')
            else:
                terms.append(f'x^{i}')
    print(' + '.join(terms))

def print_cycle(state, t):
    print('��������Ϊ��', end='')
    print_array(state[:t])

def print_state(state, n, num, s_N):
    print(f'״̬{num}:  ', end='')
    for i in range(s_N):
        print(f'S{i}:{state[num + i]}  ', end='')
    print(f'----->����f={state[n]}')

def lfsr(state, g_poly, s, s_N):
    feedback_bits = []
    # ��ʼ��״̬�Ĵ�������ǰ s_N λ����Ϊ�������� s ��ֵ
    for i in range(s_N):
        state[i] = s[i]

    feedback_bits.append(state[s_N-1])
    # �� s_N ��ʼ������ִ�� LFSR ����
    for n in range(s_N, N):
        # ȡ����ǰλ��ǰ s_N ��λ�õ�״̬��Ϊ����
        temp = state[n - s_N:n]
        # ������һλ��״̬��ʹ�� a_n �������ú���ʵ������ g_poly ��������
        state[n] = a_n(s_N, temp, g_poly)
        # ��ӡ��ǰ״̬�Լ�����λ
        print_state(state, n, n - s_N, s_N)
        feedback_bits.append(state[n])
    
    return feedback_bits

def judge(s_N, a, b):
    return all(a_i == b_i for a_i, b_i in zip(a, b))

def T(array, s_N):
    t = 0
    goal_array = array[:s_N]
    flag = False

    for i in range(N - s_N):
        if flag:
            break

        # �ӵ� i ��λ�ÿ�ʼ�� s_N ����λΪһ���������
        for k in range(s_N):
            goal_array[k] = array[i + k]

        for j in range(i + 1, N - s_N - 1):
            # �ӵ� i+1 ��λ�ÿ�ʼ�� s_N ����λΪһ���������
            temp = [array[j + l] for l in range(s_N)]
            flag = judge(s_N, temp, goal_array)
            if flag:
                t = j
                break

    return t



def exp1():
    s_N = 4
    state = [0] * N
    array = [0] * N
    s = [0, 0, 0, 1]
    g_poly = [1, 0, 0, 1, 1]

    print('����ʽa_poly: ', end='')
    print_array(g_poly)
    print('����ʽa_poly: ', end='')
    print_poly(g_poly)

    print('�����s(Ҳ���ǳ�ʼ״̬): ', end='')
    print_array(s)
    # �� g_poly �� S_N λ����
    g_poly= g_poly[:-s_N-1:-1]
    array = lfsr(state, g_poly, s, s_N)

    print('�������: ', end='')
    print_array(array)
    
    t = T(array, s_N)
    
    print(f'����: {t}')
    print_cycle(array, t)

    print()

def exp2():
    s_N = 4
    state = [0] * N
    array = [0] * N
    s = [0, 0, 0, 1]
    g_poly = [1, 1, 0, 0, 1]

    print('����ʽa_poly: ', end='')
    print_array(g_poly)
    print('����ʽa_poly: ', end='')
    print_poly(g_poly)

    print('�����s(Ҳ���ǳ�ʼ״̬): ', end='')
    print_array(s)
    # �� g_poly �� S_N λ����
    g_poly= g_poly[:-s_N-1:-1]
    array = lfsr(state, g_poly, s, s_N)

    print('�������: ', end='')
    print_array(array)

    t = T(array, s_N)
    
    print(f'����: {t}')
    print_cycle(array, t)

    print()

if __name__ == "__main__":
    exp1()
    exp2()
