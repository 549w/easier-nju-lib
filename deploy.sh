#!/bin/bash

# 部署脚本 for easier-nju-lib 项目

# 服务器信息
SERVER_IP="[您的服务器公网IP地址]"
SERVER_USER="[您的服务器用户名]"
SERVER_PASSWORD="[您的服务器密码]"

# 项目信息
PROJECT_NAME="easier-nju-lib"
LOCAL_DIR="$(pwd)"
REMOTE_DIR="/opt/easier-nju-lib"

# 新端口配置
FRONTEND_PORT=8080
BACKEND_PORT=5001

# 1. 检查并安装Docker和Docker Compose
sshpass -p "$SERVER_PASSWORD" ssh $SERVER_USER@$SERVER_IP << 'EOF'

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "Docker未安装，正在安装..."
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update
    apt-get install -y docker-ce
    echo "Docker安装完成"
else
    echo "Docker已安装"
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose未安装，正在安装..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose安装完成"
else
    echo "Docker Compose已安装"
fi

EOF

# 2. 修改本地项目的端口配置
echo "修改项目端口配置..."

# 修改docker-compose.yml中的端口
cp docker-compose.yml docker-compose.yml.backup
sed -i "s/5000:5000/$BACKEND_PORT:5000/g" docker-compose.yml
sed -i "s/80:80/$FRONTEND_PORT:80/g" docker-compose.yml

# 3. 将项目代码上传到服务器
echo "上传项目代码到服务器..."
sshpass -p "$SERVER_PASSWORD" ssh $SERVER_USER@$SERVER_IP "mkdir -p $REMOTE_DIR"
sshpass -p "$SERVER_PASSWORD" rsync -avz --exclude='node_modules' --exclude='.git' --exclude='*.pyc' --exclude='*.log' $LOCAL_DIR/ $SERVER_USER@$SERVER_IP:$REMOTE_DIR/

# 4. 部署项目
echo "部署项目..."
sshpass -p "$SERVER_PASSWORD" ssh $SERVER_USER@$SERVER_IP << EOF
cd $REMOTE_DIR
docker-compose up -d --build
echo "项目部署完成！"
echo "前端访问地址: http://$SERVER_IP:$FRONTEND_PORT"
echo "后端API地址: http://$SERVER_IP:$BACKEND_PORT"
EOF

echo "部署脚本执行完成！"
