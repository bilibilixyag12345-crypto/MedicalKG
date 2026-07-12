# 🚀 快速开始指南

## 方式一：一键配置（推荐）

### macOS / Linux
```bash
chmod +x setup.sh
./setup.sh
```

### Windows
```cmd
setup.bat
```

配置脚本会自动：
- ✅ 检查 Python 版本
- ✅ 创建虚拟环境
- ✅ 安装所有 Python 依赖
- ✅ 检查 MongoDB、Neo4j、Docker 安装状态
- ✅ 提供后续启动命令

---

## 方式二：Docker Compose（最简单，不需要本地安装服务）

适合快速测试，所有服务运行在容器中。

### 1. 启动所有服务
```bash
docker-compose up -d
```

**会自动启动：**
- MongoDB (27017)
- Neo4j (7474/7687)
- Splash (8050)

### 2. 验证服务状态
```bash
docker-compose ps
```

### 3. 安装 Python 依赖
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 4. 运行爬虫
```bash
python3 run.py
```

### 5. 构建知识图谱
```bash
# Neo4j 密码在 docker-compose.yml 中设置为 medicalkg123
python3 create_KG.py \
  --mongo_url localhost \
  --neo4j_url bolt://localhost:7687 \
  --neo4j_name neo4j \
  --neo4j_password medicalkg123
```

### 6. 查看知识图谱
- 访问 http://localhost:7474
- 用户名: `neo4j`
- 密码: `medicalkg123`

### 7. 停止所有服务
```bash
docker-compose down
```

---

## 方式三：手动配置

### 1. 安装 Python 依赖
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux 或 venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### 2. 启动 MongoDB
```bash
# 如果已安装 MongoDB
mongod --dbpath ./data
```
[MongoDB 官方安装指南](https://www.mongodb.com/try/download/community)

### 3. 启动 Neo4j
```bash
neo4j console
```
- 访问 http://localhost:7474
- 初始用户名/密码: `neo4j/neo4j`
- **首次登录会要求修改密码**

[Neo4j 官方下载](https://neo4j.com/download-center/#community)

### 4. 启动 Splash (Docker)
```bash
docker pull scrapinghub/splash
docker run -p 8050:8050 scrapinghub/splash
```

### 5. 运行爬虫
```bash
python3 run.py
```

### 6. 构建知识图谱
```bash
python3 create_KG.py \
  --mongo_url localhost \
  --neo4j_url bolt://localhost:7687 \
  --neo4j_name neo4j \
  --neo4j_password your_password
```

---

## 📊 验证各服务状态

### 测试 MongoDB
```python
from pymongo import MongoClient
client = MongoClient('localhost')
print(client)  # 应显示连接信息
```

### 测试 Neo4j
访问 http://localhost:7474

### 测试 Splash
访问 http://localhost:8050

---

## ⚠️ 常见问题

### Q: 找不到 `run.py`？
A: 确保在项目根目录运行命令，脚本位于 `./MedicalKG/run.py` 中。

### Q: Neo4j 密码忘记了？
A: 如果是 Docker 环境，密码在 `docker-compose.yml` 中设置。  
如果是本地安装，可以重置配置文件重新初始化。

### Q: Docker 容器无法连接？
A: 检查防火墙设置，确保相应端口（27017、7474、8050）未被占用。

### Q: Python 版本不兼容？
A: 项目需要 Python 3.7+，使用 `python3 --version` 检查版本。

---

## 📚 项目结构

```
MedicalKG/
├── MedicalKG/          # Scrapy 项目主目录
│   ├── spiders/        # 爬虫脚本
│   ├── items.py        # 数据项定义
│   ├── pipelines.py    # 数据处理管道
│   ├── middlewares.py  # 中间件
│   └── settings.py     # Scrapy 配置
├── run.py              # 启动爬虫
├── create_KG.py        # 构建知识图谱
├── requirements.txt    # Python 依赖
├── docker-compose.yml  # Docker 配置
└── README.md          # 详细文档
```

---

## 🔗 相关文档

- [README.md](README.md) - 完整项目文档
- [Scrapy 官方文档](https://docs.scrapy.org/)
- [Neo4j 官方文档](https://neo4j.com/developer/get-started/)
- [MongoDB 官方文档](https://docs.mongodb.com/)
