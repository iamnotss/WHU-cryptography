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
    print('周期序列为：', end='')
    print_array(state[:t])

def print_state(state, n, num, s_N):
    print(f'状态{num}:  ', end='')
    for i in range(s_N):
        print(f'S{i}:{state[num + i]}  ', end='')
    print(f'----->反馈f={state[n]}')

def lfsr(state, g_poly, s, s_N):
    feedback_bits = []
    # 初始化状态寄存器，将前 s_N 位设置为输入序列 s 的值
    for i in range(s_N):
        state[i] = s[i]

    feedback_bits.append(state[s_N-1])
    # 从 s_N 开始遍历，执行 LFSR 操作
    for n in range(s_N, N):
        # 取出当前位置前 s_N 个位置的状态作为输入
        temp = state[n - s_N:n]
        # 计算下一位的状态，使用 a_n 函数，该函数实现了与 g_poly 的异或操作
        state[n] = a_n(s_N, temp, g_poly)
        # 打印当前状态以及反馈位
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

        # 从第 i 个位置开始以 s_N 个单位为一个数组遍历
        for k in range(s_N):
            goal_array[k] = array[i + k]

        for j in range(i + 1, N - s_N - 1):
            # 从第 i+1 个位置开始以 s_N 个单位为一个数组遍历
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

    print('多项式a_poly: ', end='')
    print_array(g_poly)
    print('多项式a_poly: ', end='')
    print_poly(g_poly)

    print('输入的s(也就是初始状态): ', end='')
    print_array(s)
    # 将 g_poly 后 S_N 位逆置
    g_poly= g_poly[:-s_N-1:-1]
    array = lfsr(state, g_poly, s, s_N)

    print('输出序列: ', end='')
    print_array(array)
    
    t = T(array, s_N)
    
    print(f'周期: {t}')
    print_cycle(array, t)

    print()

def exp2():
    s_N = 4
    state = [0] * N
    array = [0] * N
    s = [0, 0, 0, 1]
    g_poly = [1, 1, 0, 0, 1]

    print('多项式a_poly: ', end='')
    print_array(g_poly)
    print('多项式a_poly: ', end='')
    print_poly(g_poly)

    print('输入的s(也就是初始状态): ', end='')
    print_array(s)
    # 将 g_poly 后 S_N 位逆置
    g_poly= g_poly[:-s_N-1:-1]
    array = lfsr(state, g_poly, s, s_N)

    print('输出序列: ', end='')
    print_array(array)

    t = T(array, s_N)
    
    print(f'周期: {t}')
    print_cycle(array, t)

    print()

if __name__ == "__main__":
    exp1()
    exp2()
