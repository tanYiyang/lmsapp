from rest_framework import serializers
from .models import *
from accounts.serializers import ProfileSerializer 

class CourseSerializer(serializers.ModelSerializer):
    teacher = ProfileSerializer()
    class Meta:
        model = Course
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class DeadlineSerializer(serializers.ModelSerializer):
    course_title = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    has_submission = serializers.BooleanField()

    class Meta:
        model = Post
        fields = ['title', 'deadline', 'course_title', 'has_submission']

    def get_course_title(self, obj):
        return obj.course.title

    def get_deadline(self, obj):
        if obj.deadline:
            return obj.deadline.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return None