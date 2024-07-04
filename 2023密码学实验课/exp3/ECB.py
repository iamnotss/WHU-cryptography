# coding=gbk
# coding=utf-8


import base64
from Cryptodome.Cipher import AES
import timeit
def aes_decode(data, key):
    try:
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    except Exception as e:
        decrypted_text = "解密失败"
    return decrypted_text

# 加密
def aes_encode(data, key):
    while len(data) % 16 != 0:  # 补足字符串长度为16的倍数
        data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
        data = str.encode(data)
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
    return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # 加密


if __name__ == '__main__':
    # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
    key = 'asdfghivjklwrtay' 
    # 待加密文本
    
    data = "AAAABBBBCCCCDDDDEEEEFFFFGGG" 
    #(5)
    # 使用 timeit 测量加密时间
    encrypt_time = timeit.timeit(lambda: aes_encode(data, key), number=1)
    print("加密时间：", encrypt_time, "秒")

    # 使用 timeit 测量解密时间
    cipher = aes_encode(data, key)
    decrypt_time = timeit.timeit(lambda: aes_decode(cipher, key), number=1)
    print("解密时间：", decrypt_time, "秒")
    
    #(1)
    data1 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"
    data2 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"

    # 加密
    cipher1 = aes_encode(data1, key)
    cipher2 = aes_encode(data2, key)

    # 判断是否满足Ci = Cj
    if cipher1 == cipher2:
        print("加密结果相同，对应相同的明文。")
    else:
        print("加密结果不同，对应不同的明文。")
    
    #(2)
    data3 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"
    data4 = "AAAABBBBCCCCDDDHEEEEFFFFGGG"

    # 加密原始明文和篡改后的明文
    cipher3 = aes_encode(data3, key)
    cipher4 = aes_encode(data4, key)

    # 输出结果
    print("原始密文：", cipher3)
    print("篡改后密文：", cipher4)

    # 解密原始密文和篡改后的密文
    decrypted3 = aes_decode(cipher3, key)
    decrypted4 = aes_decode(cipher4, key)

    # 输出解密结果
    print("原始解密结果：", decrypted3)
    print("篡改后解密结果：", decrypted4)
    if decrypted3[16:] == decrypted4[16:]:
            print("加密错误传播有界")
    else:
        print("加密错误传播无界")
    #(3)
    # 篡改密文
    data5 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"
    cipher5 = aes_encode(data5, key)
    print("原始密文：", cipher5)

    cipher6 = cipher5[:16] + 'b' + cipher5[17:]
    print("修改后的密文：", cipher6)
    

    # 解密
    decrypted5 = aes_decode(cipher5, key)
    decrypted6 = aes_decode(cipher6, key)
    if decrypted5[16:] == decrypted6[16:]:
            print("解密错误传播有界")
    else:
        print("解密错误传播无界")

    
    

