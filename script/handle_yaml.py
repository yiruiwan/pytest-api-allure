import yaml
from script.path_split import CONFIG_PATH_YAML,USER_ACCOUNTS_YAML_PATH


class HandleYaml:

    def __init__(self, filename=None):
        if filename is None:
            filename = CONFIG_PATH_YAML
        else:
            filename = filename
        with open(filename, encoding="utf-8") as file:
            self.config_data = yaml.full_load(file)

    def get_data(self, section, option):
        """
        读取配置文件数据
        :param section: 区域名
        :param option: 选项名
        :return: 值
        """
        return self.config_data[section][option]

    def write_yaml(self, file, data, encoding='utf-8',mode='a'):
        """向yaml文件写入数据"""
        with open(file, encoding=encoding, mode=mode) as f:
            return yaml.dump(data, stream=f, allow_unicode=True)

do_yaml = HandleYaml()
user_accounts = HandleYaml(USER_ACCOUNTS_YAML_PATH)


if __name__ == '__main__':
    do_yaml = HandleYaml()
    print(do_yaml.get_data("log", "handle_formate"))
    data = {"login_token":{"token":"123"},}
    # do_yaml.write_yaml(CONFIG_PATH_YAML,data)
    do_yaml.write_yaml(USER_ACCOUNTS_YAML_PATH,data,mode='w')
    a = user_accounts.get_data('invest_use', 'mobilephone')
    print(a)
    print(type(a))

