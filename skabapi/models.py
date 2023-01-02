from django.db import models

STATE_CHOICE = ((
    ('All', 'All'),
    ('Tea', 'Tea'),
    ('Biryani', 'Biryani'),
    ('Karhai', 'Karhai'),
    ('Cakes', 'Cakes'),
    ('Vegetables', 'Vegetables'),
    ('Salad', 'Salad'),
))


# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirmPassword = models.CharField(max_length=100)


class RecipeModel(models.Model):
    productName = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=300)
    makeRecipe = models.CharField(max_length=300)
    categories = models.CharField(max_length=150)
    image = models.ImageField(upload_to="my_picture", blank=True)
