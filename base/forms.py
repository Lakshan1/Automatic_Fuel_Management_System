from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username','class':'border-gray-100 border-solid border-4 rounded-md mb-4 pl-2 h-10 mr-2'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'border-gray-100 border-solid border-4 rounded-md mb-4 pl-2 h-10 mr-2'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'border-gray-100 border-solid border-4 rounded-md mb-4 pl-2 h-10 mr-2'}))