from django.contrib import admin

from accounts.models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):

    list_display=['uid','mobile_no','uimage','uadd']


admin.site.register(Profile,ProfileAdmin)