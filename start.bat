@echo off
chcp 65001 >nul
title 闲鱼AI客服 - xianyvAgent

echo ================================
echo   闲鱼AI智能客服 xianyvAgent
echo ================================
echo.

:: 检查 .env
if not exist .env (
    echo [!] 未找到 .env 文件，正在从模板创建...
    copy .env.example .env >nul
    echo [✓] 已创建 .env，请编辑填入 API_KEY 和 COOKIES_STR 后重新运行
    start notepad .env
    pause
    exit
)

:: 检查依赖
python -c "import openai" 2>nul
if errorlevel 1 (
    echo [!] 正在安装依赖...
    pip install -r requirements.txt
)

echo [✓] 启动中...
echo [✓] 仪表板: http://localhost:8899
echo [✓] 按 Ctrl+C 退出
echo.

python main.py
pause
