#!/bin/bash

# Smart Class Companion - Interactive Setup Script
# This script will guide you through the complete setup process

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Welcome message
clear
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║       Smart Class Companion - Setup Script              ║"
echo "║                                                          ║"
echo "║       This script will guide you through setup          ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

sleep 1

# Step 1: Check Python version
print_header "Step 1: Checking Python Installation"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Step 2: Check if virtual environment exists
print_header "Step 2: Virtual Environment Setup"
if [ -d "venv" ]; then
    print_info "Virtual environment already exists."
    read -p "Do you want to use the existing virtual environment? (y/n): " use_existing
    if [ "$use_existing" != "y" ]; then
        print_info "Creating new virtual environment..."
        rm -rf venv
        python3 -m venv venv
        print_success "New virtual environment created"
    fi
else
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Step 3: Install dependencies
print_header "Step 3: Installing Dependencies"
print_info "Installing required Python packages..."

if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed successfully"
else
    print_warning "requirements.txt not found. Installing core dependencies..."
    pip install --upgrade pip
    pip install django==4.2.25 oracledb Pillow
    print_success "Core dependencies installed"
fi

# Step 4: Database Configuration
print_header "Step 4: Database Configuration"
print_info "Choose your database type:"
echo "1) Oracle Database (Production)"
echo "2) SQLite (Development/Testing)"
read -p "Enter your choice (1 or 2): " db_choice

if [ "$db_choice" == "1" ]; then
    USE_ORACLE="true"
    print_info "Configuring Oracle Database..."
    
    read -p "Enter Oracle Database Name: " ORACLE_DB_NAME
    read -p "Enter Oracle Username: " ORACLE_USER
    read -sp "Enter Oracle Password: " ORACLE_PASSWORD
    echo
    read -p "Enter Oracle Host (default: localhost): " ORACLE_HOST
    ORACLE_HOST=${ORACLE_HOST:-localhost}
    read -p "Enter Oracle Port (default: 1521): " ORACLE_PORT
    ORACLE_PORT=${ORACLE_PORT:-1521}
    
    # Create .env file
    cat > .env << EOF
USE_ORACLE=true
ORACLE_DB_NAME=$ORACLE_DB_NAME
ORACLE_USER=$ORACLE_USER
ORACLE_PASSWORD=$ORACLE_PASSWORD
ORACLE_HOST=$ORACLE_HOST
ORACLE_PORT=$ORACLE_PORT
DJANGO_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=True
EOF
    print_success "Oracle configuration saved to .env"
    
else
    USE_ORACLE="false"
    # Create .env file for SQLite
    cat > .env << EOF
USE_ORACLE=false
DJANGO_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=True
EOF
    print_success "SQLite configuration saved to .env"
fi

# Step 5: Run Migrations
print_header "Step 5: Database Migrations"
print_info "Creating database tables..."

python3 manage.py makemigrations
python3 manage.py migrate

print_success "Database migrations completed"

# Step 6: Create Superuser
print_header "Step 6: Create Superuser Account"
print_info "You need to create an admin account to manage the application."
echo

read -p "Do you want to create a superuser now? (y/n): " create_superuser
if [ "$create_superuser" == "y" ]; then
    python3 manage.py createsuperuser
    print_success "Superuser created successfully"
else
    print_warning "Skipped superuser creation. You can create one later with: python manage.py createsuperuser"
fi

# Step 7: Collect Static Files (optional)
print_header "Step 7: Static Files"
read -p "Do you want to collect static files now? (recommended for production) (y/n): " collect_static
if [ "$collect_static" == "y" ]; then
    python3 manage.py collectstatic --noinput
    print_success "Static files collected"
else
    print_info "Skipped static files collection"
fi

# Step 8: Run Tests
print_header "Step 8: Testing"
read -p "Do you want to run the test suite? (y/n): " run_tests
if [ "$run_tests" == "y" ]; then
    print_info "Running tests..."
    python3 manage.py test core.tests_models --verbosity=2
    print_success "Tests completed"
else
    print_info "Skipped tests"
fi

# Step 9: Setup Complete
print_header "Setup Complete!"
print_success "Smart Class Companion is now installed and configured!"

echo -e "\n${GREEN}Next Steps:${NC}"
echo "1. Start the development server:"
echo -e "   ${YELLOW}python3 manage.py runserver${NC}\n"
echo "2. Open your browser and visit:"
echo -e "   ${YELLOW}http://localhost:8000${NC}\n"
echo "3. Access the admin panel at:"
echo -e "   ${YELLOW}http://localhost:8000/admin/${NC}\n"

if [ "$USE_ORACLE" == "true" ]; then
    print_info "You are using Oracle Database"
    print_warning "Make sure Oracle Instant Client is installed and LD_LIBRARY_PATH is set"
else
    print_info "You are using SQLite Database (development mode)"
fi

echo -e "\n${BLUE}Configuration saved in:${NC}"
echo "  - .env (database credentials)"
echo "  - db.sqlite3 (SQLite database)" 
echo

# Ask if user wants to start the server now
read -p "Do you want to start the development server now? (y/n): " start_server
if [ "$start_server" == "y" ]; then
    print_success "Starting development server..."
    echo -e "\n${YELLOW}Press Ctrl+C to stop the server${NC}\n"
    sleep 2
    python3 manage.py runserver
else
    print_info "Setup complete! Run 'python3 manage.py runserver' when you're ready."
fi

echo -e "\n${GREEN}Thank you for using Smart Class Companion!${NC}\n"
