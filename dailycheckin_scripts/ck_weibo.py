# -*- coding: utf-8 -*-
"""
new Env('微博');
"""
from urllib import parse

import requests
import urllib3

from utils import check

urllib3.disable_warnings()


class WeiBo:
    name = "微博"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def sign(token):
        headers = {"User-Agent": "Weibo/52588 (iPhone; iOS 14.5; Scale/3.00)"}
        response = requests.get(
            url=f"https://api.weibo.cn/2/checkin/add?c=iphone&{token}", headers=headers, verify=False
        )
        result = response.json()
        if result.get("status") == 10000:
            msg = [
                {"name": "连续签到", "value": f'{result.get("data").get("continuous")}天'},
                {"name": "本次收益", "value": result.get("data").get("desc")},
            ]
        elif result.get("errno") == 30000:
            msg = [
                {"name": "每日签到", "value": "已签到"},
            ]
        elif result.get("status") == 90005:
            msg = [
                {"name": "每日签到", "value": result.get("msg")},
            ]
        else:
            msg = [
                {"name": "每日签到", "value": "签到失败"},
            ]
        return msg

    @staticmethod
    def card(token):
        headers = {"User-Agent": "Weibo/52588 (iPhone; iOS 14.5; Scale/3.00)"}
        response = requests.get(
            url=f"https://api.weibo.cn/2/!/ug/king_act_home?c=iphone&{token}", headers=headers, verify=False
        )
        result = response.json()
        if result.get("status") == 10000:
            nickname = result.get("data").get("user").get("nickname")
            msg = [
                {"name": "用户昵称", "value": nickname},
                {"name": "每日打卡", "value": f'{result.get("data").get("signin").get("title").split("<")[0]}天'},
                {"name": "积分总计", "value": result.get("data").get("user").get("energy")},
            ]
        else:
            msg = [
                {"name": "每日打卡", "value": "活动过期或失效"},
            ]
        return msg

    @staticmethod
    def pay(token):
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "pay.sc.weibo.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Weibo (iPhone10,1__weibo__11.2.1__iphone__os14.5)",
        }
        data = token + "&lang=zh_CN&wm=3333_2001"
        response = requests.post(
            url=f"https://pay.sc.weibo.com/aj/mobile/home/welfare/signin/do", headers=headers, data=data, verify=False
        )
        try:
            result = response.json()
            if result.get("status") == 1:
                msg = [
                    {"name": "微博钱包", "value": f'{result.get("score")} 积分'},
                ]
            elif result.get("status") == 2:
                msg = [
                    {"name": "微博钱包", "value": f"已签到"},
                ]
                info_response = requests.post(
                    url="https://pay.sc.weibo.com/api/client/sdk/app/balance", headers=headers, data=data
                )
                info_result = info_response.json()
                msg += [
                    {"name": "当前现金", "value": f"{info_result.get('data').get('balance')} 元"},
                ]
            else:
                msg = [
                    {"name": "微博钱包", "value": f"Cookie失效"},
                ]
            return msg
        except Exception as e:
            msg = [
                {"name": "微博钱包", "value": f"Cookie失效"},
            ]
            return msg

    def main(self):
        url = self.check_item.get("url")
        query_dict = dict(parse.parse_qsl(parse.urlsplit(url).query))
        token = "&".join([f"{key}={value}" for key, value in query_dict.items() if key in ["from", "uid", "s", "gsid"]])
        sign_msg = self.sign(token=token)
        card_msg = self.card(token=token)
        pay_msg = self.pay(token=token)
        msg = sign_msg + card_msg + pay_msg
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="微博", run_script_expression="WEIBO")
def main(*args, **kwargs):
    return WeiBo(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
