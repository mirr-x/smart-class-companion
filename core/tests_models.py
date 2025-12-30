"""
Test suite for Core app models
Tests User, Class, Enrollment, Lesson, Assignment, Submission models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import Class, Enrollment, Lesson, Assignment, Submission, Question, Answer

User = get_user_model()


class UserModelTest(TestCase):
    """Test custom User model with role field"""
    
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher_test',
            email='teacher@test.com',
            password='testpass123',
            role='TEACHER',
            first_name='Test',
            last_name='Teacher'
        )
        self.student = User.objects.create_user(
            username='student_test',
            email='student@test.com',
            password='testpass123',
            role='STUDENT',
            first_name='Test',
            last_name='Student'
        )
    
    def test_user_creation(self):
        """Test user can be created with role"""
        self.assertEqual(self.teacher.role, 'TEACHER')
        self.assertEqual(self.student.role, 'STUDENT')
        self.assertTrue(self.teacher.is_active)
        self.assertTrue(self.student.is_active)
    
    def test_user_string_representation(self):
        """Test __str__ method"""
        # String representation includes full name
        self.assertIn('Test Teacher', str(self.teacher))
        self.assertIn('Test Student', str(self.student))
    
    def test_get_full_name(self):
        """Test get_full_name method"""
        self.assertEqual(self.teacher.get_full_name(), 'Test Teacher')
        self.assertEqual(self.student.get_full_name(), 'Test Student')


class ClassModelTest(TestCase):
    """Test Class model"""
    
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher_class',
            password='testpass123',
            role='TEACHER'
        )
        self.class_obj = Class.objects.create(
            name='Mathematics 101',
            subject='Math',
            description='Intro to Math',
            teacher=self.teacher
        )
    
    def test_class_creation(self):
        """Test class is created correctly"""
        self.assertEqual(self.class_obj.name, 'Mathematics 101')
        self.assertEqual(self.class_obj.teacher, self.teacher)
        self.assertTrue(self.class_obj.is_active)
        self.assertIsNotNone(self.class_obj.class_code)
    
    def test_class_code_unique(self):
        """Test class code is unique"""
        class2 = Class.objects.create(
            name='Science 101',
            subject='Science',
            teacher=self.teacher
        )
        self.assertNotEqual(self.class_obj.class_code, class2.class_code)
    
    def test_class_code_length(self):
        """Test class code has correct length"""
        self.assertEqual(len(self.class_obj.class_code), 6)
    
    def test_class_string_representation(self):
        """Test __str__ method"""
        expected = f"{self.class_obj.name} ({self.class_obj.class_code})"
        self.assertEqual(str(self.class_obj), expected)


class EnrollmentModelTest(TestCase):
    """Test Enrollment model"""
    
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher_enroll',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_enroll',
            password='testpass123',
            role='STUDENT'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            subject='Test',
            teacher=self.teacher
        )
    
    def test_enrollment_creation(self):
        """Test student can enroll in class"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            class_enrolled=self.class_obj
        )
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.class_enrolled, self.class_obj)
        self.assertTrue(enrollment.is_active)
    
    def test_unique_enrollment(self):
        """Test student cannot enroll twice in same class"""
        Enrollment.objects.create(
            student=self.student,
            class_enrolled=self.class_obj
        )
        # Try to create duplicate
        with self.assertRaises(Exception):
            Enrollment.objects.create(
                student=self.student,
                class_enrolled=self.class_obj
            )


class LessonModelTest(TestCase):
    """Test Lesson model"""
    
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher_lesson',
            password='testpass123',
            role='TEACHER'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            subject='Test',
            teacher=self.teacher
        )
        self.lesson = Lesson.objects.create(
            title='Introduction',
            description='Lesson content here',
            class_lesson=self.class_obj
        )
    
    def test_lesson_creation(self):
        """Test lesson is created correctly"""
        self.assertEqual(self.lesson.title, 'Introduction')
        self.assertEqual(self.lesson.class_lesson, self.class_obj)
        self.assertTrue(self.lesson.is_published)
    
    def test_lesson_ordering(self):
        """Test lessons are ordered by creation date"""
        lesson2 = Lesson.objects.create(
            title='Lesson 2',
            description='Content 2',
            class_lesson=self.class_obj
        )
        lessons = Lesson.objects.filter(class_lesson=self.class_obj)
        self.assertEqual(lessons[0], lesson2)  # Most recent first
        self.assertEqual(lessons[1], self.lesson)


