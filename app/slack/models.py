from django.db import models
from django.utils import timezone
# Create your models here.

class Order(models.Model):
    user_id = models.CharField(max_length=16)
    price = models.IntegerField()
    ordered_at = models.DateField(default=timezone.now)

class Gaman(models.Model):
    user_id = models.CharField(max_length=16)
    price = models.IntegerField()
    ordered_at = models.DateField(default=timezone.now)