from django.db import models
from django.contrib.auth.models import User
# Create your models here.
 

class Customer(models.Model):
    user = models.OneToOneField(User , null=True ,on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outoor'),
    )
    name = models.CharField(max_length=30)
    price = models.FloatField()
    category = models.CharField(max_length=50,choices=CATEGORY)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
     )
    customer = models.ForeignKey(Customer,null=True,on_delete = models.SET_NULL) 
    product = models.ForeignKey(Product,null=True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS,null=True)
    note = models.CharField(max_length=50,null=True)
    

    def __str__(self):
        return self.product.name
    