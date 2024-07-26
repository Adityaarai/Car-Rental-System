from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  address = models.CharField(max_length=100, null=True)
  license_photo = models.ImageField(upload_to='license_pictures/')
  contact = models.CharField(max_length=100, null=True)

  def __str__(self):
    return f'{self.user.get_full_name()} - {self.user.email} - {self.contact}'

class DistributorRequest(models.Model):
  requester = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, null=True)
  car_detail = models.ForeignKey('cars.CarDetail', on_delete=models.DO_NOTHING, null=True)
  distributor_status = models.BooleanField(default=False)

