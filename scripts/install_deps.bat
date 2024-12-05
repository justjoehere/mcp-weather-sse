@echo off
:: Remove SETLOCAL to allow environment changes to persist

echo Activating virtual environment...
CALL .venv\scripts\activate.bat
if errorlevel 1 (
    echo Venv activation failed
    exit /b 1
)

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    exit /b 1
)

echo Dependencies installed successfully
