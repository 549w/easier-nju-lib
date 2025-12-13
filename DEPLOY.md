# easier-nju-lib 项目部署指南

## 服务器信息
- IP地址: [您的服务器公网IP地址]
- 用户名: [您的服务器用户名]
- 密码: [您的服务器密码]

## 部署步骤

### 1. 连接到云服务器
使用SSH客户端（如PuTTY或Windows Terminal）连接到服务器：
```bash
ssh [用户名]@[服务器IP地址]
```
输入密码：[您的服务器密码]

### 2. 安装Docker和Docker Compose

#### 安装Docker
```bash
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce
```

#### 安装Docker Compose
```bash
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3. 下载项目代码
```bash
mkdir -p /opt/easier-nju-lib
cd /opt/easier-nju-lib
git clone https://github.com/549w/easier-nju-lib .
```

### 4. 修改端口配置
根据需求修改端口配置，默认前端使用80端口，后端使用5000端口。如果需要修改，可以编辑`docker-compose.yml`文件：

```bash
# 修改docker-compose.yml文件
nano docker-compose.yml
```

找到以下行并修改端口：
```yaml
# 后端端口
ports:
  - "5000:5000"  # 修改为 "新端口:5000"

# 前端端口
ports:
  - "80:80"  # 修改为 "新端口:80"
```

按`Ctrl+O`保存，`Ctrl+X`退出。

### 5. 部署项目
```bash
docker-compose up -d --build
```

### 6. 验证部署

部署完成后，可以通过以下命令检查容器状态：
```bash
docker-compose ps
```

如果容器状态为"Up"，则部署成功。您可以通过以下地址访问项目：
- 前端: http://[服务器IP地址]:80（或您修改的前端端口）
- 后端API: http://[服务器IP地址]:5000（或您修改的后端端口）

## 其他命令

- 停止项目：
  ```bash
  docker-compose down
  ```

- 查看日志：
  ```bash
  docker-compose logs -f
  ```

- 重新构建并启动：
  ```bash
  docker-compose up -d --build
  ```

## 注意事项
1. 确保服务器的防火墙已开放相应的端口
2. 如果遇到端口占用问题，可以修改`docker-compose.yml`中的端口映射
3. 首次部署可能需要较长时间，因为需要下载依赖和构建镜像
