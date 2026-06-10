@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo Sports Signal Bot - Initialization and Startup Sequence
echo ========================================================

:: Ensure we are in the root directory by checking for pyproject.toml
if not exist "pyproject.toml" (
    echo [ERROR] Must be run from the root directory of the repository.
    pause
    goto :EOF
)

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.12+.
    pause
    goto :EOF
)

:: Ensure logs directory exists
if not exist "logs" mkdir logs

:: Create venv if it doesn't exist
if not exist ".venv" (
    echo [INFO] Virtual environment not found. Creating virtual environment...
    python -c "import venv; venv.create(".venv", with_pip=True)"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment. Check logs\windows_startup.log
        echo Failed to create virtual environment. > logs\windows_startup.log
        pause
        goto :EOF
    )
) else (
    echo [INFO] Virtual environment found.
)

:: Activate virtual environment securely
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment appears corrupted. Try deleting .venv and re-run.
    pause
    goto :EOF
)

echo [INFO] Activating virtual environment...
set VIRTUAL_ENV=%cd%\.venv
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%

:: Install and update dependencies
echo [INFO] Installing/Updating dependencies...
python -m pip install --upgrade pip setuptools wheel > logs\windows_startup.log 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Failed to upgrade pip/setuptools.
)

python -m pip install poetry >> logs\windows_startup.log 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install poetry.
    pause
    goto :EOF
)

poetry install >> logs\windows_startup.log 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install project dependencies. Check logs\windows_startup.log
    pause
    goto :EOF
)

:: Environment variables wizard
echo [INFO] Checking environment configuration...
if not exist ".env" (
    echo [WARNING] .env file not found. Let's create one.
    echo # Environment Variables > .env

    set /p "api_key=Enter API Key (or press enter to skip): "
    if not "!api_key!"=="" echo API_KEY=!api_key! >> .env

    set /p "api_secret=Enter API Secret (or press enter to skip): "
    if not "!api_secret!"=="" echo API_SECRET=!api_secret! >> .env

    set /p "tg_token=Enter Telegram Bot Token (or press enter to skip): "
    if not "!tg_token!"=="" echo TELEGRAM_BOT_TOKEN=!tg_token! >> .env

    set /p "tg_chat_id=Enter Telegram Chat ID (or press enter to skip): "
    if not "!tg_chat_id!"=="" echo TELEGRAM_CHAT_ID=!tg_chat_id! >> .env

    echo [INFO] .env file created successfully.
)

:: Verify Gitignore ignores secrets
findstr /C:".env" .gitignore >nul 2>&1
if %errorlevel% neq 0 (
    echo .env >> .gitignore
    echo .venv >> .gitignore
    echo logs/ >> .gitignore
)

:: Healthcheck
echo [INFO] Running healthcheck...
set PYTHONPATH=./src;%PYTHONPATH%
python scripts\windows_healthcheck.py > logs\healthcheck.log 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Healthcheck failed! Check logs\healthcheck.log for details.
    pause
    goto :EOF
)
echo [INFO] Healthcheck passed.

:: Tests
echo [INFO] Running tests (import and unit tests)...
python -m pytest tests/geo_hardening/ > logs\tests.log 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Tests failed. Check logs\tests.log.
    set /p "continue_anyway=Do you want to start the bot anyway? (y/n): "
    if /i not "!continue_anyway!"=="y" (
        echo [INFO] Startup aborted.
        pause
        goto :EOF
    )
) else (
    echo [INFO] Tests passed!
)

:: Start the application with Supervisor
echo [INFO] Starting the bot supervisor...
echo [INFO] Runtime logs available at logs\windows_supervisor.log
echo [INFO] Press Ctrl+C to gracefully stop the bot.
echo ========================================================

python scripts\windows_supervisor.py

if %errorlevel% neq 0 (
    echo [ERROR] Supervisor exited with an error. Check logs\windows_supervisor.log
    pause
)

echo [INFO] Shutdown complete.
pause
