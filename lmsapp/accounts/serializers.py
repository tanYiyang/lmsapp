from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    profile_url = serializers.CharField(source='get_profile_url', read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'desc', 'profile_pic', 'is_teacher', 'profile_url']
        read_only_fields = ['id', 'user', 'profile_url']

class TeacherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher_request
        fields = ['id', 'teacher_profile', 'teacher_email']
        read_only_fields = ['id', 'teacher_profile']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # variable to control the UI
    is_authenticated = serializers.BooleanField(default=False)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'