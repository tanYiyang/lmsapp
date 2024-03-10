from django.db import models
from django.contrib.auth.models import User
from PIL import Image
#default.jpg from https://www.vecteezy.com/vector-art/20765399-default-profile-account-unknown-icon-black-silhouette

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pic') #saves to media folder as defined in settings.py
    profile_url = models.CharField(max_length=250, blank=True, null=True)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=255, blank=True, null=True) 
    
    def __str__(self):
        return self.user.username + ' Profile'
    
    def save(self, *args, **kwargs):
        if not self.profile_url:  #checks if profile_url is not set
            self.profile_url = f'/profiles/{self.user.username}/'
        super().save(*args, **kwargs)


    def get_profile_url(self): #method to return profile_url
        return f'/profiles/{self.user.username}/'


class Teacher_request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Teacher request for {self.user.username}"
    


