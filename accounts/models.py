from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):

    mobile_no=models.IntegerField()
    uimage=models.ImageField(upload_to="user_image")
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    uadd=models.CharField(max_length=555)