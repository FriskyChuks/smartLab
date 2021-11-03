from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm, UserGroupForm


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    update_form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    group_form = UserGroupForm

    list_display = ('username', 'admin',)
    list_filter = ('admin', 'staff',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','staff','active', 'group')}),
        # ('Groups', {'fields': ('name')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)