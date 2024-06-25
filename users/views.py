from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.views import View
from .forms import LoginForm, SignupForm
from django.contrib.auth.models import User

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
                messages.success(request, 'You have logged in successfully!')
                if user.is_staff and user.is_superuser:
                  return redirect('admin_dashboard')
                if user.is_staff and not user.is_superuser:
                  return redirect('distributor_dashboard')
                return redirect('index')  
            else:
                messages.error(request, 'Unable to login. Please check your credentials.')
        return render(request, self.template_name, {'form': form})


class AdminDashboardView(View):
  template_name = 'users/admin_dashboard.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['total_distributor_count'] = User.objects.filter(is_staff=True, is_superuser=False).count()
    context['total_user_count'] = User.objects.filter(is_staff=False).count()
    context['recent_users'] = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    context['user_details'] = User.objects.all()
    return context

  def get(self, request):
    return render(request, self.template_name)
    



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

class LogoutView(View):
  def get(self, request):
    logout(request)
    messages.success(request, 'You have successfully logged out!!')
    return redirect('index')