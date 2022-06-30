import hashlib


def md5Encode(str_):  #  md5编码转换
    m = hashlib.md5()
    str_ = str(str_)
    m.update(str_.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()