"""
Forms for Smart Class Companion
"""
from django import forms
from .models import (
    Class, Enrollment, Lesson, LessonFile, Assignment, Submission, 
    Question, Answer, Announcement
)


class ClassCreateForm(forms.ModelForm):
    """Form for teachers to create a new class"""
    
    class Meta:
        model = Class
        fields = ['name', 'description', 'subject', 'room']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science 101'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Brief description of the class...'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science'
            }),
            'room': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Room 201'
            }),
        }


class JoinClassForm(forms.Form):
    """Form for students to join a class using a code"""
    class_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-character class code',
            'style': 'text-transform: uppercase;'
        })
    )

    def clean_class_code(self):
        code = self.cleaned_data['class_code'].upper()
        try:
            Class.objects.get(class_code=code, is_active=True)
        except Class.DoesNotExist:
            raise forms.ValidationError('Invalid class code. Please check and try again.')
        return code


class LessonForm(forms.ModelForm):
    """Form for teachers to create/edit lessons"""
    
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'order', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lesson title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Lesson content and instructions...'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class AssignmentForm(forms.ModelForm):
    """Form for teachers to create/edit assignments"""
    
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_points', 'allow_late_submission', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Assignment title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Assignment instructions and requirements...'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'value': 100
            }),
            'allow_late_submission': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


from .validators import validate_file_extension, validate_file_size

class SubmissionForm(forms.ModelForm):
    """Form for students to submit assignments"""
    
    file = forms.FileField(
        validators=[validate_file_extension, validate_file_size],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt,.zip'
        })
    )

    class Meta:
        model = Submission
        fields = ['file']


class QuestionForm(forms.ModelForm):
    """Form for students to ask questions"""
    
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Type your question here...'
            }),
        }


class AnswerForm(forms.ModelForm):
    """Form for teachers to answer questions"""
    
    class Meta:
        model = Answer
        fields = ['answer_text']
        widgets = {
            'answer_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Type your answer here...'
            }),
        }


class AnnouncementForm(forms.ModelForm):
    """Form for teachers to post announcements"""
    
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Announcement title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Announcement content...'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
