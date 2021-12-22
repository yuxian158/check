# -*- coding: utf-8 -*-
"""
new Env('吾爱破解');
"""
from utils import check
import re

import requests


class Pojie:
    name = "吾爱破解"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(headers):
        msg = ""
        try:
            session = requests.session()
            session.get(url="https://www.52pojie.cn/home.php?mod=task&do=apply&id=2", headers=headers)
            resp = session.get(url="https://www.52pojie.cn/home.php?mod=task&do=draw&id=2", headers=headers)
            content = re.findall(r'<div id="messagetext".*?\n<p>(.*?)</p>', resp.text)[0]
            if "您需要先登录才能继续本操作" in resp.text:
                msg += "吾爱破解 cookie 失效"
            elif "安域防护节点" in resp.text:
                msg += "触发吾爱破解安全防护，访问出错。自行修改脚本运行时间和次数，总有能访问到的时间"
            elif "恭喜" in resp.text:
                msg += "吾爱破解签到成功"
            else:
                msg += content
        except Exception as e:
            print("签到错误", e)
            msg += "吾爱破解出错"
        return msg

    def main(self):
        cookie = self.check_item.get("cookie")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "Cookie": cookie,
            "ContentType": "text/html;charset=gbk",
        }
        try:
            uid = re.findall(r"htVD_2132_lastcheckfeed=(.*?);", cookie)[0].split("%7C")[0]
        except Exception as e:
            print(e)
            uid = "未获取到用户 uid"
        sign_msg = self.sign(headers=headers)
        msg = [
            {"name": "帐号信息", "value": f"{uid}"},
            {"name": "签到信息", "value": f"{sign_msg}"},
        ]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg

@check(run_script_name="吾爱破解", run_script_expression="POJIE")
def main(*args, **kwargs):
    return Pojie(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
