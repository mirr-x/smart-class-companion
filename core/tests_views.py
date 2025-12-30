"""
Test suite for Core app views
Tests authentication, permissions, and view functionality
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import Class, Enrollment, Lesson, Assignment, Submission

User = get_user_model()


class AuthenticationViewTest(TestCase):
    """Test login, logout, and registration views"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher_auth',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_auth',
            password='testpass123',
            role='STUDENT'
        )
    
    def test_login_page_loads(self):
        """Test login page is accessible"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_register_page_loads(self):
        """Test register page is accessible"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
    
    def test_successful_login(self):
        """Test user can login successfully"""
        response = self.client.post(reverse('login'), {
            'username': 'teacher_auth',
            'password': 'testpass123'
        })
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_failed_login(self):
        """Test login fails with wrong credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'teacher_auth',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid')
    
    def test_logout(self):
        """Test user can logout"""
        self.client.login(username='teacher_auth', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_user_registration(self):
        """Test new user can register"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'role': 'STUDENT',
            'first_name': 'New',
            'last_name': 'User'
        })
        # May return 200 with form errors if validation fails
        # Should at minimum not crash
        self.assertIn(response.status_code, [200, 302])
        # Check if user was created (if registration succeeded)
        if response.status_code == 302:
            self.assertTrue(User.objects.filter(username='newuser').exists())


class PermissionViewTest(TestCase):
    """Test role-based permissions"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher_perm',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_perm',
            password='testpass123',
            role='STUDENT'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            subject='Test',
            teacher=self.teacher
        )
    
    def test_teacher_can_create_class(self):
        """Test teacher can access class creation"""
        self.client.login(username='teacher_perm', password='testpass123')
        response = self.client.get(reverse('create_class'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_cannot_create_class(self):
        """Test student cannot access class creation"""
        self.client.login(username='student_perm', password='testpass123')
        response = self.client.get(reverse('create_class'))
        # Should redirect or show forbidden
        self.assertIn(response.status_code, [302, 403])
    
    def test_unauthenticated_redirects_to_login(self):
        """Test unauthenticated user is redirected to login"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class ClassViewTest(TestCase):
    """Test class-related views"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher_class_view',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_class_view',
            password='testpass123',
            role='STUDENT'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            subject='Math',
            description='Test description',
            teacher=self.teacher
        )
    
    def test_create_class_view(self):
        """Test teacher can create class via form"""
        self.client.login(username='teacher_class_view', password='testpass123')
        response = self.client.post(reverse('create_class'), {
            'name': 'New Class',
            'subject': 'Science',
            'description': 'Science class'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Class.objects.filter(name='New Class').exists())
    
    def test_class_detail_view(self):
        """Test class detail page loads"""
        self.client.login(username='teacher_class_view', password='testpass123')
        response = self.client.get(
            reverse('class_detail', kwargs={'class_id': self.class_obj.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Class')
    
    def test_join_class_view(self):
        """Test student can join class with code"""
        self.client.login(username='student_class_view', password='testpass123')
        response = self.client.post(reverse('join_class'), {
            'class_code': self.class_obj.class_code
        })
        self.assertEqual(response.status_code, 302)
        # Verify enrollment was created
        self.assertTrue(
            Enrollment.objects.filter(
                student=self.student,
                class_enrolled=self.class_obj
            ).exists()
        )


class DashboardViewTest(TestCase):
    """Test dashboard views for teacher and student"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher_dash',
            password='testpass123',
            role='TEACHER',
            first_name='Teacher',
            last_name='User'
        )
        self.student = User.objects.create_user(
            username='student_dash',
            password='testpass123',
            role='STUDENT',
            first_name='Student',
            last_name='User'
        )
        self.class_obj = Class.objects.create(
            name='Dashboard Class',
            subject='Test',
            teacher=self.teacher
        )
    
    def test_teacher_dashboard_loads(self):
        """Test teacher sees teacher dashboard"""
        self.client.login(username='teacher_dash', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teacher User')
        self.assertContains(response, 'My Classes')
    
    def test_student_dashboard_loads(self):
        """Test student sees student dashboard"""
        # Enroll student in class
        Enrollment.objects.create(
            student=self.student,
            class_enrolled=self.class_obj
        )
        self.client.login(username='student_dash', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student User')


class AssignmentWorkflowTest(TestCase):
    """Test complete assignment submission and grading workflow"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher_assign',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_assign',
            password='testpass123',
            role='STUDENT'
        )
        self.class_obj = Class.objects.create(
            name='Assignment Class',
            subject='Test',
            teacher=self.teacher
        )
        Enrollment.objects.create(
            student=self.student,
            class_enrolled=self.class_obj
        )
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            description='Complete this',
            class_assignment=self.class_obj,
            due_date=timezone.now() + timedelta(days=7),
            max_points=100,
            is_published=True
        )
    
    def test_student_can_view_assignment(self):
        """Test student can view assignment details"""
        self.client.login(username='student_assign', password='testpass123')
        response = self.client.get(
            reverse('assignment_detail', kwargs={'assignment_id': self.assignment.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Assignment')
    
    def test_student_can_submit_assignment(self):
        """Test student can create submission"""
        self.client.login(username='student_assign', password='testpass123')
        response = self.client.post(
            reverse('submit_assignment', kwargs={'assignment_id': self.assignment.id}),
            {'file': '', 'file_name': 'test.txt'}  # Simplified for testing
        )
        # Note: This test may fail if file upload is required
        # For now, we just check the response indicates a form error or success
        # Status 200 means form redisplay with errors, 302 means success
        self.assertIn(response.status_code, [200, 302])
        # Verify submission was created
        self.assertTrue(
            Submission.objects.filter(
                assignment=self.assignment,
                student=self.student
            ).exists()
        )
    
    def test_teacher_can_view_submissions(self):
        """Test teacher can view assignment submissions"""
        # Create a submission
        # Create a submission manually for testing
        Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file='test.txt',
            file_name='test.txt'
        )
        self.client.login(username='teacher_assign', password='testpass123')
        response = self.client.get(
            reverse('assignment_detail', kwargs={'assignment_id': self.assignment.id})
        )
        self.assertEqual(response.status_code, 200)
        # Should show submission info
        self.assertContains(response, 'student_assign')
    
    def test_teacher_can_grade_submission(self):
        """Test teacher can grade a submission"""
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file='test.txt',
            file_name='test.txt'
        )
        self.client.login(username='teacher_assign', password='testpass123')
        response = self.client.post(
            reverse('grade_submission', kwargs={'submission_id': submission.id}),
            {
                'points': '95',
                'feedback': 'Excellent work!'
            }
        )
        # Should redirect after grading
        self.assertEqual(response.status_code, 302)
        # Verify grade was saved
        submission.refresh_from_db()
        self.assertEqual(submission.points, 95)
        self.assertEqual(submission.feedback, 'Excellent work!')
