from django.contrib import admin
from .models import Boutique, Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]
    search_fields = ('product_name', 'category__category_name')  # Ajout de la barre de recherche

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')
    search_fields = ('product__product_name', 'variation_category', 'variation_value')  # Ajout de la barre de recherche

class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('boutique_name', 'boutique_address')
    search_fields = ('boutique_name', 'boutique_address')  # Ajout de la barre de recherche

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product__product_name', 'user__first_name', 'user__last_name')  # Ajout de la barre de recherche

class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__product_name',)  # Ajout de la barre de recherche


# Traduire les noms des modèles
Boutique._meta.verbose_name = _('Shop')
Boutique._meta.verbose_name_plural = _('Shops')
Product._meta.verbose_name = _('Product')
Product._meta.verbose_name_plural = _('Products')
Variation._meta.verbose_name = _('Variation')
Variation._meta.verbose_name_plural = _('Variations')
ReviewRating._meta.verbose_name = _('Review Rating')
ReviewRating._meta.verbose_name_plural = _('Reviews Rating')
ProductGallery._meta.verbose_name = _('Product Gallery')
ProductGallery._meta.verbose_name_plural = _('Products Gallery')

admin.site.register(Boutique, BoutiqueAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
