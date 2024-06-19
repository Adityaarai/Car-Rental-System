from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from .models import CarDetail, CarOrder, User


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

class AboutUsView(View):
  template_name = 'main/about.html'

  def get(self, request):
    return render(request, self.template_name)