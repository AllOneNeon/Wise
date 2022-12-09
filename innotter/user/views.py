from requests import Response

from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf

from rest_framework import  viewsets, status
from rest_framework.views import APIView

from .utilite import get_token
from .permissions import *
from user.serializers import UserSerializer, LoginSerializer

# class Register(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        response = Response()

        if not serializer.data:
            return Response({"data": "Bad request."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=serializer.data["username"], password=serializer.data["password"])

        if user is not None:
            data = get_token(user)
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=data["access"],
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            csrf.get_token(request)
            response.data = {"Success": "Login successfully", "data": data}

            return response
        else:
            return Response({"data": "Invalid credentials."}, status=status.HTTP_404_NOT_FOUND)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    permissions_dict = {
        'partial_update': (permissions.IsAuthenticated),
        'update': (permissions.IsAuthenticated),
        'destroy': (permissions.IsAuthenticated),
        'create': (permissions.AllowAny,),
        'list': (permissions.IsAuthenticated, IsAdmin,),
        'retrieve': (permissions.IsAuthenticated,),
        'image': (permissions.IsAuthenticated)
    }

    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]