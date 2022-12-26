from rest_framework import status, viewsets, filters
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import  UserSerializer#, LoginSerializer, RegistrationSerializer,
from .models import User
from .permissions import *

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for all User objects"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    permissions_dict = {
        'partial_update': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
        'update': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
        'destroy': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
        'create': (permissions.AllowAny,),
        'list': (permissions.IsAuthenticated, IsAdmin,),
        'retrieve': (permissions.IsAuthenticated,),
    }

# переделать на viewset
# class RegistrationAPIView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class UserUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer

#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):
#         serializer_data = request.data
#         serializer = self.serializer_class(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class UserModelViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['username', 'email', ]

