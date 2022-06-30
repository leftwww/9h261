import datetime
import time
from datetime import datetime

from dateutil.relativedelta import relativedelta
from jira import JIRA

jira_server = 'http://jira.sunaw.com'
jira_username = 'zuowei'
jira_password = 'zw1997515'
# jira_username = 'xiaowenb'
# jira_password = 'xwb2834'

# jira = JIRA(basic_auth=(jira_username, jira_password), options = {'server': jira_server})
jira = JIRA(jira_server, basic_auth=(jira_username, jira_password))  # 创建jira连接


def delay_time(time_str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    if type(time_str) == str:
        time_str = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    ret = time_str + relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return ret


def searchIssues(jql, max_results=999999):
    ''' Search issues
    @param jql: JQL, str
    @param max_results: max results, int, default 100
    @return issues: result, list
    '''
    try:
        issues = jira.search_issues(jql, maxResults=max_results)
        return issues
    except Exception as e:
        print(e)


jql_colse = '''
    issuetype = Bug AND reporter in (currentUser()) order by created DESC
'''
jpl_open = 'issuetype = Bug AND status in (打开, 进行中, 重新打开) AND reporter in (currentUser()) order by created DESC'

issues = searchIssues(jql_colse)
# print(len(issues))
# todo assignee：经办人created: 创建时间creator: 创建人labels: 标签priorit: 优先级progress:project: 所示项目reporter: 报告人
# todo status: 状态summary: 问题描述worklog: 活动日志updated: 更新时间watches: 关注者comments: 评论resolution: 解决方案
# todo subtasks: 子任务issuelinks: 连接问题lastViewed: 最近查看时间

list_assignee_all = []  # 总数表
list_left_over_all = []  # 未关闭表
sum = 0
# list_left_over_lv_all = []
for issue in issues:  # todo 总表
    # print(format(issue.fields.created)[0:10]
    list_assignee_all.append(format(issue.fields.assignee))  # 经办人
    if format(issue.fields.status) == "已关闭":
        # print(format(issue.fields.summary), format(issue.fields.status))
        list_left_over_all.append(format(issue.fields.assignee))  # 添加月份遗留数量
lv_all = (len(list_left_over_all) / len(list_assignee_all)) * 100
print('----------左维个人提交总bug数量：%s,明细如下：' % len(list_assignee_all))
print("")
print('**********总bug关闭数为：%s'%len(list_left_over_all) + ',关闭率为：%.2f' % lv_all + "% **********")
print("")
myset = set(list_assignee_all)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
for item in myset:
    print("All the %s has found %s,The total proportion is %0.2f" % (
        item, list_assignee_all.count(item), list_assignee_all.count(item) / len(list_assignee_all) * 100) + "%")

list_assignee_30 = []
list_left_over_30 = []


def month_926(now_time):
    # 1个月前
    ret2 = delay_time(now_time, months=-1)
    now_time_year = str(now_time)[0:4]
    # print(ret2, '一个月前')
    begin_year = str(ret2)[0:4]
    begin_month = str(ret2)[5:7]
    begin_day = str(ret2)[8:10]
    for issue in issues:  # todo 总表
        if int(begin_year) < int(now_time_year):  # 判断一个月前年份时间小于当前年份
            # 将去年的满足条件的帅选出来
            if int(format(issue.fields.created)[0:4]) == int(begin_year) and int(
                    format(issue.fields.created)[5:7]) == 12 and int(format(issue.fields.created)[8:10]) >= int(
                begin_day):
                list_assignee_30.append(format(issue.fields.assignee))  # 经办人
                if format(issue.fields.status) == "已关闭":
                    # print(format(issue.fields.summary), format(issue.fields.status))
                    list_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
            # 将今年的满足条件的帅选出来
            if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                    format(issue.fields.created)[5:7]) == datetime.now().month and int(
                format(issue.fields.created)[8:10]) <= datetime.now().day:
                list_assignee_30.append(format(issue.fields.assignee))  # 经办人
                if format(issue.fields.status) == "已关闭":
                    # print(format(issue.fields.summary), format(issue.fields.status))
                    list_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
        else:
            if int(begin_month) < datetime.now().month:
                if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                        format(issue.fields.created)[5:7]) == int(begin_month) and int(
                    format(issue.fields.created)[8:10]) >= int(begin_day):
                    list_assignee_30.append(format(issue.fields.assignee))  # 经办人
                    if format(issue.fields.status) == "已关闭":
                        # print(format(issue.fields.summary), format(issue.fields.status))
                        list_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
                if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                        format(issue.fields.created)[5:7]) == datetime.now().month and int(
                    format(issue.fields.created)[8:10]) <= datetime.now().day:
                    list_assignee_30.append(format(issue.fields.assignee))  # 经办人
                    if format(issue.fields.status) == "已关闭":
                        # print(format(issue.fields.summary), format(issue.fields.status))
                        list_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
            else:
                if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                        format(issue.fields.created)[5:7]) == int(begin_month) and int(
                    format(issue.fields.created)[8:10]) <= datetime.now().day:
                    list_assignee_all.append(format(issue.fields.assignee))  # 经办人
                    if format(issue.fields.status) == "已关闭":
                        # print(format(issue.fields.summary), format(issue.fields.status))
                        list_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
    # print(len(list_left_over_30))
    # print(len(list_assignee_30))
    try:
        zlv_30 = (len(list_left_over_30) / len(list_assignee_30)) * 100
    except ZeroDivisionError:
        zlv_30 = 0
    print("")
    print('----------左维近30天个人提交总bug数量：%s,明细如下：' % len(list_assignee_30))
    print("")
    print('**********30天总bug关闭数为:%s'%len(list_left_over_30) + ',关闭率为:%.2f' % zlv_30 + "%**********")
    print("")
    myset = set(list_assignee_30)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
    for item in myset:
        print("All the %s has found %s,The total proportion is %0.2f" % (
            item, list_assignee_30.count(item), list_assignee_30.count(item) / len(list_assignee_30) * 100) + "%")

