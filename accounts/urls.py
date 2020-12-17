from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home ,name='home'),
    path('product/' , views.product, name='product'),
    path('customer/<int:id>/' , views.customer, name='customer'),

]
