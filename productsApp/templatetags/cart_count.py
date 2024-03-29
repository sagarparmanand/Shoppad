from django import template
from productsApp.models import Cart

register = template.Library()

@register.simple_tag
def cart_count(uid):
    return Cart.objects.filter(u_id=uid).count()