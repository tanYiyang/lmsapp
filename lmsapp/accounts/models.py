from django.db import models
from django.contrib.auth.models import User
from PIL import Image
#default.jpg from https://www.vecteezy.com/vector-art/20765399-default-profile-account-unknown-icon-black-silhouette

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(default='default.jpg')
    profile_url = models.CharField(max_length=250, blank=True, null=True)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' Profile'
    
    def save(self, *args, **kwargs):
        if not self.profile_url:  # Check if profile_url is not set
            self.profile_url = f'/profiles/{self.user.username}/'
        super().save(*args, **kwargs)
        

    def get_profile_url(self):
        return f'/profiles/{self.user.username}/'

class Teacher_request(models.Model):
    teacher_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    teacher_email = models.EmailField(max_length=200)

    def __str__(self):
        return self.teacher_profile.user.username
    
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

class Feedback(models.Model):
    student = models.ForeignKey(User, related_name='feedbacks', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='feedbacks', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

