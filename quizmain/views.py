from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin


from .forms import AuthUserForm


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_url = '/'
    success_message = 'Добро пожаловать!'