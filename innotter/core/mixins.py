from rest_framework.decorators import action
from rest_framework.response import Response
from . import utilites
from .serializers import LikeSerializer, SubscriberUserSerializer


class LikedMixin:
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        obj = self.get_object()
        utilites.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        obj = self.get_object()
        utilites.remove_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['GET'])
    def fans(self, request, pk=None):
        obj = self.get_object()
        fans = utilites.get_fans(obj)
        serializer = LikeSerializer(fans, many=True)
        return Response(serializer.data)


class SubscribersMixin:
    @action(detail=True, methods=['POST'])
    def subscribes(self, request, pk=None):
        obj = self.get_object()
        utilites.add_subscription(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST'])
    def unsubscribes(self, request, pk=None):
        obj = self.get_object()
        utilites.remove_subscription(obj, request.user)
        return Response()

    @action(detail=True, methods=['GET'])
    def follow_requests(self, request, pk=None):
        obj = self.get_object()
        follow_requests = utilites.get_follow_requests(obj)
        serializer = SubscriberUserSerializer(follow_requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def followers(self, request, pk=None):
        obj = self.get_object()
        subscribers = utilites.get_subscribers(obj)
        serializer = SubscriberUserSerializer(subscribers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def confirm(self, request, pk=None):
        obj = self.get_object()
        utilites.confirm_subscription_everybody(obj, request.user)
        return Response()

