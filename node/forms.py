from django import forms
from django.contrib.auth.models import User
from .models import FromMicroController, ProjectModel
from django.contrib.auth.forms import UserCreationForm

# class ToMcForm(forms.ModelForm):
#     class Meta:
#         model = ToMicroController
#         fields = ['speed']

class FromMcForm(forms.ModelForm):
    class Meta:
        model = FromMicroController
        fields = ['data']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60,
                                 widget=forms.TextInput(attrs={'class':'validate'}))
    username = forms.EmailField(max_length=60,
                                widget=forms.TextInput(attrs={'class':'validate'}))
    password1 = forms.CharField(max_length=60,
                                widget=forms.PasswordInput(attrs={'class':'validate'}))
    password2 = forms.CharField(max_length=60,
                                widget=forms.PasswordInput(attrs={'class':'validate'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']

    
class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['name','description','write_api','email','field']