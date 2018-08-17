from django.shortcuts import render, redirect, HttpResponse
from time import localtime, strftime, gmtime
from django.contrib import messages
from apps.belt_app.models import *
import bcrypt

def loginReg(request):
    return render(request, 'belt_app/loginReg.html')

def login_process(request):
    email_input = request.POST['email']
    user = User.objects.filter(email=email_input)
    try:
        bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode())
        messages.success(request, "Successfully logged in!")
        request.session['id'] = user[0].id
        return redirect('/quotes')
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
    return redirect('/quotes')

def quotes(request):
    if 'id' in request.session:
        print('request_session'*12, request.session['id'])
        post_id = User.objects.get(id=request.session['id']).id
        data={
            'user':User.objects.get(id=request.session['id']),
            'quotes':Quote.objects.all()
        }

        return render(request, 'belt_app/quotes.html', data)
    else:
        return redirect('/')

def edit(request, num):
    if 'id' in request.session:
        user_info = User.objects.get(id=num)
        user_data = {
            "first_name":user_info.first_name,
            "last_name":user_info.last_name,
            "email":user_info.email
        }
        return render(request, 'belt_app/edit.html', user_data)
    else:
        return redirect('/')

def update(request):
    str_id = str(request.session['id'])
    errors = User.objects.edit_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, "update")
        return redirect('/myaccount/'+ str_id)
    else:
        uInfo = User.objects.get(id=request.session['id'])
        uInfo.first_name = request.POST['first_name']
        uInfo.last_name = request.POST['last_name']
        if User.objects.filter(email = request.POST['email']):
            messages.error(request, "Email already exists", "update")
            uInfo.save()
            return redirect('/myaccount/'+str_id)
        else:
            uInfo.email = request.POST['email']
            uInfo.save()
            messages.success(request, "Successfully updated")
            return redirect('/myaccount/'+str_id)

def user(request, num):
    poster_info = User.objects.get(id=num)
    context ={
        "first_name":User.objects.get(id=num).first_name,
        "last_name":User.objects.get(id=num).last_name,
        "quote_content":Quote.objects.filter(poster=poster_info)
    }
    return render(request, 'belt_app/user_quotes.html', context)

def like(request, num):
    liked_user_id = request.session['id']
    this_quote = Quote.objects.get(id=num)
    this_poster = User.objects.get(id=request.session['id'])
    this_poster.liked_quotes.add(this_quote)
    return redirect('/quotes')

def add_quote(request):
    adder_id = request.session['id']
    errors = User.objects.quote_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, "add_quote")
            return redirect('/quotes')
    else:
        print('THIS IS REQUEST POST', request.POST)
        this_poster = User.objects.get(id=request.session['id'])
        this_quote = Quote.objects.create(author=request.POST['author_name'], quote=request.POST['quote_content'], poster=this_poster)
        print("*-"*15,'DID THIS QUOTE CREATED?', this_quote)
        return redirect('/quotes')

def delete(request, num):
    d = Quote.objects.get(id=num)
    d.delete()
    return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/')