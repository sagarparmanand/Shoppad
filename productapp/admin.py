from django.contrib import admin

from productapp.models import Product

# Register your models here.

# admin.site.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','pdiscount','qty','cat','is_available','pimages','pdetails']
    list_filter=['name','is_available']

admin.site.register(Product,ProductAdmin)
admin.site.site_header="Ekart Dashboard"