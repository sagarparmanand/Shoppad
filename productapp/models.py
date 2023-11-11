from django.db import models

# Create your models here.

class Product(models.Model):

    CAT=(
        (1,"Mobile"),
        (2,"Shoes"),
        (3,"Cloths")
    )

    AVAIL=(
        (1,"Yes"),
        (0,"No")
    )

    name=models.CharField(max_length=50,verbose_name="Name")
    price=models.FloatField(verbose_name="price per item")
    qty=models.IntegerField(verbose_name="Quantity")
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    is_available=models.BooleanField(verbose_name="is available",choices=AVAIL)
    pdetails=models.CharField(max_length=500,verbose_name="Description")
    pimages=models.ImageField(upload_to='appimages/products',verbose_name="Product images")
    pdiscount=models.IntegerField(verbose_name="Discount")

    def __str__(self):
        return self.name