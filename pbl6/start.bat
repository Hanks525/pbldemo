@echo off
chcp 65001 >nul
echo ================================================
echo         校园活动发布平台 - 一键启动脚本
echo ================================================
echo.

set "BASE_DIR=%~dp0"

echo [1/3] 检查 Node.js 环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)
echo  Node.js 环境正常

echo.
echo [2/3] 启动后端服务 (端口: 5000)...
start "后端服务" cmd /k "cd /d ""%BASE_DIR%"" && npm run server"

echo.
echo [3/3] 启动前端开发服务器 (端口: 5173)...
start "前端服务" cmd /k "cd /d ""%BASE_DIR%campus-events\frontend"" && npm install && npm run dev"

echo.
echo 正在启动服务，请稍候...
echo 后端服务: http://localhost:5000
echo 前端页面: http://localhost:5173
echo.
echo 按任意键退出监控...
pause