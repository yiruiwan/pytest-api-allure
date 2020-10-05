import pytest
from script.do_excel import HandleExcel
from script.handle_reques import HttpRequste
from script.handle_sql import HandleMysql
from script.rebulit_log import do_log
from script.handle_yaml import do_yaml
from script.api_request import TokenRequest


@pytest.fixture(scope='class')
def init_reg():
    open_request = HttpRequste()
    header = do_yaml.get_data('headers','headers')
    open_request.add_headers(header) # 踩坑，获取的是字典字符串，要使用eval换成字典。考虑把config配置文件换成yaml可能可以避免这个问题
    handmysql = HandleMysql()
    do_log.info("start run")
    yield open_request,handmysql
    open_request.close()
    handmysql.close()
    do_log.info('over run')


@pytest.fixture(scope='class')
def init():
    open_request = TokenRequest()
    handmysql = HandleMysql()
    do_log.info("start run")
    yield open_request,handmysql
    handmysql.close()
    do_log.info('over run')