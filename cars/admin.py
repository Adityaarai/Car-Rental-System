from django.contrib import admin
from .models import CarDetail, CarOrder

class CarOrderAdmin(admin.ModelAdmin):
  list_display = ('order_id','rentee', 'product', 'start_date', 'end_date', 'status')
  list_filter = ('rentee', 'status', 'product')

class CarDetailAdmin(admin.ModelAdmin):
  list_display = ('car_id','renter', 'car_type', 'car_model', 'availability')
  list_filter = ['car_type', 'car_model', 'availability']

# Register your models here.
admin.site.register(CarDetail, CarDetailAdmin)
admin.site.register(CarOrder, CarOrderAdmin)