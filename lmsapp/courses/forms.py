from django import forms
from .models import *

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CoursePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'file', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

