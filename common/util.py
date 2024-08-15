from django.utils.text import slugify

def license_picture_path(instance, filename):
  renter_name = slugify(instance.user.get_full_name())
  return f'license_pictures/{renter_name}/{filename}'


def car_blue_book_path(instance, filename):
  renter_name = slugify(instance.renter.user.get_full_name())
  return f'car_blue_books/{renter_name}/{filename}'