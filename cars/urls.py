from django.urls import path
from .views import *


urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('cars/', CarsListView.as_view(), name='carlisting'),
  path('about/', AboutUsView.as_view(), name='aboutus'),
  path('orders/<int:pk>', CarDetailView.as_view(), name='orders'),
  path('orders/create', OrderCreateView.as_view(), name='order_create'),
  path('orders/complete', OrderPlacedView.as_view(), name='booking_complete'),
  path('about/learnmore', LearnMoreView.as_view(), name='learnmore'),
]