now_time = datetime.now()
# now_time = delay_time(now_time, days=55)
month_926(now_time)  # datetime.now()当前时间


# todo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
jira_username = 'xiaowenb'
jira_password = 'xwb2834'

# jira = JIRA(basic_auth=(jira_username, jira_password), options = {'server': jira_server})
jira = JIRA(jira_server, basic_auth=(jira_username, jira_password))  # 创建jira连接
def searchIssues_x(jql, max_results=10000):
    ''' Search issues
    @param jql: JQL, str
    @param max_results: max results, int, default 100
    @return issues: result, list
    '''
    try:
        issues_x = jira.search_issues(jql, maxResults=max_results)
        return issues_x
    except Exception as e:
        print(e)
jql_colse_x = '''
    issuetype = Bug AND reporter in (currentUser()) order by created DESC

'''
jpl_open_x = 'issuetype = Bug AND status in (打开, 进行中, 重新打开) AND reporter in (currentUser()) order by created DESC'

issues_x = searchIssues_x(jql_colse_x)
# print(len(issues_x))
# todo assignee：经办人created: 创建时间creator: 创建人labels: 标签priorit: 优先级progress:project: 所示项目reporter: 报告人
# todo status: 状态summary: 问题描述worklog: 活动日志updated: 更新时间watches: 关注者comments: 评论resolution: 解决方案
# todo subtasks: 子任务issuelinks: 连接问题lastViewed: 最近查看时间

xlist_assignee_all = []  # 总数表
xlist_left_over_all = []  # 未关闭表
xf = []
# xlist_left_over_lv_all = []
for issue in issues_x:  # todo 总表
    # print(format(issue.fields.created)[0:10]
    xlist_assignee_all.append(format(issue.fields.assignee))  # 经办人
    xf.append(format(issue.fields.status))
    # print(len(xf))
    if format(issue.fields.status) == "已关闭":
        # print(format(issue.fields.summary), format(issue.fields.status))
        xlist_left_over_all.append(format(issue.fields.assignee))  # 添加月份遗留数量
# print('xlist_left_over_all',xlist_left_over_all)
# print('xlist_assignee_all',xlist_assignee_all)
xlv_all = (len(xlist_left_over_all) / len(xlist_assignee_all)) * 100
print('----------肖文波个人提交总bug数量：%s,明细如下：' % len(xlist_assignee_all))
print("")
print('总bug关闭数为:%s'%len(xlist_left_over_all) + ',关闭率为:%.2f' % xlv_all + "%")
print("")
myset = set(xlist_assignee_all)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
for item in myset:
    print("All the %s has found %s,The total proportion is %0.2f" % (
        item, xlist_assignee_all.count(item), xlist_assignee_all.count(item) / len(xlist_assignee_all) * 100) + "%")

