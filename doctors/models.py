from django.db import models

from django.contrib.auth.models import User


# Create your models here.




class DoctorProfile(models.Model):
    doctor_ID = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True )
    Enroll_No = models.CharField(max_length=255,null=True,blank=True )
    Doctor_name = models.CharField(max_length=200,null=True,blank=True)
    Specialised_In = models.CharField(max_length=200,null=True,blank=True)
    Experience = models.TextField(max_length=200,null=True,blank=True)
    Clinic_Name = models.CharField(max_length=200,null=True,blank=True)
    Contact_Number = models.CharField(max_length=200,null=True,blank=True)
    Clinic_Address = models.TextField(max_length=200,null=True,blank=True)
    About = models.TextField(max_length=200,null=True,blank=True)
    Doctor_Photo = models.ImageField(upload_to="doctors",null=True,blank=True)