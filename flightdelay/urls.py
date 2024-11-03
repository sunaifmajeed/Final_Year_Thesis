


from django.contrib import admin
from django.urls import path
from flightapp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('login/', loginpage, name="login"),
    path('register/', register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
