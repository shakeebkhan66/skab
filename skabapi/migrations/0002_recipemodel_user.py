# Generated by Django 4.1.4 on 2023-01-04 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skabapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipemodel',
            name='user',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='skabapi.usermodel'),
        ),
    ]