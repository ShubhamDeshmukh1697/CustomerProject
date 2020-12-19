from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm , CreateUserForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required



# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                # print("post",request.POST)
                user = form.cleaned_data.get('username')
                messages.success(request , f"Account was created for {user} ")
                return redirect('login')

        context = {'form':form}

        return render(request , 'accounts/register.html' ,context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request , username=username ,password = password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'usename or pasword is incorrect')
                return redirect('login')
            
        context = {}
        return render(request , 'accounts/login.html' ,context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
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

@login_required(login_url='login')
def customer(request,id):
    customer = Customer.objects.get(id=id)
    cus_order = customer.order_set.all()
    
    myFilter = OrderFilter(request.GET ,queryset=cus_order)
    cus_order = myFilter.qs

    # gives orders for customer with id which is accepted as string 
    context = {'customer':customer,'cus_order':cus_order,'myFilter':myFilter}
    return render(request,'accounts/customer.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request,'accounts/delete.html',context)