from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import VechicleUsers,VechicleTypes,Stations
from .serializers import VechicleUserSerializer ,StationUserSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        station = StationUserSerializer(Stations.objects.get(user=user)).data
        # Add custom claims
        token['station'] = station
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    return Response ([
        {
            'Endpoint': '/getVechicle/<str:vechicleno>/',
            'Methods': 'GET',
            'body': None,
            'description': 'Get vechicle details '
        }, 
        {
            'Endpoint': 'updateFullQuota/<str:vechicleno>/',
            'Methods': 'GET',
            'body': None,
            'description': 'update full quota'
        },
        {
            'Endpoint': '/updateQuota/<str:vechicleno>/<int:quantity>/',
            'Methods': 'GET',
            'body': None,
            'description': 'update vechicle Quota'
        },
        {
            'Endpoint': 'refreshQuota/',
            'Methods': 'GET',
            'body': None,
            'description': 'refresh vechicle quota'
        },
        {
            'Endpoint': 'token/',
            'Methods': 'POST',
            'body': {
                        "username": "",
                        "password": ""
                    },
            'description': 'get refresh and access token'
        },
        {
            'Endpoint': 'token/refresh/',
            'Methods': 'POST',
            'body': {
                        "refresh": ""
                    },
            'description': 'get new refresh and access token'
        },
        



    ])

@api_view(['GET'])
def getVechicle(request , vechicleno):  
    vechicle =   VechicleUsers.objects.get(vechicle_no=vechicleno)
    serializer = VechicleUserSerializer(vechicle,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def updateFullQuota(request,vechicleno):
    vechicle = VechicleUsers.objects.get(vechicle_no=vechicleno)
    vechicle_type = VechicleTypes.objects.get(name=vechicle.vechicle_type)
    if vechicle.quota_used > 0:
        data = {"Message": f"available quota is {vechicle_type.quota_limit - vechicle.quota_used}","Available_limit":f"{vechicle_type.quota_limit - vechicle.quota_used}"}
    else:
        vechicle.quota_used = vechicle_type.quota_limit
        vechicle.save()
        data = {"Message": " success"}
    return Response (data)
    


@api_view(['GET'])
def updateQuota (request , vechicleno,quantity):
    vechicle = VechicleUsers.objects.get(vechicle_no=vechicleno)
    vechicle_type = VechicleTypes.objects.get(name=vechicle.vechicle_type)
    total_used = vechicle.quota_used
    if (total_used + quantity) > vechicle_type.quota_limit:
        data = {"Message": " Weekly quota limit exit!"}
    else:
        vechicle.quota_used += quantity 
        vechicle.save()
        data = {"Message": " success"}
    return Response (data)

@api_view(['GET'])
def refreshQuota(request):
    vechicles = VechicleUsers.objects.all()
    try:
        for obj in vechicles:
            obj.quota_used = 0
            obj.save()
        data = {"Message": " success"}
    except:
        data = {"Message": "There is an error!"}
    return Response (data)
    






