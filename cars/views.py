from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from .models import CarDetail, CarOrder, User
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import LoginForm
from users.models import UserProfile


# Create your views here.
class IndexView(View):
  template_name = 'main/index.html'
  form_class = LoginForm

  def get(self, request):
    return render(request, self.template_name)

# ------------------------------------------------------------------------------------------------


class CarsListView(ListView):
  model = CarDetail
  template_name = 'cars/cars_listing.html'

# ------------------------------------------------------------------------------------------------


class CarDetailView(DetailView):
  template_name = 'cars/car_booking.html'
  model = CarDetail
  context_object_name = 'detail'

# ------------------------------------------------------------------------------------------------


# ------------------------create orders------------------------

class OrderCreateView(LoginRequiredMixin, View):
  login_url = 'login'
  template_name = 'cars/car_booking.html'

  def handle_no_permission(self):
    messages.error(self.request, "You need to be logged in to book a car.")
    return redirect(reverse(self.login_url))
  
  def post(self, request, *args, **kwargs):
    current_url = request.get_full_path()

    rentee = UserProfile.objects.get(user__username=request.user.username)
  
    car_id = request.POST.get('car_id')
    booking_start_date = request.POST.get('bookingStartDate')
    booking_end_date = request.POST.get('bookingEndDate')

    try:
      car_detail = CarDetail.objects.get(car_id=car_id)

      if not booking_start_date or not booking_end_date:
        messages.error(request, "Please enter start and end date to proceed with the booking process.")
        return redirect(reverse('orders', kwargs={'pk': car_detail.car_id}))

      start_date = datetime.strptime(booking_start_date, '%Y-%m-%d').date()
      end_date = datetime.strptime(booking_end_date, '%Y-%m-%d').date()

      if start_date < timezone.now().date():
        messages.error(request, "Can not book cars in the past.")
        return redirect(reverse('orders', kwargs={'pk': car_detail.car_id}))

      if end_date < start_date:
        messages.error(request, "Unless you have a time machine, can not book cars in the past.")
        return redirect(reverse('orders', kwargs={'pk': car_detail.car_id})) 


      existing_order = CarOrder.objects.filter(rentee=rentee, status='Pending').first()
      if existing_order:
        messages.error(request, "You have already placed an order!")
        return redirect('booking_complete')

      price = car_detail.price
      duration = (end_date - start_date).days
      total_price = price * duration

      order = CarOrder.objects.create(
        car_detail=car_detail,
        start_date=start_date,
        end_date=end_date,
        rentee=rentee,
        total_price=total_price
      )
      order.save()
      messages.success(request, 'Car booked successfully!')
    except CarDetail.DoesNotExist:
      messages.error(request, "CarDetail matching the provided details does not exist.")

    return redirect('booking_complete')

# ------------------------------------------------------------------------------------------------

class OrderPlacedView(View):
  template_name = 'cars/booking_complete.html'

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)

# ------------------------------------------------------------------------------------------------


class AboutUsView(View):
  template_name = 'main/about.html'

  def get(self, request):
    return render(request, self.template_name)

# ------------------------------------------------------------------------------------------------

class LearnMoreView(View):
  template_name = 'main/learn_more.html'

  def get(self, request):
    return render(request, self.template_name)

# ------------------------------------------------------------------------------------------------

class PaymentView(View):
  template_name = 'users/user/payment.html'

  def get(self, request, pk):
    booking = CarOrder.objects.filter(order_id=pk).first()

    car_detail = booking.car_detail
    car_name = f"{car_detail.car_type} {car_detail.car_model}"
    car_image = car_detail.image.url
    context = {
      'car_name': car_name,
      'price': booking.total_price,
      'pickup_date': booking.start_date,
      'dropoff_date': booking.end_date,
      'image': car_image
    }

    return render(request, self.template_name, context)

class AddCarView(View):
  template_name = 'cars/car_add_form.html'

  def get(self, request):
    return render(request, self.template_name)