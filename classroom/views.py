from django.shortcuts import render, redirect
from classroom.models import *

def home(req):
    return render(req, 'classroom/home.html')

