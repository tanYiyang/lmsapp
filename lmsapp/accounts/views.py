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

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import ProfileSerializer, UserLoginSerializer
from .forms import SignupForm
from django.shortcuts import render, redirect
from .models import *
def signup_form(request):
    return render(request, 'signup.html')

def login_form(request):
    return render(request, 'login.html')

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user)
            return render(request, 'login.html') 
        else:
            return render(request, 'signup.html', {'form': form})

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                profile = Profile.objects.get(user=user)
                profile_url = profile.get_profile_url()
                response_data = {
                    'token': token.key,
                    'profile_url': profile_url,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return render(request, 'profile.html', {'username':username})
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")
