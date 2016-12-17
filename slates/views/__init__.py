from django.shortcuts import render
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.views.decorators.csrf import ensure_csrf_cookie

from user import *
from message import *
from event import *
from mark import *
from school import *
from flashcard import *
from mcq import *

# Create your views here.

def login_page(request):
    return render(request, 'login.html')


@ensure_csrf_cookie
def do_login(request):
    user_name = request.POST['username']
    password = request.POST['password']
    user = authenticate(user_name=user_name, password=password)

    if user is not None:
    	login(request, user)
        return redirect('/home')
    return redirect('/')


def do_logout(request):
	logout(request)
	return redirect('/')

@login_required
def home(request):
    return render(request, 'home.html', {})

@login_required
def marks(request):
    if request.user.user_type == "student":
        return render(request, 'marks.html', {})
    return render(request, "access_denied.html")

@login_required
def events(request):
    if request.user.user_type == "student":
        return render(request, 'events.html', {})
    return render(request, "access_denied.html")

@login_required
def news(request):
    if request.user.user_type == "student":
        return render(request, 'news.html', {})
    return render(request, "access_denied.html")

@login_required
def profile(request):
    return render(request, 'profile.html', {})

@login_required
def view(request):
    return render(request, 'view.html', {})

@login_required
def manage(request):
    if request.user.user_type != "student":
        return render(request, 'manage.html', {})
    return render(request, "access_denied.html")

@login_required
def flash(request):
    return render(request, 'flashcard.html', {})

@login_required
def mcq(request):
    return render(request, 'mcq.html', {})