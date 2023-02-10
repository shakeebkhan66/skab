from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import Token
from skabapi.models import User, RecipeModel
from skabapi.serializers import UserRegisterSerializer, RecipeSerializer, ProfileSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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

class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {'detail': user.username + ' registered successfully!'}
            return Response(data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = validate_user(request.data)
        serializer = ProfileSerializer(user)
        data = serializer.data

        try:
            token = generate_token(user)
            data.update({'token': token.key})
            return Response(data, status=HTTP_200_OK)
        except Exception as e:
            return Response(e, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
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
                return Response({"msg": "Login Success"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"non_field_errors": ["Email or Password is not valid"]}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Recipes(APIView):
    def get(self, request, format=None):
        try:
            recipes = RecipeModel.objects.all()
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": serializer.errors, "Exception": e}, status=status.HTTP_400_BAD_REQUEST)


class CreateRecipes(APIView):
    def post(self, request, format=None):
        # user = UserModel.objects.get(username=request.data)
        recipe = request.data
        new_recipe = RecipeModel.objects.create(
            username=User.objects.get(id=recipe["username"]),
            productName=recipe["productName"],
            ingredients=recipe["ingredients"],
            makeRecipe=recipe["makeRecipe"],
            categories=recipe["categories"],
            image=recipe["image"]
        )
        new_recipe.save()
        serializer = RecipeSerializer(new_recipe)
        return Response(serializer.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'msg': 'Recipe Uploaded Successfully',
        #                      'status': 'success', 'candidate': serializer.data}, status=status.HTTP_201_CREATED)
        # return Response({'msg': 'Failed to upload', 'status': 'failed', 'candidate': serializer.errors},
        #                 status=status.HTTP_400_BAD_REQUEST)
