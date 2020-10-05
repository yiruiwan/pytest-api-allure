import requests
from script.create_user import generate_new_user
# from script.rebulit_config import role_token
from script.handle_yaml import user_accounts
from script.path_split import USER_ACCOUNTS_YAML_PATH


class Requests:
    generate_new_user()  # 生成角色账号
    login_token = {}

    def get_token(self, type =None):
        header = {"X-Lemonban-Media-Type":"lemonban.v2","Content-Type":"application/json"}
        login_url = "http://api.lemonban.com/futureloan/member/login"
        global tokens
        global login_mobile,login_pwd
        if type =='admin':  # 管理员登录
            login_mobile = user_accounts.get_data('admin_user', 'mobilephone')
            login_pwd = user_accounts.get_data('admin_user', 'pwd')

        elif type == 'brow':  # 投资者登录
            login_mobile = user_accounts.get_data('borw_user', 'mobilephone')
            login_pwd = user_accounts.get_data('borw_user', 'pwd')

        elif type =='invest':  # 借款者登录
            login_mobile = user_accounts.get_data('invest_use', 'mobilephone')
            login_pwd = user_accounts.get_data('invest_use', 'pwd')

        if type not in self.login_token:
            datas = {"mobile_phone": login_mobile, "pwd": login_pwd}
            tokens = requests.post(url=login_url, json=datas, headers=header)
            try:
                tokens = tokens.json()['data']['token_info']['token']
                dict = {type: tokens}
                self.login_token.update(dict)
            except:
                tokens = tokens.json()
        else:

            tokens = self.login_token[type]
            # print(2)

        return tokens


    '''def write_config(self,login_url,login_data):
        tokens_data = self.get_token(login_url=login_url,login_data=login_data)
        token = {"token":{'token': tokens_data},}
        api_config.write_config(datas=token,filename=API_TOKEN_PATH)'''

request1 = Requests()


if __name__ == '__main__':
    print(request1.get_token(type='admin'))
    request1.get_token(type='admin')



