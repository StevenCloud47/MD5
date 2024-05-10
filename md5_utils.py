import hashlib
import struct
import math

# md5 in one step
def md5_encode_onestep(message): 
    """
    调库一步完成对输入的消息进行MD5编码
    :param message: 输入的消息
    :return: MD5编码后的字符串
    """
    # 创建一个md5对象
    md5 = hashlib.md5()
    # 使用md5对象进行编码，参数必须是byte类型，所以需要对str类型的message进行编码
    md5.update(message.encode('utf-8'))
    # 返回一个MD5编码后的字符串
    return md5.hexdigest()

# md5 self
def left_rotate(x, amount):
    x = x & 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

def F(x,y,z):
    return ((x & y) | (~x & z))

def G(x,y,z):
    return ((x & z) | (y & ~z))

def H(x,y,z):
    return (x ^ y ^ z)

def I(x,y,z):
    return (y ^ (x | ~z))

def j_index(i):
    if 0 <= i <= 15:
        j = i
    elif 16 <= i <= 31:
        j = (5 * i + 1) % 16
    elif 32 <= i <= 47:
        j = (3 * i + 5) % 16
    elif 48 <= i <= 63:
        j = (7 * i) % 16
    return j

def FGHI(x,y,z,i):
    if 0 <= i <= 15:
        X = F(x,y,z)
    elif 16 <= i <= 31:
        X = G(x,y,z)
    elif 32 <= i <= 47:
        X = H(x,y,z)
    elif 48 <= i <= 63:
        X = I(x,y,z)
    return X

def FFGGHHII(a,b,c,d,K,w,s,i):
    j = j_index(i)
    # print(hex(K[i]))
    if i % 2 == 0:
        a = (a + FGHI(b,c,d,i) + K[i] + w[j]) & 0xFFFFFFFF
        a = left_rotate(a, s[i])
        a = (a + b) & 0xFFFFFFFF    
    else:
        c = (c + FGHI(d,a,b,i) + K[i] + w[j]) & 0xFFFFFFFF
        c = left_rotate(c, s[i])
        c = (c + d) & 0xFFFFFFFF   
    return b,c,d,a

def md5_encode(message):
    # 初始化MD5的四个缓冲区变量，它们是32位的寄存器，用于存储中间和最终的散列值
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # 按照RFC 1321的标准，定义四轮中使用的64个操作的K常量
    K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
    # K = [int(abs(math.sin(i + 1)) * 2**32) for i in range(64)]

    # 初始化四轮中的移位量
    s = ([7, 12, 17, 22] * 4 +
         [5,  9, 14, 20] * 4 +
         [4, 11, 16, 23] * 4 +
         [6, 10, 15, 21] * 4)

    # 对消息进行预处理：填充 + 添加长度值
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message += b'\x80'
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)

    # print(len(message))
    message += struct.pack('<Q', original_bit_len)

    # 处理消息的每个512位块
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        # print(block)
        w = list(struct.unpack('<' + 'I' * 16, block))
        #print(w)
        a, b, c, d = A, B, C, D
        # 主循环
        for n in range(64):
            # print("%s,%s,%s,%s"%(hex(a),hex(b),hex(c),hex(d)))
            a,b,c,d = FFGGHHII(a,b,c,d,K,w,s,n)

        # 添加本块的计算结果到全局结果中
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # 将最终的结果转化为字节序列
    digest = struct.pack('<IIII', A, B, C, D)
    return ''.join(f'{i:02x}' for i in digest)

