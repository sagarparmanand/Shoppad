from django.urls import path
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

path('login',views.user_login),
path('register',views.user_register),
path('logout',views.user_logout),
path('profile',views.uesr_profile),

]
if settings.DEBUG:

    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)