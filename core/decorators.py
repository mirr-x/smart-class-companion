"""
Permission decorators for role-based access control
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def teacher_required(view_func):
    """
    Decorator to restrict access to teachers only.
    Usage: @teacher_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        if request.user.role != 'TEACHER':
            messages.error(request, 'Access denied. This page is for teachers only.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def student_required(view_func):
    """
    Decorator to restrict access to students only.
    Usage: @student_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        if request.user.role != 'STUDENT':
            messages.error(request, 'Access denied. This page is for students only.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def role_required(*allowed_roles):
    """
    Decorator to restrict access to specific roles.
    Usage: @role_required('TEACHER', 'STUDENT')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, f'Access denied. This page is restricted.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
