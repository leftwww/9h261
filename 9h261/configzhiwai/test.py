import pytest

@pytest.fixture(scope='function')
def setup_function(request):
    def teardown_function():
        print("teardown_function called.")
    request.addfinalizer(teardown_function)  # 此内嵌函数做teardown工作
    print('setup_function called.')

@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called.")
    request.addfinalizer(teardown_module)
    print('setup_module called.')

@pytest.mark.website
def test_1(setup_function):
    print('Test_1 called.')

def test_4(setup_function):
    print('Test_4 called.')


def test_2(setup_module):
    print('Test_2 called.')

def test_3(setup_module):
    print('Test_3 called.')
#    assert 2==1+1

b = {'data': {'current': 1, 'pages': 1, 'records': [{'abnormalState': 0, 'businessOpportunityOrderSn': 'ZC200402181745UEK0ND27', 'businessOpportunitySn': 'SJ200402181745UEK0ND27', 'companyName': '企业名称', 'id': 32, 'isDistribution': 0, 'managementDistributionTime': 1585822687000, 'servicerFollowUpUser': '', 'servicerFollowUpUserId': 0, 'state': 2, 'updateTime': 1585822687000}, {'abnormalState': 0, 'businessOpportunityOrderSn': 'ZC200324151511MN358J10', 'businessOpportunitySn': 'SJ200324151511MN358J10', 'companyName': '2345', 'id': 15, 'isDistribution': 0, 'managementDistributionTime': 1585298865000, 'servicerFollowUpUser': '', 'servicerFollowUpUserId': 0, 'state': 2, 'updateTime': 1585298865000}, {'abnormalState': 0, 'businessOpportunityOrderSn': 'ZC200325111338GH4NH519', 'businessOpportunitySn': 'SJ200325111338GH4NH519', 'companyName': '1111', 'id': 24, 'isDistribution': 0, 'managementDistributionTime': 1585106041000, 'servicerFollowUpUser': '', 'servicerFollowUpUserId': 0, 'state': 2, 'updateTime': 1585106041000}, {'abnormalState': 0, 'businessOpportunityOrderSn': 'ZC200325111351BIR0QK20', 'businessOpportunitySn': 'SJ200325111351BIR0QK20', 'companyName': '1111', 'id': 25, 'isDistribution': 0, 'managementDistributionTime': 1585106036000, 'servicerFollowUpUser': '', 'servicerFollowUpUserId': 0, 'state': 2, 'updateTime': 1585106036000}, {'abnormalState': 0, 'businessOpportunityOrderSn': 'ZC200325111005DA2OFY14', 'businessOpportunitySn': 'SJ200325111005DA2OFY14', 'companyName': '1', 'id': 19, 'isDistribution': 0, 'managementDistributionTime': 1585105817000, 'servicerFollowUpUser': '', 'servicerFollowUpUserId': 0, 'state': 2, 'updateTime': 1585105817000}, {'abnormalState': 1, 'businessOpportunityOrderSn': 'ZC2003250953084KEJLR11', 'businessOpportunitySn': 'SJ2003250953084KEJLR11', 'companyName': 'qwer', 'id': 16, 'isDistribution': 0, 'managementDistributionTime': 1585101201000, 'servicerFollowUpUser': '', 'servicerFollowUpUserId': 0, 'state': 2, 'updateTime': 1585101789000}, {'abnormalState': 1, 'businessOpportunityOrderSn': 'ZC200323145809OZJ8W708', 'businessOpportunitySn': 'SJ200323145809OZJ8W708', 'companyName': '1314', 'id': 13, 'isDistribution': 0, 'managementDistributionTime': 1584946712000, 'servicerFollowUpUser': '', 'servicerFollowUpUserId': 0, 'state': 2, 'updateTime': 1584946712000}], 'size': 10, 'total': 7}, 'msg': '处理成功', 'ret': 0}
#print(b['data']['records'][0]['id'])
#print(b['data']['records'])
pytest.main(['-s','test.py'])