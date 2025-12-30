from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Class, Enrollment, Lesson, LessonFile,
    Assignment, Submission, Question, Answer, Announcement
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Profile', {'fields': ('role', 'bio', 'avatar')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Profile', {'fields': ('role', 'email', 'first_name', 'last_name')}),
    )


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """Admin configuration for Class model"""
    list_display = ['name', 'teacher', 'class_code', 'subject', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'class_code', 'subject', 'teacher__username']
    readonly_fields = ['class_code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'teacher', 'subject', 'room')
        }),
        ('Status', {
            'fields': ('is_active', 'class_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for Enrollment model"""
    list_display = ['student', 'class_enrolled', 'enrolled_at', 'is_active']
    list_filter = ['is_active', 'enrolled_at']
    search_fields = ['student__username', 'class_enrolled__name']
    readonly_fields = ['enrolled_at']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model"""
    list_display = ['title', 'class_lesson', 'order', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'class_lesson__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LessonFile)
class LessonFileAdmin(admin.ModelAdmin):
    """Admin configuration for LessonFile model"""
    list_display = ['file_name', 'lesson', 'file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['file_name', 'lesson__title']
    readonly_fields = ['uploaded_at']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin configuration for Assignment model"""
    list_display = ['title', 'class_assignment', 'due_date', 'max_points', 'is_published']
    list_filter = ['is_published', 'due_date', 'created_at']
    search_fields = ['title', 'class_assignment__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for Submission model"""
    list_display = ['student', 'assignment', 'status', 'points', 'submitted_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['student__username', 'assignment__title']
    readonly_fields = ['submitted_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model"""
    list_display = ['student', 'lesson', 'is_answered', 'created_at']
    list_filter = ['created_at']
    search_fields = ['student__username', 'lesson__title', 'question_text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin configuration for Answer model"""
    list_display = ['teacher', 'question', 'created_at']
    list_filter = ['created_at']
    search_fields = ['teacher__username', 'question__question_text']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Admin configuration for Announcement model"""
    list_display = ['title', 'class_announcement', 'teacher', 'is_pinned', 'created_at']
    list_filter = ['is_pinned', 'created_at']
    search_fields = ['title', 'class_announcement__name', 'teacher__username']
    readonly_fields = ['created_at', 'updated_at']
