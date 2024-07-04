# coding=gbk
# coding=utf-8
import base64
import os
from Cryptodome.Cipher import AES
import timeit
def generate_random_iv():
    """
    ��������ĳ�ʼ������ (IV)
    """
    return os.urandom(AES.block_size)

def pkcs7padding(text):
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    
    padding_text = chr(padding) * padding
    return text + padding_text


def pkcs7unpadding(text):
    try:
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]
    except Exception as e:
        pass


def aes_encode(key, content):
    key_bytes = bytes(key, encoding='utf-8')
    iv = generate_random_iv()  # ʹ��������ɵ� IV
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    content_padding = pkcs7padding(content)
    aes_encode_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    result = str(base64.b64encode(iv + aes_encode_bytes), encoding='utf-8')
    return result

def aes_decode(key, content):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        content_bytes = base64.b64decode(content)
        iv = content_bytes[:AES.block_size]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        aes_decode_bytes = cipher.decrypt(content_bytes[AES.block_size:])
        result = str(aes_decode_bytes, encoding='utf-8')
        result = pkcs7unpadding(result)
    except Exception as e:
        result = ""
    return result


if __name__ == '__main__':
    key = 'asdfqwerg01234ab'
    # ��Ӣ�ļ���
    data = '2021302181040yys'
    #(5)
    # ����CBC����ʱ��
    encrypt_time = timeit.timeit(lambda: aes_encode(key,data), number=1000)
    print("CBC����ʱ�䣺", encrypt_time, "��")

    # ����CBC����ʱ��
    cipher = aes_encode(key,data)
    decrypt_time = timeit.timeit(lambda: aes_decode(key,cipher), number=1000)
    print("CBC����ʱ�䣺", decrypt_time, "��")
    
    #(1)
    data1 = '2021302181040yys'
    data2 = '2021302181040yys'

    cipher1 = aes_encode(key, data1)
    cipher2 = aes_encode(key, data2)
    decrpyted1 = aes_decode(key,cipher1)
    decrpyted2 = aes_decode(key,cipher2)
    
    print("data1:", data1)
    print("cipher1:", cipher1)
    print("decrpyted1:", decrpyted1)
    print("data2:", data2)
    print("cipher2:", cipher2)
    print("decrpyted2:", decrpyted2)

    if cipher1 == cipher2:
        print("CBC Mode fails to mask patterns in data.")
    else:
        print("CBC Mode successfully masks patterns in data.")
        
    #(2)
    data3 = '2021302181040yys2021302181040yys'
    data4 = 'X021302181040yys2021302181040yys'  # �۸� data2 �е�ĳ���ֿ�
    
    cipher3 = aes_encode(key, data3)
    cipher4 = aes_encode(key, data4)
    decrpyted3 = aes_decode(key,cipher3)
    decrpyted4 = aes_decode(key,cipher4)
    print("data3:", data3)
    print("cipher3:", cipher3)
    #print("decrpyted3:", decrpyted3)
    print("data4:", data4)
    print("cipher4:", cipher4)
    #print("decrpyted4:", decrpyted4)
    
    
    if cipher3[AES.block_size:] == cipher4[AES.block_size:]:
        print("���ܴ��󴫲��н�")
    else:
        print("���ܴ��󴫲��޽�")
        
    #(3)
    # �۸�����
    data5 = '2021302181040yys2021302181040yys'
    cipher5 = aes_encode(key,data5)
    cipher6 = cipher5[:16] + 'K' + cipher5[17:]
    print("Original Cipher:", cipher5)
    print("Tampered Cipher:", cipher6)
    # ����
    decrypted5 = aes_decode(key,cipher5)
    decrypted6 = aes_decode(key,cipher6)
    print("Original Decrypted Text:", decrypted5)
    print("Tampered Decrypted Text:", decrypted6)

    if decrypted5[16:] == decrypted6[16:]:
            print("���ܴ��󴫲��н�")
    else:
        print("���ܴ��󴫲��޽�")

    
