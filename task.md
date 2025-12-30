Smart Class Companion - Task Checklist
PHASE 0 — Understand the System
 Review project requirements and objectives
 Identify core features (Classes, Lessons, Assignments, Submissions, Q&A, Dashboards)
PHASE 1 — Project Setup
 Environment setup
 Create virtual environment
 Install Django and Oracle dependencies (cx_Oracle/oracledb)
 Create Django project structure
 Initialize Django project smartclass
 Create Django app core
 Configure Oracle database in settings
 Test database connection
 Verify Django admin works
PHASE 2 — Database & Models
 Design database schema (ER diagram)
 Implement Django models
 Custom User model with role field
 Class model
 Enrollment model
 Lesson model
 Assignment model
 Submission model
 Question model
 Answer model
 Run migrations
 Verify tables in Oracle
PHASE 3 — Authentication & Roles
 Extend Django AbstractUser
 Add role field (TEACHER/STUDENT)
 Implement session-based login/logout
 Create permission decorators
 @teacher_required
 @student_required
 Apply decorators to views
PHASE 4 — Core Class System
 Class creation (Teacher)
 Auto-generate class code
 Join class (Student)
 Validate enrollment
 Class detail page
PHASE 5 — Lessons System
 Create lesson (Teacher)
 Lesson file upload handling
 View lesson (Student)
 Download lesson files
 Q&A on lessonsctionality
PHASE 6 — Assignments & Submissions
 Create assignment (Teacher)
 Student submission
 Grading system
 View submissions
 Late submission handling status (on-time/late)
 View submissions (Teacher)
 Track missing assignments
PHASE 7 — Q&A System
 Ask question (Student)
 Answer question (Teacher)
 Mark answered/unanswered
 Sort and filter questions
PHASE 8 — Dashboards
 Student dashboard
 Missing assignments
 Upcoming deadlines
 Recent lessons
 Teacher dashboard
 Class overview
 Submission statistics
 Unanswered questions
PHASE 9 — UI & UX Polish
 Create responsive layout
 Design clean navigation
 Add CSS styling
 Optimize user flows
PHASE 10 — Security & Validation
 Form validation
 Role-based access control
 File upload protection
 Session management
PHASE 11 — Testing
 Test teacher workflows
 Test student workflows
 Test edge cases
 Fix identified bugs
PHASE 12 — Documentation
 Project description
 System architecture
 ER diagram
 User flows
 Screenshots
 README
PHASE 13 — Final Review
 Code cleanup
 Remove unused files
 GitHub repository
 Deployment preparation