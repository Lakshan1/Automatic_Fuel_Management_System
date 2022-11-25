from rest_framework.serializers import ModelSerializer
from base.models import VechicleUsers,Stations,VechicleTypes
from django.contrib.auth.models import User
from rest_framework import serializers

class VechicleTypesSerializer(ModelSerializer):
    class Meta:
        model = VechicleTypes
        fields = '__all__'

class VechicleUserSerializer(ModelSerializer):
    vechicle_type = VechicleTypesSerializer()

    class Meta:
        model = VechicleUsers
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','date_joined']
        # exclude = ['password']

class StationUserSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Stations
        fields = '__all__'