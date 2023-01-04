from django.contrib import admin

from skabapi.models import UserModel, RecipeModel


# Register your models here.
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'fullname', 'password', 'confirmPassword']


@admin.register(RecipeModel)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'productName', 'ingredients', 'makeRecipe', 'categories', 'image', 'username']
