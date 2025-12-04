# 南京大学图书馆检索系统

一个基于React和Flask的图书检索网站，支持从南京大学图书馆OPAC系统搜索图书并展示馆藏信息。

## 功能特点

- 🔍 支持按书名搜索图书
- 📚 显示图书的作者、出版社、出版年份等基本信息
- 🏢 显示馆藏地、索书号和借阅状态
- 📱 响应式设计，支持移动端访问
- 🐳 容器化部署，支持Docker

## 技术栈

- **前端**: React + Vite
- **后端**: Flask + BeautifulSoup4
- **部署**: Docker + Docker Compose + Nginx

## 快速开始

### 前提条件

- Docker
- Docker Compose

### 部署步骤

1. 克隆项目（如果需要）

```bash
git clone <repository-url>
cd nju-lib-search
```

2. 使用Docker Compose启动服务

```bash
docker-compose up -d --build
```

3. 访问网站

打开浏览器，访问 `http://localhost`

## 项目结构

```
.
├── backend/           # 后端Flask应用
│   ├── app.py         # Flask主应用
│   ├── opac_spider.py # 图书馆OPAC爬虫模块
│   ├── requirements.txt # Python依赖
│   └── Dockerfile     # 后端Docker配置
├── frontend/          # 前端React应用
│   ├── public/        # 静态资源
│   ├── src/           # 源代码
│   │   ├── components/ # React组件
│   │   ├── App.jsx    # 主应用组件
│   │   └── main.jsx   # 入口文件
│   ├── nginx.conf     # Nginx配置
│   ├── package.json   # 前端依赖
│   └── Dockerfile     # 前端Docker配置
└── docker-compose.yml # Docker Compose配置
```

## API说明

### 搜索图书

```
GET /api/search?query=<书名>
```

**参数**:
- `query`: 要搜索的书名

**返回**: JSON格式的图书列表

## 注意事项

1. 本系统使用爬虫技术从南京大学图书馆OPAC系统获取数据，请合理使用
2. 爬虫可能会因为网站结构变化而失效，需要定期维护
3. 生产环境部署时建议设置适当的访问频率限制

## License

MIT

## 贡献

欢迎提交Issue和Pull Request！