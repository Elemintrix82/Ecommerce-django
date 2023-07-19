from django.contrib import admin
from .models import Category

from django.utils.translation import gettext_lazy as _

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

# Traduire les noms des modèles
Category._meta.verbose_name = _('Category')
Category._meta.verbose_name_plural = _('Categories')

admin.site.register(Category, CategoryAdmin)
