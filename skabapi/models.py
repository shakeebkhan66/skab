from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from skabapi.managers import CustomUserManager

CATEGORY_CHOICE = ((
    ('Tea', 'Tea'),
    ('Rice', 'Rice'),
    ('Pizza', 'Pizza'),
    ('Karhai', 'Karhai'),
    ('Cake', 'Cake'),
    ('Vegetable', 'Vegetable'),
    ('Salad', 'Salad'),
    ('Roti', 'Roti'),
))


# Create your models here.
# class UserModel(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(blank=False)
#     fullname = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     confirmPassword = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.username
#
#     def set_password(self, password):
#         pass

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, help_text='username')
    email = models.EmailField(unique=True, help_text='email')
    fullname = models.CharField(max_length=50, help_text='fullname')
    password = models.CharField(max_length=255, help_text='password')
    confirmPassword = models.CharField(max_length=255, help_text='confirmPassword')
    image = models.ImageField(upload_to="user_profile_images", default=None, blank=False)
    bio = models.CharField(max_length=500, blank=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class RecipeModel(models.Model):
    productName = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=300)
    makeRecipe = models.CharField(max_length=300)
    categories = models.CharField(max_length=150, choices=CATEGORY_CHOICE, )
    image = models.ImageField(upload_to="my_picture", blank=False)
    favorite = models.BooleanField(default=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f'{self.username}'
