from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm

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

def createOrder(request):

    form = OrderForm()
    if request.method=="POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    # instance directly shows value of order in input fields
    if request.method=="POST":
        form = OrderForm(request.POST , instance=order)
        # it will not create new record and change the old instance
        if form.is_valid():
            form.save()
            return redirect('/')
    

    context = {'form':form,'order':order}
    return render(request,'accounts/order_form.html',context)
