from django.shortcuts import render,redirect
from django.http import HttpResponse
from email import message

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from users.models import UserProfile
from users.models import Booking
from doctors.models import DoctorProfile

# Create your views here.


# def admin_page(request):
#     return HttpResponse("Hello world!")

def admin_page(request):
    user_count=UserProfile.objects.count()
    doctor_count=DoctorProfile.objects.count()
    booking_count=Booking.objects.count()
    return render(request,"admin/admin.html",{"user_count":user_count,"doc_count": doctor_count,"bookings":booking_count})




def admin_signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            request .session["username"]=username
            request .session["password"]=password
            login(request,user)
            return redirect("admin_page")
        else:
            
            messages.info(request,"username or password incorrect")
            return redirect("admin_signin")

    return render(request,"admin/admin_signin.html")

def admin_signout(request):

    logout(request)
    return redirect("admin_signin")    

def view_doctors_list(request):
    all_doctors = DoctorProfile.objects.all()
    doctor_count = all_doctors.count()
    return render(request,"admin/doctors_view.html",{"all_doctors":all_doctors,"doctor_count":doctor_count})
def delete_doctor(request,id):
    doctor = User.objects.get(id=id)
    doctor.delete()
    return redirect("view_doctors_list")

def view_users_list(request):
    all_users = UserProfile.objects.all()
    user_count = all_users.count()
    return render(request,"admin/user_view.html",{"all_users":all_users,"user_count":user_count})

def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("view_users_list")


def view_bookings_list(request):
    all_bookings = Booking.objects.all()
    b_count = all_bookings.count()
    return render(request,"admin/booking_view.html",{"all_bookings":all_bookings,"b_count":b_count})