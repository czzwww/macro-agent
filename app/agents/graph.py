from typing import TypedDict
from langgraph.graph import StateGraph, END # 用于定义状态图 ，END 表示结束节点
from app.agents import interpret, allocate, risk
from app.tools import registry

class MacroState(TypedDict):
    task: str
    raw: dict
    news: str
    interpretation: dict
    allocation: dict
    risk: dict

def fetch_node(state):
    raw = registry.run_tool("get_macro_snapshot", {})
    news = registry.run_tool("search_news", {"query": "宏观 货币政策 经济数据"})
    return {"raw": raw, "news": news}

def interpret_node(state):
    return {"interpretation": interpret.interpret(state["raw"], state["news"])}

def allocate_node(state):
    return {"allocation": allocate.allocate(state["interpretation"])}

def risk_node(state):
    return {"risk": risk.risk_check(state["interpretation"], state["allocation"])}

def route_after_fetch(state):
    vals = [v for v in state["raw"].values() if "失败" not in v]
    return "degrade" if not vals else "interpret"

def degrade_node(state):
    return {"interpretation": {"cycle_position": "数据获取失败，无法给出可靠配置建议"},
            "allocation": {"weights": {"股票": 0, "债券": 0, "商品": 0, "现金": 1},
                           "summary": "建议持有现金观望，数据恢复后再分析"},
            "risk": {"risks": ["数据缺失"], "conclusion": "降级模式"}}

def final_node(state):
    return state

g = StateGraph(MacroState)  # 定义状态图，状态类型为 MacroState
g.add_node("fetch", fetch_node)
g.add_node("interpret", interpret_node)
g.add_node("allocate", allocate_node)
g.add_node("risk", risk_node)
g.add_node("degrade", degrade_node)
g.add_node("final", final_node)
g.set_entry_point("fetch")
g.add_conditional_edges("fetch", route_after_fetch,
                        {"interpret": "interpret", "degrade": "degrade"})
g.add_edge("interpret", "allocate")
g.add_edge("allocate", "risk")
g.add_edge("risk", "final")
g.add_edge("degrade", "final")
g.add_edge("final", END)
app_graph = g.compile()

def run_analysis():
    return app_graph.invoke({"task": "今天该配什么？"})