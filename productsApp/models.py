from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Product(models.Model):
    pname = models.CharField(max_length=255,verbose_name='NAME')
    pcat = models.CharField(max_length=255,verbose_name='Category')
    subcat = models.CharField(max_length=255,verbose_name='Sub_Category')
    price = models.IntegerField(verbose_name="Price")
    pdis = models.IntegerField(verbose_name="Discount")
    fprice = models.IntegerField(verbose_name="Final_Price")
    psize = models.CharField(max_length=255,verbose_name='Size')
    description = models.CharField(max_length=255,verbose_name='Description')
    img1=models.ImageField(upload_to='Images',verbose_name="Image1")
    img2=models.ImageField(upload_to='Images',verbose_name="Image2")
    img3=models.ImageField(upload_to='Images',verbose_name="Image3")
    img4=models.ImageField(upload_to='Images',verbose_name="Image4")

    def __str__(self):
        return self.pname

class Cart(models.Model):

    u_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    p_id=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    size = models.CharField(max_length=255,verbose_name='Size')
    fprice_tot = models.CharField(max_length=100)

    def __str__(self):
        return str(self.u_id)

class Orders(models.Model):
    order_id=models.CharField(max_length=100)
    # u_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    u_username=models.CharField(max_length=100)
    # p_id=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    o_sub_cat=models.CharField(max_length=100)
    o_p_name=models.CharField(max_length=100)
    o_price=models.CharField(max_length=100)
    qty=models.IntegerField(default=1)
    size = models.CharField(max_length=255,verbose_name='Size')
    o_date=models.DateField(auto_now_add=True)

    
class Banner(models.Model):
    ban_cat = models.CharField(max_length=255,verbose_name='Description')
    ban_img=models.ImageField(upload_to='Images',verbose_name="Image1")