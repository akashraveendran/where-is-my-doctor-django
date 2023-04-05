from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.doctor_home, name="doctor_home"),
    path('signup/', views.d_signup, name="d_signup"),
    path('signin/', views.d_signin, name="d_signin"),
    path('signout/', views.d_signout, name="d_signout"),
    path('add-profile/', views.add_doctor_profile, name="add_doctor_profile"),
    path('view-profile/', views.view_doctor_profile, name="view_doctor_profile"),
    path('view-doctor_feedbacks/', views.doctor_feedbacks, name="doctor_feedbacks"),
    path('upadate_doctor_profile/', views.upadate_doctor_profile, name="upadate_doctor_profile"),
    path('upadate_doctor_profileImage/', views.upadate_doctor_profileImage, name="upadate_doctor_profileImage"),
    path('view-doctor-appoinments/', views.view_doctor_appoinments, name="view_doctor_appoinments"),
    path('view-doctor-messages/', views.view_doctor_messages, name="view_doctor_messages"),
    path('reply_message/<int:id>', views.reply_message, name="reply_message"),
    path('view-patient/<int:id>', views.view_patient, name="view_patient"),
    path('cancel-booking/<int:id>', views.cancel_booking, name="cancel_booking"),
    path('completed_checkup/<int:id>', views.completed_checkup, name="completed_checkup"),
]