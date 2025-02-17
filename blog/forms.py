from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Post

class SignUpForm(UserCreationForm):
    password1= forms.CharField(label='Password', 
                               widget=forms.PasswordInput(attrs={'class':'form-control custom-width'}))
    
    password2= forms.CharField(label='Confirm Password', widget=forms.PasswordInput
                               (attrs={'class':'form-control custom-width'}))
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email']
        labels= {'first_name' : 'First Name', 'last_name' : 'Last Name', 'email' : 'Email'}

        widgets = {
                    'username' : forms.TextInput(attrs={'class':'form-control custom-width'}),
                    'first_name' : forms.TextInput(attrs={'class':'form-control custom-width'}),
                    'last_name' : forms.TextInput(attrs={'class':'form-control custom-width'}),
                    'email' : forms.EmailInput(attrs={'class':'form-control custom-width'})}
        

class LoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs=
                            {'autofocus': True, 'class' : 'form-control custom-width'}))
    
    password = forms.CharField(label=('Password'), strip=False, 
                               widget=forms.PasswordInput(attrs={'autocomplete': 
                               'current-password', 'class' : 'form-control custom-width'}))

    
class PostForm(forms.ModelForm):
    class  Meta:
        model = Post
        fields = ['title', 'description']
        labels = {'title' : 'Title', 'description' : 'Description'}

        widgets = {
                    'title':forms.TextInput(attrs={'class':'form-control'}),
                    'description' : forms.Textarea(attrs={'class':'form-control'}),
                    }
      
    
