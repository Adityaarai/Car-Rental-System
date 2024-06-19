from django.urls import path
from .views import *


urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('cars/', CarsView.as_view(), name='carlisting'),
  path('about/', AboutUsView.as_view(), name='aboutus'),
  path('orders/<int:pk>', CarDetailView.as_view(), name='orders'),
]