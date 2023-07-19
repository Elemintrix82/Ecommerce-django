from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture:
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
        return ''
    thumbnail.short_description = _('Profile Picture')
    list_display = ('thumbnail','user', 'city', 'state', 'country', 'address_line_1', 'address_line_2')
    
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'city', 'state', 'country', 'address_line_1', 'address_line_2')


# Traduire les noms des modèles
Account._meta.verbose_name = _('Account')
Account._meta.verbose_name_plural = _('Accounts')
UserProfile._meta.verbose_name = _('User profile')
UserProfile._meta.verbose_name_plural = _('User profiles')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
