from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.vechicleUsersSignup,name="signup"),
    path("fuelStationSignup/",views.fuelStationSignup,name="fuelStationSignup"),
    path("signin/",views.signin,name="signin"),
    path("logout/",views.logout_view,name="logout"),
    path("check-vechicle/",views.checkVechicle,name="check_vechicle"),
    path("verify/<str:username>/<int:phonenumber>" , views.verify,name="verify")
]