# **目标**：每日定时自动分析并推送到微信。

import requests # 导入requests库，用于发送HTTP请求
from app import config  # 导入配置模块，用于获取环境变量

def push_wechat(title: str, content: str):
    key = config.SERVERCHAN_KEY
    if not key:
        print("未配置 SERVERCHAN_KEY，跳过推送")
        return {"code": -1}
    resp = requests.post(f"https://sctapi.ftqq.com/{key}.send",
                         data={"title": title, "desp": content}, timeout=10)
    return resp.json()