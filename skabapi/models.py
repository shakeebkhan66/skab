from django.db import models

CATEGORY_CHOICE = ((
    ('Tea', 'Tea'),
    ('Rice', 'Rice'),
    ('Pizza', 'Pizza'),
    ('Karhai', 'Karhai'),
    ('Cake', 'Cake'),
    ('Vegetable', 'Vegetable'),
    ('Salad', 'Salad'),
))


# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirmPassword = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    def set_password(self, password):
        pass


class RecipeModel(models.Model):
    productName = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=300)
    makeRecipe = models.CharField(max_length=300)
    categories = models.CharField(max_length=150, choices=CATEGORY_CHOICE, )
    image = models.ImageField(upload_to="my_picture", blank=False)
    username = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f'{self.username}'

