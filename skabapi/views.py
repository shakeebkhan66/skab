from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from skabapi.models import UserModel, RecipeModel
from skabapi.serializers import UserRegisterSerializer, RecipeSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                # 'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    # permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


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
            username=UserModel.objects.get(id=recipe["username"]),
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
