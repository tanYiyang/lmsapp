from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_form, name='signup_form'),
    path('api/signup/', views.signup, name='signup'),
    path('login/', views.login_form, name='login_form'),
    path('api/login/', views.login, name='login'),
    path('profiles/<str:username>/', views.user_profile, name='user_profile'),
]
