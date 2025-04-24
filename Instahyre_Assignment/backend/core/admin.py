from django.contrib import admin
from .models import User, Contact, SpamReport
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'phone_number', 'name', 'email', 'is_staff')
    search_fields = ('phone_number', 'name', 'email')
    ordering = ('phone_number',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'email', 'password1', 'password2')}
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(SpamReport)
