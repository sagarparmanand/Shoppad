# Generated by Django 5.0.3 on 2024-03-06 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsApp', '0002_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(default=0, max_length=255, verbose_name='Size'),
            preserve_default=False,
        ),
    ]
