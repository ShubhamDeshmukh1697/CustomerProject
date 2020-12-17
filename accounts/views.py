from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm
from .filters import OrderFilter

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
    
    myFilter = OrderFilter(request.GET ,queryset=cus_order)
    cus_order = myFilter.qs

    # gives orders for customer with id which is accepted as string 
    context = {'customer':customer,'cus_order':cus_order,'myFilter':myFilter}
    return render(request,'accounts/customer.html', context)

def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields =['product','status'],extra=6)
    # extra 6 means that 6 forms will be present


    customer = Customer.objects.get(id = pk)
    # get customer with id 

    formset = OrderFormSet(queryset=Order.objects.none() , instance = customer)
    # queryset hides already present data by setting none

    if request.method=="POST":
        formset = OrderFormSet(request.POST , instance=customer)
        
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
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

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request,'accounts/delete.html',context)