xlist_assignee_30 = []
xlist_left_over_30 = []
def delay_time(time_str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    if type(time_str) == str:
        time_str = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    ret = time_str + relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return ret

def month_926(now_time):
    # 1个月前
    ret2 = delay_time(now_time, months=-1)
    now_time_year = str(now_time)[0:4]
    # print(ret2, '一个月前')
    begin_year = str(ret2)[0:4]
    begin_month = str(ret2)[5:7]
    begin_day = str(ret2)[8:10]
    for issue in issues_x:  # todo 总表
        if int(begin_year) < int(now_time_year):  # 判断一个月前年份时间小于当前年份
            # 将去年的满足条件的帅选出来
            if int(format(issue.fields.created)[0:4]) == int(begin_year) and int(
                    format(issue.fields.created)[5:7]) == 12 and int(format(issue.fields.created)[8:10]) >= int(
                begin_day):
                xlist_assignee_30.append(format(issue.fields.assignee))  # 经办人
                if format(issue.fields.status) == "已关闭":
                    # print(format(issue.fields.summary), format(issue.fields.status))
                    xlist_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
            # 将今年的满足条件的帅选出来
            if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                    format(issue.fields.created)[5:7]) == datetime.now().month and int(
                format(issue.fields.created)[8:10]) <= datetime.now().day:
                xlist_assignee_30.append(format(issue.fields.assignee))  # 经办人
                if format(issue.fields.status) == "已关闭":
                    # print(format(issue.fields.summary), format(issue.fields.status))
                    xlist_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
        else:
            if int(begin_month) < datetime.now().month:
                if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                        format(issue.fields.created)[5:7]) == int(begin_month) and int(
                    format(issue.fields.created)[8:10]) >= int(begin_day):
                    xlist_assignee_30.append(format(issue.fields.assignee))  # 经办人
                    if format(issue.fields.status) == "已关闭":
                        # print(format(issue.fields.summary), format(issue.fields.status))
                        xlist_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
                if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                        format(issue.fields.created)[5:7]) == datetime.now().month and int(
                    format(issue.fields.created)[8:10]) <= datetime.now().day:
                    xlist_assignee_30.append(format(issue.fields.assignee))  # 经办人
                    if format(issue.fields.status) == "已关闭":
                        # print(format(issue.fields.summary), format(issue.fields.status))
                        xlist_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
            else:
                if int(format(issue.fields.created)[0:4]) == int(now_time_year) and int(
                        format(issue.fields.created)[5:7]) == int(begin_month) and int(
                    format(issue.fields.created)[8:10]) <= datetime.now().day:
                    xlist_assignee_all.append(format(issue.fields.assignee))  # 经办人
                    if format(issue.fields.status) == "已关闭":
                        # print(format(issue.fields.summary), format(issue.fields.status))
                        xlist_left_over_30.append(format(issue.fields.assignee))  # 添加月份遗留数量
    # print(len(xlist_left_over_30))
    # print(len(xlist_assignee_30))
    try:
        xlv_30 = (len(xlist_left_over_30) / len(xlist_assignee_30)) * 100
    except ZeroDivisionError:
        xlv_30 = 0
    print("")
    print('----------肖文波近30天个人提交总bug数量：%s,明细如下：' % len(xlist_assignee_30))
    print("")
    print('**********30天总bug关闭数为:%s'%len(xlist_left_over_30) + ',关闭率为:%.2f' % xlv_30 + "% **********")
    print("")
    myset = set(xlist_assignee_30)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项z
    for item in myset:
        print("All the %s has found %s,The total proportion is %0.2f" % (
            item, xlist_assignee_30.count(item), xlist_assignee_30.count(item) / len(xlist_assignee_30) * 100) + "%")

