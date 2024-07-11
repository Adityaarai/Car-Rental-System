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
  template_name = 'cars/car_details.html'
  model = CarDetail
  context_object_name = 'detail'

# ------------------------------------------------------------------------------------------------


# ------------------------create orders------------------------

class OrderCreateView(LoginRequiredMixin, View):
  login_url = 'login'
  template_name = 'cars/car_details.html'

  def handle_no_permission(self):
    messages.error(self.request, "You need to be logged in to book a car.")
    return redirect(reverse(self.login_url))
  
  def post(self, request, *args, **kwargs):
    current_url = request.get_full_path()

    rentee = UserProfile.objects.get(user__username=request.user.username)
  
    renter_contact = request.POST.get('renter_contact')
    car_model = request.POST.get('car_model')
    renter_name = request.POST.get('renter_name')
    booking_start_date = request.POST.get('bookingStartDate')
    booking_end_date = request.POST.get('bookingEndDate')

    try:
      product = CarDetail.objects.get(car_model=car_model, renter_name=renter_name, renter_contact=renter_contact)

      if not booking_start_date or not booking_end_date:
        messages.error(request, "Please enter start and end date to proceed with the booking process.")
        return redirect(reverse('orders', kwargs={'pk': product.car_id}))

      start_date = datetime.strptime(booking_start_date, '%Y-%m-%d').date()
      end_date = datetime.strptime(booking_end_date, '%Y-%m-%d').date()

      if start_date < timezone.now().date():
        messages.error(request, "Can not book cars in the past.")
        return redirect(reverse('orders', kwargs={'pk': product.car_id}))

      if end_date < start_date:
        messages.error(request, "Unless you have a time machine, can not book cars in the past.")
        return redirect(reverse('orders', kwargs={'pk': product.car_id})) 


      existing_order = CarOrder.objects.filter(rentee=rentee, status='Pending').first()
      if existing_order:
        messages.error(request, "You have already placed an order!")
        return redirect('booking_complete')

      price = product.price
      duration = (end_date - start_date).days
      total_price = price * duration

      order = CarOrder.objects.create(
        product=product,
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
