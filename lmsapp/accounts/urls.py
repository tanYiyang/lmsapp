from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profiles/<str:username>/', user_profile, name='user_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('api/request_teacher_role', request_teacher_role, name='request_teacher_role'),
    path('social/', social, name='social'),
    path('api/profile/status/', ProfileStatusAPIView.as_view(), name='profile_status_api'),
]
