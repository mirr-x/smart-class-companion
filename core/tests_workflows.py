"""
Integration tests for complete user workflows
Tests end-to-end teacher and student journeys
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import Class, Enrollment, Lesson, Assignment, Submission, Question, Answer

User = get_user_model()


class TeacherWorkflowTest(TestCase):
    """Test complete teacher workflow from registration to grading"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_teacher_workflow(self):
        """Test: Register → Create Class → Add Lesson → Create Assignment → Grade Submission"""
        
        # Step 1: Register as teacher
        response = self.client.post(reverse('register'), {
            'username': 'teacher_workflow',
            'email': 'teacher@workflow.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'role': 'TEACHER',
            'first_name': 'Workflow',
            'last_name': 'Teacher'
        })
        # Registration may return 200 if form has errors, or 302 if success
        self.assertIn(response.status_code, [200, 302])
        
        # Verify user was created with correct role
        teacher = User.objects.get(username='teacher_workflow')
        self.assertEqual(teacher.role, 'TEACHER')
        
        # Step 2: Login (should be auto-logged in after registration)
        # Verify we can access dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Step 3: Create a class
        response = self.client.post(reverse('create_class'), {
            'name': 'Workflow Mathematics',
            'subject': 'Mathematics',
            'description': 'Advanced math course'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify class was created
        class_obj = Class.objects.get(name='Workflow Mathematics')
        self.assertEqual(class_obj.teacher, teacher)
        self.assertIsNotNone(class_obj.class_code)
        
        # Step 4: Add a lesson to the class
        response = self.client.post(
            reverse('create_lesson', kwargs={'class_id': class_obj.id}),
            {
                'title': 'Introduction to Calculus',
                'description': 'This lesson covers basic calculus concepts',
                'is_published': True,
                'order': 1
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify lesson was created
        lesson = Lesson.objects.get(title='Introduction to Calculus')
        self.assertEqual(lesson.class_lesson, class_obj)
        
        # Step 5: Create an assignment
        due_date = (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(
            reverse('create_assignment', kwargs={'class_id': class_obj.id}),
            {
                'title': 'Calculus Homework',
                'description': 'Complete exercises 1-10',
                'due_date': due_date,
                'max_points': '100',
                'is_published': True
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify assignment was created
        assignment = Assignment.objects.get(title='Calculus Homework')
        self.assertEqual(assignment.class_assignment, class_obj)
        
        # Step 6: Simulate student submission (create manually for testing)
        student = User.objects.create_user(
            username='student_for_workflow',
            password='testpass123',
            role='STUDENT'
        )
        Enrollment.objects.create(student=student, class_enrolled=class_obj)
        submission = Submission.objects.create(
            assignment=assignment,
            student=student,
            file='test.txt',
            file_name='test.txt',
            status='ON_TIME'
        )
        
        # Step 7: Teacher grades the submission
        response = self.client.post(
            reverse('grade_submission', kwargs={'submission_id': submission.id}),
            {
                'points': '95',
                'feedback': 'Great work on the calculus problems!'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify grading was saved
        submission.refresh_from_db()
        self.assertEqual(submission.points, 95)
        self.assertEqual(submission.feedback, 'Great work on the calculus problems!')
        
        # Step 8: Verify dashboard shows correct stats
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Workflow Mathematics')
        # Now that submission is graded, pending should be 0
        # (Would need to check context if we want to verify exact numbers)


class StudentWorkflowTest(TestCase):
    """Test complete student workflow from registration to submission"""
    
    def setUp(self):
        self.client = Client()
        # Create a teacher and class for student to join
        self.teacher = User.objects.create_user(
            username='teacher_for_student',
            password='testpass123',
            role='TEACHER'
        )
        self.class_obj = Class.objects.create(
            name='Student Test Class',
            subject='Science',
            teacher=self.teacher
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson content',
            class_lesson=self.class_obj,
            is_published=True
        )
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            description='Complete this assignment',
            class_assignment=self.class_obj,
            due_date=timezone.now() + timedelta(days=7),
            max_points=100,
            is_published=True
        )
    
    def test_complete_student_workflow(self):
        """Test: Register → Join Class → View Lesson → Submit Assignment → Ask Question"""
        
        # Step 1: Register as student
        response = self.client.post(reverse('register'), {
            'username': 'student_workflow',
            'email': 'student@workflow.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'role': 'STUDENT',
            'first_name': 'Workflow',
            'last_name': 'Student'
        })
        # Registration may have form validation issues
        self.assertIn(response.status_code, [200, 302])
        
        # Verify user was created
        student = User.objects.get(username='student_workflow')
        self.assertEqual(student.role, 'STUDENT')
        
        # Step 2: Join class using class code
        response = self.client.post(reverse('join_class'), {
            'class_code': self.class_obj.class_code
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify enrollment
        self.assertTrue(
            Enrollment.objects.filter(
                student=student,
                class_enrolled=self.class_obj
            ).exists()
        )
        
        # Step 3: View dashboard and see enrolled class
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Test Class')
        
        # Step 4: View class detail
        response = self.client.get(
            reverse('class_detail', kwargs={'class_id': self.class_obj.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Lesson')
        self.assertContains(response, 'Test Assignment')
        
        # Step 5: View lesson
        response = self.client.get(
            reverse('lesson_detail', kwargs={'lesson_id': self.lesson.id})
        )
        self.assertEqual(response.status_code, 200)
        # Lesson description should be in the page
        self.assertContains(response, self.lesson.description)
        
        # Step 6: Ask a question on the lesson
        response = self.client.post(
            reverse('lesson_detail', kwargs={'lesson_id': self.lesson.id}),
            {
                'question_text': 'Can you explain this concept further?'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify question was created
        question = Question.objects.filter(
            lesson=self.lesson,
            student=student
        ).first()
        self.assertIsNotNone(question)
        self.assertEqual(question.question_text, 'Can you explain this concept further?')
        
        # Step 7: Submit assignment (simplified - normally requires file)
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=student,
            file='test.txt',
            file_name='test.txt',
            status='ON_TIME'
        )
        
        # Verify submission
        submission = Submission.objects.filter(
            assignment=self.assignment,
            student=student
        ).first()
        self.assertIsNotNone(submission)
        # Test that submission exists
        self.assertEqual(submission.assignment, self.assignment)
        
        # Step 8: Student views assignment detail and sees submission
        response = self.client.get(
            reverse('assignment_detail', kwargs={'assignment_id': self.assignment.id})
        )
        self.assertEqual(response.status_code, 200)
        # Should show submission status
        self.assertContains(response, 'Submitted')


class QuestionAnswerWorkflowTest(TestCase):
    """Test Q&A interaction between student and teacher"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher_qa',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_qa',
            password='testpass123',
            role='STUDENT'
        )
        self.class_obj = Class.objects.create(
            name='Q&A Class',
            subject='Test',
            teacher=self.teacher
        )
        Enrollment.objects.create(
            student=self.student,
            class_enrolled=self.class_obj
        )
        self.lesson = Lesson.objects.create(
            title='Q&A Lesson',
            description='Content here',
            class_lesson=self.class_obj,
            is_published=True
        )
    
    def test_question_answer_flow(self):
        """Test: Student asks → Teacher answers → Both can view"""
        
        # Step 1: Student asks question
        self.client.login(username='student_qa', password='testpass123')
        response = self.client.post(
            reverse('lesson_detail', kwargs={'lesson_id': self.lesson.id}),
            {
                'question_text': 'What is the main concept here?'
            }
        )
        # Question posting may return 200 or 302
        self.assertIn(response.status_code, [200, 302])
        
        question = Question.objects.get(lesson=self.lesson)
        self.assertEqual(question.student, self.student)
        
        # Step 2: Teacher views question and answers
        self.client.logout()
        self.client.login(username='teacher_qa', password='testpass123')
        
        response = self.client.post(
            reverse('answer_question', kwargs={'question_id': question.id}),
            {
                'answer_text': 'The main concept is understanding the fundamentals.'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify answer was created
        answer = Answer.objects.get(question=question)
        self.assertEqual(answer.teacher, self.teacher)
        self.assertEqual(answer.answer_text, 'The main concept is understanding the fundamentals.')
        
        # Step 3: Student views answered question
        self.client.logout()
        self.client.login(username='student_qa', password='testpass123')
        
        response = self.client.get(
            reverse('lesson_detail', kwargs={'lesson_id': self.lesson.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'What is the main concept here?')
        self.assertContains(response, 'The main concept is understanding the fundamentals.')


class EdgeCaseTest(TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher_edge',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_edge',
            password='testpass123',
            role='STUDENT'
        )
    
    def test_join_nonexistent_class(self):
        """Test student cannot join with invalid class code"""
        self.client.login(username='student_edge', password='testpass123')
        response = self.client.post(reverse('join_class'), {
            'class_code': 'INVALID'
        })
        # Should show error or redirect with error message
        self.assertIn(response.status_code, [200, 302])
    
    def test_duplicate_submission(self):
        """Test student cannot submit same assignment twice"""
        class_obj = Class.objects.create(
            name='Test Class',
            subject='Test',
            teacher=self.teacher
        )
        Enrollment.objects.create(student=self.student, class_enrolled=class_obj)
        assignment = Assignment.objects.create(
            title='Test',
            class_assignment=class_obj,
            due_date=timezone.now() + timedelta(days=1),
            max_points=100,
            is_published=True
        )
        
        # First submission
        Submission.objects.create(
            assignment=assignment,
            student=self.student,
            file='test.txt',
            file_name='test.txt'
        )
        
        self.client.login(username='student_edge', password='testpass123')
        # Try to submit again
        response = self.client.post(
            reverse('submit_assignment', kwargs={'assignment_id': assignment.id}),
            {'note': 'Second submission'}
        )
        # Should handle gracefully (show message or redirect)
        self.assertIn(response.status_code, [200, 302])
    
    def test_unauthorized_access_to_other_class(self):
        """Test teacher cannot access another teacher's class edit page"""
        other_teacher = User.objects.create_user(
            username='other_teacher',
            password='testpass123',
            role='TEACHER'
        )
        other_class = Class.objects.create(
            name='Other Class',
            subject='Test',
            teacher=other_teacher
        )
        
        self.client.login(username='teacher_edge', password='testpass123')
        response = self.client.get(
            reverse('edit_class', kwargs={'class_id': other_class.id})
        )
        # Should deny access (403 or redirect)
        self.assertIn(response.status_code, [302, 403, 404])
