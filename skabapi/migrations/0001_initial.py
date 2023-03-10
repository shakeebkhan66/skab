# Generated by Django 4.1.4 on 2023-03-14 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(help_text='username', max_length=50, unique=True)),
                ('email', models.EmailField(help_text='email', max_length=254, unique=True)),
                ('fullname', models.CharField(help_text='fullname', max_length=50)),
                ('password', models.CharField(help_text='password', max_length=255)),
                ('confirmPassword', models.CharField(help_text='confirmPassword', max_length=255)),
                ('image', models.ImageField(default=None, upload_to='user_profile_images')),
                ('bio', models.CharField(max_length=500)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecipeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=100)),
                ('ingredients', models.CharField(max_length=300)),
                ('makeRecipe', models.CharField(max_length=300)),
                ('categories', models.CharField(choices=[('Tea', 'Tea'), ('Rice', 'Rice'), ('Pizza', 'Pizza'), ('Karhai', 'Karhai'), ('Cake', 'Cake'), ('Vegetable', 'Vegetable'), ('Salad', 'Salad'), ('Roti', 'Roti')], max_length=150)),
                ('image', models.ImageField(upload_to='my_picture')),
                ('favorite', models.BooleanField(default=False)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
