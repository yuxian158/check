# -*- coding: utf-8 -*-
"""
new Env('芒果TV');
"""
import json
import time
from urllib import parse

import requests

from utils import check


class Mgtv:
    name = "芒果TV"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(params):
        url = "https://credits.bz.mgtv.com/user/creditsTake"
        user_params = {
            "abroad": params.get("abroad"),
            "ageMode": "0",
            "appVersion": params.get("appVersion"),
            "artistId": params.get("uuid"),
            "device": params.get("device"),
            "did": params.get("did"),
            "mac": params.get("did"),
            "osType": params.get("osType"),
            "src": "mgtv",
            "testversion": "",
            "ticket": params.get("ticket"),
            "uuid": params.get("uuid"),
        }
        try:
            user_info = requests.get(url="https://homepage.bz.mgtv.com/v2/user/userInfo", params=user_params).json()
            username = user_info.get("data", {}).get("nickName")
        except Exception as e:
            print("获取账号信息失败", e)
            username = params.get("uuid")
        res = requests.get(url=url, params=params)
        res_json = json.loads(res.text.replace(f"{params.get('callback')}(", "").replace(");", ""))
        if res_json["code"] == 200:
            cur_day = res_json["data"]["curDay"]
            _credits = res_json["data"]["credits"]
            msg = [
                {"name": "帐号信息", "value": username},
                {"name": "签到积分", "value": f"{_credits}积分"},
                {"name": "已经签到", "value": f"{cur_day}天/21天"},
            ]
        else:
            msg = [
                {"name": "帐号信息", "value": username},
                {"name": "签到信息", "value": f"已完成签到 or 签到失败"},
            ]
        return msg

    def main(self):
        mgtv_params = self.check_item.get("params")
        params = parse.parse_qs(mgtv_params)
        params["timestamp"] = [round(time.time())]
        params = {key: value[0] for key, value in params.items()}
        msg = self.sign(params=params)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="芒果TV",run_script_expression="MGTV")
def main(*args, **kwargs):
    return Mgtv(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()

