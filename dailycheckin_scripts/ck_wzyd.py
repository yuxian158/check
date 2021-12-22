# -*- coding: utf-8 -*-
"""
new Env('王者营地');
"""
from urllib import parse

import requests

from utils import check


class WZYD:
    name = "王者营地"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(data):
        response = requests.post(url="https://ssl.kohsocialapp.qq.com:10001/play/h5sign", data=data).json()
        try:
            if response["result"] == 0:
                msg = "签到成功"
            else:
                msg = response["returnMsg"]
        except:
            msg = "请求失败,请检查接口"
        return msg

    def main(self):
        wzyd_data = self.check_item.get("data")
        data = {k: v[0] for k, v in parse.parse_qs(wzyd_data).items()}
        try:
            user_id = data.get("userId", "")
        except Exception as e:
            print(f"获取账号信息失败: {e}")
            user_id = "未获取到账号信息"
        sign_msg = self.sign(data=data)
        msg = [
            {"name": "帐号信息", "value": user_id},
            {"name": "签到信息", "value": sign_msg},
        ]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="王者营地",run_script_expression="WZYD")
def main(*args, **kwargs):
    return WZYD(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()

