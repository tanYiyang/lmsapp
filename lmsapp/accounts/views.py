from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'register.html',
                  {'user_form': user_form,
                    'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../register')
            else:
                return HttpResponse("Account disabled")
        else:
            return HttpResponse('Invalid login')
    else:
        return render(request, 'login.html')
