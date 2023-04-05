from django.shortcuts import render,redirect
from django.contrib import messages

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

from .forms import UserAddForm,DoctorProfieForm
from .models import DoctorProfile
from users.models import Booking,UserProfile,Vaccination,Feedback,Message

from .decorators import doctor_only, not_auth_doctor

# Create your views here.

@doctor_only
def doctor_home(request):
    return render(request, "doctors/doctor-home.html")

@not_auth_doctor
def d_signup(request):  # first get the user form from forms.py to render with signup.html
    signup_form = UserAddForm()
    if(request.method == "POST"):
        form = UserAddForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("password")
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken !!! Retry")
                return redirect("d_signup")
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken !!! Retry")
                return redirect("d_signup")
            else:
                new_user = form.save()
                new_user.is_active =  False
                new_user.save()
                # getting and assigning group to the user
                group = Group.objects.get(name="doctors")
                new_user.groups.add(group)
                messages.info(request, "doctor Account Created!!! Please wait for the Approval of Admin")
                return redirect("d_signin")
        else:
            messages.info(
                request, "Fom validation Failed!!! Try a defferent password.")

    return render(request, "doctors/signup.html", {"signup_form": signup_form})


@not_auth_doctor
def d_signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session["username"] = username
            request.session["password"] = password
            login(request, user)
            return redirect("doctor_home")
        else:
            messages.info(request, "Username or password incorrect or Account is Not Activated")
            return redirect("d_signin")
    return render(request, "doctors/signin.html")

@doctor_only
def d_signout(request):
    logout(request)
    return redirect("d_signin")


@doctor_only
def add_doctor_profile(request):
    form = DoctorProfieForm()
    if request.method == "POST":
        add_form = DoctorProfieForm(request.POST,request.FILES)
        if(add_form.is_valid()):
            doctor = User.objects.get(id=request.user.id)
            updated_profile = add_form.save()
            updated_profile.doctor_ID = doctor
            updated_profile.save()
            return redirect("doctor_home")
    return render(request, "doctors/add-profile.html",{"form":form})

@doctor_only
def view_doctor_profile(request):
    doctor = DoctorProfile.objects.filter(doctor_ID=request.user.id)
    if(len(doctor) == 0):
        return redirect("add_doctor_profile")
    return render(request,"doctors/doctor-profile.html",{"doctor":doctor[0]})


@doctor_only
def doctor_feedbacks(request):
    feedbacks = Feedback.objects.filter(doctor_id=request.user.id)
    feedback_count = feedbacks.count()
    return render(request, "doctors/view-feedbacks.html",{"feedbacks":feedbacks,"feedback_count":feedback_count})


@doctor_only
def upadate_doctor_profile(request):
    doctor = DoctorProfile.objects.get(doctor_ID=request.user.id)
    if request.method == "POST":
        doctor.Enroll_No=request.POST["Enroll_No"]
        doctor.Doctor_name=request.POST["Doctor_name"]
        doctor.Specialised_In=request.POST["Specialised_In"]
        doctor.Experience=request.POST["Experience"]
        doctor.Clinic_Name=request.POST["Clinic_Name"]
        doctor.Contact_Number=request.POST["Contact_Number"]
        doctor.Clinic_Address=request.POST["Clinic_Address"]
        doctor.About=request.POST["About"]
        doctor.save()
        return redirect("view_doctor_profile")
    return render(request, "doctors/update-profile.html",{"doctor":doctor})
@doctor_only
def upadate_doctor_profileImage(request):
    if request.method == "POST":
        doctor = DoctorProfile.objects.get(doctor_ID=request.user.id)
        doctor.Doctor_Photo=request.FILES["Doctor_Photo"] 
        doctor.save()
        return redirect("view_doctor_profile")

@doctor_only
def view_doctor_appoinments(request):
    all_bookings = Booking.objects.filter(Doctor_ID=request.user.id)
    app_count = all_bookings.count()
    return render(request,"doctors/appoinments.html",{"all_bookings":all_bookings,"app_count":app_count})

@doctor_only
def view_doctor_messages(request):
    doctor = DoctorProfile.objects.get(doctor_ID=request.user)
    user_messages = Message.objects.filter(doctor=doctor).exclude(reply=False)
    reply_messages = Message.objects.filter(doctor=doctor).exclude(reply=True)
    user_messages_count = user_messages.count()
    reply_messages_count = reply_messages.count()
    return render(request, "doctors/view-messages.html",{"user_messages":user_messages,"reply_messages":reply_messages,"user_messages_count":user_messages_count,"reply_messages_count":reply_messages_count})

@doctor_only
def reply_message(request,id):
  if request.method == "POST":
    doctor = DoctorProfile.objects.get(doctor_ID=request.user)
    user = User.objects.get(id=id)
    message = request.POST["message"]
    f = Message(message=message,doctor=doctor,user=user,reply=True)
    f.save()
    messages.info(request, "Message Sent")
    return redirect("view_doctor_messages")


@doctor_only
def view_patient(request,id):
    user = UserProfile.objects.get(user_ID=id)
    all_vaccines = Vaccination.objects.filter(user_ID=user.user_ID)
    return render(request,"doctors/patient-profile.html",{"user":user,"all_vaccines":all_vaccines})

@doctor_only
def cancel_booking(request,id):
    booking = Booking.objects.get(id=id)
    booking.status = "Cancelled By Doctor"
    booking.save()
    return redirect("view_doctor_appoinments")

@doctor_only
def completed_checkup(request,id):
    booking = Booking.objects.get(id=id)
    booking.status = "Completed Checkup"
    booking.save()
    return redirect("view_doctor_appoinments")