# Generated by Django 5.0.3 on 2024-06-19 12:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarDetail',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('renter_name', models.CharField(max_length=100, null=True)),
                ('renter_contact', models.CharField(max_length=10, null=True)),
                ('car_type', models.CharField(choices=[('SUV', 'SUV'), ('EV', 'EV'), ('Truck', 'Truck'), ('Sedan', 'Sedan')], max_length=100, null=True)),
                ('car_model', models.CharField(max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('availability', models.CharField(choices=[('Unlisted', 'Unlisted'), ('Booked', 'Booked'), ('Available', 'Available')], default='Available', max_length=20, null=True)),
                ('image', models.ImageField(default='static/images/lambo.jpg', upload_to='static/car_images')),
            ],
        ),
        migrations.CreateModel(
            name='CarOrder',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Paid', 'Paid'), ('Completed', 'Completed')], default='Pending', max_length=100, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cars.cardetail')),
                ('rentee', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
