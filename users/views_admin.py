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

# ------------------------------------------------------------------------------------------------

class AdminDashboardView(View):
    template_name = 'users/admin/admin_dashboard.html'

    def get(self, request):
        user = request.user

        if not user.is_superuser:
          return redirect('index')

        total_distributor_count = UserProfile.objects.filter(user__is_staff=True, user__is_superuser=False).count()
        total_user_count = UserProfile.objects.filter(user__is_staff=False).count()
        recent_users = UserProfile.objects.filter(user__is_staff=False).order_by('-user__date_joined')[:5]
        user_details = UserProfile.objects.all()
        distributor_requests = DistributorRequest.objects.all()

        context = {
            'total_distributor_count': total_distributor_count,
            'total_user_count': total_user_count,
            'recent_users': recent_users,
            'user_details': user_details,
            'distributor_requests': distributor_requests,
        }
        return render(request, self.template_name, context)

# ------------------------------------------------------------------------------------------------

class UserDeleteView(DeleteView):
  template_name = 'users/admin/admin_dashboard.html'
  model = User
  success_url = reverse_lazy('admin_dashboard')

# ------------------------------------------------------------------------------------------------

class UserUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/admin/update_user.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['user_detail'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['user_detail'] = self.object
        return kwargs
    
    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER')

        if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={self.request.get_host()}):
          return referer
        return super(UserUpdateView, self).get_success_url()

# ------------------------------------------------------------------------------------------------

class UserCreateView(CreateView):
    model = User
    form_class = UserProfileCreateForm
    template_name = 'users/admin/add_user.html'
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        user = form.save()
        user.save()
        messages.success(self.request, "User added successfully!!")
        return super().form_valid(form)

# ------------------------------------------------------------------------------------------------

class DistributorCreateView(CreateView):
    model = User
    form_class = UserProfileCreateForm
    template_name = 'users/admin/add_distributor.html'
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        user = form.save()

        user_email = form.cleaned_data['email']
        user.is_staff = True  
        
        car_detail_content_type = ContentType.objects.get_for_model(CarDetail)
        car_detail_permissions = Permission.objects.filter(content_type=car_detail_content_type)

        car_order_content_type = ContentType.objects.get_for_model(CarOrder)
        car_order_permissions = Permission.objects.filter(content_type=car_order_content_type)

        all_permissions = car_detail_permissions | car_order_permissions
        user.user_permissions.add(*all_permissions)

        user.save()

        messages.success(self.request, "Distributor added successfully!!")
        return super().form_valid(form)

# ------------------------------------------------------------------------------------------------

class RejectRequestsView(View):
    template_name = 'users/admin/admin_dashboard.html'
    success_url = reverse_lazy('admin_dashboard')

    def post(self, request, pk):
        request_detail = get_object_or_404(DistributorRequest, pk=pk)

        if request_detail:

            subject = "Distributor Request Rejected Unfortunately!!"
            message = f"""Hello {request_detail.requester.user.username},

We regret to inform you that your request to apply as a distributor has been rejected. Please check your license and contact details before trying again.
We apologize for any inconvenience this may cause. Please check your documents and try again.

Thank you for choosing VROOM-Car-Rental-Service. We value your patronage and look forward to serving you in the future.

If you have any questions or need further assistance, please don't hesitate to reach out to our support team.

Best regards,
The VROOM-Car-Rental-Service Team
"""

            from_email = settings.EMAIL_HOST_USER
            to_list = [request_detail.requester.user.email]
            try:
                send_mail(subject, message, from_email, to_list, fail_silently=False)
                messages.success(request, "Request rejected and email sent successfully!")
            except Exception as e:
                messages.error(request, f"Request rejected, but failed to send email. Error: {str(e)}")

            car_detail = CarDetail.objects.get(car_id=request_detail.car_detail.car_id)
            car_detail.delete()
            request_detail.delete()
            return redirect(self.success_url)
        else:
            messages.error(request, "Distributor request not found!")
            return redirect(self.success_url)

# ------------------------------------------------------------------------------------------------

class ApproveRequestsView(View):
    template_name = 'users/admin/admin_dashboard.html'
    success_url = reverse_lazy('admin_dashboard')

    def post(self, request, pk):
        request_detail = get_object_or_404(DistributorRequest, pk=pk)

        if request_detail:
            user = request_detail.requester.user
              
            user.is_staff = True

            # Get permissions for CarDetail and CarOrder models
            car_detail_content_type = ContentType.objects.get_for_model(CarDetail)
            car_detail_permissions = Permission.objects.filter(content_type=car_detail_content_type)

            car_order_content_type = ContentType.objects.get_for_model(CarOrder)
            car_order_permissions = Permission.objects.filter(content_type=car_order_content_type)

            # Add permissions to the user
            all_permissions = car_detail_permissions | car_order_permissions
            user.user_permissions.add(*all_permissions)

            user.save()

            subject = "Distributor Request Approved!"
            message = f"""Hello {request_detail.requester.user.username},

We are pleased to inform you that your request to become a distributor has been approved! Welcome to the VROOM-Car-Rental-Service team.

You can now start adding your cars to our platform and begin renting them out.

Thank you for choosing VROOM-Car-Rental-Service. We value your partnership and look forward to a successful collaboration.

If you have any questions or need further assistance, please don't hesitate to reach out to our support team.

Best regards,
The VROOM-Car-Rental-Service Team
"""

            from_email = settings.EMAIL_HOST_USER
            to_list = [request_detail.requester.user.email]
            try:
                send_mail(subject, message, from_email, to_list, fail_silently=False)
                messages.success(request, "Request approved and email sent successfully!")
            except Exception as e:
                messages.error(request, f"Request approved, but failed to send email. Error: {str(e)}")

            request_detail.distributor_status = True
            request_detail.save()
            return redirect(self.success_url)
        else:
            messages.error(request, "Distributor request not found!")
            return redirect(self.success_url)

