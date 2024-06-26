from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  address = models.CharField(max_length=100, null=True)
  license_photo = models.ImageField(upload_to='static/license_pictures')
  contact = models.CharField(max_length=100, null=True)

  def __str__(self):
    return f'{self.user.username} - {self.user.email} - {self.user.get_full_name()}'
