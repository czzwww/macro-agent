# **目标**：把原始数据解读成「货币信用四象限」定位，JSON 输出，禁止编造。

import json
from app import config
from openai import OpenAI

_client = OpenAI(api_key=config.OPENAI_API_KEY, base_url=config.OPENAI_BASE_URL)

SYSTEM = """你是宏观经济学家。根据给定的宏观数据，判断当前货币信用状态。
只允许基于提供的数据，数据没有的项标注"未知"。
输出 JSON：
{"growth":"扩张|收缩|未知","inflation":"高|低|未知",
 "money":"宽松|收紧|中性|未知","credit":"宽松|收紧|中性|未知",
 "cycle_position":"对当前周期的中文判断（2-3句话）"}"""

def interpret(data_snapshot: dict, news: str = "") -> dict:
    material = json.dumps(data_snapshot, ensure_ascii=False)
    prompt = f"""宏观数据如下：
{material}

最新新闻（供参考）：
{news}

请给出 JSON 解读。"""
    r = _client.chat.completions.create(
        model=config.MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return json.loads(r.choices[0].message.content)