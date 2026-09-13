import requests
from app import config, db
BOCHA_URL = "https://api.bochaai.com/v1/web-search"

def search_news(query: str, max_results: int = 5) -> str:
    cached = db.get_cache(f"search_{query}_{max_results}", max_age_hours=6)
    if cached:
        return cached
    try:
        resp = requests.post(
            BOCHA_URL,
            headers={
                "Authorization": f"Bearer {config.BOCHA_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"query": query, "summary": True, "count": max_results},
            timeout=15,
        )
        resp.raise_for_status()
        pages = resp.json().get("data", {}).get("webPages", {}).get("value", [])
        items = [f"- {it.get('name', '')}: {it.get('snippet', '')[:150]}"
                 for it in pages]
        text = f"关于「{query}」的最新新闻：\n" + "\n".join(items)
        db.set_cache(f"search_{query}_{max_results}", text)
        return text
    except Exception as e:
        return f"搜索失败：{type(e).__name__}: {e}"