# utf-8

from testcase_py import login
from testcase_py.integration import file_save, Integration, Agent_Integration, Sale_Integration, Purchase_Integration
# from testcase_py import integration
# from pychartdir import *
from function import public
import importlib, copy, re, time, os, datetime,hashlib
from config import http_

def md5Encode(str_):
    m = hashlib.md5()
    str_ = str(str_)
    m.update(str_.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()

def load_module():
    name_list, import_name_list = get_testname_list()
    for i in import_name_list:
        exec("from testcase_py import " + i)
    print("load success")


def get_apiname_list():
    """
    :return file_name_list:testcase.py下的文件名列表[a.py,b.py]
    :return import_name_list:导入模块名[a,b]
    """
    # 获取测试用例接口名称
    # print(os.listdir(testcase_path))
    testcase_path = "E:\sunaw\\HDapi-auto-test\\testcase_py"
    files = os.listdir(testcase_path)
    nmodule_list = []

    for file in files:
        if not file.startswith("__"):
            name, ext = os.path.splitext(file)
            # print(name,ext)
            nmodule_list.append(name)
    return nmodule_list


def dynamic_import(module):
    return importlib.import_module(module, "testcase_py")


def get_module_list():
    # load_module()
    module_list = []
    import_name_list = get_apiname_list()
    import_name_list.remove("login")
    # import_name_list.remove("load_source")
    for i in import_name_list:
        i = dynamic_import(i)
        iname = str(i).split("'")[1]
        module_list.append((i, iname))
        # print(module_list)
    return module_list


def get_testname_list():
    """
    :return name_list:testcase.py下的文件名列表[a.py,b.py]
    :return import_name_list:导入模块名[a,b]
    """
    # 获取测试用例接口名称
    # print(os.listdir(testcase_path))
    testcase_path = "E:\sunaw\\HDapi-auto-test\\testcase_py"
    name_list = os.listdir(testcase_path)
    import_name_list = []
    for i in name_list:
        i1 = i.split(".")[0]
        if i1 and i1 not in import_name_list:
            import_name_list.append(i1)

    return name_list, import_name_list


def get_integration(cla, token,*args):
    dir_def = dir(cla)  # 获取类下所有的函数
    for de in dir_def:
        # print('de', de)
        if re.findall("__", de) or re.findall("pass_1", de):
            pass
        # if re.findall("a004_", de)or re.findall("a001_", de) or re.findall("a002_", de)or re.findall("a003_", de):
        # if re.findall("a147_", de):
        else:
            # print(i)
            func = getattr(cla, de)
            # print(func)
            # print('member is :' + str(m   ember))
            func("seif", token,args[0])


def main():
    print('))))))))))))))))))))))))))))))))))))))')
    start_time = datetime.datetime.now()
    print(start_time)
    # # load_module()
    # module_list = get_module_list()
    # # print("11111")
    # # 1.生成API_test_report.xlsx测试报告模板

    # worksheet, workbook = public.write_report()

    # print("22222")
    # 2.执行用例
    # total_pass_num, total_failed_num, total_unexecuted_num = login.test_case(worksheet, workbook, "login")

    # login.test_case(worksheet, workbook, "login")

    # print(33333)
    # token_1 = public.get_token(http_.supplier_phone, md5Encode(123456))  # 发起 销售方
    # token_2 = public.get_token(http_.purchaser_phone, md5Encode(123456))  # 收到 采购方
    # token_3 = public.get_token(13245678999, md5Encode(123456))  # 代理方

    list_integration = []
    list_integration.append(Integration)
    list_integration.append(Agent_Integration)
    list_integration.append(Sale_Integration)  # 收到 采购方
    list_integration.append(Purchase_Integration)  # 发起 销售方
    print("<" * 50 + "接口测试环节" + ">" * 50)
    a = 0
    while a <= 20:
        for cla in list_integration:  # 遍历出所有的方法
            # if re.findall("Integration",cla):  # 判断出所有的测试Integration类
            # print(list_integration)
            if cla == Agent_Integration:  # 判断是否为代理方
                # print(cla)
                token = public.get_token(http_.agent_phone, md5Encode(123456))  # 代理方
                get_integration(cla, token,a)
            elif cla == Purchase_Integration:  # 判断是否为代理方
                token = public.get_token(http_.purchaser_phone, md5Encode(123456))  # 收到 采购方
                get_integration(cla, token,a)
            elif cla == Sale_Integration:  # 判断是否为代理方
                token = public.get_token(http_.supplier_phone, md5Encode(123456))  # 发起 销售方
                get_integration(cla, token,a)
            else:
                token = ""  # 三方总流程
                get_integration(cla, token,a)

        file_save()
        a += 1

    endtime = datetime.datetime.now()
    print(endtime)
    print(endtime - start_time)
    # worksheet.write(0, 14, total_pass_num)
    # worksheet.write(1, 14, total_failed_num)
    # worksheet.write(2, 14, total_unexecuted_num)


if __name__ == "__main__":
    main()
