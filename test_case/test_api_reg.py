import pytest
import inspect
from script.do_excel import handle_new_api_reg
from script.rebulit_log import do_log
from script.handle_context02 import HandleContext
from script.path_split import NEW_API_DATA_PATH
from script.handle_yaml import do_yaml
case = handle_new_api_reg.get_all_datas()
#print(case)


class TestReg:

    pytestmark = [pytest.mark.webtest, pytest.mark.slowtest]

    @pytest.mark.reg
    @pytest.mark.parametrize('val', case)
    def test_login(self, val, init_reg):
        open_request,handmysql=init_reg
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id']  # 获取excel中case_id行数据
        response_url = val['url']
        new_data = HandleContext().register_param(val['data'])
        print(type(new_data))
        mobile = eval(new_data)['mobile_phone']
        print(type(mobile))
        actual_result = open_request(method=val['method'],
                                     url=response_url,
                                     data=new_data,
                                     is_json=True)

        code = actual_result.json()['code']

        try:
            assert val['expected']==code
        except Exception as e:
            # raise e
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            handle_new_api_reg.write_datas(other_file=NEW_API_DATA_PATH,
                                           other_sheet='reg',
                                           write_num=case_id + 1,
                                           actual_result=actual_result.text,
                                           result=do_yaml.get_data('excel', 'fail_result'))
            raise e
        else:
            # 将通过结果写入
            handle_new_api_reg.write_datas(other_file=NEW_API_DATA_PATH,
                                           other_sheet='reg',
                                           write_num=case_id + 1,
                                           actual_result=actual_result.text,
                                           result=do_yaml.get_data('excel', 'pass_result'))


if __name__ == '__main__':
    pytest.main(['-m reg'])

