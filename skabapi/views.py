from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from skabapi.models import UserModel
from skabapi.serializers import UserRegisterSerializer
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



