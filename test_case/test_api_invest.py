import pytest
import inspect
from script.do_excel import handle_new_api_invest
from script.handle_yaml import do_yaml
from script.rebulit_log import do_log
from script.handle_context02 import HandleContext
from script.path_split import NEW_API_DATA_PATH
invest_case = handle_new_api_invest.get_all_datas()
# print(invest_case)


class TestInvest:

    pytestmark = [pytest.mark.webtest, pytest.mark.slowtest]

    @pytest.mark.invest
    @pytest.mark.parametrize('val', invest_case)
    def test_invest(self, val, init):
        open_request,handmysql = init
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id']  # 获取excel中case_id行数据
        response_url = val['url']
        method = val['method']
        type = val['type']
        check_sql = val['check_sql']
        new_data = HandleContext().invest_param(val['data'])
        # 发送请求，返回请求json数据
        actual_result = open_request(method=method,
                                     url=response_url,
                                     data=new_data,
                                     is_json=True,
                                     type=type)
        code = actual_result.json()['code']
        # 捕获异常 判断excel中expected值是否和返回的code值一致
        try:
            assert 200 == actual_result.status_code
        except AssertionError as e:
            do_log.error(e)
            raise e
        if check_sql:
            check_sql = HandleContext().invest_param(check_sql)
            id = handmysql(check_sql)
            HandleContext.load_id = id["id"]
        # 捕获异常，判断excel中expected值是否和返回的code值一致
        try:
            assert val['expected'] == code
        except Exception as e:
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            handle_new_api_invest.write_datas(other_file=NEW_API_DATA_PATH,
                                              other_sheet='invest',
                                              write_num=case_id + 1,
                                              actual_result=actual_result.text,
                                              result=do_yaml.get_data('excel', 'fail_result'))
            raise e
        else:
            # 将通过结果写入
            handle_new_api_invest.write_datas(other_file=NEW_API_DATA_PATH,
                                              other_sheet='invest',
                                              write_num=case_id + 1,
                                              actual_result=actual_result.text,
                                              result=do_yaml.get_data('excel', 'pass_result'))


if __name__ == '__main__':
    pytest.main()