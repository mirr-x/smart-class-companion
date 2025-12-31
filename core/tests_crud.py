from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import Class, Lesson, Assignment, Enrollment

User = get_user_model()

class CRUDCoverageTest(TestCase):
    """
    Tests for Edit and Delete operations to ensure full API coverage.
    Covers:
    - Class: Edit, Delete
    - Lesson: Edit, Delete
    - Assignment: Edit, Delete
    """

    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='crud_teacher',
            password='testpass123',
            role='TEACHER'
        )
        self.client.login(username='crud_teacher', password='testpass123')
        
        # Initial Setup for tests
        self.class_obj = Class.objects.create(
            name='Original Class',
            subject='Original Subject',
            teacher=self.teacher
        )
        self.lesson = Lesson.objects.create(
            title='Original Lesson',
            description='Original Desc',
            class_lesson=self.class_obj,
            is_published=True
        )
        self.assignment = Assignment.objects.create(
            title='Original Assignment',
            description='Original Desc',
            class_assignment=self.class_obj,
            due_date=timezone.now() + timedelta(days=7),
            max_points=100
        )

    def test_class_crud(self):
        """Test Edit and Delete Class"""
        # Edit Class
        response = self.client.post(
            reverse('edit_class', kwargs={'class_id': self.class_obj.id}),
            {
                'name': 'Updated Class',
                'subject': 'Updated Subject',
                'description': 'Updated Desc',
                'room': '101'
            }
        )
        if response.status_code == 200:
             print("Edit Class Failed:", response.context['form'].errors)
        self.assertIn(response.status_code, [200, 302])
        self.class_obj.refresh_from_db()
        self.assertEqual(self.class_obj.name, 'Updated Class')

        # Delete Class (Soft Delete)
        response = self.client.post(
            reverse('delete_class', kwargs={'class_id': self.class_obj.id})
        )
        self.assertIn(response.status_code, [200, 302])
        self.class_obj.refresh_from_db()
        self.assertFalse(self.class_obj.is_active)

    def test_lesson_crud(self):
        """Test Edit and Delete Lesson"""
        # Edit Lesson
        response = self.client.post(
            reverse('edit_lesson', kwargs={'lesson_id': self.lesson.id}),
            {
                'title': 'Updated Lesson',
                'description': 'Updated Desc',
                'is_published': True,
                'order': 1
            }
        )
        if response.status_code == 200:
             print("Edit Lesson Failed:", response.context['form'].errors)
        self.assertIn(response.status_code, [200, 302])
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

        # Delete Lesson
        response = self.client.post(
            reverse('delete_lesson', kwargs={'lesson_id': self.lesson.id})
        )
        self.assertIn(response.status_code, [200, 302])
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_assignment_crud(self):
        """Test Edit and Delete Assignment"""
        # Edit Assignment
        response = self.client.post(
            reverse('edit_assignment', kwargs={'assignment_id': self.assignment.id}),
            {
                'title': 'Updated Assignment',
                'description': 'Updated Desc',
                'due_date': (timezone.now() + timedelta(days=10)).strftime('%Y-%m-%dT%H:%M'),
                'max_points': 50,
                'is_published': False,
                'allow_late_submission': True
            }
        )
        if response.status_code == 200:
             print("Edit Assignment Failed:", response.context['form'].errors)
        self.assertIn(response.status_code, [200, 302])
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.title, 'Updated Assignment')

        # Delete Assignment
        response = self.client.post(
            reverse('delete_assignment', kwargs={'assignment_id': self.assignment.id})
        )
        self.assertIn(response.status_code, [200, 302])
        self.assertFalse(Assignment.objects.filter(id=self.assignment.id).exists())

    def test_logout(self):
        """Test Logout"""
        response = self.client.get(reverse('logout'))
        self.assertIn(response.status_code, [200, 302])
        # Check that we are logged out (session key _auth_user_id shouldn't exist or we can't access dashboard)
        response = self.client.get(reverse('dashboard'))
        # Should redirect to login
        self.assertNotEqual(response.status_code, 200)

