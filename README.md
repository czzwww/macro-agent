# 宏观资产配置 Agent

基于 LangGraph 多智能体流水线的自主宏观资产配置工具：自主联网搜索宏观数据与舆情，
结合货币信用框架解读经济周期，输出股/债/商品/现金配置建议，每日定时推送微信。

## 技术亮点
- LangGraph 四节点多智能体编排（数据→解读→配置→风控），含数据失败降级
- 统一工具系统 + MCP 格式工具声明（AKShare 宏观数据 + 博查 舆情搜索）
- 结构化 JSON 输出 + 权重自动校验归一化
- SQLite 数据缓存 + 历史记录
- FastAPI + Docker 部署 + Server酱 微信定时推送
- 评测体系：通过率 / 数据获取成功率 / 平均耗时（见 metrics.json）

## 快速开始
1. uv sync
2. cp .env.example .env  # 填 3 个 Key
3. uv run python main.py
4. 访问 http://localhost:8000/docs

## 免责声明
仅供个人研究参考，不构成投资建议。
