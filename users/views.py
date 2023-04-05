from django.shortcuts import render,redirect
from django.contrib import messages

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

from .forms import UserAddForm,AddUserForm,AddBookingForm,AddVaccineForm
from .models import UserProfile,Booking,Vaccination,Feedback,Message
from doctors.models import DoctorProfile
from datetime import datetime

from .decorators import user_only, not_auth_user
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.


def index(request):
    return render(request, "home.html")

@user_only
def user_home(request):
    print("user home")
    user = UserProfile.objects.filter(user_ID=request.user.id)
    vaccine = Vaccination.objects.filter(user_ID=request.user).last()
    today  = datetime.today().date()
    # print(vaccine.Vaccinated_Date == str(today.replace(year=today.year - 1)))
    if(len(user) == 0):
        user = False
    else:
        user = user[0]
    vaccine_alert=False
    print(vaccine)
    if vaccine != None:
        if(vaccine.Vaccinated_Date == str(today.replace(year=today.year - 1))):
            vaccine_alert="It's Time for your next vaccine"
    
    return render(request, "users/user-home.html",{"user":user,"vaccine_alert":vaccine_alert})

@not_auth_user
def signup(request):  # first get the user form from forms.py to render with signup.html
    signup_form = UserAddForm()
    if(request.method == "POST"):
        form = UserAddForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("password")
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken !!! Retry")
                return redirect("signup")
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken !!! Retry")
                return redirect("signup")
            else:
                new_user = form.save()
                new_user.save()

                # getting and assigning group to the user
                group = Group.objects.get(name="users")
                new_user.groups.add(group)
                messages.info(request, "User Account Created")
                return redirect("signin")
        else:
            messages.info( request, "Fom validation Failed!!! Try a defferent password.")

    return render(request, "users/signup.html", {"signup_form": signup_form})


@not_auth_user
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session["username"] = username
            request.session["password"] = password
            login(request, user)
            return redirect("user_home")
        else:
            # print("LOgin Failed")
            messages.info(request, "Username or password incorrect ")
            return redirect("signin")
    return render(request, "users/signin.html")

@user_only
def signout(request):
    logout(request)
    return redirect("signin")

@user_only
def add_user_profile(request):
    form = AddUserForm()
    if request.method == "POST":
        add_form = AddUserForm(request.POST,request.FILES)
        if(add_form.is_valid()):
            user = User.objects.get(id=request.user.id)
            updated_profile = add_form.save()
            updated_profile.user_ID = user
            updated_profile.save()
            return redirect("view_user_profile")
    return render(request, "users/add-profile.html",{"form":form})
@user_only
def upadate_user_profile(request):
    user = UserProfile.objects.get(user_ID=request.user)
    if request.method == "POST":
        user.User_Name=request.POST["User_Name"]
        user.Phone_Number=request.POST["Phone_Number"]
        user.Address=request.POST["Address"]
        user.Age=request.POST["Age"]
        user.save()
        return redirect("view_user_profile")
    return render(request, "users/update-profile.html",{"user":user})
@user_only
def upadate_profileImage(request):
    if request.method == "POST":
        user = UserProfile.objects.get(user_ID=request.user)
        user.User_photo=request.FILES["User_photo"] 
        user.save()
        return redirect("view_user_profile")

@user_only
def view_user_profile(request):
    user = UserProfile.objects.filter(user_ID=request.user.id)
    if(len(user) == 0):
        return redirect("add_user_profile")
    return render(request,"users/user-profile.html",{"user":user[0]})

def services_page(request):
    return render(request,"services.html")

@user_only
def user_services_page(request):
    return render(request,"users/services.html")


def view_all_doctors(request):
    all_doctors = DoctorProfile.objects.all()
    doctor_count = all_doctors.count()
    return render(request,"users/view-all-doctors.html",{"all_doctors":all_doctors,"doctor_count":doctor_count})

@user_only
def view_doctor_profile(request,id):
    doctor = DoctorProfile.objects.get(id=id)
    return render(request,"users/doctor-profile.html",{"doctor":doctor})

