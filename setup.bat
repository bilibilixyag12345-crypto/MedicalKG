@echo off
REM Medical Knowledge Graph 一键配置脚本 (Windows)
REM 本脚本自动配置 Python 环境

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo   医疗知识图谱 (MedicalKG) 环境配置
echo ==========================================
echo.

REM 1. 检查 Python
echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装，请先安装 Python 3.7+
    echo 官网: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python 版本: %PYTHON_VERSION%
echo.

REM 2. 创建虚拟环境
echo [2/3] 配置 Python 虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo ✓ 虚拟环境创建完成
) else (
    echo ✓ 虚拟环境已存在
)
echo.

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 3. 安装依赖
echo [3/3] 安装 Python 依赖包...
pip install -r requirements.txt -q
echo ✓ Python 依赖安装完成
echo.

echo ==========================================
echo ✓ 配置完成！
echo ==========================================
echo.
echo 📋 后续步骤:
echo.
echo 1️⃣  启动 MongoDB 服务:
echo    mongod --dbpath ./data
echo    (需要先安装: https://www.mongodb.com/try/download/community)
echo.
echo 2️⃣  启动 Neo4j 服务:
echo    neo4j console
echo    访问 http://localhost:7474 (初始密码: neo4j/neo4j)
echo    (需要先安装: https://neo4j.com/download-center/#community)
echo.
echo 3️⃣  启动 Splash 服务 (Docker):
echo    docker pull scrapinghub/splash
echo    docker run -p 8050:8050 scrapinghub/splash
echo    (需要先安装 Docker: https://www.docker.com/products/docker-desktop)
echo.
echo 4️⃣  运行爬虫:
echo    python run.py
echo.
echo 5️⃣  构建知识图谱:
echo    python create_KG.py --neo4j_password ^<你的neo4j密码^>
echo.
echo 📚 更多详情请查看 README.md
echo.
pause
