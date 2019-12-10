from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as _UserAdmin


from smartmodels.admin.mixins import SmartModelAdminMixin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Group, Permission


class UserAdmin(SmartModelAdminMixin, _UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('is_active', 'email', 'phone', 'first_name', 'last_name', 'is_staff')
    list_filter = ('email', 'phone', 'is_staff', 'is_active',)
    search_fields = ('email', 'phone', 'first_name', 'last_name')
    ordering = ('email', 'phone')
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    # change_password_form = AdminPasswordChangeForm
    filter_horizontal = ('groups', 'user_permissions',)


class GroupAdmin(admin.ModelAdmin):
    pass


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'codename', 'name')
    list_filter = ('content_type', 'codename')
    search_fields = ('content_type__app_label', 'codename', 'name')


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission, GroupAdmin)