@user_only
def book_doctor(request,id):
    user = UserProfile.objects.filter(user_ID=request.user.id)
    if(len(user) == 0):
        return redirect("add_user_profile")
    doctor = DoctorProfile.objects.get(id=id)
    form = AddBookingForm()
    if request.method == "POST":
        add_form = AddBookingForm(request.POST,request.FILES)
        if(add_form.is_valid()):
            booked_form = add_form.save()
            patient = User.objects.get(id=request.user.id)
            booked_form.Patient_ID = patient.id
            booked_form.Patient_Name = patient.username
            booked_form.Doctor_ID = doctor.doctor_ID
            booked_form.Doctor_Name = doctor.Doctor_name
            booked_form.status = "Payment Pending"
            booked_form.save()
            return redirect("payment_page")
    return render(request,"users/book-doctor.html",{"doctor":doctor,"form":form})


@user_only
def view_my_bookings(request):
    all_bookings = Booking.objects.filter(Patient_ID=request.user.id).exclude(status="Cancelled").exclude(status="Cancelled By Doctor")
    app_count = all_bookings.count()
    return render(request,"users/view-all-bookings.html",{"all_bookings":all_bookings,"app_count":app_count})

def user_cancel_booking(request,id):
    booking = Booking.objects.get(id=id)
    booking.status = "Cancelled"
    booking.save()
    return redirect("view_my_bookings")

@user_only
def add_vaccine(request):
    user = UserProfile.objects.filter(user_ID=request.user.id)
    if(len(user) == 0):
        return redirect("add_user_profile")
    form = AddVaccineForm()
    if request.method == "POST":
        add_form = AddVaccineForm(request.POST,request.FILES)
        print(request.FILES)
        if(add_form.is_valid()):
            vaccine_form = add_form.save()
            user = UserProfile.objects.get(user_ID=request.user.id)
            vaccine_form.user_ID = request.user
            vaccine_form.User_name = user.User_Name
            vaccine_form.save()
            return redirect("view_my_vaccines")
    return render(request, "users/add-vaccine.html",{"form":form})


@user_only
def view_my_vaccines(request):
    all_vaccines = Vaccination.objects.filter(user_ID=request.user.id)
    vaccinecount = all_vaccines.count()
    return render(request,"users/view-all-vaccines.html",{"all_vaccines":all_vaccines,"vaccinecount":vaccinecount})

@user_only
def payment_page(request):
    currency = 'INR'
    amount = 50000  # Rs. 200
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency, payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    print(context)
    return render(request, 'users/payment-page.html', context=context)

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            params_dict = {'razorpay_order_id': razorpay_order_id,'razorpay_payment_id': payment_id,'razorpay_signature': signature}
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print("result : ",result)
            if result is not None:
                amount = 50000  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    booking = Booking.objects.all().last()
                    booking.status = "Booked"
                    booking.save()
                    # render success page on successful caputre of payment
                    return redirect("view_my_bookings")

                except:
                    # if there is an error while capturing payment.
                    return redirect("view_my_bookings")

            else:
                # if signature verification fails.
                return redirect("view_my_bookings")
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

@user_only
def give_feedback(request,id):
    
    if request.method == "POST":
        feedback = request.POST["feedback"]
        f = Feedback(feedback=feedback,doctor_id=id,user=request.user)
        f.save()
        messages.info(request, "Added Feedback")
        return redirect("view_my_bookings")
    return render(request,"users/feedback-form.html")


@user_only
def view_feedbacks(request,id):
    feedbacks = Feedback.objects.filter(doctor_id=id)
    feedback_count = feedbacks.count()
    return render(request, "users/view-feedbacks.html",{"feedbacks":feedbacks,"feedback_count":feedback_count})

@user_only
def send_message(request,id):
    if request.method == "POST":
        message = request.POST["message"]
        doc = User.objects.get(id=id)
        doctor = DoctorProfile.objects.get(doctor_ID=doc)
        f = Message(message=message,doctor=doctor,user=request.user)
        f.save()
        messages.info(request, "Message Sent")
        return redirect("view_messages")

@user_only
def view_messages(request):
    user_messages = Message.objects.filter(user=request.user).exclude(reply=True)
    reply_messages = Message.objects.filter(user=request.user).exclude(reply=False)
    user_messages_count = user_messages.count()
    reply_messages_count = reply_messages.count()
    return render(request, "users/view-messages.html",{"user_messages":user_messages,"reply_messages":reply_messages,"user_messages_count":user_messages_count,"reply_messages_count":reply_messages_count})