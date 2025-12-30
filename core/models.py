from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import string
import random


class User(AbstractUser):
    """
    Custom user model with role-based access.
    Extends Django's AbstractUser to add teacher/student roles.
    """
    ROLE_CHOICES = [
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def is_teacher(self):
        return self.role == 'TEACHER'

    def is_student(self):
        return self.role == 'STUDENT'


class Class(models.Model):
    """
    Represents a class/course in the system.
    Teachers create classes and students join them using a unique code.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='classes_taught',
        limit_choices_to={'role': 'TEACHER'}
    )
    class_code = models.CharField(max_length=10, unique=True, editable=False)
    subject = models.CharField(max_length=100, blank=True)
    room = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'classes'
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.class_code})"

    def save(self, *args, **kwargs):
        if not self.class_code:
            self.class_code = self.generate_class_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_class_code():
        """Generate a unique 6-character alphanumeric class code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Class.objects.filter(class_code=code).exists():
                return code

    def get_student_count(self):
        return self.enrollments.count()

    def get_assignment_count(self):
        return self.assignments.count()


class Enrollment(models.Model):
    """
    Represents a student's enrollment in a class.
    """
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        limit_choices_to={'role': 'STUDENT'}
    )
    class_enrolled = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'enrollments'
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ['student', 'class_enrolled']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.get_full_name()} in {self.class_enrolled.name}"


class Lesson(models.Model):
    """
    Represents a lesson/lecture within a class.
    Teachers create lessons and attach materials.
    """
    class_lesson = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons'
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['class_lesson', 'order', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.class_lesson.name}"

    def get_questions_count(self):
        return self.questions.count()

    def get_unanswered_questions_count(self):
        return self.questions.filter(answer__isnull=True).count()


class LessonFile(models.Model):
    """
    File attachments for lessons (PDFs, slides, etc.)
    """
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='files'
    )
    file = models.FileField(upload_to='lessons/')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()  # in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lesson_files'
        verbose_name = 'Lesson File'
        verbose_name_plural = 'Lesson Files'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name} - {self.lesson.title}"


class Assignment(models.Model):
    """
    Represents homework/assignments for a class.
    """
    class_assignment = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='assignments'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_points = models.IntegerField(default=100)
    allow_late_submission = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignments'
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} - {self.class_assignment.name}"

    def is_overdue(self):
        return timezone.now() > self.due_date

    def get_submission_count(self):
        return self.submissions.count()

    def get_missing_count(self):
        """Count students who haven't submitted"""
        total_students = self.class_assignment.enrollments.filter(is_active=True).count()
        submitted = self.submissions.count()
        return total_students - submitted


class Submission(models.Model):
    """
    Student submission for an assignment.
    """
    STATUS_CHOICES = [
        ('ON_TIME', 'On Time'),
        ('LATE', 'Late'),
        ('GRADED', 'Graded'),
    ]

    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        related_name='submissions'
    )
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='submissions',
        limit_choices_to={'role': 'STUDENT'}
    )
    file = models.FileField(upload_to='submissions/')
    file_name = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    points = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        db_table = 'submissions'
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assignment.title}"

    def save(self, *args, **kwargs):
        # Set submitted_at if this is a new submission
        if not self.pk and not self.submitted_at:
            self.submitted_at = timezone.now()
        
        # Auto-determine status based on submission time
        if not self.status:
            if self.submitted_at <= self.assignment.due_date:
                self.status = 'ON_TIME'
            else:
                self.status = 'LATE'
        super().save(*args, **kwargs)


class Question(models.Model):
    """
    Student question on a lesson.
    """
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='questions',
        limit_choices_to={'role': 'STUDENT'}
    )
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Q by {self.student.get_full_name()} on {self.lesson.title}"

    def is_answered(self):
        return hasattr(self, 'answer')


class Answer(models.Model):
    """
    Teacher's answer to a student question.
    """
    question = models.OneToOneField(
        Question, 
        on_delete=models.CASCADE, 
        related_name='answer'
    )
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='answers',
        limit_choices_to={'role': 'TEACHER'}
    )
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'answers'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ['-created_at']

    def __str__(self):
        return f"A by {self.teacher.get_full_name()} to Q#{self.question.id}"


class Announcement(models.Model):
    """
    Class announcements posted by teachers.
    """
    class_announcement = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='announcements'
    )
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='announcements',
        limit_choices_to={'role': 'TEACHER'}
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'announcements'
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.class_announcement.name}"
