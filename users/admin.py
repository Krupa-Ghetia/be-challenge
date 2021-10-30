from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'is_instructor', 'is_staff', 'is_active')
    list_filter = ('username', 'email', 'is_instructor', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'is_instructor', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'is_instructor', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
