from django.db import models

# Create your models here.
class products(models.Model):
    p_name_short = models.CharField(max_length=20)
    p_name = models.CharField(max_length=120)
    p_image = models.ImageField(upload_to = "images")   #new
    p_price = models.IntegerField()
    p_quantity = models.IntegerField()
    p_specifications = models.CharField(max_length=500)
    p_seller_name = models.CharField(max_length=20)
    h1 = models.CharField(max_length=60)
    h2 = models.CharField(max_length=60)
    h3 = models.CharField(max_length=60)
    h4 = models.CharField(max_length=60)
    h5 = models.CharField(max_length=60)
    p_category = models.CharField(max_length=20)
    c_tags = models.CharField(max_length=400)


class customer(models.Model):
    c_name = models.CharField(max_length=20)
    c_email = models.EmailField()
    c_address = models.CharField(max_length=150)


class comments(models.Model):
    comment = models.CharField(max_length=500)
    c_datetime = models.DateTimeField()
    username_comment = models.CharField(max_length=20)
    p_id = models.IntegerField()


class cart(models.Model):
    cart_item = models.IntegerField()
    c_datetime = models.DateTimeField()
    username_cart = models.CharField(max_length=20)

class records(models.Model):
    username = models.CharField(max_length=20)
    product = models.IntegerField()
    quanity  = models.IntegerField()
    c_datetime = models.DateTimeField()
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20)
    address = models.CharField(max_length=150)