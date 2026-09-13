MCP_TOOLS = {
    "get_macro_snapshot": {
        "name": "get_macro_snapshot",
        "description": "获取最新宏观数据快照（PMI/CPI/PPI/M2/Shibor/GDP）",
        "inputSchema": {"type": "object",
                        "properties": {"indicator_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "指标名列表，如 ['PMI','CPI']"}},
                        "required": []},
    },
    "search_news": {
        "name": "search_news",
        "description": "搜索最新财经新闻与舆情",
        "inputSchema": {"type": "object",
                        "properties": {"query": {"type": "string",
                                                 "description": "搜索关键词"},
                                       "max_results": {"type": "integer",
                                                       "description": "返回条数"}},
                        "required": ["query"]},
    },
}