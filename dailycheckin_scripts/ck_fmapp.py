# -*- coding: utf-8 -*-
"""
new Env('米家');
"""
import json

import requests

from utils import check


class FMAPP:
    name = "Fa米家"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/market/member/signin/sign"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = (
                    f"在坚持{data.get('nextDay')}天即可获得{data.get('nextNumber')}个发米粒, "
                    f"签到{data.get('lastDay')}天可获得{data.get('lastNumber')}个发米粒"
                )
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        msg = {"name": "签到信息", "value": msg}
        return msg

    @staticmethod
    def user_info(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/info"
            response = requests.post(url=url, headers=headers).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("nickName")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        msg = {"name": "帐号信息", "value": msg}
        return msg

    @staticmethod
    def mili_count(headers):
        try:
            url = "https://fmapp.chinafamilymart.com.cn/api/app/member/v1/mili/service/detail"
            response = requests.post(url=url, headers=headers, data=json.dumps({"pageSize": 10, "pageNo": 1})).json()
            code = response.get("code")
            if code == "200":
                data = response.get("data", {})
                msg = data.get("miliNum")
            else:
                msg = response.get("message")
        except Exception as e:
            print("错误信息", str(e))
            msg = "未知错误，检查日志"
        msg = {"name": "米粒数量", "value": msg}
        return msg

    def main(self):
        token = self.check_item.get("token")
        cookie = self.check_item.get("cookie")
        blackbox = self.check_item.get("blackbox")
        device_id = self.check_item.get("device_id")
        fmversion = self.check_item.get("fmversion", "2.2.3")
        fm_os = self.check_item.get("os", "ios")
        useragent = self.check_item.get("useragent", "Fa")
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-Hans;q=1.0",
            "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
            "Host": "fmapp.chinafamilymart.com.cn",
            "Content-Type": "application/json",
            "loginChannel": "app",
            "token": token,
            "fmVersion": fmversion,
            "deviceId": device_id,
            "User-Agent": useragent,
            "os": fm_os,
            "cookie": cookie,
            "blackBox": blackbox,
        }
        sign_msg = self.sign(headers=headers)
        name_msg = self.user_info(headers=headers)
        mili_msg = self.mili_count(headers=headers)
        msg = [name_msg, sign_msg, mili_msg]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="米家", run_script_expression="fmapp|米家")
def main(*args, **kwargs):
    return FMAPP(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
