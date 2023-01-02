from django.contrib.auth.models import User
from rest_framework import serializers

from skabapi.models import UserModel, RecipeModel


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'fullname',
            'password',
            'confirmPassword',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'confirmPassword': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        fullname = validated_data.get('fullname')
        password = validated_data.get('password')
        confirmPassword = validated_data.get('confirmPassword')

        if password == confirmPassword:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({
                'error': 'Both passwords dont match'
            })


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeModel
        fields = ['id', 'productName', 'ingredients', 'makeRecipe', 'categories', 'image']
