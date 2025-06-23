import pytest

if __name__ == '__main__':
    pytest.main(['-s', '-v', './testcase', '--capture=sys'])
    # run only one test case
    # pytest.main(['-s', '-v', '--capture=sys', 'accountManage/test_userLog.py'])