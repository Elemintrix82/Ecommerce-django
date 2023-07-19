from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Account
from store.models import Product, Variation

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    payment_id = models.CharField(max_length=200, verbose_name=_('Payment ID'))
    payment_method = models.CharField(max_length=200, verbose_name=_('Payment Method'))
    amount_paid = models.CharField(max_length=200, verbose_name=_('Amount Paid'))
    status = models.CharField(max_length=200, verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    
    def __str__(self):
        return self.payment_id
    

class Order(models.Model):
    STATUS = (
        ('New', _('New')),
        ('Accepted', _('Accepted')),
        ('Completed', _('Completed')),
        ('Cancelled', _('Cancelled')),
    )
    
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name=_('User'))
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, verbose_name=_('Payment'))
    order_number = models.CharField(max_length=30, verbose_name=_('Order Number'))
    first_name = models.CharField(max_length=60, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=60, verbose_name=_('Last Name'))
    phone = models.CharField(max_length=30, verbose_name=_('Phone'))
    email = models.EmailField(max_length=60, verbose_name=_('Email'))
    address_line_1 = models.CharField(max_length=60, verbose_name=_('Address Line 1'))
    address_line_2 = models.CharField(max_length=60, blank=True, verbose_name=_('Address Line 2'))
    country = models.CharField(max_length=60, verbose_name=_('Country'))
    state = models.CharField(max_length=60, verbose_name=_('State'))
    city = models.CharField(max_length=60, verbose_name=_('City'))
    order_note = models.CharField(max_length=100, blank=True, verbose_name=_('Order Note'))
    order_total = models.FloatField(verbose_name=_('Order Total'))
    tax = models.FloatField(verbose_name=_('Tax'))
    status = models.CharField(max_length=15, choices=STATUS, default='New', verbose_name=_('Status'))
    ip = models.CharField(blank=True, max_length=20, verbose_name=_('IP'))
    is_ordered = models.BooleanField(default=False, verbose_name=_('Is Ordered'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'
    
    def __str__(self):
        return self.first_name
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Order'))
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, verbose_name=_('Payment'))
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variations = models.ManyToManyField(Variation, blank=True, verbose_name=_('Variations'))
    # color = models.CharField(max_length=60)
    # size = models.CharField(max_length=60)
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    product_price = models.FloatField(verbose_name=_('Product Price'))
    ordered = models.BooleanField(default=False, verbose_name=_('Ordered'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    def __str__(self):
        return self.product.product_name
