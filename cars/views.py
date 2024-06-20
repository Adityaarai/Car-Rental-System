from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from .models import CarDetail, CarOrder, User
from datetime import datetime


# Create your views here.
class IndexView(View):
  template_name = 'main/index.html'

  def get(self, request):
    return render(request, self.template_name)

class CarsView(ListView):
  model = CarDetail
  template_name = 'main/carlisting.html'

class CarDetailView(DetailView):
  template_name = 'main/car_details.html'
  model = CarDetail
  context_object_name = 'detail'

class OrderCreateView(View):
  template_name = 'main/car_details.html'

  def post(self, request, *args, **kwargs):
        rentee = User.objects.get(username=request.user.username) 

        renter_contact = request.POST.get('renter_contact')
        car_model = request.POST.get('car_model')
        renter_name = request.POST.get('renter_name')
        booking_start_date = request.POST.get('bookingStartDate')
        booking_end_date = request.POST.get('bookingEndDate')

        start_date = datetime.strptime(booking_start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(booking_end_date, '%Y-%m-%d').date()

        product = CarDetail.objects.get(car_model=car_model, renter_name=renter_name, renter_contact=renter_contact)

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

class OrderPlacedView(View):
  template_name = 'main/booking_complete.html'

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)

class AboutUsView(View):
  template_name = 'main/about.html'

  def get(self, request):
    return render(request, self.template_name)