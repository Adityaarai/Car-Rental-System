from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.views import View
from .forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import UserProfileForm, UserProfileCreateForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from cars.models import CarDetail, CarOrder

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

class DistributorDashboardView(View):
    template_name = 'users/distributor_dashboard.html'

    def get(self, request):
        total_car_count = CarDetail.objects.all().count()
        available_car_count = CarDetail.objects.filter(availability='Available').count()
        booked_car_count = CarDetail.objects.filter(availability='Booked').count()
        unlisted_car_count = CarDetail.objects.filter(availability='Unlisted').count()
        total_bookings_count = CarOrder.objects.all().count()
        approved_bookings_count = CarOrder.objects.filter(status='Approved').count()
        pending_bookings_count = CarOrder.objects.filter(status='Pending').count()
        paid_bookings_count = CarOrder.objects.filter(status='Paid').count()
        completed_bookings_count = CarOrder.objects.filter(status='Completed').count()
        recent_orders = CarOrder.objects.all()[:5]
        car_details = CarDetail.objects.all()
        car_orders = CarOrder.objects.all()

        context = {
            'total_car_count': total_car_count,
            'available_car_count': available_car_count,
            'booked_car_count': booked_car_count,
            'unlisted_car_count': unlisted_car_count,
            'total_bookings_count': total_bookings_count,
            'approved_bookings_count': approved_bookings_count,
            'pending_bookings_count': pending_bookings_count,
            'paid_bookings_count': paid_bookings_count,
            'completed_bookings_count': completed_bookings_count,
            'recent_orders' : recent_orders,
            'car_details': car_details,
            'car_orders': car_orders,
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
    model = User
    form_class = UserProfileCreateForm
    template_name = 'users/add_user.html'
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        # Save the user instance from the form
        user = form.save()

        # Example logic to assign permissions if email matches a specific domain
        user_email = form.cleaned_data['email']
        if '.vroom@gmail.com' in user_email:
            user.is_staff = True  # Example: Make user staff
            # Example: Assign permissions for specific models
            car_detail_content_type = ContentType.objects.get_for_model(CarDetail)
            car_detail_permissions = Permission.objects.filter(content_type=car_detail_content_type)

            car_order_content_type = ContentType.objects.get_for_model(CarOrder)
            car_order_permissions = Permission.objects.filter(content_type=car_order_content_type)

            all_permissions = car_detail_permissions | car_order_permissions
            user.user_permissions.add(*all_permissions)

        user.save()

        messages.success(self.request, "User added successfully!!")
        return super().form_valid(form)
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
