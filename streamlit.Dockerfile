# 使用官方的 Python 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的 requirements.txt 到容器中的 /app 目录
COPY requirements.txt .

# 安装所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用的所有代码到容器中的 /app 目录
COPY . /app

# 暴露端口，Streamlit 默认运行在 8501 端口
EXPOSE 8501

# 启动 Streamlit 服务
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]