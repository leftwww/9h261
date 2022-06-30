# -- coding: utf-8 --
# @Author : Zw
# @File : globalvar.py

# todo 全局变量管理模块

def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value
    # print(_global_dict)  #


def get_value(name, defValue="123"):  # 原本为None，但是None用于正则会报错，改为"None"
    try:
        return _global_dict[name]
    except KeyError:
        return defValue

# gl.set_value('supplier_name',supplier_name) # 供方企业名
# gl.set_value('purchaser_name', purchaser_name) # 采方企业名

# gl.set_value('contractnumber', contractnumber)  #   合同编号 CT
# gl.set_value("picture", picture)  #  # 图片.ipg
# gl.set_value('contract_mark', contract_mark)  #  原始合同编号 手动输入的
# gl.set_value("settlement_date", settlement_date)  # 结算方式 票到XX天
# gl.set_value("supplier_audit_time", supplier_audit_time)  # 内部提交时间
# gl.set_value('purchaser_name', purchaser_name)  # 甲（采购）方企业名
# gl.set_value('purchaser_926', purchaser_926)  #  甲（采购）方926链号
# gl.set_value('purchaser_email', purchaser_email)  #  甲（采购）方邮箱
# gl.set_value('purchaser_phone', purchaser_phone)  #  甲（采购）方电话
# gl.set_value('agent_name', agent_name)  #  乙（代理)  #方企业名
# gl.set_value('agent_926', agent_926)  #  乙（代理)  #方926链号
# gl.set_value('agent_email', agent_email)  #  乙（代理)  #方邮箱
# gl.set_value('agent_phone', agent_phone)  #  乙（代理)  #方电话
# gl.set_value('supplier_926', supplier_926)  #   丙（销售)  #方926链号
# gl.set_value('supplier_email', supplier_email)  #  丙（销售)  #方邮箱
# gl.set_value('supplier_name', supplier_name)  #  丙（销售)  #方企业名
# gl.set_value('supplier_phone', supplier_phone)  #  丙（销售)  #方电话

# gl.set_value('purchaser_bank', purchaser_bank)  # 采购（甲）方开户行
# gl.set_value('purchaser_account', purchaser_account)  # 采购（甲）方账号
# gl.set_value('purchaser_address', purchaser_address)  # 采购（甲）方地址
# gl.set_value('purchaser_contacts', purchaser_contacts)  # 采购（甲）方联系人
#
# gl.set_value('agent_bank', agent_bank)  # 代理（乙）方开户行
# gl.set_value('agent_account', agent_account)  # 代理（乙）方账号
# # gl.set_value('agent_contacts',agent_contacts)
# # gl.set_value('agent_address',agent_address)
#
# gl.set_value('supplier_bank', supplier_bank)  # 销售方（丙）开户行
# gl.set_value('supplier_account', supplier_account)  # 销售方（丙）方账号
# gl.set_value('supplier_contacts', supplier_contacts)  # 销售方（丙）方联系人
# gl.set_value('supplier_address', supplier_address)  # 销售方（丙）方地址

# gl.set_value('price_single_1', price_single_1)  #  一类商品总价
# gl.set_value('price_sum_check_all_1', price_sum_check_all_1)  #  一种商品总价
# gl.set_value('apply_number', apply_number)  # 创建编号 CR
# gl.set_value('price_many_2', price_many_2)  # 二类商品总价
# gl.set_value('price_sum_check_all_2', price_sum_check_all_2)  # 两种商品总价
# gl.set_value('agent_refuse_reason', agent_refuse_reason)  #  代理方拒绝理由
# gl.set_value('agent_refuse_details', agent_refuse_details)  #  代理方拒绝详情
# gl.set_value('cooperation_refuse_details', cooperation_refuse_details)  #  合作方拒绝详情
# gl.set_value('cooperation_refuse_reason', cooperation_refuse_reason)  #  合作方绝理由

# gl.set_value('invoiceApplySn',invoiceApplySn)  # # DF 发货单编号
# gl.set_value('their_service_charge', their_service_charge)  #  他方服务费
# gl.set_value('our_service_charge',our_service_charge)  #  我方服务费
# gl.set_value('total_goods',total_goods)  #  # 货品总价 10000

