from django.urls import path
from .views import *

urlpatterns = [
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('signup/', SignupView.as_view(), name='signup'),
  path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
  path('admin_dashboard/user/add/', UserCreateView.as_view(), name='add_user'),
  path('admin_dashboard/distributor/add/', DistributorCreateView.as_view(), name='add_distributor'),
  path('admin_dashboard/user/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
  path('admin_dashboard/user/update/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
  path('distributor_dashboard/', DistributorDashboardView.as_view(), name='distributor_dashboard'),
  path('distributor_dashboard/order/approve/<int:pk>/', ApproveBookingsView.as_view(), name='approve_bookings'),
  path('distributor_dashboard/order/reject/<int:pk>/', RejectBookingsView.as_view(), name='reject_bookings'),
  path('distributor_dashboard/cars/update/<int:pk>/', UpdateCarDetailsView.as_view(), name='update_cars'),
  path('user_profile/', UserProfileView.as_view(), name='user_profile'),
  path('user_profile/update/', UserUpdateView.as_view(), name='update_user_profile'),
  path('user_profile/register_as_distributor/', DistributorRegisterView.as_view(), name='register_distributor'),
  path('admin_dashboard/request/approve/<int:pk>/', ApproveRequestsView.as_view(), name='approve_requests'),
  path('admin_dashboard/request/reject/<int:pk>/', RejectRequestsView.as_view(), name='reject_requests'),
]