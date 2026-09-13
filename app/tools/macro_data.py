import akshare as ak
from app import db

FETCHERS = {
    "PMI": ak.macro_china_pmi,
    "CPI": ak.macro_china_cpi_yearly,
    "PPI": ak.macro_china_ppi_yearly,
    "M2": ak.macro_china_money_supply,
    "Shibor": ak.macro_china_shibor_all,
    "GDP": ak.macro_china_gdp_yearly,
}

def _latest_rows_to_text(name, df, n=1):
    rows = df.tail(n)
    return f"[{name}]\n" + rows.to_string()

def get_macro_indicator(name: str) -> str:
    cached = db.get_cache(f"macro_{name}")  # 从缓存中获取
    if cached:
        return cached
    fn = FETCHERS.get(name)  # 从字典中获取函数
    if fn is None:
        return f"{name}: 未知指标"
    try:
        df = fn()
        text = _latest_rows_to_text(name, df)
        db.set_cache(f"macro_{name}", text)  # 缓存结果
        return text
    except Exception as e:
        return f"{name}: 获取失败（{e}）"   # 降级，不中断流程

def get_macro_snapshot(indicator_names=None):
    names = indicator_names or list(FETCHERS.keys())
    return {n: get_macro_indicator(n) for n in names}