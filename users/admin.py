from django.contrib import admin
from .models import UserProfile, DistributorRequest

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user','contact', 'address')

class DistributorRequestAdmin(admin.ModelAdmin):
  list_display = ('requester','car_detail', 'distributor_status')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DistributorRequest, DistributorRequestAdmin)
