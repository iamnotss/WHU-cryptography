# coding=gbk
# coding=utf-8
import timeit
from Cryptodome.Cipher import AES
from binascii import a2b_hex
from Cryptodome import Random
from Cryptodome.Random import get_random_bytes
import operator

# �������(bytes ^ bytes) ��λ��򣬵�����
def xor_block(left, right):
    return map(operator.xor, left, right)

# ת��Ϊbytes����
def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    
# bytesתΪʮ��������
def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')
  
class CTRCipher(object):
    def __init__(self, key):
        self._cipher = AES.new(key, AES.MODE_ECB)
        self.block_size = AES.block_size

    def encrypt(self, data, count):
        count = bytes(count)
        # ����������ֵ
        counters = self._get_timers(count, len(data))
        blocks = xor_block(self._cipher.encrypt(counters), data)
        cipher = bytes(blocks)
        return count + cipher[:len(data)]

    def decrypt(self, cipher):
        blockSZ = self.block_size
        # ���ܺͽ���ֻ�����벻ͬ
        pt = self.encrypt(cipher[blockSZ:], cipher[:blockSZ])
        return pt[blockSZ:]

    # ���ɸ�����������ֵ
    def _get_timers(self, iv, msgLen):
        # iv: ��ʱ����ֵ
        # msgLen: ���ĳ���(����)
        blockSZ = self.block_size
        blocks = int((msgLen + blockSZ - 1) // blockSZ)
        timer = int_from_bytes(iv)
        timers = iv
        for i in range(1, blocks):
            timer += 1
            timers += int_to_bytes(timer)
        return timers

if __name__ == '__main__':
    iv = Random.new().read(AES.block_size)
    ctr_key = "36f18357be4dbd77f050515c73fcf9f2"
    decryptor = CTRCipher(a2b_hex(ctr_key))
    
    data = b"2021302181040yys"
    #(5)
    # ����CTR����ʱ��
    encrypt_time = timeit.timeit(lambda: decryptor.encrypt(data, iv), number=1000)
    print("CTR����ʱ�䣺", encrypt_time, "��")
    
    # ����CTR����ʱ��
    cipher = decryptor.encrypt(data, iv)
    decrypt_time = timeit.timeit(lambda: decryptor.decrypt(cipher), number=1000)
    print("CTR����ʱ�䣺", decrypt_time, "��")
    
    #(1)
    data1 = b"2021302181040yys"
    data2 = b"2021302181040yys"
    counter1 = Random.new().read(AES.block_size)
    counter2 = Random.new().read(AES.block_size)
    cipher1 = decryptor.encrypt(data1, counter1)
    cipher2 = decryptor.encrypt(data2, counter2)

    print("data1:", data1)
    print("cipher1:", cipher1)
    print("data2:", data2)
    print("cipher2:", cipher2)

    if cipher1 == cipher2:
        print("CTR Mode fails to mask patterns in data.")
    else:
        print("CTR Mode successfully masks patterns in data.")
        
    #(2)
    # Original data
    data3 = b"2021302181040yys2021302181040yys"
    data4 = b"2021302181040mjn2021302181040yys"
    cipher3 = decryptor.encrypt(data3, iv)
    cipher4 = decryptor.encrypt(data4, iv)

    print("Original Cipher:", cipher3)
    print("Tampered Cipher:", cipher4)
    decrypt3 = decryptor.decrypt(cipher3)
    decrypt4 = decryptor.decrypt(cipher4)
    print("Original decrypted:", decrypt3)
    print("Tampered decrypted:", decrypt4)
    if decrypt3[16:] == decrypt4[16:]:
        print("���ܴ��������н�")
    else:
        print("���ܴ��������޽�")
    
    #(3)
    # Original data
    data5 = b"2021302181040yys2021302181040yys"
    cipher5 = decryptor.encrypt(data5, iv)

    cipher6 = bytearray(cipher5)
    cipher6[15] = cipher5[15] ^ 0x01  # Modify the 16th byte
    cipher6 = bytes(cipher6)
    # Tamper one block in the cipher
    cipher6 = cipher5[:16] + b'X'  + cipher5[17:]
    decrypt6 = decryptor.decrypt(cipher6)

    print("Original Cipher:", cipher5)
    print("Tampered Cipher:", cipher6)
    print("Decrypted Text:", decrypt6)

    if data5[16:] == decrypt6[16:]:
        print("���ܴ��������н�")
    else:
        print("���ܴ��������޽�")
