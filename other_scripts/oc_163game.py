# -*- coding: utf-8 -*-
"""
cron: 20 8 * * *
new Env('网易云游戏');
"""

from utils import check
import requests


class Game163:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def checkin(authorization):
        url = "http://n.cg.163.com/api/v2/sign-today"
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi K30 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36",
            "authorization": authorization,
        }
        r = requests.post(url, headers=headers).text
        if r[0] == "{":
            return "cookie 已失效"
        else:
            return "签到成功"

    def main(self):
        msg_all = ""
        authorization = str(self.check_items.get("authorization"))
        msg = self.checkin(authorization=authorization)
        msg_all += msg + "\n\n"
        return msg_all


@check(run_script_name="网易云游戏", run_script_expression="GAME163")
def main(*args, **kwargs):
    return Game163(check_items=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
