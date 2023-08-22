from django.contrib import admin

# Register your models here.
from consumer.models import products,customer,comments,records,cart #importing model for registering model in admin panel

admin.site.register(products) #registering model in admin panel
admin.site.register(customer) #registering model in admin panel
admin.site.register(comments) #registering model in admin panel
admin.site.register(records) #registering model in admin panel
admin.site.register(cart) #registering model in admin panel