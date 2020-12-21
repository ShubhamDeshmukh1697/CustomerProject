from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm , CreateUserForm ,CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users,admin_only



# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    
    orders = request.user.customer.order_set.all()
    order = orders
    ordDel=orders.filter(status="Delivered")
    ordPen = orders.filter(status='Pending')
    context = {'orders':orders,'order':order,'ordDel' :ordDel ,"ordPen":ordPen}
    return render(request ,'accounts/user.html' , context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method=="POST":
        form = CustomerForm(request.POST , request.FILES , instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    
    return render(request,'accounts/account_settings.html',context)


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            
            # associating group for created user
            group =  Group.objects.get(name='customer')

            user.groups.add(group)

            # assigning customer to a new user
            Customer.objects.create(
                user=user ,
            )

            messages.success(request , f"Account was created for {username} ")
            return redirect('login')

    context = {'form':form}

    return render(request , 'accounts/register.html' ,context)

@unauthenticated_user
# above decorator will be called first 
def loginPage(request):
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
@admin_only
def home(request):
    order=Order.objects.all().order_by('id')
    orders = order[:5]
    ordDel=Order.objects.filter(status="Delivered")

    ordPen = Order.objects.filter(status='Pending')
    customers = Customer.objects.all()
    context={'orders':orders,'customers':customers,'order':order,'ordDel':ordDel,'ordPen':ordPen}
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,'accounts/product.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,id):
    customer = Customer.objects.get(id=id)
    cus_order = customer.order_set.all()
    
    myFilter = OrderFilter(request.GET ,queryset=cus_order)
    cus_order = myFilter.qs

    # gives orders for customer with id which is accepted as string 
    context = {'customer':customer,'cus_order':cus_order,'myFilter':myFilter}
    return render(request,'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request,'accounts/delete.html',context)