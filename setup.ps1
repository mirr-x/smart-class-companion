# Smart Class Companion - Windows Setup Script (PowerShell)
# Run this script with: .\setup.ps1

# Enable strict mode
$ErrorActionPreference = "Stop"

# Colors
function Write-Success { param($msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "✗ $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "ℹ $msg" -ForegroundColor Cyan }
function Write-Warning { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-Header {
    param($msg)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "$msg" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
}

# Welcome message
Clear-Host
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║       Smart Class Companion - Setup Script              ║" -ForegroundColor Green
Write-Host "║                Windows PowerShell Version                ║" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "║       This script will guide you through setup          ║" -ForegroundColor Green
Write-Host "║                                                          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Start-Sleep -Seconds 1

# Step 1: Check Python
Write-Header "Step 1: Checking Python Installation"
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python found: $pythonVersion"
} catch {
    Write-Error "Python is not installed or not in PATH"
    Write-Info "Please install Python 3.8+ from https://www.python.org/downloads/"
    Write-Info "Make sure to check 'Add Python to PATH' during installation"
    exit 1
}

# Step 2: Virtual Environment
Write-Header "Step 2: Virtual Environment Setup"
if (Test-Path "venv") {
    Write-Info "Virtual environment already exists."
    $useExisting = Read-Host "Use existing virtual environment? (y/n)"
    if ($useExisting -ne "y") {
        Write-Info "Creating new virtual environment..."
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Success "New virtual environment created"
    }
} else {
    Write-Info "Creating virtual environment..."
    python -m venv venv
    Write-Success "Virtual environment created"
}

# Activate virtual environment
Write-Info "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"
Write-Success "Virtual environment activated"

# Step 3: Install Dependencies
Write-Header "Step 3: Installing Dependencies"
Write-Info "Installing required Python packages..."

if (Test-Path "requirements.txt") {
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Write-Success "Dependencies installed successfully"
} else {
    Write-Warning "requirements.txt not found. Installing core dependencies..."
    python -m pip install --upgrade pip
    python -m pip install django==4.2.25 oracledb Pillow
    Write-Success "Core dependencies installed"
}

# Step 4: Database Configuration
Write-Header "Step 4: Database Configuration"
Write-Info "Choose your database type:"
Write-Host "1) Oracle Database (Production)"
Write-Host "2) SQLite (Development/Testing)"
$dbChoice = Read-Host "Enter your choice (1 or 2)"

if ($dbChoice -eq "1") {
    $USE_ORACLE = "true"
    Write-Info "Configuring Oracle Database..."
    
    $ORACLE_DB_NAME = Read-Host "Enter Oracle Database Name"
    $ORACLE_USER = Read-Host "Enter Oracle Username"
    $ORACLE_PASSWORD = Read-Host "Enter Oracle Password" -AsSecureString
    $ORACLE_PASSWORD_PLAIN = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($ORACLE_PASSWORD))
    $ORACLE_HOST = Read-Host "Enter Oracle Host (default: localhost)"
    if ([string]::IsNullOrWhiteSpace($ORACLE_HOST)) { $ORACLE_HOST = "localhost" }
    $ORACLE_PORT = Read-Host "Enter Oracle Port (default: 1521)"
    if ([string]::IsNullOrWhiteSpace($ORACLE_PORT)) { $ORACLE_PORT = "1521" }
    
    # Generate secret key
    $SECRET_KEY = -join ((65..90) + (97..122) + (48..57) + 33,35,36,37,38,42,43,45,61,63,64,94,95 | Get-Random -Count 50 | ForEach-Object {[char]$_})
    
    # Create .env file
    @"
USE_ORACLE=true
ORACLE_DB_NAME=$ORACLE_DB_NAME
ORACLE_USER=$ORACLE_USER
ORACLE_PASSWORD=$ORACLE_PASSWORD_PLAIN
ORACLE_HOST=$ORACLE_HOST
ORACLE_PORT=$ORACLE_PORT
DJANGO_SECRET_KEY=$SECRET_KEY
DEBUG=True
"@ | Out-File -FilePath ".env" -Encoding UTF8
    
    Write-Success "Oracle configuration saved to .env"
    
} else {
    $USE_ORACLE = "false"
    # Generate secret key
    $SECRET_KEY = -join ((65..90) + (97..122) + (48..57) + 33,35,36,37,38,42,43,45,61,63,64,94,95 | Get-Random -Count 50 | ForEach-Object {[char]$_})
    
    # Create .env file for SQLite
    @"
USE_ORACLE=false
DJANGO_SECRET_KEY=$SECRET_KEY
DEBUG=True
"@ | Out-File -FilePath ".env" -Encoding UTF8
    
    Write-Success "SQLite configuration saved to .env"
}

# Step 5: Run Migrations
Write-Header "Step 5: Database Migrations"
Write-Info "Creating database tables..."

python manage.py makemigrations
python manage.py migrate

Write-Success "Database migrations completed"

# Step 6: Create Superuser
Write-Header "Step 6: Create Superuser Account"
Write-Info "You need to create an admin account to manage the application."
$createSuperuser = Read-Host "`nCreate superuser now? (y/n)"
if ($createSuperuser -eq "y") {
    python manage.py createsuperuser
    Write-Success "Superuser created successfully"
} else {
    Write-Warning "Skipped superuser creation. Create one later with: python manage.py createsuperuser"
}

# Step 7: Collect Static Files
Write-Header "Step 7: Static Files"
$collectStatic = Read-Host "Collect static files now? (recommended for production) (y/n)"
if ($collectStatic -eq "y") {
    python manage.py collectstatic --noinput
    Write-Success "Static files collected"
} else {
    Write-Info "Skipped static files collection"
}

# Step 8: Run Tests
Write-Header "Step 8: Testing"
$runTests = Read-Host "Run the test suite? (y/n)"
if ($runTests -eq "y") {
    Write-Info "Running tests..."
    python manage.py test core.tests_models --verbosity=2
    Write-Success "Tests completed"
} else {
    Write-Info "Skipped tests"
}

# Step 9: Complete
Write-Header "Setup Complete!"
Write-Success "Smart Class Companion is now installed and configured!"

Write-Host "`nNext Steps:" -ForegroundColor Green
Write-Host "1. Start the development server:"
Write-Host "   python manage.py runserver`n" -ForegroundColor Yellow
Write-Host "2. Open your browser and visit:"
Write-Host "   http://localhost:8000`n" -ForegroundColor Yellow
Write-Host "3. Access the admin panel at:"
Write-Host "   http://localhost:8000/admin/`n" -ForegroundColor Yellow

if ($USE_ORACLE -eq "true") {
    Write-Info "You are using Oracle Database"
    Write-Warning "Make sure Oracle Instant Client is installed and PATH is set"
} else {
    Write-Info "You are using SQLite Database (development mode)"
}

Write-Host "`nConfiguration saved in:" -ForegroundColor Cyan
Write-Host "  - .env (database credentials)"
Write-Host "  - db.sqlite3 (SQLite database)`n"

# Ask to start server
$startServer = Read-Host "Start the development server now? (y/n)"
if ($startServer -eq "y") {
    Write-Success "Starting development server..."
    Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    python manage.py runserver
} else {
    Write-Info "Setup complete! Run 'python manage.py runserver' when you're ready."
}

Write-Host "`nThank you for using Smart Class Companion!`n" -ForegroundColor Green
