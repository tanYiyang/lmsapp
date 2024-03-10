from django.test import TestCase
from .models import *
from accounts.models import *

class CourseAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Emily',
            last_name='Smith',
            address='101 Elm Street, Rivertown, OH 43015',
            is_teacher=True
        )

    def test_course_str_method(self):
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            teacher=self.profile
        )
        self.assertEqual(str(self.course), 'Test Course')


class FeedbackModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Emily',
            last_name='Smith',
            address='101 Elm Street, Rivertown, OH 43015',
            is_teacher=True
        )
        self.course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.profile)
        

    def test_feedback_str_method(self):
        self.feedback = Feedback.objects.create(
            student=self.user, 
            course=self.course, 
            content='Test Content'
        )
        self.assertEqual(str(self.feedback), 'Test Content')

class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Emily',
            last_name='Smith',
            address='101 Elm Street, Rivertown, OH 43015',
            is_teacher=True
        )
        self.course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.profile)

    def test_post_str_method(self):
        self.post = Post.objects.create(
            title='Test Post', 
            content='Test Content', 
            course=self.course
        )
        self.assertEqual(str(self.post), 'Test Post')

class SubmissionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Emily',
            last_name='Smith',
            address='101 Elm Street, Rivertown, OH 43015',
            is_teacher=True
        )
        self.course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.profile)
        self.post = Post.objects.create(title='Test Post', content='Test Content', course=self.course)

    def test_submission_str_method(self):
        self.submission = Submission.objects.create(
            student=self.user, 
            post=self.post, 
            submitted_file='test_file.txt'
        )
        self.submitted_at = self.submission.submitted_at
        expected_str = f"Submission by {self.user.username} for {self.post.title} submitted at {self.submitted_at}"
        self.assertEqual(str(self.submission), expected_str)

class NotificationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        

    def test_notification_str_method(self):
        self.notification = Notification.objects.create(
            user=self.user, 
            notification_type='Post', 
            message='Test Message'
        )
        expected_str = f'{self.user.username} created a notification Test Message of Post type'
        self.assertEqual(str(self.notification), expected_str)

