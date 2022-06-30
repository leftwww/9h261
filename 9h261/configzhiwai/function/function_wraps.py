from functools import wraps
from function import public




def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        nor, table, nol, url = public.get_case('party_building', apiname)
        if url == "BaseUrl":
            unexecuted_num = nor - 5
            return unexecuted_num
        return f(*args, **kwargs)
    return decorated


@decorator_name
def test_case(worksheet, workbook, apiname, token):

    print("-" * 50 + "%s" % apiname + "-" * 50)
    nor, table, nol, url = public.get_case('party_building', apiname)
    if url == "BaseUrl":
        unexecuted_num = nor-5
        print("unexcuted_num:%d"% unexecuted_num)
        return unexecuted_num

worksheet, workbook = public.write_report()
test_case(worksheet,workbook,"getBranchList",token)

