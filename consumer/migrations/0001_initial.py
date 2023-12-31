# Generated by Django 4.0.6 on 2022-09-09 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_item', models.IntegerField()),
                ('c_datetime', models.DateTimeField()),
                ('username_cart', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('c_datetime', models.DateTimeField()),
                ('username_comment', models.CharField(max_length=20)),
                ('p_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=20)),
                ('c_email', models.EmailField(max_length=254)),
                ('c_address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name_short', models.CharField(max_length=20)),
                ('p_name', models.CharField(max_length=120)),
                ('p_image', models.ImageField(upload_to='images')),
                ('p_price', models.IntegerField()),
                ('p_quantity', models.IntegerField()),
                ('p_specifications', models.CharField(max_length=500)),
                ('p_seller_name', models.CharField(max_length=20)),
                ('h1', models.CharField(max_length=60)),
                ('h2', models.CharField(max_length=60)),
                ('h3', models.CharField(max_length=60)),
                ('h4', models.CharField(max_length=60)),
                ('h5', models.CharField(max_length=60)),
                ('p_category', models.CharField(max_length=20)),
                ('c_tags', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='records',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('product', models.IntegerField()),
                ('quanity', models.IntegerField()),
                ('c_datetime', models.DateTimeField()),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10)),
                ('payment_method', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
    ]
