from django.contrib import admin
from .models import Payment, Order, OrderProduct

from django.utils.translation import gettext_lazy as _


# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "full_name", "phone", "email", "city", "order_total", "tax", "status", "is_ordered", "created_at"]
    list_filter = ["status", "is_ordered"]
    search_fields = ["order_number", "first_name", "last_name", "phone", "email"]  # Ajout des champs pour la recherche
    list_per_page = 20
    inlines = [OrderProductInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ["order", "payment", "user", "product", "quantity", "product_price", "ordered", "created_at"]
    search_fields = ["order__order_number", "user__first_name", "user__last_name", "product__product_name"]  # Ajout des champs pour la recherche

# Traduire les noms des modèles
Payment._meta.verbose_name = _('Payment')
Payment._meta.verbose_name_plural = _('Payments')
Order._meta.verbose_name = _('Order')
Order._meta.verbose_name_plural = _('Orders')
OrderProduct._meta.verbose_name = _('Order Product')
OrderProduct._meta.verbose_name_plural = _('Order Products')

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
