# 使用官方的 Python 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的 requirements.txt 到容器中的 /app 目录
COPY dashboard/requirements.txt .

# 安装所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用的所有代码到容器中的 /app 目录
COPY dashboard /app

# 暴露端口，Streamlit 默认运行在 8502 端口
EXPOSE 8502

# 启动 Streamlit 服务
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]