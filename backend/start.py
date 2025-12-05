#!/usr/bin/env python3
# 简单的后端启动脚本
import subprocess
import time

print("启动后端服务...")

# 使用subprocess启动Flask应用，设置较长的超时时间
try:
    process = subprocess.Popen(
        ["python", "app.py"],
        cwd=".",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待服务启动
    time.sleep(5)
    
    # 检查进程是否还在运行
    if process.poll() is None:
        print("后端服务启动成功！")
        print("服务运行在 http://127.0.0.1:5000")
        print("按 Ctrl+C 停止服务")
        # 保持脚本运行
        process.wait()
    else:
        print("后端服务启动失败")
        stderr = process.stderr.read()
        if stderr:
            print(f"错误信息: {stderr}")
            
except Exception as e:
    print(f"启动过程中发生错误: {e}")
