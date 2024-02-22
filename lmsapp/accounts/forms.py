from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        #ensures passwords match
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

class Login(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        #ensures passwords match
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data