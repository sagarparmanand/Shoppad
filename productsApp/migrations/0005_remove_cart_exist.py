# Generated by Django 5.0.3 on 2024-03-07 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productsApp', '0004_cart_exist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='exist',
        ),
    ]