class AssignmentModelTest(TestCase):
    """Test Assignment model"""
    
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher_assign',
            password='testpass123',
            role='TEACHER'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            subject='Test',
            teacher=self.teacher
        )
        self.due_date = timezone.now() + timedelta(days=7)
        self.assignment = Assignment.objects.create(
            title='Homework 1',
            description='Complete exercises',
            class_assignment=self.class_obj,
            due_date=self.due_date,
            max_points=100
        )
    
    def test_assignment_creation(self):
        """Test assignment is created correctly"""
        self.assertEqual(self.assignment.title, 'Homework 1')
        self.assertEqual(self.assignment.max_points, 100)
        self.assertEqual(self.assignment.class_assignment, self.class_obj)
        self.assertTrue(self.assignment.is_published)
    
    def test_assignment_due_date(self):
        """Test due date is set correctly"""
        self.assertIsNotNone(self.assignment.due_date)
        self.assertGreater(self.assignment.due_date, timezone.now())


class SubmissionModelTest(TestCase):
    """Test Submission model"""
    
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher_sub',
            password='testpass123',
            role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_sub',
            password='testpass123',
            role='STUDENT'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            subject='Test',
            teacher=self.teacher
        )
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            class_assignment=self.class_obj,
            due_date=timezone.now() + timedelta(days=1),
            max_points=100
        )
    
    def test_submission_creation(self):
        """Test submission can be created"""
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file='test_file.txt',
            file_name='test_file.txt',
            status='ON_TIME'
        )
        self.assertEqual(submission.student, self.student)
        self.assertEqual(submission.assignment, self.assignment)
        self.assertIsNone(submission.points)
        self.assertIsNotNone(submission.submitted_at)
    
    def test_submission_grading(self):
        """Test submission can be graded"""
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file='test_file.txt',
            file_name='test_file.txt',
            status='ON_TIME'
        )
        submission.points = 95
        submission.feedback = 'Great work!'
        submission.save()
        
        self.assertEqual(submission.points, 95)
        self.assertEqual(submission.feedback, 'Great work!')
    
    def test_late_submission_status(self):
        """Test late submission detection"""
        # Create assignment with past due date
        past_assignment = Assignment.objects.create(
            title='Past Due',
            class_assignment=self.class_obj,
            due_date=timezone.now() - timedelta(days=1),
            max_points=100
        )
        submission = Submission.objects.create(
            assignment=past_assignment,
            student=self.student,
            file='test_file.txt',
            file_name='test_file.txt',
            status='LATE'
        )
        # Submission is late if submitted after due date
        self.assertGreater(submission.submitted_at, past_assignment.due_date)


class QuestionAnswerModelTest(TestCase):
    """Test Question and Answer models"""
    
    def setUp(self):
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
            name='Test Class',
            subject='Test',
            teacher=self.teacher
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Content',
            class_lesson=self.class_obj
        )
    
    def test_question_creation(self):
        """Test student can create question"""
        question = Question.objects.create(
            lesson=self.lesson,
            student=self.student,
            question_text='What is this?'
        )
        self.assertEqual(question.student, self.student)
        self.assertEqual(question.lesson, self.lesson)
        self.assertIsNotNone(question.created_at)
    
    def test_answer_creation(self):
        """Test teacher can answer question"""
        question = Question.objects.create(
            lesson=self.lesson,
            student=self.student,
            question_text='What is this?'
        )
        answer = Answer.objects.create(
            question=question,
            teacher=self.teacher,
            answer_text='This is the answer'
        )
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.teacher, self.teacher)
        self.assertIsNotNone(answer.created_at)
        
        # Verify question now has answer
        question.refresh_from_db()
        self.assertIsNotNone(question.answer)
