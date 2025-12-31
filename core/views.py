"""
Core views for Smart Class Companion
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from .models import (
    User, Class, Enrollment, Lesson, LessonFile, Assignment, Submission, 
    Question, Answer, Announcement
)
from django.core.exceptions import PermissionDenied, ValidationError
from .validators import validate_file_extension, validate_file_size
from .decorators import teacher_required, student_required


def login_view(request):
    """Login page for teachers and students"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


def register_view(request):
    """Registration page for new users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        elif role not in ['TEACHER', 'STUDENT']:
            messages.error(request, 'Invalid role selected.')
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    
    return render(request, 'core/register.html')


@login_required
def dashboard_view(request):
    """Main dashboard - different view for teacher vs student"""
    if request.user.role == 'TEACHER':
        return teacher_dashboard(request)
    else:
        return student_dashboard(request)


def teacher_dashboard(request):
    """Teacher dashboard showing classes and stats"""
    classes = Class.objects.filter(teacher=request.user, is_active=True).defer('description').annotate(
        student_count=Count('enrollments', filter=Q(enrollments__is_active=True)),
        assignment_count=Count('assignments', filter=Q(assignments__is_published=True))
    )
    
    # Stats
    total_classes = classes.count()
    
    # Pending grading count
    pending_grading = Submission.objects.filter(
        assignment__class_assignment__teacher=request.user,
        points__isnull=True
    ).count()
    
    # Unanswered questions count
    unanswered_questions = Question.objects.filter(
        lesson__class_lesson__teacher=request.user,
        answer__isnull=True
    ).count()
    
    # Recent activity
    recent_submissions = Submission.objects.filter(
        assignment__class_assignment__teacher=request.user
    ).select_related('student', 'assignment', 'assignment__class_assignment').order_by('-submitted_at')[:5]
    
    context = {
        'classes': classes,
        'pending_grading': pending_grading,
        'unanswered_questions': unanswered_questions,
        'recent_submissions': recent_submissions,
    }
    
    return render(request, 'core/teacher_dashboard.html', context)


def student_dashboard(request):
    """Student dashboard showing enrolled classes and assignments"""
    enrollments = Enrollment.objects.filter(
        student=request.user, 
        is_active=True
    ).select_related('class_enrolled', 'class_enrolled__teacher')
    
    classes = [e.class_enrolled for e in enrollments]
    today = timezone.now()
    
    # Get all published assignments from enrolled classes
    all_assignments = Assignment.objects.filter(
        class_assignment__in=classes,
        is_published=True
    ).exclude(
        submissions__student=request.user
    )
    
    # Filter for upcoming and missing
    upcoming_assignments = all_assignments.filter(due_date__gte=today).order_by('due_date')[:5]
    missing_assignments = all_assignments.filter(due_date__lt=today).order_by('due_date')[:5]
    
    # Recent lessons
    recent_lessons = Lesson.objects.filter(
        class_lesson__in=classes,
        is_published=True
    ).select_related('class_lesson').order_by('-created_at')[:5]
    
    context = {
        'enrollments': enrollments,
        'upcoming_assignments': upcoming_assignments,
        'missing_assignments': missing_assignments,
        'recent_lessons': recent_lessons,
    }
    
    return render(request, 'core/student_dashboard.html', context)


@login_required
def home_view(request):
    """Landing page - redirect to dashboard"""
    return redirect('dashboard')


# ============= CLASS MANAGEMENT VIEWS =============

@teacher_required
def create_class(request):
    """Teacher creates a new class"""
    from .forms import ClassCreateForm
    
    if request.method == 'POST':
        form = ClassCreateForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = request.user
            new_class.save()
            messages.success(
                request, 
                f'Class "{new_class.name}" created successfully! Class code: {new_class.class_code}'
            )
            return redirect('class_detail', class_id=new_class.id)
    else:
        form = ClassCreateForm()
    
    return render(request, 'core/create_class.html', {'form': form})


@student_required
def join_class(request):
    """Student joins a class using a code"""
    from .forms import JoinClassForm
    
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_code = form.cleaned_data['class_code']
            class_obj = get_object_or_404(Class, class_code=class_code, is_active=True)
            
            # Check if already enrolled
            if Enrollment.objects.filter(student=request.user, class_enrolled=class_obj).exists():
                messages.warning(request, 'You are already enrolled in this class.')
            else:
                Enrollment.objects.create(
                    student=request.user,
                    class_enrolled=class_obj
                )
                messages.success(request, f'Successfully joined "{class_obj.name}"!')
            
            return redirect('class_detail', class_id=class_obj.id)
    else:
        form = JoinClassForm()
    
    return render(request, 'core/join_class.html', {'form': form})


@login_required
def class_detail(request, class_id):
    """View class details (different view for teacher vs student)"""
    class_obj = get_object_or_404(Class, id=class_id, is_active=True)
    
    # Check access permissions
    if request.user.role == 'TEACHER':
        if class_obj.teacher != request.user:
            messages.error(request, 'You do not have access to this class.')
            return redirect('dashboard')
    else:  # STUDENT
        if not Enrollment.objects.filter(student=request.user, class_enrolled=class_obj, is_active=True).exists():
            messages.error(request, 'You are not enrolled in this class.')
            return redirect('dashboard')
    
    # Get class data
    lessons = class_obj.lessons.filter(is_published=True).order_by('order', '-created_at')
    assignments = class_obj.assignments.filter(is_published=True).order_by('due_date')
    announcements = class_obj.announcements.all().order_by('-is_pinned', '-created_at')
    
    # Get enrollment for students
    enrollment = None
    if request.user.role == 'STUDENT':
        enrollment = Enrollment.objects.get(student=request.user, class_enrolled=class_obj)
    
    # Get class members for teacher
    members = None
    if request.user.role == 'TEACHER':
        members = Enrollment.objects.filter(class_enrolled=class_obj, is_active=True).select_related('student')
    
    context = {
        'class': class_obj,
        'lessons': lessons,
        'assignments': assignments,
        'announcements': announcements,
        'enrollment': enrollment,
        'members': members,
    }
    
    return render(request, 'core/class_detail.html', context)


@teacher_required
def edit_class(request, class_id):
    """Teacher edits class information"""
    from .forms import ClassCreateForm
    
    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
    
    if request.method == 'POST':
        form = ClassCreateForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully!')
            return redirect('class_detail', class_id=class_obj.id)
    else:
        form = ClassCreateForm(instance=class_obj)
    
    return render(request, 'core/edit_class.html', {'form': form, 'class': class_obj})


@teacher_required
def delete_class(request, class_id):
    """Teacher archives/deletes a class"""
    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
    
    if request.method == 'POST':
        class_obj.is_active = False
        class_obj.save()
        messages.success(request, f'Class "{class_obj.name}" has been archived.')
        return redirect('dashboard')
    
    return render(request, 'core/delete_class.html', {'class': class_obj})


# ============= LESSON MANAGEMENT VIEWS =============

@teacher_required
def create_lesson(request, class_id):
    """Teacher creates a new lesson for a class"""
    from .forms import LessonForm
    
    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            # Validate files first
            files = request.FILES.getlist('files')
            file_errors = False
            for f in files:
                try:
                    validate_file_extension(f)
                    validate_file_size(f)
                except ValidationError as e:
                    form.add_error(None, f"File '{f.name}': {e.message}")
                    file_errors = True
            
            if not file_errors:
                lesson = form.save(commit=False)
                lesson.class_lesson = class_obj
                lesson.save()
                
                # Handle file uploads
                for uploaded_file in files:
                    LessonFile.objects.create(
                        lesson=lesson,
                        file=uploaded_file,
                        file_name=uploaded_file.name,
                        file_size=uploaded_file.size
                    )
                
                messages.success(request, f'Lesson "{lesson.title}" created successfully!')
                return redirect('class_detail', class_id=class_obj.id)
    else:
        form = LessonForm()
    
    return render(request, 'core/create_lesson.html', {
        'form': form,
        'class': class_obj
    })


@login_required
def lesson_detail(request, lesson_id):
    """View lesson details with files and Q&A"""
    from .forms import QuestionForm
    
    lesson = get_object_or_404(Lesson, id=lesson_id, is_published=True)
    class_obj = lesson.class_lesson
    
    # Check access
    today = timezone.now()
    
    # Remove incorrect dashboard logic that was blocking this view
    # The view should show the lesson detail, regardless of role (as long as they have access)
    
    # Check access permissions
    if request.user.role == 'TEACHER':
        if class_obj.teacher != request.user:
             messages.error(request, 'Access denied.')
             return redirect('dashboard')
    elif request.user.role == 'STUDENT':
        if not Enrollment.objects.filter(student=request.user, class_enrolled=class_obj, is_active=True).exists():
             messages.error(request, 'You are not enrolled in this class.')
             return redirect('dashboard')
    
    # Get lesson files and questions
    files = lesson.files.all().order_by('-uploaded_at')
    questions = lesson.questions.all().select_related('student', 'answer__teacher').order_by('-created_at')
    
    # Handle question submission (students only)
    question_form = None
    if request.user.role == 'STUDENT':
        if request.method == 'POST':
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.lesson = lesson
                question.student = request.user
                question.save()
                messages.success(request, 'Question posted successfully!')
                return redirect('lesson_detail', lesson_id=lesson.id)
        else:
            question_form = QuestionForm()
    
    context = {
        'lesson': lesson,
        'class': class_obj,
        'files': files,
        'questions': questions,
        'question_form': question_form,
    }
    
    return render(request, 'core/lesson_detail.html', context)


@teacher_required
def edit_lesson(request, lesson_id):
    """Teacher edits a lesson"""
    from .forms import LessonForm
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Check ownership
    if lesson.class_lesson.teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            # Validate files first
            files = request.FILES.getlist('files')
            file_errors = False
            for f in files:
                try:
                    validate_file_extension(f)
                    validate_file_size(f)
                except ValidationError as e:
                    form.add_error(None, f"File '{f.name}': {e.message}")
                    file_errors = True
            
            if not file_errors:
                form.save()
                
                # Handle new file uploads
                for uploaded_file in files:
                    LessonFile.objects.create(
                        lesson=lesson,
                        file=uploaded_file,
                        file_name=uploaded_file.name,
                        file_size=uploaded_file.size
                    )
                
                messages.success(request, 'Lesson updated successfully!')
                return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = LessonForm(instance=lesson)
    
    files = lesson.files.all()
    
    return render(request, 'core/edit_lesson.html', {
        'form': form,
        'lesson': lesson,
        'files': files
    })


@teacher_required
def delete_lesson(request, lesson_id):
    """Teacher deletes a lesson"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    class_id = lesson.class_lesson.id
    
    # Check ownership
    if lesson.class_lesson.teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, f'Lesson "{lesson.title}" has been deleted.')
        return redirect('class_detail', class_id=class_id)
    
    return render(request, 'core/delete_lesson.html', {'lesson': lesson})


