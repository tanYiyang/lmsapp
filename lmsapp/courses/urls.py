from django.urls import path
from .views import *

urlpatterns = [
    path('courses/', course_list, name='course_list'),
    path('api/courses/', CourseListAPIView.as_view(), name='api_course_list'),
    path('create_course/', create_course, name='create_course'),
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('course_home/<int:course_id>/', course_home, name='course_home'),
    path('api/courses/<int:pk>/', CourseRetrieveAPIView.as_view(), name='api_course_retrieve'),
    path('api/enroll/<int:course_id>/', CourseEnrollAPIView.as_view(), name='course_enroll'),
    path('courses/edit/<int:course_id>/', edit_course, name='edit_course'),
    path('courses/add_post/<int:course_id>', add_post, name='add_post'),
    path('api/feedback/submit/', FeedbackSubmissionAPIView.as_view(), name='feedback_submit'),
    path('api/feedback/<int:course_id>/', CourseFeedbackAPIView.as_view(), name='course_feedback_api'),
    path('api/submit_assignment/<int:post_id>/', SubmissionSubmitAPIView.as_view(), name='submit_assignment_api'),
    path('api/deadlines/<str:username>/', DeadlineListAPIView.as_view(), name='deadline_list_api'),
    path('students_records/<int:course_id>/', students_records, name='students_records'),
    path('api/remove_student/<int:course_id>/<int:student_id>/', RemoveStudentAPIView.as_view(), name='remove_student'),
]