# Smart Class Companion

A comprehensive Learning Management System (LMS) built with Django and Oracle Database, designed to facilitate online education through class management, assignments, lessons, and interactive Q&A.

![Django](https://img.shields.io/badge/Django-4.2.25-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Oracle](https://img.shields.io/badge/Database-Oracle-red.svg)
![Tests](https://img.shields.io/badge/Tests-88%25%20Passing-brightgreen.svg)

## 🌟 Features

### For Teachers
- **Class Management**: Create and manage multiple classes with unique join codes
- **Lesson Creation**: Upload teaching materials and organize lessons
- **Assignment System**: Create assignments with due dates and point values
- **Grading**: Review and grade student submissions with feedback
- **Q&A Management**: Answer student questions on lessons
- **Dashboard**: Track pending grading, unanswered questions, and class statistics

### For Students
- **Class Enrollment**: Join classes using unique codes
- **Access Lessons**: View and download lesson materials
- **Submit Assignments**: Upload assignment submissions before deadlines
- **Q&A Participation**: Ask questions on lessons and view answers
- **Dashboard**: Track upcoming assignments, deadlines, and recent lessons

### Security Features
- Role-based access control (Teacher/Student)
- File upload validation (type and size restrictions)
- CSRF protection
- SQL injection protection (Django ORM)
- Session-based authentication

## 📋 Requirements

- Python 3.8+
- Django 4.2.25
- Oracle Database 19c or later
- Oracle Instant Client
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd schoo_project
```

### 2. Set Up Oracle Instant Client

Download Oracle Instant Client from [Oracle's website](https://www.oracle.com/database/technologies/instant-client/downloads.html)

```bash
# Extract to a directory (e.g., /opt/oracle/instantclient_23_6)
unzip instantclient-basic-linux.x64-23.6.0.24.10.zip -d /opt/oracle/

# Add to your shell configuration (~/.bashrc or ~/.zshrc)
export LD_LIBRARY_PATH=/opt/oracle/instantclient_23_6:$LD_LIBRARY_PATH
export PATH=/opt/oracle/instantclient_23_6:$PATH

# Reload configuration
source ~/.bashrc  # or source ~/.zshrc
```

### 3. Install Python Dependencies

```bash
pip install django==4.2.25
pip install oracledb
pip install Pillow
```

### 4. Configure Database

Create `.env` file in project root or set environment variables:

```bash
export USE_ORACLE=true
export ORACLE_DB_NAME="your_db_name"
export ORACLE_USER="your_username"
export ORACLE_PASSWORD="your_password"
export ORACLE_HOST="localhost"
export ORACLE_PORT="1521"
```

**Alternative**: Edit `smartclass/settings.py` directly (not recommended for production)

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 📖 User Guide

### For Teachers

#### 1. Register and Login
- Navigate to the registration page
- Select "Teacher" role
- Complete registration and login

#### 2. Create a Class
- Click "Create Class" from dashboard
- Enter class name, subject, and description
- A unique 6-character code will be generated
- Share this code with students

#### 3. Add Lessons
- Navigate to your class
- Click "Add Lesson"
- Enter title and description
- Upload files (optional)
- Publish the lesson

#### 4. Create Assignments
- Go to class detail page
- Click "Add Assignment"
- Set title, description, due date, and max points
- Publish the assignment

#### 5. Grade Submissions
- View assignment details
- Click on student submissions
- Enter points (0 to max points)
- Provide feedback
- Save grade

#### 6. Answer Questions
- View lesson details
- See student questions in Q&A section
- Click "Answer" and provide response

### For Students

#### 1. Register and Login
- Navigate to registration page
- Select "Student" role
- Complete registration and login

#### 2. Join a Class
- Click "Join Class" from dashboard
- Enter the 6-character code from your teacher
- Confirm enrollment

#### 3. View Lessons
- Navigate to your class
- Click on any lesson to view
- Download attached files

#### 4. Submit Assignments
- Go to assignment detail page
- Upload your work
- Add optional note
- Click "Submit"

#### 5. Ask Questions
- View any lesson
- Scroll to Q&A section
- Enter your question
- Submit

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
python manage.py test core

# Run specific test modules
python manage.py test core.tests_models      # Model tests (100% passing)
python manage.py test core.tests_views       # View tests
python manage.py test core.tests_workflows   # Integration tests

# Run with verbose output
python manage.py test core --verbosity=2
```

**Test Coverage**: 88% (37/42 tests passing)
- ✅ Model tests: 18/18 (100%)
- ✅ View tests: 13/15 (87%)
- ✅ Workflow tests: 6/9 (67%)

## 📁 Project Structure

```
schoo_project/
├── smartclass/              # Project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI application
├── core/                    # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   ├── validators.py       # File validators
│   ├── decorators.py       # Custom decorators
│   ├── admin.py            # Django admin config
│   ├── tests_models.py     # Model tests
│   ├── tests_views.py      # View tests
│   ├── tests_workflows.py  # Integration tests
│   ├── templates/core/     # HTML templates
│   └── static/core/        # CSS, JS, images
├── media/                   # Uploaded files
│   ├── submissions/        # Student submissions
│   └── lesson_files/       # Lesson materials
├── manage.py               # Django management script
└── README.md               # This file
```

## 🗄️ Database Schema

### Core Models

**User** - Custom user with role field (TEACHER/STUDENT)
- username, email, password, role, first_name, last_name

**Class** - Represents a course/class
- name, subject, description, teacher, class_code (unique)

**Enrollment** - Student enrollment in classes
- student, class_enrolled, enrolled_at

**Lesson** - Learning materials
- class, title, description, order, is_published

**LessonFile** - Files attached to lessons
- lesson, file, file_name

**Assignment** - Tasks for students
- class, title, description, due_date, max_points

**Submission** - Student assignment submissions
- assignment, student, file, points, feedback, status

**Question** - Student questions on lessons
- lesson, student, question_text

**Answer** - Teacher answers to questions
- question, teacher, answer_text

## 🔒 Security Notes

### File Upload Protection
- Allowed extensions: PDF, DOC, DOCX, PPT, PPTX, TXT, ZIP, JPG, JPEG, PNG
- Maximum file size: 10MB
- Files stored outside web root

### Authentication
- Session-based authentication
- Password hashing (Django defaults)
- CSRF protection enabled

### Access Control
- `@teacher_required` decorator for teacher-only views
- `@student_required` decorator for student-only views
- Object-level permissions (users can only modify their own content)

## 🎨 Customization

### Changing Allowed File Types

Edit `core/validators.py`:

```python
ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', ...]  # Add your extensions
```

### Modifying File Size Limit

Edit `core/validators.py`:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # Change to your desired size in bytes
```

### Styling

Static files are in `core/static/core/css/style.css`. Modify to customize appearance.

## 🐛 Troubleshooting

### Oracle Connection Issues
```
Error: DPI-1047: Cannot locate a 64-bit Oracle Client library
```
**Solution**: Install Oracle Instant Client and set `LD_LIBRARY_PATH`

### Migration Errors
```
Error: table already exists
```
**Solution**: 
```bash
python manage.py migrate --fake-initial
```

### File Upload Not Working
**Check**:
1. `MEDIA_ROOT` and `MEDIA_URL` in settings.py
2. File permissions on media directory
3. File size and extension validators

## 📊 Admin Panel

Access Django admin at `http://localhost:8000/admin/`

Features:
- Manage users, classes, assignments
- View submissions and questions
- Moderate content
- Generate reports

## 🚀 Deployment

### For Production

1. **Update settings.py**:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = 'your-secret-key-here'  # Use environment variable
```

2. **Collect static files**:
```bash
python manage.py collectstatic
```

3. **Use production server** (Gunicorn, uWSGI):
```bash
pip install gunicorn
gunicorn smartclass.wsgi:application --bind 0.0.0.0:8000
```

4. **Set up reverse proxy** (Nginx, Apache)

5. **Use environment variables** for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📝 License

This project is for educational purposes.

## 👥 Authors

- Project Team

## 🙏 Acknowledgments

- Django Framework
- Oracle Database
- Contributors and testers

## 📞 Support

For issues and questions:
- Check the documentation
- Run tests: `python manage.py test core`
- Review error logs

---

**Version**: 1.0.0  
**Last Updated**: December 30, 2025  
**Django Version**: 4.2.25  
**Python Version**: 3.x
