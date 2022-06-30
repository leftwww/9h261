# -- coding: utf-8 --
# @Author : Zw
# @File : Integrate.py


from testcase_py.pc_926_agent import PC_926_agent
from testcase_py.pc_926_supplier import PC_926_supplier
from testcase_py.pc_926_purchaser import PC_926_purchaser

from config.config_supplier import Config_pc_supplier
from config.config_agent import Config_pc_agent
from config.config_purchaser import Config_pc_purchaser

def run():
    gongyin = PC_926_supplier()
    caigou = PC_926_purchaser()
    daili = PC_926_agent()
    gongyin.run()  # 供应方登录
    caigou.run()  # 采购方登录
    daili.run()  # 代理方登录

    gongyin.run1()  # 发起方申请委托
    caigou.run1_1()  # 合作方拒绝委托

    gongyin.run1_1()  # 发起方修改合作方拒绝的委托
    caigou.run1()  # 合作方同意委托
    daili.run0_5()  # 代理方查看客户管理
    daili.run1_1()  # 代理方拒绝委托

    gongyin.run1_2()  # 发起方修改代理方拒绝的委托
    caigou.run1()  # 合作方同意委托
    daili.run1()  # 代理方同意委托
    gongyin.run1_3()  # 发起方校验代理方通过审批后的合同信息
    caigou.run1_2()  # 校验代理方通过审批后的合同信息

    gongyin.run2()  # 代销方申请发货
    caigou.run2_1()  # 代采方拒绝发货申请
    gongyin.run2_1()  # 代销方查看被合作方拒绝的合同

    gongyin.run2()  # 代销方申请发货
    caigou.run2()  # 代采方通过发货申请
    gongyin.run2_2()  # 查看被合作方通过的合同
    daili.run2_1()  # 代理方拒绝发货申请
    gongyin.run2_3()  # 查看被代理方拒绝的合同
    caigou.run2_2()  # 代采方查看被代理方拒绝的发货申请

    gongyin.run2()  # 代销方申请发货
    caigou.run2()  # 代采方通过发货申请
    daili.run2()  # 代理方通过发货申请
    gongyin.run2_4()  # gongyin查看被代理方通过的合同
    caigou.run2_3()  # 代采方查看被代理方tongugo的发货申请

    gongyin.run3()  # 供应方出货
    daili.run3_1()  # 代理方查看供方出货后的货品信息
    caigou.run3()  # 采购方收货
    gongyin.run3_1()  # 供应方查看采方收货后的出货信息
    daili.run3_2()  # 代理方查看采方收货后的货品信息
    caigou.run3_1()  # 采购方品检
    gongyin.run3_2()  # 供应方查看采购品检后的出货信息
    daili.run3_3()  # 代理方查看采购品检后的货品信息
    caigou.run3_2()  # 采购方入库
    gongyin.run3_3()  # 供应方查看采购入库后的出货信息
    daili.run3_4()  # 代理方查看采购入库后的货品信息

    gongyin.run4()  # 供应方寄票
    daili.run4()  # 代理方收票/寄票
    # caigou.run4()  # 采购方收票
    #
    # caigou.run5()  # 采购方付款
    #
    # Config_pc_cai().excel_write()
    # Config_pc_gong().excel_write()
    # Config_pc_dai().excel_write()


if __name__ == '__main__':
    run()
