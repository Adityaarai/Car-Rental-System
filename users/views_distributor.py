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

class DistributorDashboardView(View):
    template_name = 'users/distributor/distributor_dashboard.html'

    def get(self, request):
        user = request.user

        user_profile = UserProfile.objects.get(user=user)
        total_car_count = CarDetail.objects.filter(renter=user_profile).count()
        available_car_count = CarDetail.objects.filter(availability='Available', renter=user_profile).count()
        booked_car_count = CarDetail.objects.filter(availability='Booked', renter=user_profile).count()
        unlisted_car_count = CarDetail.objects.filter(availability='Unlisted', renter=user_profile).count()
        total_bookings_count = CarOrder.objects.filter(car_detail__renter=user_profile).count()
        approved_bookings_count = CarOrder.objects.filter(status='Approved', car_detail__renter=user_profile).count()
        pending_bookings_count = CarOrder.objects.filter(status='Pending', car_detail__renter=user_profile).count()
        paid_bookings_count = CarOrder.objects.filter(status='Paid', car_detail__renter=user_profile).count()
        completed_bookings_count = CarOrder.objects.filter(status='Completed', car_detail__renter=user_profile).count()
        rejected_bookings_count = CarOrder.objects.filter(status='Rejected', car_detail__renter=user_profile).count()
        recent_orders = CarOrder.objects.filter(car_detail__renter=user_profile)[:5]
        car_details = CarDetail.objects.filter(renter=user_profile)
        car_orders = CarOrder.objects.filter(car_detail__renter=user_profile)

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
            'rejected_bookings_count': rejected_bookings_count,
            'recent_orders' : recent_orders,
            'car_details': car_details,
            'car_orders': car_orders,
        }
        return render(request, self.template_name, context)

# ------------------------------------------------------------------------------------------------

class ApproveBookingsView(View):
  template_name = 'users/distributor/distributor_dashboard.html'
  success_url = reverse_lazy('distributor_dashboard')

  def post(self, request, pk):
    car_order = get_object_or_404(CarOrder, order_id=pk)

    if car_order:
      car_order.status = 'Approved'
      car_order.save()

      subject = "Car Booking Approved Successfully!!"
      message = f"""Hello {car_order.rentee.user.username}:,

We are excited to inform you that your order for {car_order.car_detail.car_model} has been successfully approved!
Please proceed with the payment to fully complete this booking request. After payment the car will be delivered according to your needs.

Thank you for choosing VROOM-Car-Rental-Service. We are delighted to have you as a valued customer and look forward to providing you with an exceptional car rental experience.

If you have any questions or need further assistance, please don't hesitate to reach out to our support team.

Best regards,
The VROOM-Car-Rental-Service Team
"""

      from_email = settings.EMAIL_HOST_USER
      to_list = [car_order.rentee.user.email]
      try:
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        messages.success(request, "Order approved and email sent successfully!")
      except Exception as e:
        messages.error(request, f"Order approved, but failed to send email. Error: {str(e)}")

      return redirect(self.success_url)
    else:
      messages.error(request, "Car order not found!")
      return redirect(self.success_url)

# ------------------------------------------------------------------------------------------------

class RejectBookingsView(View):
  template_name = 'users/distributor/distributor_dashboard.html'
  success_url = reverse_lazy('distributor_dashboard')

  def post(self, request, pk):
    car_order = get_object_or_404(CarOrder, order_id=pk)

    if car_order:
      car_order.status = 'Rejected'
      car_order.save()

      subject = "Car Booking Rejected Unfortunately!!"
      message = f"""Hello {car_order.rentee.user.username}:,

We regret to inform you that your order for {car_order.car_detail.car_model} has been rejected. Please check your license and contact details before trying again.
We apologize for any inconvenience this may cause.

Thank you for choosing VROOM-Car-Rental-Service. We value your patronage and look forward to serving you in the future.

If you have any questions or need further assistance, please don't hesitate to reach out to our support team.

Best regards,
The VROOM-Car-Rental-Service Team
"""

      from_email = settings.EMAIL_HOST_USER
      to_list = [car_order.rentee.user.email]
      try:
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        messages.success(request, "Order rejected and email sent successfully!")
      except Exception as e:
        messages.error(request, f"Order rejected, but failed to send email. Error: {str(e)}")

      return redirect(self.success_url)
    else:
      messages.error(request, "Car order not found!")
      return redirect(self.success_url)

# ------------------------------------------------------------------------------------------------

class UpdateCarDetailsView(DeleteView):
  template_name = 'users/distributor/distributor_dashboard.html'
  success_url = reverse_lazy('distributor_dashboard')

  def post(self, request, pk):
    car_detail = get_object_or_404(CarDetail, car_id=pk)

    if 'deleteCarDetails' in request.POST:
      car_detail.delete()
      messages.success(request, "Car detail deleted successfully!")
    elif 'changeUnlisted' in request.POST:
      car_detail.availability = 'Unlisted'
      car_detail.save()
      messages.success(request, 'Changed availability of car to Unlisted!')
    elif 'changeAvailable' in request.POST:
      car_detail.availability = 'Available'
      car_detail.save()
      messages.success(request, 'Changed availability of car to Available!')
    else:
      messages.error(request, "Unexpected error occured!")

    return redirect(self.success_url)


