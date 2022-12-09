from rest_framework import serializers

from .models import *


class PageAdminOrModerSerializer(serializers.ModelSerializer):
    unblock_date = serializers.DateTimeField(default=None)

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'image', 'is_private', 'follow_requests', 'unblock_date')

        def update(self, instance, validated_data):
            if validated_data['unblock_date']:
                instance.unblock_date = validated_data['unblock_date']
                instance.save()
                validated_data.pop('unblock_date')
            return instance

class PageUserSerializer(serializers.ModelSerializer):
    unblock_date = serializers.DateTimeField(default=None)

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'followers',
                  'image', 'is_private', 'follow_requests', 'unblock_date')
        read_only_fields = ('unblock_date', 'owner')

class PageModelFollowRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('follow_requests', 'followers')

class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
