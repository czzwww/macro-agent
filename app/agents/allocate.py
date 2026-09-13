# **目标**：输出股/债/商品/现金权重，加总必须 100%，含自动归一化兜底。

import json # `json` 模块用于解析 JSON 字符串
from app import config  # 导入配置模块
from openai import OpenAI  # 导入 OpenAI 客户端模块 : 用于与 OpenAI API 交互

_client = OpenAI(api_key=config.OPENAI_API_KEY, base_url=config.OPENAI_BASE_URL)

RULES = """货币信用四象限对应倾向（仅作参考基准）：
- 宽货币+宽信用：股票、商品偏多
- 宽货币+紧信用：债券偏多
- 紧货币+宽信用：股票偏多，注意债券压力
- 紧货币+紧信用：现金为主，防御"""

SYSTEM = f"""你是大类资产配置专家。根据宏观解读给出配置建议。
{RULES}
硬性要求：
1. 输出 JSON：{{"weights": {{"股票":0,"债券":0,"商品":0,"现金":0}},
    "reasons": {{"股票":"理由",...}}, "summary": "一句话总结"}}
2. 四个权重是 0-1 小数，相加严格等于 1.0"""

def allocate(interpretation: dict) -> dict:
    r = _client.chat.completions.create(
        model=config.MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user",
                   "content": f"宏观解读：{json.dumps(interpretation, ensure_ascii=False)}"}],
        temperature=0.2,
    )
    result = json.loads(r.choices[0].message.content)
    w = result["weights"]
    s = sum(w.values())
    if abs(s - 1.0) > 0.02:
        result["weights"] = {k: round(v / s, 3) for k, v in w.items()}
        result["warnings"] = "权重已自动归一化"
    return result