""" from django.shortcuts import render
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
    
def home(request):

    return render(request, 'accounts/index.html') """

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from courses.models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response

class ProfileSearchAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            results = Profile.objects.filter(
                models.Q(first_name__icontains=query) | models.Q(last_name__icontains=query)
            )
            return results
        return Profile.objects.none()  
    
class ProfileStatusAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        # Retrieve and return the user's profile
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        # Retrieve the user's profile
        profile = self.get_object()

        # Update the status if present in the request data
        if 'user_status' in request.data:
            profile.status = request.data['user_status']
            profile.save()
            return Response({'status': profile.status}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Status field not found in request data'}, status=status.HTTP_400_BAD_REQUEST)
        
def social(request):
    if request.user.profile.is_teacher:
        profiles = Profile.objects.filter(is_teacher=True)
    else:
        profiles = Profile.objects.filter(is_teacher=False)

    return render(request, 'social.html', {'profiles': profiles})

def user_list(request):
    query = request.GET.get('q', '')
    users = User.objects.all()

    if query:
        users = users.filter(username__icontains=query)

    context = {'users': users}
    return render(request, 'user_list.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # create user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            
            # create profile
            profile = Profile(user=user)
            profile.save()
            
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')

            return redirect(reverse('user_profile', args=[username]))  
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  


def user_profile(request, username):
    
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if profile.is_teacher:
        courses_taught = Course.objects.filter(teacher=profile)
        data = {
            'profile': profile,
            'courses_taught': courses_taught
        }
    else:
        courses_enrolled = user.enrolled_courses.all()
        data = {
            'profile': profile,
            'courses_enrolled': courses_enrolled
        }
   

    return render(request, 'profile.html', data)

@login_required
def request_teacher_role(request):
    if request.method == 'POST':
        if not Teacher_request.objects.filter(user=request.user).exists():
            Teacher_request.objects.create(user=request.user)

    return redirect('user_profile', username=request.user.username)

@login_required
def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    user_teacher_request = Teacher_request.objects.filter(user=user).exists() #checks if teacher request has been sent
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email'] #saves the email directly into the User model
            user.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile', username=request.user.username)  
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    
    return render(request, 'update_profile.html', {'form': form,'user_teacher_request': user_teacher_request})

