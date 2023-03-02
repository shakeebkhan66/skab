from xml.dom import ValidationErr
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from skabapi.models import User, RecipeModel
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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

    def validate(self, attrs):
        password = attrs.get("password")
        confirmPassword = attrs.get("confirmPassword")
        if password != confirmPassword:
            raise serializers.ValidationError("Password and ConfirmPassword doesn't match")
        return attrs

    def create(self, validated_data):
        password = make_password(validated_data.get('password'))
        validated_data.update({'password': password})
        return super(UserRegisterSerializer, self).create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'fullname',
            # 'password',
            # 'confirmPassword',
        )


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirmPassword = serializers.CharField(max_length=255, style={'input_type': 'confirmPassword'}, write_only=True)

    class Meta:
        fields = ['password', 'confirmPassword']

    def validate(self, attrs):
        password = attrs.get("password")
        confirmPassword = attrs.get("confirmPassword")
        user = self.context.get('user')
        if password != confirmPassword:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded ID", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password", token)
            link = "http:localhost:3000/api/user/reset/" + uid + '/' + token
            print("Password Reset Link", link)
            # SEND EMAIL
            return attrs
        else:
            raise ValidationErr("You are not a registered user")


class ResetPasswordSubmitSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirmPassword = serializers.CharField(max_length=255, style={'input_type': 'confirmPassword'}, write_only=True)

    class Meta:
        fields = ['password', 'confirmPassword']

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            confirmPassword = attrs.get("confirmPassword")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != confirmPassword:
                raise serializers.ValidationError("Password and confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationErr("Token is not valid and expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationErr("Token is not valid and expired")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token": ("Token is expired or invalid")
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class RecipeSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=True, read_only=True)
    # username = serializers.CharField(source="username.username")

    def create(self, validated_data):
        return RecipeModel.objects.create(**validated_data)

    class Meta:
        model = RecipeModel
        fields = ['id', 'productName', 'ingredients', 'makeRecipe', 'categories', 'image', 'username']
        depth = 1
