from multiprocessing import context
from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from twilio.rest import Client


from .models import *
from .decorators import unauthenticated_user
import os

# account_sid = 'ACe58095480bb51e29d89a4a76ef6110c6'
# auth_token = 'de1b808cfdc2914ae80aab343f2b0e43'
# verify_sid = 'VA7bd85bed5b1a7aeffac5d6052e051a44'

account_sid = os.environ.get('Account_sid')
auth_token = os.environ.get('Auth_token')
verify_sid = os.environ.get('Service_sid')

client = Client(account_sid, auth_token)

# Create your views here.
@login_required(login_url="signin")
def index(request):
    user = VechicleUsers.objects.get(user=request.user)
    vechicleType = VechicleTypes.objects.get(name=user.vechicle_type)
    price = Price.objects.get(type=user.fuel_type)
    context = {'user':user,'vechicleType':vechicleType,'price':price}
    return render(request,"base/index.html",context)

@unauthenticated_user
def vechicleUsersSignup(request):
    form = CreateUserForm()
    vechicleTypes = VechicleTypes.objects.all()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        vechicle_no = request.POST.get('VechileNum')
        vechicle_type = request.POST.get('vechicle_type')
        phone_no = request.POST.get('Phone-No')
        fuel_type = request.POST.get('Fuel_type')
        vechicle_type = VechicleTypes.objects.get(name=vechicle_type)

        if form.is_valid():
            user = form.save()
            VechicleUsers.objects.create(
                user =  user,
                username = username,
                first_name = first_name,
                last_name = last_name,
                email=email,
                vechicle_no = vechicle_no,
                vechicle_type = vechicle_type,
                phone_no = phone_no,
                fuel_type = fuel_type
            )
            return redirect("verify", username=username, phonenumber=phone_no)
    context = {"form":form,'VechicleTypes':vechicleTypes}
    return render(request,"base/signup.html",context)

@unauthenticated_user
def verify(request,username,phonenumber):
    verification = client.verify.services(verify_sid).verifications.create(to=f"+94{phonenumber}", channel='sms')
    if request.method == "POST":
        otp = request.POST.get("OTP")
        verification_check = client.verify.services(verify_sid).verification_checks.create(to=f"+94{phonenumber}", code=otp)
        print(verification_check.status)
        if verification_check.status == "approved":
            user = VechicleUsers.objects.get(username=username)
            user.active = True
            user.save()
            return redirect("signin")
        else:
            user = User.objects.get(username=username)
            user.delete()
            messages.error(request, 'Invalid OTP Number! Your account has been exposed because of security purpose, please make a new account')
            return redirect("signup")
    context = {"username":username, "phonenumber": phonenumber}
    return render(request,"base/Verify.html",context)

@unauthenticated_user
def fuelStationSignup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        name = request.POST.get('station_name')
        address = request.POST.get('station_address')
        phone_no = request.POST.get('phone_no')
        city = request.POST.get('city')
        reg_no = request.POST.get('regnumber')
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='station')
            user.groups.add(group)

            Stations.objects.create(
                user =  user,
                name = name,
                address = address,
                city = city,
                phone_no = phone_no,
                registration_number=reg_no
            )
            messages.success(request, 'You have successfully signed up')
            return redirect('fuelStationSignup')
    context = {'form':form}
    return render(request,"base/fuelStationSignup.html",context)

@unauthenticated_user
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            if User.objects.get(username=username).groups.filter(name="station").exists():
                messages.error(request, 'Please Login with our Desktop Application!')
                return redirect('signin')
            else:
                if VechicleUsers.objects.get(username=username).active == True:
                    login(request,user)
                    return redirect('index')
                else:
                    return redirect('verify',username=username, phonenumber=VechicleUsers.objects.get(username=username).phone_no)
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    context = {}
    return render(request,"base/signin.html",context)

@login_required(login_url="signin")
def logout_view(request):
    logout(request)
    return redirect('signin')

def checkVechicle(request):
    if request.method == "GET":
        vechicle_no = request.GET.get("vechicle_no")
        if VechicleUsers.objects.filter(vechicle_no=vechicle_no).exists():
            return JsonResponse({'data':"vechicle already exists"})
        else:
            return JsonResponse({'data':"vechicle not exists"})
