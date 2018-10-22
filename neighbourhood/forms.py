from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Business


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Name', 'dp', 'bio', 'neighbourhood')


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields =('Name','owner','describe','neighbourhood')