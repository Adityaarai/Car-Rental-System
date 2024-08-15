from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.views import View
from .forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import UserProfileForm, UserProfileCreateForm, DistributorRegistrationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from cars.models import CarDetail, CarOrder
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseRedirect
from .models import DistributorRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
class LoginView(View):
    form_class = LoginForm  
    initial = {}
    template_name = 'users/signin.html'  

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username_or_email, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                if user.is_staff and user.is_superuser:
                  return redirect('admin_dashboard')
                elif user.is_staff and not user.is_superuser:
                  if 'distributor-login' in request.POST:
                    return redirect('distributor_dashboard')
                  elif 'user-login' in request.POST:
                    return redirect('index')
                else:
                  return redirect('index')  
            else:
                messages.error(request, 'Unable to login. Please check your credentials.')
        return render(request, self.template_name, {'form': form})

# ------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------

class SignupView(View):
  form_class = SignupForm
  initial = {}
  template_name = 'users/signup.html'

  def get(self, request):
    form = self.form_class(initial=self.initial)
    return render(request, self.template_name, {'form': form})

  def post(self, request):
    form = self.form_class(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      password = form.cleaned_data['password']
      confirm_password = form.cleaned_data['confirm_pass']

      if password == confirm_password:
        user = User.objects.create_user(username=username, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()
        messages.success(request, 'You have successfully signed up!')
        return redirect('login')
      else:
        messages.error(request, 'Passwords do not match!')
    return render(request, self.template_name, {'form': form})

# ------------------------------------------------------------------------------------------------

class LogoutView(View):
  def get(self, request):
    logout(request)
    return redirect('index')

# ------------------------------------------------------------------------------------------------

class UserProfileView(View):
    template_name = 'users/user/user_profile.html'

    def get(self, request):
      user = request.user
      user_profile = UserProfile.objects.get(user=user)

      user_cars = CarDetail.objects.filter(renter=user_profile)
      pending_bookings = CarOrder.objects.filter(rentee=user_profile, status='Pending')
      approved_bookings = CarOrder.objects.filter(rentee=user_profile, status='Approved')
      paid_bookings = CarOrder.objects.filter(rentee=user_profile, status='Paid')
      completed_bookings = CarOrder.objects.filter(rentee=user_profile, status='Completed')

      context = {
        'user_profile': user_profile,
        'user_cars': user_cars,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'paid_bookings': paid_bookings,
        'completed_bookings': completed_bookings
      }

      return render(request, self.template_name, context)

    def post(self, request):
      user = request.user

      if 'updateProfile' in request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        license_photo = request.FILES.get('license_photo')
        contact = request.POST.get('contact')

        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()

        user_profile.address = address
        if license_photo:
          user_profile.license_photo = license_photo
        user_profile.contact = contact

        user_profile.save()
        messages.success(request, "Profile updated successfully")

        return redirect('user_profile')
      elif 'changePassword' in request.POST:
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
          form.save()
          update_session_auth_hash(request, form.user)
          messages.success(request, "Password updated successfully.")
          return redirect('user_profile')  # Redirect to the same page to ensure data is refreshed
        else:
          for field, errors in form.errors.items():
              for error in errors:
                  messages.error(request, f"{field}: {error}")
                  return redirect('user_profile')
      messages.error(request, "Invalid request.")
      return redirect('user_profile')

# ------------------------------------------------------------------------------------------------

class DistributorRegisterView(View):
  template_name = 'users/user/distributor_registration_form.html'

  def get(self, request):
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist.")
            return redirect('user_profile')

        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'address': user_profile.address,
            'contact': user_profile.contact,
        }

        form = DistributorRegistrationForm(initial=initial_data)
        context = {
            'user_profile': user_profile,
            'form': form,
        }
        return render(request, self.template_name, context)

  def post(self, request):
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist.")
            return redirect('user_profile')

        form = DistributorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Update user profile
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.save()

            user_profile.address = form.cleaned_data.get('address')
            user_profile.contact = form.cleaned_data.get('contact')
            if form.cleaned_data.get('license_photo'):
                user_profile.license_photo = form.cleaned_data.get('license_photo')
            user_profile.save()

            # Save car details
            car_detail = form.save(commit=False)
            car_detail.renter = user_profile
            if form.cleaned_data.get('car_image'):
                car_detail.image = form.cleaned_data.get('car_image')
            if form.cleaned_data.get('bluebook_image'):
                car_detail.blue_book = form.cleaned_data.get('bluebook_image')
            car_detail.save()


            # Create distributor request
            DistributorRequest.objects.create(
                requester=user_profile,
                car_detail=car_detail
            )

            messages.success(request, "Registration successful.")
            return redirect('user_profile')
        else:
            # If the form is not valid, render the form with errors
            context = {
                'user_profile': user_profile,
                'form': form,
            }
            return render(request, self.template_name, context)

