from django.db import models
from store.models import Product, Variation
from accounts.models import Account

from django.utils.translation import gettext_lazy as _

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, verbose_name=_('Cart Id'))
    data_added = models.DateField(auto_now_add=True, verbose_name=_('Data Added'))
    
    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variations = models.ManyToManyField(Variation, blank=True, verbose_name=_('Variations'))
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name=_('cart'))
    quantity = models.IntegerField(verbose_name=_('quantity'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product