now_time = datetime.now()
# now_time = delay_time(now_time, days=15)
month_926(now_time)  # datetime.now()当前时间
#
# # def month_926(year,month):
# #     for issue in issues:  # 2019年分表
# #         if str(format(issue.fields.created)[0:4]) == year and int(
# #                 format(issue.fields.created)[5:7]) == month:  # 获取2019年
# #             list_assignee_19.append(format(issue.fields.assignee))  # 经办人
# #
# #             # print(len(list_assignee_19))
# #             list_assignee_month.append(list_assignee_19)  # 添加所有月份的bug数量
# #
# #             if format(issue.fields.status) != "已关闭":
# #                 # print(format(issue.fields.summary), format(issue.fields.status))
# #                 list_left_over.append(format(issue.fields.assignee))  # 添加月份遗留数量
# #
# #     if len(list_left_over):
# #         list_left_over_lv.append(list_left_over)
# #     else:
# #         list_left_over_lv.append([])
# #     # print('月份为',i,list_assignee_19,len(list_assignee_19))
# #     if list_assignee_number:  # 不为空时表示为2月以上 将之前的和2月以商的相加
# #         len(list_assignee_19) + list_assignee_number[len(list_assignee_number) - 1]
# #         list_assignee_number.append(
# #             len(list_assignee_19) + list_assignee_number[len(list_assignee_number) - 1])  # 添加进入年度表
# #     else:  # 为空时表示为1月 将18年的和1月的相加
# #         list_assignee_number.append(len(list_assignee_18) + len(list_assignee_19))  # 添加进入年度表
# #
# #     # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
# #     # print(list_left_over)
# #     # print(list_left_over_lv)
# #     # print('当前月份为%s ' % i)
# #     # print('当前总bug数量为%s' % list_assignee_number[i - 1])
# #     # print('新增数量为%s' % (len(list_assignee_month[i - 1])))
# #     # print('解决数量为%s' % (len(list_assignee_month[i - 1]) - len(list_left_over)))
# #     if len(list_left_over_lv[i - 1]):
# #         # print('遗留数为%s' % len(list_left_over_lv[i - 1]))
# #         list_xlsx.append(len(list_left_over_lv[i - 1]))  # 遗留数
# #     else:
# #         # print('遗留数为0')
# #         list_xlsx.append(0)  # 遗留数
# #     list_xlsx.append(list_assignee_number[i - 1])  # 当前总bug数
# #     if len(list_left_over_lv[i - 1]):
# #         # print('遗留率为%s' % str(len(list_left_over_lv[i - 1]) / len(list_assignee_month[i - 1]) * 100)[0:4])
# #         lv = str(len(list_left_over_lv[i - 1]) / len(list_assignee_month[i - 1]) * 100)[0:4]
# #         list_xlsx.append(float(lv))  # 遗留lv
# #     else:
# #         # print('遗留率为0')
# #         list_xlsx.append(0)  # 遗留lv
# #     # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
# #
# #     list_xlsx.append(len(list_assignee_month[i - 1]))  # 新增数量
# #     list_xlsx.append((len(list_assignee_month[i - 1]) - len(list_left_over)))  # 解决数量
# #
# #     list_assignee_19.clear()  # 清空月表,进入下一个月
# #     list_left_over.clear()
# #     # myset = set(list_assignee_19)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
# #     # for item in myset:
# #     #     print("2019 the %s has found %s" % (item, list_assignee_19.count(item)))
# #
# #
# # for x in (["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]):
# #     for i in range(1, (datetime.now().month) + 1):  # 遍历当前月份i
# #         # print("i = ",i)
# #         month_926(x,i)
# #
# # list_assignee_2019 = []
# # list_created = []
# # for issue in issues:  # todo 2019年分表
# #     print(format(issue.fields.created)[5:7])
# #     # print(format(issue.fields.created)[0:10])
# #     # list_created.append(format(issue.fields.created)[0:4])  # 创办时间
# #     if str(format(issue.fields.created)[0:4]) == '2019':
# #         list_assignee_2019.append(format(issue.fields.assignee))  # 经办人
# #
# #         # print('{0}: {1}:{2}'.format(issue.key, issue.fields.summary,issue.fields.assignee))
# # # print('list_assignee_2019',list_assignee_2019)
# # print()
# # print('----------2019年左维个人提交总bug数量：%s,明细如下：' % (len(list_assignee_2019)))
# # myset = set(list_assignee_2019)  # myset是另外一个列表，里面的内容是mylist里面的无重复 项
# # for item in myset:
# #     print("2019 the %s has found %s" % (item, list_assignee_2019.count(item)))
# #
# # list_assignee_all_open = []
# # issues_open = searchIssues(jpl_open)
# # for issue_open in issues_open:  # todo 总表
# #     # print(format(issue.fields.created)[0:10]
# #     list_assignee_all_open.append(format(issue_open.fields.assignee))  # 经办人
# #
# # print(list_assignee_all_open)

time.sleep(100)
