from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .forms import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseEnrollAPIView(LoginRequiredMixin, generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def post(self, request, course_id):
        course = get_object_or_404(self.queryset, pk=course_id)
    
        if course.students.filter(pk=request.user.pk).exists():
            return Response({'message': 'You are already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)
        course.students.add(request.user)

        teacher = course.teacher.user
        message = f'{request.user.username} has enrolled in {course.title}.'
        Notification.objects.create(
            user=teacher,
            notification_type='Enrollment',
            message=message
        )
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",  
            {
                "type": "send_notification",
                "message": message
            },
        )
        return Response({'message': f'You have been enrolled in {course.title}.'}, status=status.HTTP_200_OK)

class FeedbackSubmissionAPIView(LoginRequiredMixin, generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class CourseFeedbackAPIView(generics.ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Feedback.objects.filter(course_id=course_id)

class SubmissionSubmitAPIView(LoginRequiredMixin, generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(post_id=post_id, student=self.request.user)

class DeadlineListAPIView(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = DeadlineSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)

        if user.enrolled_courses.exists():
            queryset = Post.objects.filter(course__in=user.enrolled_courses.all(), deadline__isnull=False)

            #boolean flag to check if user has submitted
            for post in queryset:
                post.has_submission = Submission.objects.filter(post=post, student=user).exists()

            return queryset
        else:
            #returns empty queryset else it will display the last retrieved queryset for some reason
            return Post.objects.none()

class RemoveStudentAPIView(LoginRequiredMixin, generics.DestroyAPIView):
    serializer_class = CourseSerializer

    def delete(self, request, *args, **kwargs):
        try:
            course_id = kwargs.get('course_id')
            student_id = kwargs.get('student_id')
            course = Course.objects.get(id=course_id)
            student = course.students.get(id=student_id)
            course.students.remove(student)
            return Response({'message': 'Student removed from course successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
         
def course_list(request):
    return render(request, 'course_list.html')

@login_required
def create_course(request):
    if not request.user.profile.is_teacher:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            user_profile = request.user.profile
            course = form.save(commit=False)
            course.teacher = user_profile
            course.save()
            return redirect('course_list')  
    else:
        form = CourseCreateForm()
    return render(request, 'create_course.html', {'form': form})


def course_detail(request, course_id):
    return render(request, 'course_detail.html', {'course_id': course_id})

@login_required
def course_home(request, course_id):
    course = Course.objects.get(id=course_id)
    posts = Post.objects.filter(course_id=course_id)

    for post in posts:
        post.has_submission = Submission.objects.filter(post=post, student=request.user).exists()

    return render(request, 'course_home.html', {'course': course, 'posts': posts})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.profile.is_teacher:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = CourseEditForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = CourseEditForm(instance=course)
    data = {
        'form': form,
        'course_id': course_id,
    }
    return render(request, 'edit_course.html', data)

@login_required
def add_post(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user == course.teacher.user:
        if request.method == 'POST':
            form = CoursePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.course = course
                post.save()

                for student in course.students.all():
                    message = f'A new post "{post.title}" has been added to the course "{course.title}".'
                    notification = Notification.objects.create(
                        user=student,
                        notification_type='Post',
                        message=message
                    )
                    notification.save()

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "notifications",  
                        {
                            "type": "send_notification",
                            "message": message
                        },
                    )

                return redirect('user_profile', username=request.user.username)
        else:
            form = CoursePostForm()
        data = {
            'form': form,
            'course_id': course_id,
        }
        return render(request, 'add_post.html', data)

@login_required 
def students_records(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.profile.is_teacher:
        return render(request, '403.html', status=403)
    enrolled_students = course.students.all()

    return render(request, 'students_records.html', {'course': course, 'enrolled_students': enrolled_students})

