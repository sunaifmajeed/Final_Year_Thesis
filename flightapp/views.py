from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import pickle
from django.core.mail import send_mail
from django.contrib import messages
from flightdelay import settings
from collections import defaultdict
@login_required
def home(request):
    form = FlightForm()
    with open('data/flightmodel.pkl', 'rb') as file:  
        model = pickle.load(file)
    if request.method == "POST":

        
        try:
            DAY_OF_WEEK = int(request.POST.get('DAY_OF_WEEK'))
            AIRLINE_NAME = int(request.POST.get('airline'))
            FLIGHT_NUMBER = int(request.POST.get('FLIGHT_NUMBER'))
            ORIGIN_AIRPORT = int(request.POST.get('origin_airport'))
            AIRPORT = int(request.POST.get('destination_airport'))
            SCHEDULED_DEPARTURE = request.POST.get('SCHEDULED_DEPARTURE')
            SCHEDULED_DEPARTURE = int(SCHEDULED_DEPARTURE[:-3]) * 60 + int(SCHEDULED_DEPARTURE[-2:])
            DEPARTURE_TIME = request.POST.get('DEPARTURE_TIME')
            DEPARTURE_TIME = int(DEPARTURE_TIME[:-3]) * 60 + int(DEPARTURE_TIME[-2:])
            DEPARTURE_DELAY = int(request.POST.get('DEPARTURE_DELAY'))
        
            result = model.predict([[DAY_OF_WEEK,AIRLINE_NAME,FLIGHT_NUMBER,ORIGIN_AIRPORT,AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY]])
            result = int(result[0])
            if result == 0:
                messages.success(request,"FLight is on time , No delay")
            elif result > 0:
                messages.success(request,"FLight will delay ,"+str(result)+" minutes")
            else:
                messages.success(request,"FLight will be ,"+str(result)+" minutes early")

            send_mail_delay(request.user.username,result)

        except:
            messages.warning(request, "Please check the data you have entered !")
        # print(DAY_OF_WEEK,AIRLINE_NAME,FLIGHT_NUMBER,ORIGIN_AIRPORT,AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY)
        # print("result.......",result)

    context = {
        
        "form":form,
    }

    return render(request, "index.html",context)

def loginpage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        except:
            messages.warning("Fill the details")
        if user is not None:
            request.session['username'] = username
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)
def send_mail_delay(name,result):
    from django.template.loader import get_template
    from django.core.mail import EmailMultiAlternatives
    htmly = get_template('new.html')
    subject = 'Delay details'
    to = 'abinjoshy3@gmail.com'
    try:
        html_content = htmly.render({
            'result': result,
            'name': name,

        })
        print(name)
        print(result)

        msg = EmailMultiAlternatives(subject, subject, settings.EMAIL_HOST_USER, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        status = True
    except Exception as e:
        status = False
        print(e,'--------------exceptions')
    print(status,'-----------status')
    return status