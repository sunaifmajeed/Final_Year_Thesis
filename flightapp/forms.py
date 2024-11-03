from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
import csv


with open('data/airline.csv') as f:
    AIRLINE_CHOICES=[tuple(line) for line in csv.reader(f)]

with open('data/destination_airport.csv') as f:
    DESTINATION_AIRPORT_CHOICES=[tuple(line) for line in csv.reader(f)]

with open('data/orgin_airport.csv') as f:
    ORIGIN_AIRPORT_CHOICES=[tuple(line) for line in csv.reader(f)]



class FlightForm(forms.Form):
    airline = forms.ChoiceField(choices = AIRLINE_CHOICES)
    origin_airport = forms.ChoiceField(choices = ORIGIN_AIRPORT_CHOICES)
    destination_airport = forms.ChoiceField(choices = DESTINATION_AIRPORT_CHOICES)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField( widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)



