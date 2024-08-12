from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from cars.models import CarDetail, CarOrder

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
    'placeholder': 'First Name',
    'value': '{{ user_detail.first_name}}'
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
    
class UserProfileCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    address = forms.CharField(max_length=100, required=False)
    contact = forms.CharField(max_length=100, required=False)

    def save(self, commit=True):
      user = super(UserProfileCreateForm, self).save(commit=False)
      user.set_password('Vroom@123')
      if commit:
        user.save()
        profile = UserProfile.objects.get(user=user)
        profile.contact = self.cleaned_data['contact']
        profile.address = self.cleaned_data['address']
        profile.save()
      return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'license_photo', 'contact']

class CarDetailForm(forms.ModelForm):
    class Meta:
        model = CarDetail
        fields = ['car_type', 'car_model', 'image', 'blue_book', 'price']

class DistributorRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=255, required=True)
    license_photo = forms.ImageField(required=False)
    contact = forms.CharField(max_length=15, required=True)

    car_type = forms.CharField(max_length=50, required=True)
    car_model = forms.CharField(max_length=50, required=True)
    car_image = forms.ImageField(required=True)
    bluebook_image = forms.ImageField(required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = CarDetail
        fields = ['car_type', 'car_model', 'car_image', 'bluebook_image', 'price']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(user__username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(user__email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        return contact

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price