from django.shortcuts import render
from accounts.models import *
from django.contrib.auth.decorators import login_required

@login_required
def chat(request, room_name):
    username = request.user.username
    return render(request, 'chat.html', {
        'room_name': room_name,
        'username': username
    })
