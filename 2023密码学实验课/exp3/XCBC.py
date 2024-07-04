# coding=gbk
# coding=utf-8
from Cryptodome.Cipher import AES
from Cryptodome.Util.strxor import strxor
import base64
import timeit
class AES_XCBC:
    def __init__(self, key1, key2):
        self.key1 = key1
        self.key2 = key2
        self.cipher = AES.new(key1, AES.MODE_ECB)

    def _encrypt_block(self, block):
        return self.cipher.encrypt(block)

    def encrypt(self, plaintext):
        if len(plaintext) % AES.block_size != 0:
            raise ValueError("Plaintext length must be a multiple of block size.")

        ciphertext = b''
        prev_ciphertext = b'\x00' * AES.block_size

        for i in range(0, len(plaintext), AES.block_size):
            block = plaintext[i:i + AES.block_size]

            if i == 0:
                tag = self._encrypt_block(strxor(self.key2, block))
            else:
                tag = self._encrypt_block(strxor(self.key2, strxor(prev_ciphertext, block)))

            ciphertext += strxor(self.key1, tag)
            prev_ciphertext = ciphertext[-AES.block_size:]

        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % AES.block_size != 0:
            raise ValueError("Ciphertext length must be a multiple of block size.")

        plaintext = b''
        prev_ciphertext = b'\x00' * AES.block_size

        for i in range(0, len(ciphertext), AES.block_size):
            block = ciphertext[i:i + AES.block_size]

            if i == 0:
                tag = self._encrypt_block(strxor(self.key2, strxor(self.key1, block)))
            else:
                tag = self._encrypt_block(strxor(self.key2, strxor(prev_ciphertext, strxor(self.key1, block))))

            plaintext += strxor(tag, self.key1)

            prev_ciphertext = block

        return plaintext

if __name__ == '__main__':
    key1 = b'key1key1key1key1'
    key2 = b'key2key2key2key2'
    aes_xcbc = AES_XCBC(key1, key2)

    plaintext = '2021302181040yys'  # Encode plaintext as a string

    # 测量XCBC加密时间
    encrypt_time = timeit.timeit(lambda: aes_xcbc.encrypt(plaintext.encode('utf-8')), number=1000)
    print("XCBC加密时间：", encrypt_time, "秒")

    ciphertext = aes_xcbc.encrypt(plaintext.encode('utf-8'))

    # 测量XCBC解密时间
    decrypt_time = timeit.timeit(lambda: aes_xcbc.decrypt(ciphertext), number=1000)
    print("XCBC解密时间：", decrypt_time, "秒")

    
    #(1)
    data1 = '2021302181040yys'
    data2 = '2021302181040yys'
    aes = AES_XCBC(key1, key2)
    cipher1 = aes.encrypt(data1.encode('utf-8'))
    aes = AES_XCBC(key1, key2)
    cipher2 = aes.encrypt(data2.encode('utf-8'))

    print("data1:", data1)
    print("cipher1:", cipher1)
    print("data2:", data2)
    print("cipher2:", cipher2)

    if cipher1 == cipher2:
        print("XCBC Mode fails to mask patterns in data.")
    else:
        print("XCBC Mode successfully masks patterns in data.")
        
    #(2)
    # Original data
    data3 = "2021302181040yys2021302181040yys"
    data4 = "3221302181040yys2021302181040yys"
    cipher3 = aes.encrypt(data3.encode('utf-8'))
    cipher4 = aes.encrypt(data4.encode('utf-8'))

    print("Original Cipher:", cipher3)
    print("Tampered Cipher:", cipher4)
    if cipher3[AES.block_size:] == cipher4[AES.block_size:]:
        print("加密错误传播有界")
    else:
        print("加密错误传播无界")
    


    #(3)
    # Original data
    data5 = "2021302181040yys2021302181040yys"
    cipher5 = aes.encrypt(data5.encode('utf-8'))
    
    cipher6 = bytearray(cipher5)
    cipher6[15] = cipher5[15] ^ 0x01  # Modify the 16th byte
    cipher6 = bytes(cipher6)
    
    cipher6 = cipher5[:16] + b'X'  + cipher5[17:]
    decrypt6 = aes.decrypt(cipher6)

    print("Original Cipher:", cipher5)
    print("Tampered Cipher:", cipher6)
    print("Decrypted Text:", decrypt6)

    if data5[16:] == decrypt6[16:]:
        print("解密传播错误有界")
    else:
        print("解密传播错误无界")
