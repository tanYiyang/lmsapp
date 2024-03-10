from django.urls import path
from .views import *

urlpatterns = [
    path('chat/<str:room_name>/', chat, name='chat'),
]