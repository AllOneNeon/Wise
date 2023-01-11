from django.shortcuts import render

from rest_framework import viewsets, mixins

from .permissions import *
from .serializers import *


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = []
    permissions_dict = {
        'partial_update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'destroy': (permissions.IsAuthenticated, IsPageOwner),
        'create': (permissions.IsAuthenticated,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated, PageIsPublicOrOwner),
        'follow_requests': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'followers': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'follow': (permissions.IsAuthenticated, ),
        'posts': (permissions.IsAuthenticated, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin),
        'image': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin,)
    }

    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]
    
    def get_serializer_class(self):
        if self.action in ('followers', 'follow_requests', 'follow'):
            self.serializer_class = PageModelFollowRequestsSerializer
            return self.serializer_class
        if self.request.user.role in (User.Roles.ADMIN, User.Roles.MODERATOR):
            self.serializer_class = PageAdminOrModerSerializer
        else:
            self.serializer_class = PageUserSerializer
        return self.serializer_class


class TagViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, 
                mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                mixins.ListModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer
    permission_classes = ()
    permissions_dict = {
        'destroy': (permissions.IsAuthenticated, IsAdminOrModerator),
        'create': (permissions.IsAuthenticated, IsAdminOrModerator),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }

    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]