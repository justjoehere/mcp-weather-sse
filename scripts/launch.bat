@echo off
setlocal enabledelayedexpansion

:: Set paths
set PROJECT_ROOT=%~dp0..
set VENV_PATH=%PROJECT_ROOT%\.venv
set SCRIPT_PATH=%PROJECT_ROOT%\src\mcp_weather_service\weather_server.py

:: Debug info
echo Project root: %PROJECT_ROOT%
echo Looking for script at: %SCRIPT_PATH%

:: Configuration
set SERVER_HOST=0.0.0.0
set SERVER_PORT=3001

:: Check if script exists
if not exist "%SCRIPT_PATH%" (
    echo ERROR: Server script not found at: %SCRIPT_PATH%
    echo Current directory: %CD%
    echo Checking package directory content:
    dir "%PROJECT_ROOT%\src\mcp_weather_service"
    pause
    exit /b 1
)

:: Set PYTHONPATH to include src directory
set PYTHONPATH=%PROJECT_ROOT%\src;%PYTHONPATH%

:: Activate the virtual environment
call "%VENV_PATH%\Scripts\activate"
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo Virtual environment activated
echo Starting Weather SSE Server...
echo Host: %SERVER_HOST%
echo Port: %SERVER_PORT%
echo PYTHONPATH: %PYTHONPATH%
echo.

:: Start the server
python "%SCRIPT_PATH%"

:: If the server exits, wait before closing
if %ERRORLEVEL% neq 0 (
    echo Server stopped with error code %ERRORLEVEL%
    pause
) else (
    echo Server stopped successfully
    pause
)

:: Deactivate virtual environment
deactivate