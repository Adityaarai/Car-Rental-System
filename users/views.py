from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.views import View
from .forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import UserProfileForm

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
                if user.is_staff and not user.is_superuser:
                  return redirect('distributor_dashboard')
                return redirect('index')  
            else:
                messages.error(request, 'Unable to login. Please check your credentials.')
        return render(request, self.template_name, {'form': form})

# ------------------------------------------------------------------------------------------------

class AdminDashboardView(View):
    template_name = 'users/admin_dashboard.html'

    def get(self, request):
        total_distributor_count = UserProfile.objects.filter(user__is_staff=True, user__is_superuser=False).count()
        total_user_count = UserProfile.objects.filter(user__is_staff=False).count()
        recent_users = UserProfile.objects.filter(user__is_staff=False).order_by('-user__date_joined')[:5]
        user_details = UserProfile.objects.all()

        context = {
            'total_distributor_count': total_distributor_count,
            'total_user_count': total_user_count,
            'recent_users': recent_users,
            'user_details': user_details,
        }
        return render(request, self.template_name, context)

# ------------------------------------------------------------------------------------------------

class UserDeleteView(DeleteView):
  template_name = 'users/admin_dashboard.html'
  model = User
  success_url = reverse_lazy('admin_dashboard')

# ------------------------------------------------------------------------------------------------

class UserUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['user_detail'] = self.object
        return context

# ------------------------------------------------------------------------------------------------

class UserCreateView(CreateView):
  template_name = 'users/admin_dashboard.html'
  query_set = User.objects.all()

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
    messages.success(request, 'You have successfully logged out!!')
    return redirect('index')

# ------------------------------------------------------------------------------------------------
