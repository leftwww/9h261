import pytest  # 注意导包

test_lest=[]
class TestLogin:

    @pytest.mark.run(order=0)
    def test_sucess(self):  # 定义的第一个case，上面有一个装饰器

        print("test sucess1")


    @pytest.mark.run(order=2)
    def test_sucess2(self):
        print(test_lest)
        print("test sucess2")

    @pytest.mark.run(order=100)
    def test_fail(self):
        print("test fail3")

    @pytest.mark.run(order=1)
    def test_sucess4(self):
        A =1
        test_lest.append(A)
        print("test sucess4")

    @pytest.mark.skipif(True, reason='')
    def test_sucess5(self):
        print('232424')

    @pytest.mark.skipif(True, reason='')
    def test_sucess6(self):
        print('232424')


pytest.main(['-s','test_aaa.py'])
pytest.main(["-m","test_aaa","--html=Report/report.html"])