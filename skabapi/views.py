from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.http.multipartparser import MultiPartParser
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import Token
from skabapi.models import User, RecipeModel
from skabapi.renderers import UserRenderer
from skabapi.serializers import UserRegisterSerializer, ProfileRecipeSerializer, UserLoginSerializer, \
    UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, \
    ResetPasswordSubmitSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
# class RegisterAPIView(APIView):
#     serializer_class = UserRegisterSerializer
#
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token = RefreshToken.for_user(user)
#             response = {
#                 'refresh_token': str(token),
#                 'access_token': str(token.access_token),
#             }
#             return Response(response, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
#
#
# class LoginView(APIView):
#     # This view should be accessible also for unauthenticated users.
#     # permission_classes = (permissions.AllowAny)
#
#     def post(self, request, format=None):
#         serializer = LoginSerializer(data=self.request.data,
#                                      context={'request': self.request})
#         if serializer.is_valid():
#             user = serializer.validated_data['username']
#             print(user)
#             login(request, user)
#         return Response({"payload": serializer.data, 'status': status.HTTP_200_OK})

# Generate Token Manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def validate_user(attrs):
    print(attrs)
    try:
        user = User.objects.get(email=attrs['email'])
        check = check_password(attrs['password'], user.password)
        if check:
            return user
        else:
            raise exceptions.AuthenticationFailed('Invalid Password')
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('No such user')


def generate_token(user):
    try:
        Token.objects.get(user=user).delete()
    except:
        pass
    return Token.objects.create(user=user)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            data = {'detail': user.username + ' registered successfully!'}
            return Response({'data': data, 'status': HTTP_201_CREATED, 'token': token})
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         user = validate_user(request.data)
#         serializer = UserProfileSerializer(user)
#         data = serializer.data
#
#         try:
#             token = generate_token(user)
#             data.update({'token': token.key})
#             return Response(data, status=HTTP_200_OK)
#         except Exception as e:
#             return Response(e, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            print(email)
            print(password)
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"token": token, "msg": "Login Success"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"non_field_errors": ["Email or Password is not valid"]}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserProfileView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer = UserProfileSerializer(user)
        recipes = RecipeModel.objects.filter(username=user)
        recipe_serializer = ProfileRecipeSerializer(recipes, many=True)
        data = {
            'user': user_serializer.data,
            'recipes': recipe_serializer.data
        }
        return Response(data)








class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Changed Password Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"msg": "Password reset link send, Please check your email"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordSubmitView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = ResetPasswordSubmitSerializer(data=request.data,
                                                   context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Recipes(APIView):
    def get(self, request, format=None):
        try:
            recipes = RecipeModel.objects.all()
            serializer = ProfileRecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": serializer.errors, "Exception": e}, status=status.HTTP_400_BAD_REQUEST)


class CreateRecipes(APIView):
    def post(self, request, format=None):
        # user = UserModel.objects.get(username=request.data)
        recipe = request.data
        print("Hello" + str(recipe))
        if recipe is not None:
            new_recipe = RecipeModel.objects.create(
                username=User.objects.get(username=recipe["username"]),
                productName=recipe["productName"],
                ingredients=recipe["ingredients"],
                makeRecipe=recipe["makeRecipe"],
                categories=recipe["categories"],
                image=recipe["image"]
            )
            new_recipe.save()
            serializer = ProfileRecipeSerializer(new_recipe)
            return Response(serializer.data)
        else:
            print("Error")
            return Response({"msg": "Please enter the data"})

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'msg': 'Recipe Uploaded Successfully',
        #                      'status': 'success', 'candidate': serializer.data}, status=status.HTTP_201_CREATED)
        # return Response({'msg': 'Failed to upload', 'status': 'failed', 'candidate': serializer.errors},
        #                 status=status.HTTP_400_BAD_REQUEST)
