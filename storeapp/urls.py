
from django.urls import path
from storeapp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home',views.homepage),
    path('contact',views.contact),
    path('about',views.about),
    path('edit/<id>',views.edit),
    path('delete/<id>',views.delete),
    path('add/<x>/<y>',views.add),




    path('',views.home),
    path('pabout',views.about),
    path('pcontact',views.contact),
    path('pcart',views.cart),
    path('pplace_order',views.place_order),
    path('pproduct_details/<pid>',views.product_details),
    path('cartfilter/<catv>',views.cart_filter),
    path('price_range',views.price_range),
    path('sort',views.sorting),
    path('search',views.searching),
    path('cart/<prod_id>',views.addcart),
    path('remove/<rid>',views.remove_product),
    path('changeqty/<cid>',views.changeqty),
    path('cancel_order/<cid>',views.cancel_order),
    path('makepayment',views.make_payment),
    path('sendmail',views.sendmail),

]

if settings.DEBUG:

    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)