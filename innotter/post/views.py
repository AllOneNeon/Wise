from django.shortcuts import render

from rest_framework import viewsets

from page.permissions import *
from .models import Post
from .serializers import PostModelSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostModelSerializer
    permission_classes = ()
    queryset = Post.objects.all()
    permissions_dict = {
        'list': (permissions.IsAuthenticated,),  
        'create': (permissions.IsAuthenticated,),  
        'partial_update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'destroy': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'retrieve': (permissions.IsAuthenticated, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin),
        'like': (permissions.IsAuthenticated, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin)
    }

    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]
