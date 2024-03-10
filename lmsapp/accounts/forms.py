from django import forms
from .models import *
    
class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(disabled=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'address', 'email', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        user = kwargs['instance'].user
        self.initial['email'] = user.email
        self.fields['email'].widget.attrs['class'] = 'shadow appearence-none border rounded w-full py-2 px-4 focus:shadow-outline mb-4'
        self.fields['first_name'].widget.attrs['class'] = 'shadow appearence-none border rounded w-full py-2 px-4 focus:shadow-outline mb-4'
        self.fields['last_name'].widget.attrs['class'] = 'shadow appearence-none border rounded w-full py-2 px-4 focus:shadow-outline mb-4'
        self.fields['address'].widget.attrs['class'] = 'shadow appearence-none border rounded w-full py-2 px-4 focus:shadow-outline mb-4'