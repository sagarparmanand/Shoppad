# Generated by Django 5.0.3 on 2024-03-28 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsApp', '0011_rename_u_id_orders_u_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='p_id',
            new_name='o_p_name',
        ),
        migrations.AddField(
            model_name='orders',
            name='o_sub_cat',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
