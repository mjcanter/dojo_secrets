# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render, redirect
import random
import re
from django.contrib import messages
from django.db.models import Count, DateTimeField
from models import *
import bcrypt

def index(request):
	context = {
		"Users": Users.objects.all(),
		"Secrets": Secrets.objects.all()
		}
	return render(request, 'dojosecrets/index.html', context)
def home(request):
	context = {
		"Users": Users.objects.all(),
		"curr_user": Users.objects.filter(id=request.session['userid']),
		"Secrets": Secrets.objects.all(),
		"count": Secrets.objects.annotate(num_likes=Count('secret_likes')).order_by('num_likes')}
	return render(request, 'dojosecrets/home.html', context)
def popular(request):
   	context = {
		"Users": Users.objects.all(),
		"curr_user": Users.objects.filter(id=request.session['userid']),
		"Secrets": Secrets.objects.all().annotate(num_likes=Count('secret_likes')).order_by('-num_likes'),
	}
	return render(request, 'dojosecrets/popular.html', context)



def register(request): 
    #errors = []

    # if request.session['first_name'] = None
    #     errors.append("Please enter a first name")
    #     return redirect("/")

    # if not request.session['last_name']:
    #     errors.append("Please enter a last name")
    #     return redirect("/")

    # if not request.session['email']:
    #     errors.append("Please enter an email")
    #     return redirect("/")
    # elif not re.match(EMAIL_REGEX,request.session['email']):
    #     errors.append("Not a valid email")
    #     return redirect("/")
    # elif user:
    #     errors.append("Email is already in use")
    #     return redirect("/")

    # if not request.session['password']:
    #     errors.append("enter a password")
    #     return redirect("/")
    # elif len(request.session['password']) < 8:
    #     errors.append("Password must be at least 8 characters")
    #     return redirect("/")
    # elif request.session['password'] != request.session["confirm"]:
    #     errors.append("Password must match")
    #     return redirect("/")

    # if errors:
    #     for error in errors:
    #         flash(error)
    #     return redirect("/")
    #else:
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if not request.POST['first_name']:
        messages.error(request, "Please enter a first name")
        return redirect("/")

    elif not request.POST['last_name']:
        messages.error(request, "Please enter a last name")
        return redirect("/")

    elif not request.POST['email']:
        messages.error(request, "Please enter an email")
        return redirect("/")
    elif not re.match(EMAIL_REGEX,request.POST['email']):
        messages.error(request, "Not a valid email")
        return redirect("/")
    elif Users.objects.filter(email=request.POST['email'])==True:
        messages.error(request, "Email is already in use")
        return redirect("/")

    elif not request.POST['password']:
        messages.error(request, "enter a password")
        return redirect("/")
    elif len(request.POST['password']) < 8:
        messages.error(request, "Password must be at least 8 characters")
        return redirect("/")
    elif request.POST['password'] != request.POST["confirm"]:
        messages.error(request, "Password must match")
        return redirect("/")
    else:
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        Users.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],pw_hash=hashed)
        return redirect('/home')

def login(request):
    Key = Users.objects.get(email=request.POST['email'])
    storedhash = Key.pw_hash.encode('utf-8')
    inputdata = bcrypt.hashpw(request.POST['lgpassword'].encode('utf-8'), storedhash)
    if inputdata == storedhash:
    	request.session['userid'] = Key.id
    	print request.session['userid']
        return redirect('/home')
    else:
        messages.error(request, "User name or password not valid")
        return redirect('/')
def secret(request):
	print request.POST['new_secret']
	Secrets.objects.create(secret_text=request.POST['new_secret'],user_id=Users.objects.get(id=request.session['userid']))
	return redirect('/home')	
def like(request):
    Likes.objects.create(user_likes=Users.objects.get(id=request.session['userid']),secret_likes=Secrets.objects.get(id=request.POST['like_this']))
    return redirect('/home')
def delete(request):
    print request.POST['delete_this']
    Secrets.objects.get(id=request.POST['delete_this']).delete()
    return redirect('/home')
def popsecret(request):
	print request.POST['new_secret']
	Secrets.objects.create(secret_text=request.POST['new_secret'],user_id=Users.objects.get(id=request.session['userid']))
	return redirect('/popular')	
def poplike(request):
    Likes.objects.create(user_likes=Users.objects.get(id=request.session['userid']),secret_likes=Secrets.objects.get(id=request.POST['like_this']))
    return redirect('/popular')	
def popdelete(request):
    print request.POST['delete_this']
    Secrets.objects.get(id=request.POST['delete_this']).delete()
    return redirect('/popular')	
def deleteuser(request):
    print request.POST['delete_this']
    Users.objects.get(id=request.POST['delete_this']).delete()
    return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')



# def wall():
#     # refresh wall content
#     #query for messages
#     if "user_id" not in session and request.endpoint != "/": #ask Jack about this
#         return redirect('/')

#     userquery = "SELECT first_name FROM users WHERE id = :id;"

#     data = {"id":session["user_id"]}

#     user_first = mysql.query_db(userquery,data)[0]


#     messagequery = "SELECT messages.id, messages.users_id, messages.message, messages.created_at, users.first_name, users.last_name FROM messages LEFT JOIN users ON users.id = messages.users_id ORDER BY messages.created_at DESC"
#     messagedata = mysql.query_db(messagequery)

#     #query for comments
#     commentquery = "SELECT comments.id, comments.comment, comments.created_at, comments.messages_id, comments.users_id, users.first_name, users.last_name FROM comments LEFT JOIN messages ON comments.messages_id = messages.id LEFT JOIN users  ON comments.users_id = users.id ORDER BY comments.created_at DESC"
#     commentdata = mysql.query_db(commentquery)


#     return render_template('index.html', messagedata = messagedata, commentdata= commentdata, user_first=user_first)



