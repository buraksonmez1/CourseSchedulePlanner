from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import Group

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, AllOpenCourses, Courses

class UserAdmin(BaseUserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    model = User
    list_display = ['username', 'name',]
    fieldsets = (
        ('Account Information', {
            'fields': (
                'username',
                'password',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_staff',
                'is_superuser',
            )
        }),
        ('Personal Information', {
            'fields': (
                'name',
                'gpa',
            )
        }))
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

class AllOpenCoursesAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'long_name', 'section']
    search_fields = ('short_name',)

admin.site.register(User, UserAdmin)
admin.site.register(AllOpenCourses,AllOpenCoursesAdmin)
admin.site.register(Courses)
