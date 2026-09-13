import time
from app.tools import macro_data, search

REGISTRY = {
    "get_macro_indicator": macro_data.get_macro_indicator,
    "get_macro_snapshot": macro_data.get_macro_snapshot,
    "search_news": search.search_news,
}

SCHEMA = {
    "get_macro_indicator": ["name"],
    "get_macro_snapshot": [],
    "search_news": ["query"],
}

def run_tool(name: str, args: dict, max_retry: int = 2):
    if name not in REGISTRY:
        return f"错误：未知工具 {name}"
    for required in SCHEMA.get(name, []):
        if required not in args:
            return f"参数错误：缺少 {required}"
    for attempt in range(1, max_retry + 1):
        try:
            return REGISTRY[name](**args)
        except Exception as e:
            if attempt == max_retry:
                return f"[失败] {name}: {e}"
            time.sleep(0.5 * attempt)
    return "[失败]"