# Quick Start Guide - Smart Class Companion

## For First-Time Setup

### Option 1: Automated Setup (Recommended)

Run the interactive setup script:

```bash
./setup.sh
```

The script will guide you through:
1. ✅ Python version check
2. ✅ Virtual environment creation
3. ✅ Dependency installation
4. ✅ Database configuration (Oracle or SQLite)
5. ✅ Running migrations
6. ✅ Creating superuser account
7. ✅ Collecting static files
8. ✅ Running tests
9. ✅ Starting the server

**Just answer the prompts and you're done!**

### Option 2: Manual Setup

If you prefer manual setup:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure database (edit .env file or settings.py)

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

## For Returning Users

If you've already set up the project:

```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python manage.py runserver
```

Visit `http://localhost:8000` in your browser!

## Quick Commands

```bash
# Run tests
python manage.py test core

# Create new user
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## Troubleshooting

### Oracle Connection Issues
Run the setup script and choose SQLite (option 2) for testing

### Permission Denied on setup.sh
```bash
chmod +x setup.sh
```

### Virtual Environment Issues
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

For more details, see README.md
