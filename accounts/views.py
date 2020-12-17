from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def home(request):
    order=Order.objects.all().order_by('id')
    orders = order[:5]
    ordDel=Order.objects.filter(status="Delivered")

    ordPen = Order.objects.filter(status='Pending')
    customers = Customer.objects.all()
    context={'orders':orders,'customers':customers,'order':order,'ordDel':ordDel,'ordPen':ordPen}
    return render(request,'accounts/dashboard.html',context)

def product(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,'accounts/product.html',context)

def customer(request,id):
    customer = Customer.objects.get(id=id)
    cus_order = customer.order_set.all()
    # gives orders for customer with id which is accepted as string 
    
    return render(request,'accounts/customer.html',{'customer':customer,'cus_order':cus_order})
