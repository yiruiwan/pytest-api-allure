import pytest
import inspect
from script.do_excel import handle_new_api_recharge
from script.rebulit_log import do_log
from script.handle_context02 import HandleContext
from script.path_split import NEW_API_DATA_PATH
from script.handle_yaml import do_yaml
case = handle_new_api_recharge.get_all_datas()
print(case)


class TestRecharge:

    pytestmark = [pytest.mark.webtest, pytest.mark.slowtest]

    @pytest.mark.recharge
    @pytest.mark.parametrize('val', case)
    def test_recharge(self, val, init):
        open_request,handmysql=init
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id']  # 获取excel中case_id行数据
        response_url = val['url']
        method = val['method']
        type = val['type']
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
            assert val['expected'] == code
        except AssertionError as e:
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            handle_new_api_recharge.write_datas(other_file=NEW_API_DATA_PATH,
                                                other_sheet='recharge',
                                                write_num=case_id + 1,
                                                actual_result=actual_result.text,
                                                result=do_yaml.get_data('excel', 'fail_result'))
            raise e
        else:
            # 将通过结果写入
            handle_new_api_recharge.write_datas(other_file=NEW_API_DATA_PATH,
                                                other_sheet='recharge',
                                                write_num=case_id + 1,
                                                actual_result=actual_result.text,
                                                result=do_yaml.get_data('excel', 'pass_result'))


if __name__ == '__main__':
    pytest.main()