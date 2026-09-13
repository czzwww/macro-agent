import schedule, time, threading    # 导入schedule库，用于定时任务
import time # 导入time库，用于线程休眠
import threading # 导入threading库，用于创建线程
from app.agents.graph import run_analysis   # 导入分析函数
from app.notifier import push_wechat  # 导入推送微信函数
from app import db  # 导入数据库模块

def daily_job():
    result = run_analysis()
    db.save_history(result)
    w = result["allocation"]["weights"]
    lines = [
        "📊 今日大类资产配置建议",
        f"- 股票 {w.get('股票',0)*100:.0f}%  债券 {w.get('债券',0)*100:.0f}%",
        f"- 商品 {w.get('商品',0)*100:.0f}%  现金 {w.get('现金',0)*100:.0f}%",
        f"- 周期判断：{result['interpretation'].get('cycle_position','')}",
        f"- 结论：{result['allocation'].get('summary','')}",
    ]
    push_wechat("每日宏观配置建议", "\n".join(lines))

def start_scheduler():
    schedule.every().day.at("08:00").do(daily_job)
    def _loop():
        while True:
            schedule.run_pending()
            time.sleep(60)
    threading.Thread(target=_loop, daemon=True).start()