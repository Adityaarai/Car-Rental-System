from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile
from common.util import car_blue_book_path

class CarType(models.Model):
  car_type = models.CharField(max_length=100)
  logo = models.ImageField(upload_to='car_type_logo')

  def __str__(self):
    return f'{self.car_type}'

STATUS = (
  ('Pending', 'Pending'),
  ('Approved', 'Approved'),
  ('Paid', 'Paid'),
  ('Completed', 'Completed'),
  ('Rejected', 'Rejected'),
)

AVAILABILITY = (
  ('Unlisted', 'Unlisted'),
  ('Booked', 'Booked'),
  ('Available', 'Available'),
)


# Create your models here.
class CarDetail(models.Model):
    car_id = models.AutoField(primary_key=True)
    renter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=100, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY, null=True, default='Available')
    blue_book = models.ImageField(upload_to = car_blue_book_path, blank=True)
    image = models.ImageField(default='static/images/lambo.jpg', upload_to='car_images/')

    # display what is shown in the product name
    def __str__(self):
        return f'{self.car_id} - {self.car_model} - {self.car_type}'

# car orders table model
class CarOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    car_detail = models.ForeignKey(CarDetail, on_delete=models.CASCADE)
    rentee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, default='Pending')
    
    # display what is shown in the order name
    def __str__(self):
        return f'{self.rentee} - {self.product} - {self.total_price} - {self.status}'