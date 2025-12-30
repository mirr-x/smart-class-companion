# Setup Instructions for Smart Class Companion

## Quick Start (All Platforms)

### Windows Users

**Option 1: PowerShell (Recommended)**
1. Right-click on `setup.ps1`
2. Select "Run with PowerShell"
3. If you get a security warning, run this first:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
   Then run: `.\setup.ps1`

**Option 2: Batch File**
1. Double-click `setup.bat`
2. Follow the prompts in the window

**Option 3: Command Line**
```cmd
setup.bat
```

### Linux/Mac Users

```bash
chmod +x setup.sh
./setup.sh
```

## What the Setup Scripts Do

All three scripts (setup.sh, setup.ps1, setup.bat) perform the same functions:

1. ✅ **Check Python** - Verifies Python 3.8+ is installed
2. ✅ **Virtual Environment** - Creates and activates Python virtual environment
3. ✅ **Install Dependencies** - Installs Django, Oracle driver, and other packages
4. ✅ **Database Setup** - Lets you choose Oracle or SQLite
5. ✅ **Run Migrations** - Creates all database tables
6. ✅ **Create Admin** - Optional superuser account creation
7. ✅ **Collect Static** - Optional static file collection
8. ✅ **Run Tests** - Optional test suite execution
9. ✅ **Start Server** - Optionally starts the development server

## Interactive Prompts

The scripts will ask you questions:

| Prompt | Recommendation | Notes |
|--------|---------------|-------|
| Database type? | Choose 2 (SQLite) | Easiest for testing |
| Oracle credentials? | Only if you chose Oracle | |
| Create superuser? | Yes (y) | Needed for admin access |
| Collect static files? | No (n) for development | Yes for production |
| Run tests? | Optional | Takes ~3 seconds |
| Start server? | Yes (y) | Starts at localhost:8000 |

## After Setup

Once setup is complete:

### First Time Access
1. Open browser to: `http://localhost:8000`
2. Click "Register" to create an account
3. Choose "Teacher" or "Student" role
4. Start using the application!

### Admin Panel
- URL: `http://localhost:8000/admin/`
- Login with the superuser account you created
- Manage users, classes, assignments, etc.

## Common Issues

### Windows PowerShell Security Error
```powershell
# Run this in PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned
```

Or run once per session:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

### "Port already in use"
Another server is running. Stop it with:
- Windows: `Ctrl+C` in the server window
- Or: `taskkill /F /IM python.exe` (Windows)
- Linux/Mac: `pkill -f runserver`

### Python not found
- **Windows**: Reinstall Python from python.org
  - ✅ Check "Add Python to PATH" during installation
- **Linux**: `sudo apt install python3 python3-pip python3-venv`
- **Mac**: `brew install python3`

### Oracle Connection Issues
Choose SQLite (option 2) instead for easier setup.

## Manual Setup (If Scripts Fail)

### Windows
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Daily Usage

After initial setup, you only need:

### Windows
```cmd
venv\Scripts\activate
python manage.py runserver
```

### Linux/Mac
```bash
source venv/bin/activate
python manage.py runserver
```

## File Descriptions

| File | Platform | Description |
|------|----------|-------------|
| `setup.sh` | Linux/Mac | Bash script |
| `setup.ps1` | Windows | PowerShell script |
| `setup.bat` | Windows | Batch file (older Windows) |
| `requirements.txt` | All | Python dependencies |
| `.env` | All | Configuration (created by setup) |

## Getting Help

- Check `README.md` for detailed documentation
- Check `QUICKSTART.md` for quick commands
- Check `DEPLOYMENT_CHECKLIST.md` for production deployment

## Testing Your Installation

After setup, verify everything works:

```bash
# Activate virtual environment first!
python manage.py test core.tests_models
```

You should see:
```
Ran 18 tests in 2.659s
OK
```

---

**Ready to go!** Run your setup script and start building your classes! 🎓
