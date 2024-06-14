from django import forms

class LoginForm(forms.Form):
  email = forms.EmailField(max_length=100, label="Email", required=True,
  widget=forms.TextInput(attrs={
    'type': 'email',
    'class': 'form-control',
    'placeholder': 'Enter your email...'
  }))
  password = forms.CharField(max_length=100, label="Password", required=True,
  widget=forms.TextInput(attrs={
    'type': 'password',
    'class': 'form-control',
    'placeholder': 'Enter your password...'
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

