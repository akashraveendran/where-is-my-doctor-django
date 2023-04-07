from django.urls import path
from . import views

urlpatterns = [
    
    path('admin_page', views.admin_page, name='admin_page'),
    path('signin',views.admin_signin,name='admin_signin'),
    path('signout',views.admin_signout,name='admin_signout'),
    path('view_doctor',views.view_doctors_list, name='view_doctors_list'),
    path('delete_doctor/<int:id>',views.delete_doctor, name='delete_doctor'),
    path('view_users',views.view_users_list, name='view_users_list'),
    path('delete_user/<int:id>',views.delete_user, name='delete_user'),
    path('view_bookings_list',views.view_bookings_list, name='view_bookings_list'),
]