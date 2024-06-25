from django.urls import path
from .views import *

urlpatterns = [
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('signup/', SignupView.as_view(), name='signup'),
  path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]