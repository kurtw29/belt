from django.shortcuts import render, redirect, HttpResponse
from time import localtime, strftime, gmtime
from django.contrib import messages
from apps.belt_app.models import *
import bcrypt

def loginReg(request):
    return render(request, 'belt_app/loginReg.html')

def login_process(request):
    email_input = request.POST['email']
    print('*-'*15, "REQUEST EMAIL", request.POST, 'and', email_input)
    print('*\n'+'*-', "DATABASE", User.objects.values())
    user = User.objects.filter(email=email_input)
    try:
        bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode())
        messages.success(request, "Successfully logged in!")
        request.session['id'] = user[0].id
        return redirect('/success')
    except:
        messages.error(request, "Invalid Login", "login")
        return redirect('/')

def reg_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, "registration")
        return redirect('/')
    else:
        hashIt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],password=hashIt)
        request.session['name'] = request.POST['first_name']
        request.session['id'] = User.objects.last().id
        print('*-'*15, 'REQUEST SESSION: ', request.session)
        messages.success(request, "Successfully registered!")
    return redirect('/success')

def success(request):
    if 'id' in request.session:
        return render(request, 'belt_app/success.html')
    else:
        return redirect('/')