import md5_utils

if 'name' == '__main__':
    input_message0 = input("Please enter the string you want to encrypt:")
    input_message1 = input_message0.encode()
    result0 = md5_utils.md5_encode_onestep(input_message0)
    result1 = md5_utils.md5_encode(input_message1)
    print("MD5_onestep(%s) = %s" %(input_message0, result0))
    print("MD5_self(%s) = %s" %(input_message1, result1))
    print("Verification: %d" %(result0 == result1))
    # 验证位数
    # print("width = %d and %d" %(len(result0),len(result1)))