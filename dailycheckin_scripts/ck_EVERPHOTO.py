# -*- coding: utf-8 -*-
"""
new Env('时光相册');
"""
import requests

from utils import check


class EverPhoto:
    name = "时光相册"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(mobile, password):
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
            "accept": "*/*",
            "origin": "https://web.everphoto.cn",
            "referer": "https://web.everphoto.cn/",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

        data = {"mobile": mobile, "password": password}
        try:
            response = requests.post(url="https://web.everphoto.cn/api/auth", headers=headers, data=data).json()
            if response.get("code") == 0:
                data = response.get("data")
                token = data.get("token")
                mobile = data.get("user_profile", {}).get("mobile")
                return token, {"name": "账号信息", "value": mobile}
            else:
                return False, {"name": "账号信息", "value": "登录失败"}
        except Exception as e:
            return False, {"name": "账号信息", "value": "登录失败"}

    @staticmethod
    def checkin(token):
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
            "accept": "*/*",
            "origin": "https://web.everphoto.cn",
            "authorization": f"Bearer {token}",
            "referer": "https://web.everphoto.cn/",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        try:
            response = requests.post(url="https://api.everphoto.cn/users/self/checkin/v2", headers=headers).json()
            if response.get("code") == 0:
                data = response.get("data")
                checkin_result = data.get("checkin_result")
                if checkin_result:
                    return {"name": "签到信息", "value": "签到成功"}
                else:
                    return {"name": "签到信息", "value": "已签到过或签到失败"}
            else:
                return {"name": "签到信息", "value": "签到失败"}
        except Exception as e:
            return {"name": "签到信息", "value": "签到失败"}

    def main(self):
        mobile = self.check_item.get("mobile")
        password = self.check_item.get("password")
        token, sign_msg = self.sign(mobile=mobile, password=password)
        msg = [sign_msg]
        if token:
            checkin_msg = self.checkin(token=token)
            msg.append(checkin_msg)
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="时光相册", run_script_expression="EVERPHOTO|时光")
def main(*args, **kwargs):
    return EverPhoto(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
