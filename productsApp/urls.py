from django.urls import path
from productsApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home),

    path('admin_add',views.admin_add),
    path('admin_del/<did>',views.admin_delete),
    path('admin_update/<uid>',views.admin_update),
    path('admin_logout/', views.admin_logout),
    # path('admin_ban_add',views.admin_ban_add),
    # path('admin_ban_del/<did>',views.admin_ban_del),


    path('mens',views.mens),
    path('womens',views.womens),
    path('kids',views.kids),
    
    path('contact',views.contact),
    
    path('details/<vid>',views.details),

    path('cart',views.cart),
    path('cart_add/<cid>',views.cart_add),
    path('cart_del/<did>',views.cart_del),
    path('cart_qty/<qid>',views.qty),

    path('search',views.searching),
    path('searched',views.searchinged),

    # path('payment/<pid>',views.payment),
    path('payment',views.payment),

    path('sendmail',views.sendmail_user),

    path('price_250_500',views.price_250_500),
    path('price_500_1000',views.price_500_1000),
    path('price_1000_1500',views.price_1000_1500),
    path('price_1500_2000',views.price_1500_2000),
    path('price_2000_3000',views.price_2000_3000),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    

