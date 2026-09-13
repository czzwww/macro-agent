from fastapi import FastAPI
from pydantic import BaseModel
from app import db
from app.agents.graph import run_analysis

app = FastAPI(title="宏观资产配置 Agent")   # 定义 FastAPI 应用，标题为 "宏观资产配置 Agent"

class AnalyzeRequest(BaseModel):
    task: str = "今天该配什么？"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    result = run_analysis()
    db.save_history(result)
    return result

@app.get("/history")
def history(limit: int = 10):
    return db.load_history(limit)

@app.get("/metrics")
def metrics():
    return {"note": "此处可接入耗时/成功率统计（评估见 Step 12）"}