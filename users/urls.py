from django.urls import path
from .views import *

urlpatterns = [
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('signup/', SignupView.as_view(), name='signup'),
  path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
  path('admin_dashboard/user/add/', UserCreateView.as_view(), name='add_user'),
  path('admin_dashboard/user/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
  path('admin_dashboard/user/update/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
]