from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from skabapi.models import User, RecipeModel


# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = [
#             'username',
#             'email',
#             'fullname',
#             'password',
#             'confirmPassword',
#         ]
#
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'confirmPassword': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         username = validated_data.get('username')
#         email = validated_data.get('email')
#         fullname = validated_data.get('fullname')
#         password = validated_data.get('password')
#         confirmPassword = validated_data.get('confirmPassword')
#
#         if password == confirmPassword:
#             user = UserModel(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             return user
#         else:
#             raise serializers.ValidationError({
#                 'error': 'Both passwords don't match'
#             })
#
#
# class LoginSerializer(serializers.Serializer):
#     """
#     This serializer defines two fields for authentication:
#       * username
#       * password.
#     It will try to authenticate the user with when validated.
#     """
#     username = serializers.CharField(
#         label="username",
#         write_only=True
#     )
#     password = serializers.CharField(
#         label="password",
#         # This will be used when the DRF browsable API is enabled
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )
#
#     def validate(self, attrs):
#         # Take username and password from request
#         username = attrs.get('username')
#         password = attrs.get('password')
#
#         if username and password:
#             # Try to authenticate the user by using Django Auth Framework
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)
#
#             if not user:
#                 # If you don't have a regular user then raise error
#                 msg = 'Access denied, wrong username and password.'
#                 raise serializers.ValidationError(msg, code='authorization')
#
#         else:
#             msg = 'Both "username" and "password" are required.'
#             raise serializers.ValidationError(msg, code='authorization')
#
#         # We have a valid user, put it in the serializer's validated_data.
#         # It will be used in the view.
#         attrs['user'] = user
#         return attrs

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'fullname',
            'password',
            'confirmPassword',
        )

    def create(self, validated_data):
        password = make_password(validated_data.get('password'))
        validated_data.update({'password': password})
        return super(UserRegisterSerializer, self).create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'fullname',
            'password',
            'confirmPassword',
        )


class RecipeSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=True, read_only=True)
    # username = serializers.CharField(source="username.username")

    def create(self, validated_data):
        return RecipeModel.objects.create(**validated_data)

    class Meta:
        model = RecipeModel
        fields = ['id', 'productName', 'ingredients', 'makeRecipe', 'categories', 'image', 'username']
        depth = 1
