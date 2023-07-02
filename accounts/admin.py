from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active', 'first_name']
    readonly_fields = ['password', 'last_login',]
    list_display_links = ['username', 'email']  # For creating hyperlink
    ordering = ('-date_joined',)

    # because we made custom usermodel we need to use this
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
