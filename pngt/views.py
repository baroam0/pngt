
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def home(request):
    return render(request, 'base.html')

