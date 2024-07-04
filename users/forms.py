from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
  username_or_email = forms.CharField(max_length=100, label="Username", required=True,
  widget=forms.TextInput(attrs={
    'type': 'text',
    'class': 'form-control',
    'placeholder': 'Enter your username...',
    'id': 'username_or_email',
  }))
  password = forms.CharField(max_length=100, label="Password", required=True,
  widget=forms.TextInput(attrs={
    'type': 'password',
    'class': 'form-control',
    'placeholder': 'Enter your password...',
    'id' : 'password',
  }))

class SignupForm(forms.Form):
  first_name = forms.CharField(max_length=50, label="First Name", required=True,
  widget=forms.TextInput(attrs={
    'type': 'text',
    'class': 'form-control',
    'placeholder': 'First Name'
  }))
  last_name = forms.CharField(max_length=50, label="Last Name", required=True,
  widget=forms.TextInput(attrs={
    'type': 'text',
    'class': 'form-control',
    'placeholder': 'Last Name'
  }))
  username = forms.CharField(max_length=50, label="Username", required=True, 
  widget=forms.TextInput(attrs={
    'type': 'text',
    'class': 'form-control',
    'placeholder': 'Username',
  }))
  email = forms.EmailField(max_length=50, label="Email", required=True,
  widget=forms.TextInput(attrs={
    'type': 'email',
    'class': 'form-control',
    'placeholder': 'Email'
  }))
  password = forms.CharField(max_length=50, label="Password", required=True, 
  widget=forms.PasswordInput(attrs={
    'type': 'password',
    'class': 'form-control',
    'placeholder': 'Password'
  }))
  confirm_pass = forms.CharField(max_length=50, label="Confirm Password", required=True, 
  widget=forms.PasswordInput(attrs={
    'type': 'password',
    'class': 'form-control',
    'placeholder': 'Confirm your password'
  }))


class AddUserForm(forms.ModelForm):
  first_name = forms.CharField(max_length=50, label="First Name", required=True,
  widget=forms.TextInput(attrs={
    'type': 'text',
    'class': 'form-control',
    'placeholder': 'First Name'
  }))
  last_name = forms.CharField(max_length=50, label="Last Name", required=True,
  widget=forms.TextInput(attrs={
    'type': 'text',
    'class': 'form-control',
    'placeholder': 'Last Name'
  }))
  username = forms.CharField(max_length=50, label="Username", required=True, 
  widget=forms.TextInput(attrs={
    'type': 'text',
    'class': 'form-control',
    'placeholder': 'Username',
  }))
  email = forms.EmailField(max_length=50, label="Email", required=True,
  widget=forms.TextInput(attrs={
    'type': 'email',
    'class': 'form-control',
    'placeholder': 'Email'
  }))


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150,  initial='lobalcgi')
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'address' , 'contact'
        ]
        widget = forms.TextInput(attrs={
          'class': 'form-control',
        })

    def __init__(self, *args, **kwargs):
      super(UserProfileForm, self).__init__(*args, **kwargs)
      if self.instance and self.instance.pk:
          self.fields['username'].initial = self.instance.user.username
          self.fields['email'].initial = self.instance.user.email
          self.fields['first_name'].initial = self.instance.user.first_name
          self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
      user_profile = super(UserProfileForm, self).save(commit=False)
      user = user_profile.user
      user.username = self.cleaned_data['username']
      user.email = self.cleaned_data['email']
      user.first_name = self.cleaned_data['first_name']
      user.last_name = self.cleaned_data['last_name']
      if commit:
        user.save()
        user_profile.save()
      return user_profile
