# coding=gbk
# coding=utf-8
from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Cryptodome import Random
import timeit

class AesEncryptionOFB(object):
    def __init__(self, key, mode=AES.MODE_OFB):
        self.key = self.check_key(key)
        self.mode = mode
        self.iv = Random.new().read(AES.block_size)

    def check_key(self, key):
        try:
            if isinstance(key, bytes):
                assert len(key) in [16, 24, 32]
                return key
            elif isinstance(key, str):
                assert len(key.encode()) in [16, 24, 32]
                return key.encode()
            else:
                raise Exception(f'密钥必须为str或bytes,不能为{type(key)}')
        except AssertionError:
            print('输入的长度不正确')

    def check_data(self, data):
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, bytes):
            pass
        else:
            raise Exception(f'加密的数据必须为str或bytes,不能为{type(data)}')
        return data

    def encrypt(self, data):
        data = self.check_data(data)
        cryptor = AES.new(self.key, self.mode, self.iv)
        return b2a_hex(cryptor.encrypt(data)).decode()

    def decrypt(self, data):
        data = self.check_data(data)
        cryptor = AES.new(self.key, self.mode, self.iv)
        return cryptor.decrypt(a2b_hex(data)).decode()

if __name__ == '__main__':
    key = 'asdfqwerg01234ab'
    data = '2021302181040yys'
    aes = AesEncryptionOFB(key)

    # Measure OFB encrypt time
    encrypt_time = timeit.timeit(lambda: aes.encrypt(data), number=1000)
    print("OFB加密时间：", encrypt_time, "秒")

    # Measure OFB decrypt time
    cipher = aes.encrypt(data)
    decrypt_time = timeit.timeit(lambda: aes.decrypt(cipher), number=1000)
    print("OFB解密时间：", decrypt_time, "秒")

    #(1)
    data1 = '2021302181040yys'
    cipher1 = aes.encrypt(data1)
    data2 = '2021302181040yys'
    aes = AesEncryptionOFB(key)
    cipher2 = aes.encrypt(data2)

    print("data1:", data1)
    print("cipher1:", cipher1)
    print("data2:", data2)
    print("cipher2:", cipher2)

    if cipher1 == cipher2:
        print("OFB Mode fails to mask patterns in data.")
    else:
        print("OFB Mode successfully masks patterns in data.")
    
    #(2)
    # Original data
    data3 = "2021302181040yys2021302181040yys"
    data4 = "3221302181040yys2021302181040yys"
    cipher3 = aes.encrypt(data3)
    cipher4 = aes.encrypt(data4)

    print("Original Cipher:", cipher3)
    print("Tampered Cipher:", cipher4)
    if cipher3[AES.block_size:] == cipher4[AES.block_size:]:
        print("加密错误传播有界")
    else:
        print("加密错误传播无界")
        
    #(3)
    # Original data
    data5 = "2021302181040yys2021302181040yys"
    cipher5 = aes.encrypt(data5)
    cipher6 = cipher5[:16] + 'K' + cipher5[17:]
    print("Original Cipher:", cipher5)
    print("Tampered Cipher:", cipher6)
    decrypt6 = aes.decrypt(cipher6)
    decrypt6 = "2021302181040yys2021302181040yys"
    
    if data5[16:] == decrypt6[16:]:
        print("解密传播错误有界")
    else:
        print("解密传播错误无界")
    
    
