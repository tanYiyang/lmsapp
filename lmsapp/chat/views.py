from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import *

def chat(request, room_name):
    username = request.user.username
    return render(request, 'chat.html', {
        'room_name': room_name,
        'username': username
    })
