# -*- coding: utf-8 -*-
"""
new Env('智友邦');
"""
from utils import check
import json
import os
import re

import requests
import urllib3
from requests import utils

urllib3.disable_warnings()


class ZhiYoo:
    name = "智友邦"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(session):
        response = session.get(url="http://bbs.zhiyoo.net/plugin.php?id=dsu_paulsign:sign", verify=False)
        formhash = re.findall(r'<input type="hidden" name="formhash" value="(.*?)"', response.text)[0]
        params = (
            ("id", "dsu_paulsign:sign"),
            ("operation", "qiandao"),
            ("infloat", "1"),
            ("inajax", "1"),
        )
        data = {"formhash": formhash, "qdxq": "kx"}
        response = session.post(url="http://bbs.zhiyoo.net/plugin.php", params=params, data=data, verify=False)
        user_rep = session.get(url="http://bbs.zhiyoo.net/home.php")
        uid = re.findall(r"uid=(\d+)\"", user_rep.text)
        uid = uid[0] if uid else "未获取到 UID"
        if "今日已经签到" in response.text:
            msg = [
                {"name": "账号信息", "value": uid},
                {"name": "签到信息", "value": "您今日已经签到，请明天再来！"},
            ]
        else:
            check_msg = re.findall(r"恭喜你签到成功!获得随机奖励 金币 (\d+) 元.", response.text, re.S)
            check_msg = check_msg[0].strip() if check_msg else "签到失败"
            msg = [
                {"name": "账号信息", "value": uid},
                {"name": "签到信息", "value": f"恭喜你签到成功!获得随机奖励 金币 {check_msg} 元."},
            ]
        return msg

    def main(self):
        zhiyoo_cookie = {item.split("=")[0]: item.split("=")[1] for item in self.check_item.get("cookie").split("; ")}
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, zhiyoo_cookie)
        session.headers.update(
            {
                "Origin": "http://bbs.zhiyoo.net",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Referer": "http://bbs.zhiyoo.net/plugin.php?id=dsu_paulsign:sign",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )
        msg = self.sign(session=session)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="智友邦", run_script_expression="ZHIYOO")
def main(*args, **kwargs):
    return ZhiYoo(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
