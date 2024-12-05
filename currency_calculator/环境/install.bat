@echo off
echo Installing Currency Calculator dependencies...

:: 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: 创建虚拟环境
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

:: 升级pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: 安装依赖包
echo Installing required packages...
pip install requests==2.31.0
pip install datetime
pip install pytz

:: 如果需要GUI支持，取消下面的注释
:: pip install tkinter

echo.
echo Installation completed successfully!
echo.
echo To start the calculator, run: python main.py
echo.
pause