# gl.set_value("estimateReduceQuota_purchaser", estimateReduceQuota_purchaser)  #   预计减少云票
# gl.set_value('totalCreditQuota_purchaser', totalCreditQuota_purchaser)  # 甲 采购总授信云票"
# gl.set_value('totalCirculationQuota_purchaser', totalCirculationQuota_purchaser)  # 甲 采购总流转云票"
# gl.set_value('totalQuota_purchaser',totalQuota_purchaser)  # 甲 总云票 （授信+流转）
# gl.set_value('totalOccupyCreditQuota_purchaser',totalOccupyCreditQuota_purchaser) # jia 已占用授信云票
# gl.set_value('totalOccupyCirculationQuota_purchaser',totalOccupyCirculationQuota_purchaser) # jia 已占用流转云票
# gl.set_value('totalFrozenCreditQuota_purchaser',totalFrozenCreditQuota_purchaser) # jia 获取已冻结授信云票
# gl.set_value('totalFrozenCirculationQuota_purchaser',totalFrozenCirculationQuota_purchaser)  # jia 已冻结流转云票
# gl.set_value('totalOccupancyCreditQuota_purchaser',totalOccupancyCreditQuota_purchaser)  #jia 可用总授信(总-已用)
# gl.set_value('totalOccupancyCirculationQuota_purchaser',totalOccupancyCirculationQuota_purchaser)  # jia 余总流转(总-已用
# gl.set_value('contactEffectiveNum_purchaser',contactEffectiveNum_purchaser)  # 生效委托申请单
# gl.set_value('loanHistoryNum_purchaser',loanHistoryNum_purchaser)  # 贷现历史次数

# gl.set_value("estimateAddQuota", estimateAddQuota)  #   预增云票
# gl.set_value('loanAbilityQuota',loanAbilityQuota)  # 可贷现
# gl.set_value('surplusTotalCirculationQuota',surplusTotalCirculationQuota)  # 剩余流转
# gl.set_value('totalCreditQuota_supplier', totalCreditQuota_supplier)  # 丙 总授信云票"
# gl.set_value('totalCirculationQuota_supplier', totalCirculationQuota_supplier)  # 丙 总流转云票"
# gl.set_value('totalQuota_supplier', totalQuota_supplier)  # 丙 总云票 （授信+流转）
# gl.set_value('totalOccupyCreditQuota_supplier', totalOccupyCreditQuota_supplier)  # 丙 已占用授信云票
# gl.set_value('totalOccupyCirculationQuota_supplier',totalOccupyCirculationQuota_supplier)  # 丙 已占用流转云票
# gl.set_value('totalFrozenCreditQuota_supplier', totalFrozenCreditQuota_supplier)  # 丙 获取已冻结授信云票
# gl.set_value('totalFrozenCirculationQuota_supplier',totalFrozenCirculationQuota_supplier)  # 丙 已冻结流转云票
# gl.set_value('totalOccupancyCreditQuota_supplier',totalOccupancyCreditQuota_supplier)  # 丙 可用总授信(总-已用)
# gl.set_value('totalOccupancyCirculationQuota_supplier',totalOccupancyCirculationQuota_supplier)  # 丙 余总流转(总-已用
# gl.set_value('contactEffectiveNum_supplier', contactEffectiveNum_supplier)  # 生效委托申请单
# gl.set_value('loanHistoryNum_supplier', loanHistoryNum_supplier)  # 贷现历史次数

# gl.set_value('invoiceSn', invoiceSn) # 出货单编号 DO
# gl.set_value('Luckynumber',Luckynumber) # 单数自提 双数物流

# gl.set_value('logisticsSn',logisticsSn)  # 物流单号
# gl.set_value('companyName',companyName)  # 物流公司
# shipment_time = gl.get_value('shipment_time')  # 出货时间
# gl.set_value('logisticsSn', logisticsSn)  # 物流公司信息
# gl.set_value('companyName', companyName)  # 物流单号信息
# gl.set_value('logistics_img',logistics_img)  # 详情页中物流单图片
# gl.set_value('invoiceApply_img', invoiceApply_img)  # 详情页中出货单图片

# receiptSn = gl.get_value('receiptSn')  # 收票编号  SP
# send_receiptSn = gl.get_value('send_receiptSn')  # 寄票编号 JP
# gl.set_value('invoicePaymentSn',invoicePaymentSn)  # 付款编号
