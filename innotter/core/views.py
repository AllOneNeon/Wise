from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PageSerializer, PostSerializer, SubscriberSerializer
from .models import Like, Page, Post, Subscriber
from rest_framework.decorators import action
from user.models import User
from rest_framework.response import Response
import requests
from django.db.models import Q


class PageModelViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Page.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'id', 'tag__name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Post.objects.all().order_by('-updated_at')
        elif user.is_authenticated:
            owner_pages = Page.objects.filter(owner=user)
            permissions_pages = Page.objects.filter()
            return Post.objects.filter(
                page__in=permissions_pages | owner_pages
            ).order_by('-updated_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

class PostLikeModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        like_posts = Like.objects.filter(user=user)
        return Post.objects.filter(like_post__in=like_posts)


class SubscriberModelViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Subscriber.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Subscriber.objects.all()
        elif user.is_authenticated:
            pages = Page.objects.filter(owner=user)
            for page in pages:
                return Subscriber.objects.filter(
                    Q(follower=page) | Q(follow_requests=page)
                )

    @action(detail=True, methods=['POST'])
    def confirm(self, request, pk=None):
        subscribers = self.get_object()
        if request.user.is_authenticated and Page.objects.filter(owner=request.user):
            one_user = User.objects.get(pk=subscribers.subscriber.id)
            Subscriber.objects.filter(subscriber=one_user).update(follower=subscribers.follow_requests, follow_requests=None)
        return Response()

    @action(detail=True, methods=['POST'])
    def unconfirm(self, request, pk=None):
        subscribers = self.get_object()
        if request.user.is_authenticated and Page.objects.filter(owner=request.user):
            one_user = User.objects.get(pk=subscribers.subscriber.id)
            Subscriber.objects.filter(
                subscriber=one_user,
                follow_requests=subscribers.follow_requests
            ).delete()
        return Response()