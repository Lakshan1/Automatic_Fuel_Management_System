from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VechicleTypes(models.Model):
    name = models.CharField(max_length=100)
    quota_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class FuelTypes(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VechicleUsers(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    vechicle_no = models.CharField(max_length=50)
    vechicle_type = models.ForeignKey(VechicleTypes,blank=False, null=False, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=50,null=True, blank=True)
    quota_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_filled_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    active = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.user.username

class Stations(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10,null=True,blank=True)
    registration_number = models.CharField(max_length=100,default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.name

class Price(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.type
