@echo off
REM Smart Class Companion - Windows Setup Script (Batch)
REM Run this script by double-clicking or: setup.bat

setlocal enabledelayedexpansion
color 0A

echo ============================================================
echo.
echo        Smart Class Companion - Setup Script
echo                Windows Batch Version
echo.
echo        This script will guide you through setup
echo.
echo ============================================================
echo.
timeout /t 2 /nobreak >nul

REM Step 1: Check Python
echo ========================================
echo Step 1: Checking Python Installation
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python found: %PYTHON_VERSION%
echo.

REM Step 2: Virtual Environment
echo ========================================
echo Step 2: Virtual Environment Setup
echo ========================================
echo.

if exist "venv\" (
    echo Virtual environment already exists.
    set /p USE_EXISTING="Use existing virtual environment? (y/n): "
    if /i not "!USE_EXISTING!"=="y" (
        echo Creating new virtual environment...
        rmdir /s /q venv
        python -m venv venv
        echo [SUCCESS] New virtual environment created
    )
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [SUCCESS] Virtual environment activated
echo.

REM Step 3: Install Dependencies
echo ========================================
echo Step 3: Installing Dependencies
echo ========================================
echo.
echo Installing required Python packages...

if exist "requirements.txt" (
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo [SUCCESS] Dependencies installed successfully
) else (
    echo [WARNING] requirements.txt not found. Installing core dependencies...
    python -m pip install --upgrade pip
    python -m pip install django==4.2.25 oracledb Pillow
    echo [SUCCESS] Core dependencies installed
)
echo.

REM Step 4: Database Configuration
echo ========================================
echo Step 4: Database Configuration
echo ========================================
echo.
echo Choose your database type:
echo 1) Oracle Database (Production)
echo 2) SQLite (Development/Testing)
set /p DB_CHOICE="Enter your choice (1 or 2): "

if "%DB_CHOICE%"=="1" (
    echo Configuring Oracle Database...
    set /p ORACLE_DB_NAME="Enter Oracle Database Name: "
    set /p ORACLE_USER="Enter Oracle Username: "
    set /p ORACLE_PASSWORD="Enter Oracle Password: "
    set /p ORACLE_HOST="Enter Oracle Host (default: localhost): "
    if "!ORACLE_HOST!"=="" set ORACLE_HOST=localhost
    set /p ORACLE_PORT="Enter Oracle Port (default: 1521): "
    if "!ORACLE_PORT!"=="" set ORACLE_PORT=1521
    
    REM Generate simple secret key
    set SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM%%RANDOM%
    
    REM Create .env file
    (
        echo USE_ORACLE=true
        echo ORACLE_DB_NAME=!ORACLE_DB_NAME!
        echo ORACLE_USER=!ORACLE_USER!
        echo ORACLE_PASSWORD=!ORACLE_PASSWORD!
        echo ORACLE_HOST=!ORACLE_HOST!
        echo ORACLE_PORT=!ORACLE_PORT!
        echo DJANGO_SECRET_KEY=!SECRET_KEY!
        echo DEBUG=True
    ) > .env
    
    echo [SUCCESS] Oracle configuration saved to .env
) else (
    REM Generate simple secret key
    set SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM%%RANDOM%
    
    REM Create .env file for SQLite
    (
        echo USE_ORACLE=false
        echo DJANGO_SECRET_KEY=!SECRET_KEY!
        echo DEBUG=True
    ) > .env
    
    echo [SUCCESS] SQLite configuration saved to .env
)
echo.

REM Step 5: Run Migrations
echo ========================================
echo Step 5: Database Migrations
echo ========================================
echo.
echo Creating database tables...

python manage.py makemigrations
python manage.py migrate

echo [SUCCESS] Database migrations completed
echo.

REM Step 6: Create Superuser
echo ========================================
echo Step 6: Create Superuser Account
echo ========================================
echo.
echo You need to create an admin account to manage the application.
set /p CREATE_SUPERUSER="Create superuser now? (y/n): "
if /i "%CREATE_SUPERUSER%"=="y" (
    python manage.py createsuperuser
    echo [SUCCESS] Superuser created successfully
) else (
    echo [WARNING] Skipped superuser creation.
    echo You can create one later with: python manage.py createsuperuser
)
echo.

REM Step 7: Collect Static Files
echo ========================================
echo Step 7: Static Files
echo ========================================
echo.
set /p COLLECT_STATIC="Collect static files now? (recommended for production) (y/n): "
if /i "%COLLECT_STATIC%"=="y" (
    python manage.py collectstatic --noinput
    echo [SUCCESS] Static files collected
) else (
    echo Skipped static files collection
)
echo.

REM Step 8: Run Tests
echo ========================================
echo Step 8: Testing
echo ========================================
echo.
set /p RUN_TESTS="Run the test suite? (y/n): "
if /i "%RUN_TESTS%"=="y" (
    echo Running tests...
    python manage.py test core.tests_models --verbosity=2
    echo [SUCCESS] Tests completed
) else (
    echo Skipped tests
)
echo.

REM Step 9: Complete
echo ========================================
echo Setup Complete!
echo ========================================
echo.
color 0A
echo [SUCCESS] Smart Class Companion is now installed and configured!
echo.
echo Next Steps:
echo 1. Start the development server:
echo    python manage.py runserver
echo.
echo 2. Open your browser and visit:
echo    http://localhost:8000
echo.
echo 3. Access the admin panel at:
echo    http://localhost:8000/admin/
echo.
echo Configuration saved in:
echo   - .env (database credentials)
echo   - db.sqlite3 (SQLite database)
echo.

set /p START_SERVER="Start the development server now? (y/n): "
if /i "%START_SERVER%"=="y" (
    echo [SUCCESS] Starting development server...
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    timeout /t 2 /nobreak >nul
    python manage.py runserver
) else (
    echo Setup complete! Run 'python manage.py runserver' when you're ready.
)

echo.
echo Thank you for using Smart Class Companion!
echo.
pause