@teacher_required
def delete_lesson_file(request, file_id):
    """Delete a lesson file"""
    file = get_object_or_404(LessonFile, id=file_id)
    lesson_id = file.lesson.id
    
    # Check ownership
    if file.lesson.class_lesson.teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    file.delete()
    messages.success(request, f'File "{file.file_name}" deleted.')
    return redirect('edit_lesson', lesson_id=lesson_id)


# ============= Q&A MANAGEMENT VIEWS =============

@teacher_required
def answer_question(request, question_id):
    """Teacher answers a student question"""
    from .forms import AnswerForm
    
    question = get_object_or_404(Question, id=question_id)
    
    # Check if teacher owns the class
    if question.lesson.class_lesson.teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Check if already answered
    if hasattr(question, 'answer'):
        messages.warning(request, 'This question has already been answered.')
        return redirect('lesson_detail', lesson_id=question.lesson.id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.teacher = request.user
            answer.save()
            messages.success(request, 'Answer posted successfully!')
            return redirect('lesson_detail', lesson_id=question.lesson.id)
    else:
        form = AnswerForm()
    
    return render(request, 'core/answer_question.html', {
        'form': form,
        'question': question
    })


# ============= ASSIGNMENT MANAGEMENT VIEWS =============

@teacher_required
def create_assignment(request, class_id):
    """Teacher creates a new assignment"""
    from .forms import AssignmentForm
    
    class_obj = get_object_or_404(Class, id=class_id, teacher=request.user)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.class_assignment = class_obj
            assignment.save()
            messages.success(request, f'Assignment "{assignment.title}" created successfully!')
            return redirect('class_detail', class_id=class_obj.id)
    else:
        form = AssignmentForm()
    
    return render(request, 'core/create_assignment.html', {
        'form': form,
        'class': class_obj
    })


@login_required
def assignment_detail(request, assignment_id):
    """View assignment details"""
    assignment = get_object_or_404(Assignment, id=assignment_id, is_published=True)
    class_obj = assignment.class_assignment
    
    # Check access
    if request.user.role == 'TEACHER':
        if class_obj.teacher != request.user:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
        # Get all submissions for this assignment
        submissions = assignment.submissions.all().select_related('student').order_by('-submitted_at')
    else:  # STUDENT
        if not Enrollment.objects.filter(student=request.user, class_enrolled=class_obj, is_active=True).exists():
            messages.error(request, 'You must be enrolled in this class.')
            return redirect('dashboard')
        # Get student's submission
        submissions = assignment.submissions.filter(student=request.user)
    
    context = {
        'assignment': assignment,
        'class': class_obj,
        'submissions': submissions,
    }
    
    return render(request, 'core/assignment_detail.html', context)


@teacher_required
def edit_assignment(request, assignment_id):
    """Teacher edits an assignment"""
    from .forms import AssignmentForm
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Check ownership
    if assignment.class_assignment.teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = AssignmentForm(instance=assignment)
    
    return render(request, 'core/edit_assignment.html', {
        'form': form,
        'assignment': assignment
    })


@teacher_required
def delete_assignment(request, assignment_id):
    """Teacher deletes an assignment"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    class_id = assignment.class_assignment.id
    
    # Check ownership
    if assignment.class_assignment.teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, f'Assignment "{assignment.title}" has been deleted.')
        return redirect('class_detail', class_id=class_id)
    
    return render(request, 'core/delete_assignment.html', {'assignment': assignment})


@student_required
def submit_assignment(request, assignment_id):
    """Student submits work for an assignment"""
    from .forms import SubmissionForm
    
    assignment = get_object_or_404(Assignment, id=assignment_id, is_published=True)
    
    # Check enrollment
    if not Enrollment.objects.filter(
        student=request.user, 
        class_enrolled=assignment.class_assignment, 
        is_active=True
    ).exists():
        messages.error(request, 'You are not enrolled in this class.')
        return redirect('dashboard')
    
    # Check if already submitted
    existing_submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()
    
    if existing_submission and not assignment.allow_late_submission:
        messages.warning(request, 'You have already submitted this assignment.')
        return redirect('assignment_detail', assignment_id=assignment.id)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = SubmissionForm()
    
    context = {
        'form': form,
        'assignment': assignment,
        'existing_submission': existing_submission
    }
    
    return render(request, 'core/submit_assignment.html', context)


@teacher_required
def grade_submission(request, submission_id):
    """Teacher grades a student submission"""
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Check ownership
    if submission.assignment.class_assignment.teacher != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        points = request.POST.get('points')
        feedback = request.POST.get('feedback')
        
        try:
            points = int(points) if points else None
            if points is not None:
                max_points = submission.assignment.max_points
                if points < 0 or points > max_points:
                    messages.error(request, f'Points must be between 0 and {max_points}')
                else:
                    submission.points = points
                    submission.feedback = feedback
                    submission.graded_at = timezone.now()
                    submission.save()
                    messages.success(request, 'Submission graded successfully!')
                    return redirect('assignment_detail', assignment_id=submission.assignment.id)
            else:
                messages.error(request, 'Please enter a valid score.')
        except ValueError:
            messages.error(request, 'Please enter a valid number for points.')
    
    return render(request, 'core/grade_submission.html', {
        'submission': submission
    })



