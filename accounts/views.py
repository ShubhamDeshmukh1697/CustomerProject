from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('Home page')

def product(request):
    return HttpResponse("product Page")

def customer(request):
    return HttpResponse("Customer Page")