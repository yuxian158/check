# -*- coding: utf-8 -*-
"""
new Env('爱奇艺');
"""
import hashlib
import json
import os
import random
import re
import string
import time
from urllib.parse import unquote

import requests

from utils import check


class IQIYI:
    name = "爱奇艺"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def parse_cookie(cookie):
        p00001 = re.findall(r"P00001=(.*?);", cookie)[0] if re.findall(r"P00001=(.*?);", cookie) else ""
        p00002 = re.findall(r"P00002=(.*?);", cookie)[0] if re.findall(r"P00002=(.*?);", cookie) else ""
        p00003 = re.findall(r"P00003=(.*?);", cookie)[0] if re.findall(r"P00003=(.*?);", cookie) else ""
        dfp = re.findall(r"dfp=(.*?);", cookie)[0] if re.findall(r"dfp=(.*?);", cookie) else ""
        return p00001, p00002, p00003, dfp

    @staticmethod
    def md5(data):
        return hashlib.md5(bytes(data, encoding="utf-8")).hexdigest()

    def get_sign(self, c, t, e=None):
        buf = []
        for key, value in t.items():
            buf.append("=".join([key, str(value)]))
        if e is not None:
            buf.append(e)
            return self.md5(c.join(buf))
        return c.join(buf)

    @staticmethod
    def user_information(p00001):
        """
        账号信息查询
        """
        time.sleep(3)
        url = "http://serv.vip.iqiyi.com/vipgrowth/query.action"
        params = {"P00001": p00001}
        res = requests.get(url=url, params=params).json()
        if res["code"] == "A00000":
            try:
                res_data = res.get("data", {})
                level = res_data.get("level", 0)  # VIP 等级
                growthvalue = res_data.get("growthvalue", 0)  # 当前 VIP 成长值
                distance = res_data.get("distance", 0)  # 升级需要成长值
                deadline = res_data.get("deadline", "非 VIP 用户")  # VIP 到期时间
                today_growth_value = res_data.get("todayGrowthValue", 0)  # 今日成长值
                msg = [
                    {"name": "VIP 等级", "value": level},
                    {"name": "当前成长", "value": growthvalue},
                    {"name": "今日成长", "value": today_growth_value},
                    {"name": "升级还需", "value": distance},
                    {"name": "VIP 到期", "value": deadline},
                ]
            except Exception as e:
                msg = [
                    {"name": "账号信息", "value": str(e)},
                ]
                print(msg)
        else:
            msg = [
                {"name": "账号信息", "value": res.get("msg")},
            ]
        return msg

    @staticmethod
    def sign(p00001):
        """
        VIP 签到
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {"P00001": p00001, "autoSign": "yes"}
        res = requests.get(url=url, params=params).json()
        if res["code"] == "A00000":
            try:
                cumulate_sign_days_sum = res["data"]["monthlyGrowthReward"]
                msg = [
                    {"name": "当月成长", "value": f"{cumulate_sign_days_sum}成长值"},
                ]
            except Exception as e:
                print(e)
                msg = [{"name": "当月成长", "value": str(e)}]
        else:
            msg = [{"name": "当月成长", "value": res.get("msg")}]
        return msg

    def sign2(self, p00001, p00003):
        sign_date = {
            "agentType": "1",
            "agentversion": "1.0",
            "appKey": "basic_pcw",
            "authCookie": p00001,
            "qyid": self.md5("".join(random.sample(string.ascii_letters + string.digits, 16))),
            "task_code": "natural_month_sign",
            "timestamp": round(time.time() * 1000),
            "typeCode": "point",
            "userId": p00003,
        }
        post_date = {
            "natural_month_sign": {
                "agentType": "1",
                "agentversion": "1",
                "authCookie": p00001,
                "qyid": self.md5("".join(random.sample(string.ascii_letters + string.digits, 16))),
                "taskCode": "iQIYI_mofhr",
                "verticalCode": "iQIYI",
            }
        }
        sign = self.get_sign("|", sign_date, "UKobMjDMsDoScuWOfp6F")
        url = f"https://community.iqiyi.com/openApi/task/execute?{self.get_sign('&', sign_date)}&sign={sign}"
        header = {"Content-Type": "application/json"}
        res = requests.post(url, headers=header, data=json.dumps(post_date)).json()
        if res["code"] == "A00000":
            if res["data"]["code"] == "A0000":
                # quantity = res["data"]["data"]["rewards"][0]["rewardCount"]  # 积分
                # addgrowthvalue = res["data"]["data"]["rewards"][0]["rewardCount"]  # 新增成长值
                # continued = res["data"]["data"]["signDays"]  # 签到天数
                msg = [{"name": "APP 签到", "value": "签到成功"}]
            else:
                msg = [{"name": "APP 签到", "value": f"签到失败:{res['data']['msg']}"}]
        else:
            msg = [{"name": "APP 签到", "value": f"签到失败:{res['message']}"}]
        return msg

    def web_sign(self, p00001, p00003, dfp):
        dfp = dfp.split("@")[0]
        web_sign_date = {
            "agenttype": "1",
            "agentversion": "0",
            "appKey": "basic_pca",
            "appver": "0",
            "authCookie": p00001,
            "channelCode": "sign_pcw",
            "dfp": dfp,
            "scoreType": "1",
            "srcplatform": "1",
            "typeCode": "point",
            "userId": p00003,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "verticalCode": "iQIYI",
        }

        sign = self.get_sign("|", web_sign_date, "DO58SzN6ip9nbJ4QkM8H")
        url = f"https://community.iqiyi.com/openApi/score/add?{self.get_sign('&', web_sign_date)}&sign={sign}"
        res = requests.get(url).json()
        if res["code"] == "A00000":
            if res["data"][0]["code"] == "A0000":
                quantity = res["data"][0]["score"]
                continued = res["data"][0]["continuousValue"]
                msg = [{"name": "WEB 签到", "value": f"积分+{quantity} 累计签到{continued}天"}]

            else:
                msg = [{"name": "WEB 签到", "value": f"网页端签到失败:{res['data'][0]['message']}"}]
        else:
            msg = [{"name": "WEB 签到", "value": f"网页端签到失败:{res['message']}"}]
        return msg

    @staticmethod
    def query_user_task(p00001):
        """
        获取 VIP 日常任务 和 taskCode(任务状态)
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {"P00001": p00001}
        task_list = []
        res = requests.get(url=url, params=params).json()
        if res["code"] == "A00000":
            for item in res["data"]["tasks"]["daily"]:
                task_list.append(
                    {
                        "name": item["name"],
                        "taskCode": item["taskCode"],
                        "status": item["status"],
                        "taskReward": item["taskReward"]["task_reward_growth"],
                    }
                )
        return task_list

    @staticmethod
    def join_task(p00001, task_list):
        """
        遍历完成任务
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/joinTask"
        params = {"P00001": p00001, "taskCode": "", "platform": "bb136ff4276771f3", "lang": "zh_CN"}
        for item in task_list:
            if item["status"] == 2:
                params["taskCode"] = item["taskCode"]
                requests.get(url=url, params=params)

    @staticmethod
    def get_task_rewards(p00001, task_list):
        """
        获取任务奖励
        :return: 返回信息
        """
        url = "https://tc.vip.iqiyi.com/taskCenter/task/getTaskRewards"
        params = {"P00001": p00001, "taskCode": "", "platform": "bb136ff4276771f3", "lang": "zh_CN"}
        growth_task = 0
        for item in task_list:
            if item["status"] == 0:
                params["taskCode"] = item.get("taskCode")
                requests.get(url=url, params=params)
            elif item["status"] == 4:
                requests.get(url="https://tc.vip.iqiyi.com/taskCenter/task/notify", params=params)
                params["taskCode"] = item.get("taskCode")
                requests.get(url=url, params=params)
            elif item["status"] == 1:
                growth_task += item["taskReward"]
        msg = {"name": "任务奖励", "value": f"+{growth_task}成长值"}
        return msg

    @staticmethod
    def draw(draw_type, p00001, p00003):
        """
        查询抽奖次数(必),抽奖
        :param draw_type: 类型。0 查询次数；1 抽奖
        :param p00001: 关键参数
        :param p00003: 关键参数
        :return: {status, msg, chance}
        """
        url = "https://iface2.iqiyi.com/aggregate/3.0/lottery_activity"
        params = {
            "lottery_chance": 1,
            "app_k": "b398b8ccbaeacca840073a7ee9b7e7e6",
            "app_v": "11.6.5",
            "platform_id": 10,
            "dev_os": "8.0.0",
            "dev_ua": "FRD-AL10",
            "net_sts": 1,
            "qyid": "2655b332a116d2247fac3dd66a5285011102",
            "psp_uid": p00003,
            "psp_cki": p00001,
            "psp_status": 3,
            "secure_v": 1,
            "secure_p": "GPhone",
            "req_sn": round(time.time() * 1000),
        }
        if draw_type == 1:
            del params["lottery_chance"]
        res = requests.get(url=url, params=params).json()
        if not res.get("code"):
            chance = int(res.get("daysurpluschance"))
            msg = res.get("awardName")
            return {"status": True, "msg": msg, "chance": chance}
        else:
            try:
                msg = res.get("kv", {}).get("msg")
            except Exception as e:
                print(e)
                msg = res["errorReason"]
        return {"status": False, "msg": msg, "chance": 0}

    def main(self):
        p00001, p00002, p00003, dfp = self.parse_cookie(self.check_item.get("cookie"))
        sign_msg = self.sign(p00001=p00001)
        web_sign_msg = self.web_sign(p00001=p00001, p00003=p00003, dfp=dfp)
        sign2_msg = self.sign2(p00001=p00001, p00003=p00003)
        chance = self.draw(0, p00001=p00001, p00003=p00003)["chance"]
        if chance:
            draw_msg = ""
            for i in range(chance):
                ret = self.draw(1, p00001=p00001, p00003=p00003)
                draw_msg += ret["msg"] + ";" if ret["status"] else ""
        else:
            draw_msg = "抽奖机会不足"
        task_msg = ""
        for one in range(6):
            task_list = self.query_user_task(p00001=p00001)
            self.join_task(p00001=p00001, task_list=task_list)
            time.sleep(10)
            task_msg = self.get_task_rewards(p00001=p00001, task_list=task_list)
        try:
            user_info = json.loads(unquote(p00002, encoding="utf-8"))
            user_name = user_info.get("user_name")
            user_name = user_name.replace(user_name[3:7], "****")
            nickname = user_info.get("nickname")
        except Exception as e:
            print(f"获取账号信息失败，错误信息: {e}")
            nickname = "未获取到，请检查 Cookie 中 P00002 字段"
            user_name = "未获取到，请检查 Cookie 中 P00002 字段"
        user_msg = self.user_information(p00001=p00001)

        msg = (
                [
                    {"name": "用户账号", "value": user_name},
                    {"name": "用户昵称", "value": nickname},
                ]
                + user_msg
                + sign_msg
                + web_sign_msg
                + sign2_msg
                + [
                    task_msg,
                    {"name": "抽奖奖励", "value": draw_msg},
                ]
        )
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


@check(run_script_name="爱奇艺",run_script_expression="IQIYI|爱奇艺")
def main(*args, **kwargs):
    return IQIYI(check_item=kwargs.get("value")).main()


if __name__ == "__main__":
    main()
