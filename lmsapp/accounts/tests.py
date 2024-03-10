from django.test import TestCase
from .models import *

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            first_name='Emily',
            last_name='Smith',
            address='101 Elm Street, Rivertown, OH 43015'
        )
        self.assertEqual(profile.user.username, 'test_user')
        self.assertEqual(profile.get_profile_url(), '/profiles/test_user/')

    def test_teacher_request_creation(self):
        teacher_request = Teacher_request.objects.create(user=self.user)
        self.assertEqual(str(teacher_request), 'Teacher request for test_user')
