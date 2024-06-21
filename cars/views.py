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


# Create your views here.
class IndexView(View):
  template_name = 'main/index.html'

  def get(self, request):
    return render(request, self.template_name)

# ------------------------------------------------------------------------------------------------


class CarsView(ListView):
  model = CarDetail
  template_name = 'main/carlisting.html'

# ------------------------------------------------------------------------------------------------


class CarDetailView(DetailView):
  template_name = 'main/car_details.html'
  model = CarDetail
  context_object_name = 'detail'

# ------------------------------------------------------------------------------------------------


# ------------------------create orders------------------------

class OrderCreateView(LoginRequiredMixin, View):
  login_url = 'login'
  template_name = 'main/car_details.html'
  
  def post(self, request, *args, **kwargs):
    current_url = request.get_full_path()

    rentee = User.objects.get(username=request.user.username)
  
    renter_contact = request.POST.get('renter_contact')
    car_model = request.POST.get('car_model')
    renter_name = request.POST.get('renter_name')
    booking_start_date = request.POST.get('bookingStartDate')
    booking_end_date = request.POST.get('bookingEndDate')

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
    return redirect('booking_complete')

# ------------------------------------------------------------------------------------------------

class OrderPlacedView(View):
  template_name = 'main/booking_complete.html'

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)

# ------------------------------------------------------------------------------------------------


class AboutUsView(View):
  template_name = 'main/about.html'

  def get(self, request):
    return render(request, self.template_name)

# ------------------------------------------------------------------------------------------------

class LearnMoreView(View):
  template_name = 'main/learnmore.html'

  def get(self, request):
    return render(request, self.template_name)
