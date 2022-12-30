from django.contrib import admin

from skabapi.models import UserModel


# Register your models here.
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'fullname', 'password', 'confirmPassword']
