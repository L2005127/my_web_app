"""FastAPI 应用入口 —— 个人状态看板。

包含首页渲染、状态查询 API、健康检查接口。
所有数据均存储于内存，进程重启即清空，满足部署练习需求。
"""

from __future__ import annotations

import random
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# 项目根目录（my_web_app/）
BASE_DIR = Path(__file__).resolve().parent.parent

# 模板目录
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 励志语录库（内存随机选取）
QUOTES: list[str] = [
      "心若向阳，无谓悲伤；一路向前，终将抵达远方。",
      "每一个不曾起舞的日子，都是对生命的辜负。",
      "所谓的光辉岁月，并不是后来闪耀的日子，而是无人问津时对梦想的偏执。",
      "你的坚持，终将美好；你的努力，不会白费。",
      "今天撒下的种子，会在未来的某一天开出花来。",
      "自律给我自由，坚持让我与众不同。",
      "成功没有捷径，唯有脚踏实地、日积月累。",
      "长风破浪会有时，直挂云帆济沧海。",
      "把每一件简单的事做好就是不简单。",
      "不积跬步，无以至千里；不积小流，无以成江海。",
]

# 应用启动时间戳（内存态标志）
startup_time: float = time.time()

# FastAPI 应用实例
app = FastAPI(
      title="个人状态看板",
      description="用于云端部署实战练习的极简看板应用",
      version="1.0.0",
)


@app.get("/")
async def index(request: Request):
      """首页：渲染状态看板页面。"""
      return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health() -> dict[str, str]:
      """健康检查接口，供云端负载均衡器探测。"""
      return {"status": "ok"}


@app.get("/api/status")
async def status() -> dict[str, object]:
      """状态查询接口：返回当前时间戳与随机励志语录。"""
      return {
          "timestamp": int(time.time()),           # 当前 Unix 时间戳（秒）
          "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
          "timezone": time.strftime("%Z", time.localtime()),
          "system_status": "运行中",
          "uptime_seconds": int(time.time() - startup_time),  # 服务已运行时长
          "quote": random.choice(QUOTES),          # 随机励志语录
      }


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
      """兜底异常处理，避免未捕获异常导致空响应。"""
      return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


def main() -> None:
      """开发调试用入口：uvicorn app.main:app --reload。"""
      import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
      main()
  
