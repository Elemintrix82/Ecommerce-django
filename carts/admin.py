from django.contrib import admin
from .models import Cart, CartItem
from django.utils.translation import gettext_lazy as _

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "data_added")
    
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "is_active")
    
# Traduire les noms des modèles
Cart._meta.verbose_name = _('Cart')
Cart._meta.verbose_name_plural = _('Carts')
CartItem._meta.verbose_name = _('Cart Item')
CartItem._meta.verbose_name_plural = _('Cart Items')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)