# ============================================
# 个人状态看板 —— Docker 构建镜像
# 基础镜像：python:3.10-slim（体积更小，安全精简）
# ============================================

FROM python:3.10-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 设置工作目录
WORKDIR /app

# 先复制依赖文件，利用 Docker 层缓存加速后续构建
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目代码到容器
COPY app ./app
COPY templates ./templates

# 非 root 用户运行（提高安全性）
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

# 暴露 FastAPI 端口
EXPOSE 8000

# 启动 uvicorn（监听所有网卡，配合 Nginx 反代或直接访问）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
