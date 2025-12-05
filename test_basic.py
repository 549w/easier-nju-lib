#!/usr/bin/env python3
# 最基本的测试脚本
print("Hello, World!")
print("Python版本:")
import sys
print(sys.version)

# 测试循环
import time
print("开始循环测试...")
for i in range(5):
    print(f"循环 {i+1}")
    time.sleep(1)

print("测试完成！")