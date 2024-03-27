from django.contrib.auth.models import User
from . models import Profile
from django import forms
from django.forms.widgets import FileInput

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields  = ['first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields ='__all__'
        exclude=['user']
        widgets = {
            'profile_image':FileInput(),
        }
