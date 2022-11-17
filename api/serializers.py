from rest_framework.serializers import ModelSerializer
from base.models import VechicleUsers,Stations
from django.contrib.auth.models import User


class VechicleUserSerializer(ModelSerializer):
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