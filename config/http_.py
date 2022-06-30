
# todo  a == 0 测试    1 预生产   2 生产

a = 0

if a == 0:
    http_login = 'http://163.177.128.179:63201'
    http_case = 'http://163.177.128.179:63095'
    agent_phone = 17051202834
    supplier_phone = 18216482019
    purchaser_phone = 18474793371
    start_url = 'http://926-web-test.926.net.cn/#/'  # 测试
    # start_url = 'http://10.10.1.62:3002/#/'  # 测试

elif a == 1:
    http_login = 'http://120.79.223.2:2001'
    http_case = 'http://120.79.223.2:8097'
    # agent_phone = 18772606900
    # supplier_phone = 18216482018
    # purchaser_phone = 18474793370
    start_url = 'http://pre-web.926.net.cn/'  # 预生产
    # http_login = 'http://yqst.926.net.cn'
    # http_case = 'http://api.926.net.cn'
    agent_phone = 18373847538
    supplier_phone = 15183834489
    purchaser_phone = 18390552449

elif a == 2:
    http_login = 'http://yqst.926.net.cn'
    http_case = 'http://api.926.net.cn'
    agent_phone = 18373847538
    supplier_phone = 15183834489
    purchaser_phone = 18390552449
    start_url = "http://web.926.net.cn"  # 生产