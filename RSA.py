import random

# 转换为十进制编码
trans1 = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, ' 9': 9,
          'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19,
          'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29,
          'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35, 'A': 36, 'B': 37, 'C': 38, 'D': 39,
          'E': 40, 'F': 41, 'G': 42, 'H': 43, 'I': 44, 'J': 45, 'K': 46, 'L': 47, 'M': 48, 'N': 49,
          'O': 50, 'P': 51, 'Q': 52, 'R': 53, 'S': 54, 'T': 55, 'U': 56, 'V': 57, 'W': 58, 'X': 59,
          'Y': 60, 'Z': 61}
# 从十进制编码转换回字符
trans2 = {k: v for v, k in trans1.items()}


# 平方乘算法求模 a^b mod p
def repeatMod(a, b, p):
    y = 1
    while b:
        if b & 1:
            y = (y * a) % p
        a = (a * a) % p
        b = b >> 1
    return y


# 对 n 进行 cnt 轮素性测试
def Miller_Rabin(n, cnt):
    t = n - 1
    k = 0
    # 把 n-1 写成 2^k * t 其中t为奇数
    while (t & 0x1) == 0 and t:
        t = t >> 1
        k = k + 1
    while cnt:
        a = random.randint(1, n - 1)
        b = repeatMod(a, t, n)
        if b == 1 or b == n-1:
            return True
        for i in range(k):
            b = repeatMod(b, 2, n)
            if b == 1 or b == n-1:
                return True
        cnt = cnt - 1
    return False


# 生成大素数
def Build_BigPrime():
    flag = False
    while 1:
        big_num = random.randint(2**127, 2**128)  # 生成素数为 128 位
        if big_num % 2 != 0:
            flag = Miller_Rabin(big_num, 10)
        if flag:
            return big_num


# 求b模a的乘法逆y，即，by=1(mod a)
def mod_reverse(a, b):
    if b == 0:
        return 1, 0
    else:
        k = a // b
        x1, y1 = mod_reverse(b, a % b)
        x, y = y1, (x1 - k * y1)
    return x, y


def encrypt(P, key, N):
    i = 0
    p_code = []  # 每个元素是4位十进制编码，即2个字母
    C_blk = []   # 每个元素是一组密文
    # 明文转换为十进制编码
    for ch in P:
        # 只读取数字和字母
        if 48 <= ord(ch) <= 57 or 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122:
            i = i + 1
            if i % 2 != 0:
                code = trans1[ch]  # 第一个字符编码
            else:
                code = code * 100 + trans1[ch]  # 两个字符形成一组四位编码
                p_code.append(code)
    # 最后一个分组不足4位 补充一个62
    if i % 2 != 0:
        code = code * 100 + 62
        p_code.append(code)
    # 依次对每个分组进行加密
    for blk in p_code:
        c = repeatMod(blk, key, N)
        C_blk.append(c)
    return C_blk


def decrypt(C_blk, key, N):
    p_code = []  # 每个元素是一组解密得到的明文编码
    p_ch = []  # 每个元素是明文的一个字符
    # 解密
    for blk in C_blk:
        p = repeatMod(blk, key, N)
        p_code.append(p)
    # 对每一组明文编码，转换为明文字符
    for each in p_code:
        code1 = each // 100
        code2 = each - code1 * 100
        ch1 = trans2[code1]
        p_ch.append(ch1)
        if code2 != 62:
            ch2 = trans2[code2]
            p_ch.append(ch2)
    return p_ch


if __name__ == "__main__":
    p = Build_BigPrime()
    q = Build_BigPrime()
    N = p * q
    Euler_N = (p - 1) * (q - 1)
    e = 10722  # 学号后五位 10722 可用于异常测试，加解密算法选择最近的素数 10723
    print('p = ', p)
    print('q = ', q)
    print('N = ', N)
    print('Euler_N = ', Euler_N)
    print('e = ', e)
    d0, d = mod_reverse(Euler_N, e)
    if d < 0:
        d = d + Euler_N
    print('d = ', d)
    print('e*d % Euler_N = ', e*d % Euler_N)

    Plain_Text = "2002 A.M. TURING AWARD. RSA, an acronym for Rivest, Shamir and Adleman, uses algorithmic number " \
        "theory to provide an efficient realization of a public-key cryptosystem, a concept first envisioned " \
        "theoretically by Whitfield Diffie, Martin Hellman and Ralph Merkle. RSA is now the most widely used " \
        "encryption method, with applications throughout the Internet to secure on-line transactions. It has " \
        "also inspired breakthrough work in both theoretical computer science and mathematics."

    print('-----------------------------')
    print('公钥(e,N)加密的密文为')
    C_blk = encrypt(Plain_Text, e, N)
    for each in C_blk:
        print(each, end='')

    print('\n-----------------------------')
    print('私钥(d,N)解密的明文为')
    decrypt_plain_ch = decrypt(C_blk, d, N)
    for each in decrypt_plain_ch:
        print(each, end='')

    print('\n-----------------------------')
    print('私钥(d,N)加密的密文为')
    C_blk = encrypt(Plain_Text, d, N)
    for each in C_blk:
        print(each, end='')

    print('\n-----------------------------')
    print('公钥(e,N)解密的明文为')
    decrypt_plain_ch = decrypt(C_blk, e, N)
    for each in decrypt_plain_ch:
        print(each, end='')


