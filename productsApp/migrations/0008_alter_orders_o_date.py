# Generated by Django 5.0.3 on 2024-03-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsApp', '0007_remove_orders_p_name_remove_orders_p_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='o_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]