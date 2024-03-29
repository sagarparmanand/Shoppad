from django.urls import path
from accountApp import views

urlpatterns = [
    path('login',views.user_login),
    path('register',views.user_register),
    path('logout',views.user_logout),
    path('forget',views.user_forget),
]