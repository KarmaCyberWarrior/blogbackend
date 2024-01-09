from django.shortcuts import render, redirect
from blogpost.models import *
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from .forms import AccountAuthenticationForm

# Create your views here.
def index(request, *args, **kwargs):
    context = {}
    user = request.user
    context['user'] = user
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
			
            form.save(request)
            return redirect("index")

        else:
            context['login_form'] = form

    
    
    
    return render(request, "index.html", context)