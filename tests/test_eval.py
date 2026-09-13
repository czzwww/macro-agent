# **目标**：量化验证质量，产出**指标报告**（简历数字来源）。

# **评估维度**：数据获取成功率、评测通过率、平均耗时、推送成功率。
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, time
from app.agents import interpret, allocate, risk
from app.tools import registry

CASES = [
    ({"M2": "M2 增速 12%，连续 3 个月回升", "Shibor": "Shibor 下行至 1.5%",
      "社融": "社融放量 2.1 万亿"}, "宽松", "宽松"),
    ({"M2": "M2 增速 6%，收缩", "Shibor": "Shibor 上行至 2.8%",
      "社融": "社融萎缩"}, "收紧", "收紧"),
]

def run_eval():
    report = {"总用例": len(CASES), "通过": 0, "分类": {}}
    total_time = 0.0
    for data, want_m, want_c in CASES:
        t0 = time.time()
        out = interpret.interpret(data)
        total_time += time.time() - t0
        ok = (want_m in out.get("money", "")) and (want_c in out.get("credit", ""))
        report["通过"] += int(ok)
        print(f"{'✓' if ok else '✗'} 期望={want_m}/{want_c} 实际={out.get('money')}/{out.get('credit')}")
    report["通过率"] = f"{report['通过']}/{report['总用例']}"
    report["平均耗时_s"] = round(total_time / len(CASES), 2)
    # 数据获取成功率
    snap = registry.run_tool("get_macro_snapshot", {})
    ok_n = sum(1 for v in snap.values() if "失败" not in v)
    report["数据获取成功率"] = f"{ok_n}/{len(snap)}"
    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("报告已写入 metrics.json")
    return report

if __name__ == "__main__":
    print(run_eval())