@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo Sports Signal Bot - Initialization and Startup Sequence
echo ========================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python.
    goto :EOF
)

:: Check for .venv
if not exist ".venv" (
    echo [INFO] Virtual environment not found. Creating .venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        goto :EOF
    )
) else (
    echo [INFO] Virtual environment found.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install dependencies
echo [INFO] Installing/Updating dependencies...
pip install poetry
poetry install

:: Environment check
echo [INFO] Checking environment variables...
if not exist ".env" (
    echo [WARNING] .env file not found.
    set /p "create_env=Would you like to create a basic .env file now? (y/n): "
    if /i "!create_env!"=="y" (
        echo # Environment Variables > .env
        set /p "api_key=Enter API Key (or press enter to skip): "
        if not "!api_key!"=="" echo API_KEY=!api_key! >> .env
        echo [INFO] .env file created.
    )
)

:: Run Tests
echo [INFO] Running tests...
pytest tests/
if %errorlevel% neq 0 (
    echo [WARNING] Tests failed.
    set /p "continue_anyway=Do you want to start the bot anyway? (y/n): "
    if /i not "!continue_anyway!"=="y" (
        echo [INFO] Startup aborted.
        goto :EOF
    )
) else (
    echo [INFO] All tests passed!
)

:: Start the application
echo [INFO] Starting the bot...
echo [INFO] The bot will run continuously. Press Ctrl+C to stop.
echo ========================================================

python -m src.sports_signal_bot.main live-execution run-live-execution-pass

if %errorlevel% neq 0 (
    echo [ERROR] The bot stopped with an error. Check the logs above.
)

pause
