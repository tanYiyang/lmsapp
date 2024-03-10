from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(Profile, related_name='courses_taught', on_delete=models.CASCADE, null=True, blank=True)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    
    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    student = models.ForeignKey(User, related_name='feedbacks', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='feedbacks', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='teaching_files', blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def submissions(self):
        return Submission.objects.filter(post=self)
    
class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.student.username} for {self.post.title} submitted at {self.submitted_at}"
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('Post', 'Post'),  
        ('Enrollment', 'Enrollment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} created a notification {self.message} of {self.notification_type} type'

    class Meta:
        ordering = ['-created_at']