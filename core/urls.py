"""
URL Configuration for core app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Class Management
    path('class/create/', views.create_class, name='create_class'),
    path('class/join/', views.join_class, name='join_class'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('class/<int:class_id>/edit/', views.edit_class, name='edit_class'),
    path('class/<int:class_id>/delete/', views.delete_class, name='delete_class'),
    
    # Lesson Management
    path('class/<int:class_id>/lesson/create/', views.create_lesson, name='create_lesson'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('lesson/file/<int:file_id>/delete/', views.delete_lesson_file, name='delete_lesson_file'),
    
    # Q&A
    path('question/<int:question_id>/answer/', views.answer_question, name='answer_question'),
    
    # Assignment Management
    path('class/<int:class_id>/assignment/create/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/edit/', views.edit_assignment, name='edit_assignment'),
    path('assignment/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
]
