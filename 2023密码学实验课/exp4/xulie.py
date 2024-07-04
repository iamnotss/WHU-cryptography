# coding=gbk
# coding=utf-8
import random
import hashlib

def keystream_generator(seed_key, length):
    # ʹ��������Կ��ʼ��α�����������
    random.seed(seed_key)

    # ����ָ�����ȵ���Կ��
    keystream = []
    for _ in range(length):
        # ����һ��α������أ�0��1��
        bit = random.randint(0, 1)

        # ��α���������ӵ���Կ���б���
        keystream.append(bit)

    return keystream

def generate_seed_key(seed):
    # ʹ�ù�ϣ��������������Կ
    seed_key = hashlib.sha256(seed.encode()).digest()
    return seed_key

def text_to_binary(text):
    # ���ı�ת��Ϊ�����Ʊ�ʾ
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_text(binary):
    # �������Ʊ�ʾת��Ϊ�ı�
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

# ����ʾ��
seed = "1040"  # ������Ϊ������Կ������
plaintext = "2021302181040yys"  # ������

# ������ת��Ϊ�����Ʊ�ʾ
plaintext_binary = text_to_binary(plaintext)

# ����������Կ
seed_key = generate_seed_key(seed)

# ������Կ��
keystream = keystream_generator(seed_key, len(plaintext_binary))

# �����������м���
ciphertext = [int(plain_bit) ^ int(key_bit) for plain_bit, key_bit in zip(plaintext_binary, keystream)]

# ��������ת��Ϊ�����Ʊ�ʾ
ciphertext_binary = ''.join(str(bit) for bit in ciphertext)

# ���ܲ���
# ����������ͬ����Կ��
decryption_keystream = keystream_generator(seed_key, len(ciphertext))
decrypted_text = [cipher_bit ^ key_bit for cipher_bit, key_bit in zip(ciphertext, decryption_keystream)]

# �����ܺ�Ķ�������ת��Ϊ�ı�
decrypted_text = binary_to_text(''.join(str(bit) for bit in decrypted_text))

print("��������", plaintext)
print("�������������Ʊ�ʾ����", plaintext_binary)
print("��Կ���������Ʊ�ʾ����", ''.join(str(bit) for bit in keystream))
print("�������������Ʊ�ʾ����", ciphertext_binary)
print("���ܺ����������", decrypted_text)