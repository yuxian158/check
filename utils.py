import json
import os
import random
import re
import time
import traceback
# import tomli_w
from functools import wraps

import tomli

from checksendNotify import send


def toml_to_json(toml_path, to_json_path):
    """
    :param toml_path: 需要转换的toml文件的路径
    :param to_json_path: 需要输出的json文件路径
    :return: NONE
    """
    with open(toml_path, "rb") as f:
        toml_dict = tomli.load(f)
        json_date = json.dumps(toml_dict, indent=4, ensure_ascii=False)
        with open(to_json_path, 'w', encoding="utf8") as s:
            s.write(json_date)


# def json_to_toml(json_path, to_toml_path):
#     with open(json_path, "r", encoding="utf8") as f:
#         json_dict = json.load(f)
#         with open(to_toml_path, "wb") as f:
#             tomli_w.dump(json_dict, f)

class config_get(object):
    def __init__(self, config_path=None):
        """
        config_path: 自定义配置文件路径
        config_file: 实际使用的配置文件路径
        config_format: 实际使用的配置文件格式
        """
        self.config_path = config_path
        self.config_file = self.get_config_file()
        self.config_format = self.get_config_format()

    def get_config_format(self):
        if self.config_file.endswith('.toml'):
            return "toml"
        else:
            return "json"

    def get_config_file(self):
        ql_new = '/ql/config/env.sh'
        json_config_file = '/ql/config/check.json'
        toml_config_file = '/ql/config/check.toml'
        print('开始检查环境\n')
        if os.path.exists(ql_new):
            print('成功 当前环境为青龙面板继续执行\n')
            if self.config_path is not None:
                print("使用了自定义路径的配置文件")
                return self.config_path
            elif os.path.exists(toml_config_file):
                print("未使用自定义配置文件,开始从ql/config中检测")
                print("检测到toml格式配置文件\n")
                return toml_config_file
            elif os.path.exists(json_config_file):
                print("检测到json格式配置文件\n")
                return json_config_file
            else:
                print("未检测到配置文件，程序退出")
                exit(1)
        else:
            print('失败 请检查环境')
            exit(0)
            return 0

    def get_real_key(self, expression):
        """
        从配置文件中获取，re表达式想要的KEY
        :return:
        """
        pattern = re.compile(expression, re.I)
        real_key = ''
        if self.config_format == "toml":
            for key in self.get_key_for_toml(self.config_file):
                if pattern.match(key) is not None:
                    real_key = key
        else:
            for key in self.get_key_for_json(self.config_file):
                if pattern.match(key) is not None:
                    real_key = key
        if real_key is not '':
            return real_key
        else:
            print("啊哦没有找到")
            exit(1)

    def get_value(self, expression):
        real_key = self.get_real_key(expression)
        if self.config_format == "toml":
            return self.get_value_for_toml(self.config_file, real_key)
        else:
            return self.get_value_for_json(self.config_file, real_key)

    @staticmethod
    def get_value_for_toml(toml_path, key):
        with open(toml_path, "rb") as f:
            try:
                toml_dict = tomli.load(f)
                return toml_dict.get(key)
            except tomli.TOMLDecodeError:
                print(
                    f"错误：配置文件 {toml_path} 格式不对，请学习 https://toml.io/cn/v1.0.0\n错误信息：\n{traceback.format_exc()}"
                )
                exit(1)

    @staticmethod
    def get_value_for_json(json_path, key):
        with open(json_path, "r", encoding="utf8") as f:
            try:
                json_dict = json.load(f)
                return json_dict.get(key)
            except json.decoder.JSONDecodeError:
                print(f"错误：配置文件 {json_path} 格式不对，错误信息{traceback.format_exc()}")

    @staticmethod
    def get_key_for_toml(toml_path):
        with open(toml_path, "rb") as f:
            try:
                toml_dict = tomli.load(f)
                return toml_dict.keys()
            except tomli.TOMLDecodeError:
                print(
                    f"错误：配置文件 {toml_path} 格式不对，请学习 https://toml.io/cn/v1.0.0\n错误信息：\n{traceback.format_exc()}"
                )
                exit(1)

    @staticmethod
    def get_key_for_json(json_path):
        with open(json_path, "r", encoding="utf8") as f:
            try:
                json_dict = json.load(f)
                return json_dict.keys()
            except json.decoder.JSONDecodeError:
                print(f"错误：配置文件 {json_path} 格式不对，错误信息{traceback.format_exc()}")


class check(object):
    def __init__(self, run_script_name, run_script_expression, Configuration_flag=False):
        """
        :param run_script_name: 执行脚本的说明
        :param run_script_expression: 需要获取的配置键的re表达式
        :param Configuration_flag: 是否只检测True或False(默认为False)
        """
        self.run_script_name = run_script_name
        self.run_script_expression = run_script_expression
        self.Configuration_flag = Configuration_flag

    @staticmethod
    def other_task():
        change_db()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.Configuration_flag:
                config = config_get()
                value_list = config.get_value(self.run_script_expression)
                Push_message = ""
                num = 1
                for value in value_list:
                    print(f"<----------------账号【{num}】---------------->")
                    print(f"获取到的账号信息为:{value}\n")
                    num += 1
                    try:
                        result = func(value=value)
                        print(f"执行结果:\n{result}")
                        Push_message += result
                    except IndexError:
                        print("可能是示例格式被运行\n错误信息:")
                        print(f"{traceback.format_exc()}")
                        Push_message += ''
                    except AttributeError:
                        print("可能是配置文件的键名出现问题\n"
                              "例如:在此次更新中什么值得买的键名从smzdm_cookie变成了cookie\n")
                        print(f"{traceback.format_exc()}")
                        Push_message += ''
                    except TypeError:
                        print(f"{traceback.format_exc()}")
                        Push_message += ''
                send(self.run_script_name, Push_message)
            else:
                config = config_get()
                flag = config.get_value(self.run_script_expression)
                if flag is not None and flag:
                    print(f"开始执行{self.run_script_name}")
                    func()
                else:
                    print(f"设置为不执行{self.run_script_name}")

        return wrapper


def change_cron(cron_file_path="/ql/db/crontab.db",repositories="yuxian158_check"):
    def change_time(time_str: str):
        words = re.sub("\\s+", " ", time_str).split()
        words[0] = str(random.randrange(60))
        words[1] = str(random.randrange(22))
        return " ".join(words)

    time_str = time.strftime("%Y-%m-%d", time.localtime())
    os.system(f"cp /ql/db/crontab.db /ql/db/crontab.db.{time_str}.back")
    lines = []
    with open(cron_file_path, "r" ,encoding="UTF-8") as f:
        for i in f.readlines():
            # print(record.get("command"))
            if i.find(repositories) != -1:
                record = json.loads(i)
                record["schedule"] = change_time(record["schedule"])
                lines.append(json.dumps(record, ensure_ascii=False) + "\n")
            else:lines.append(i)

    with open(cron_file_path, "w", encoding="UTF-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    change_cron()
