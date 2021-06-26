from django.contrib.auth.models import User
from  django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm


#===== crop
class signUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    class Meta:
        model =User
        fields = ('first_name','last_name','username','password1','password2')

class UserProfileForm(forms.ModelForm):
    class Meta :
        labels = {
        "profile_pic": "รูปโปรไฟล์",
        "profile_bg_pic":"รูปพื้นหลัง"
    }
        
        model = UserProfile
        fields = ('profile_pic','profile_bg_pic')

class setting_pic(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['std','edu','cpenumber','nickname','count','profile_pic','profile_bg_pic']
        
        
        
class setUp(forms.ModelForm):
    class Meta:
        labels = {
        "profile_pic": "รูปโปรไฟล์",
        "profile_bg_pic":"รูปพื้นหลัง"
    }
        model = UserProfile
        fields = ['profile_pic','profile_bg_pic']
        
