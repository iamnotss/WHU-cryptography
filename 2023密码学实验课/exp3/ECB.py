# coding=gbk
# coding=utf-8


import base64
from Cryptodome.Cipher import AES
import timeit
def aes_decode(data, key):
    try:
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # ��ʼ��������
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")  # ����
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # ȥ�����ಹλ
    except Exception as e:
        decrypted_text = "����ʧ��"
    return decrypted_text

# ����
def aes_encode(data, key):
    while len(data) % 16 != 0:  # �����ַ�������Ϊ16�ı���
        data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
        data = str.encode(data)
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # ��ʼ��������
    return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # ����


if __name__ == '__main__':
    # ��Կ���ȱ���Ϊ16��24��32λ���ֱ��ӦAES-128��AES-192��AES-256
    key = 'asdfghivjklwrtay' 
    # �������ı�
    
    data = "AAAABBBBCCCCDDDDEEEEFFFFGGG" 
    #(5)
    # ʹ�� timeit ��������ʱ��
    encrypt_time = timeit.timeit(lambda: aes_encode(data, key), number=1)
    print("����ʱ�䣺", encrypt_time, "��")

    # ʹ�� timeit ��������ʱ��
    cipher = aes_encode(data, key)
    decrypt_time = timeit.timeit(lambda: aes_decode(cipher, key), number=1)
    print("����ʱ�䣺", decrypt_time, "��")
    
    #(1)
    data1 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"
    data2 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"

    # ����
    cipher1 = aes_encode(data1, key)
    cipher2 = aes_encode(data2, key)

    # �ж��Ƿ�����Ci = Cj
    if cipher1 == cipher2:
        print("���ܽ����ͬ����Ӧ��ͬ�����ġ�")
    else:
        print("���ܽ����ͬ����Ӧ��ͬ�����ġ�")
    
    #(2)
    data3 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"
    data4 = "AAAABBBBCCCCDDDHEEEEFFFFGGG"

    # ����ԭʼ���ĺʹ۸ĺ������
    cipher3 = aes_encode(data3, key)
    cipher4 = aes_encode(data4, key)

    # ������
    print("ԭʼ���ģ�", cipher3)
    print("�۸ĺ����ģ�", cipher4)

    # ����ԭʼ���ĺʹ۸ĺ������
    decrypted3 = aes_decode(cipher3, key)
    decrypted4 = aes_decode(cipher4, key)

    # ������ܽ��
    print("ԭʼ���ܽ����", decrypted3)
    print("�۸ĺ���ܽ����", decrypted4)
    if decrypted3[16:] == decrypted4[16:]:
            print("���ܴ��󴫲��н�")
    else:
        print("���ܴ��󴫲��޽�")
    #(3)
    # �۸�����
    data5 = "AAAABBBBCCCCDDDDEEEEFFFFGGG"
    cipher5 = aes_encode(data5, key)
    print("ԭʼ���ģ�", cipher5)

    cipher6 = cipher5[:16] + 'b' + cipher5[17:]
    print("�޸ĺ�����ģ�", cipher6)
    

    # ����
    decrypted5 = aes_decode(cipher5, key)
    decrypted6 = aes_decode(cipher6, key)
    if decrypted5[16:] == decrypted6[16:]:
            print("���ܴ��󴫲��н�")
    else:
        print("���ܴ��󴫲��޽�")

    
    

