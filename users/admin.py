from django.contrib import admin
from .models import UserProfile, DistributorRequest

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user','contact', 'address')

class DistributorRequestAdmin(admin.ModelAdmin):
  list_display = ('requester','', 'address')

admin.site.register(UserProfile, UserProfileAdmin)
