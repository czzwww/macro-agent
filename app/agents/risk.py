import json
from app import config
from openai import OpenAI

_client = OpenAI(api_key=config.OPENAI_API_KEY, base_url=config.OPENAI_BASE_URL)

SYSTEM = """你是风控复核员。检查配置建议，输出 JSON：
{"risks": ["风险点",...], "adjustments": ["调整建议",...], "conclusion": "复核结论"}
关注：单类权重是否过高(>70%)、数据是否有缺失导致置信度低、
是否提醒"不构成投资建议"。"""

def risk_check(interpretation: dict, allocation: dict) -> dict:
    r = _client.chat.completions.create(
        model=config.MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user",
                   "content": f"宏观解读：{json.dumps(interpretation, ensure_ascii=False)}\n配置建议：{json.dumps(allocation, ensure_ascii=False)}"}],
        temperature=0.2,
    )
    return json.loads(r.choices[0].message.content)