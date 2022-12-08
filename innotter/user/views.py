from django.shortcuts import render
from requests import Response
from .serializers import UserSerializer
from rest_framework import  viewsets

from .permissions import *
from .serializers import UserSerializer

# class Register(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

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