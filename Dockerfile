# 使用官方的 Python 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的 requirements.txt 到容器中的 /app 目录
COPY api/requirements.txt .

# 安装所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用的所有代码到容器中的 /app 目录
COPY api /app

# 设置环境变量（可以控制日志等级、API环境等）
ENV PYTHONUNBUFFERED 1

# 暴露端口，FastAPI 默认运行在 8000 端口
EXPOSE 8000

# 启动 FastAPI 服务，指定 `api.search_api:app` 为入口，监听 0.0.0.0 和 8000 端口
CMD ["uvicorn", "api.search_api:app", "--host", "0.0.0.0", "--port", "8000"]