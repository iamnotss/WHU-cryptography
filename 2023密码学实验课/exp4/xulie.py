# coding=gbk
# coding=utf-8
import random
import hashlib

def keystream_generator(seed_key, length):
    # 使用种子密钥初始化伪随机数生成器
    random.seed(seed_key)

    # 生成指定长度的密钥流
    keystream = []
    for _ in range(length):
        # 生成一个伪随机比特（0或1）
        bit = random.randint(0, 1)

        # 将伪随机比特添加到密钥流列表中
        keystream.append(bit)

    return keystream

def generate_seed_key(seed):
    # 使用哈希函数生成种子密钥
    seed_key = hashlib.sha256(seed.encode()).digest()
    return seed_key

def text_to_binary(text):
    # 将文本转换为二进制表示
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_text(binary):
    # 将二进制表示转换为文本
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

# 测试示例
seed = "1040"  # 密码作为种子密钥的输入
plaintext = "2021302181040yys"  # 明文流

# 将明文转换为二进制表示
plaintext_binary = text_to_binary(plaintext)

# 生成种子密钥
seed_key = generate_seed_key(seed)

# 生成密钥流
keystream = keystream_generator(seed_key, len(plaintext_binary))

# 对明文流进行加密
ciphertext = [int(plain_bit) ^ int(key_bit) for plain_bit, key_bit in zip(plaintext_binary, keystream)]

# 将密文流转换为二进制表示
ciphertext_binary = ''.join(str(bit) for bit in ciphertext)

# 解密步骤
# 重新生成相同的密钥流
decryption_keystream = keystream_generator(seed_key, len(ciphertext))
decrypted_text = [cipher_bit ^ key_bit for cipher_bit, key_bit in zip(ciphertext, decryption_keystream)]

# 将解密后的二进制流转换为文本
decrypted_text = binary_to_text(''.join(str(bit) for bit in decrypted_text))

print("明文流：", plaintext)
print("明文流（二进制表示）：", plaintext_binary)
print("密钥流（二进制表示）：", ''.join(str(bit) for bit in keystream))
print("密文流（二进制表示）：", ciphertext_binary)
print("解密后的明文流：", decrypted_text)