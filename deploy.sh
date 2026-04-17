#!/bin/bash

# 部署脚本

# 服务器信息
SERVER_IP="43.142.69.28"
SERVER_USER="root"
SERVER_DIR="/root/bunansou"

# 停止并删除旧容器
echo "停止并删除旧容器..."
ssh $SERVER_USER@$SERVER_IP "cd $SERVER_DIR && docker-compose down || true"

# 创建服务器目录
echo "创建服务器目录..."
ssh $SERVER_USER@$SERVER_IP "mkdir -p $SERVER_DIR"

# 上传项目文件
echo "上传项目文件..."
scp -r ./* $SERVER_USER@$SERVER_IP:$SERVER_DIR/

# 在服务器上构建并启动容器
echo "在服务器上构建并启动容器..."
ssh $SERVER_USER@$SERVER_IP "cd $SERVER_DIR && docker-compose up -d --build"

# 查看容器状态
echo "查看容器状态..."
ssh $SERVER_USER@$SERVER_IP "cd $SERVER_DIR && docker-compose ps"

echo "部署完成！"
