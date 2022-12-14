from rest_framework import serializers
from .models import Page, Post, Subscriber
from user.models import User


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_subscriber = serializers.SerializerMethodField()
    is_follow_requests = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'tag',
            'image',
            'is_private',
            'count_followers',
            'count_follow_requests',
            'unblock_date',
            'created_at',
            'updated_at',
            'posts',
            'is_subscriber',
            'is_follow_requests',
        ]

class PostSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'is_fan', 'total_likes',)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

class SubscriberUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = [
            'id',
            'subscriber',
            'follower',
            'follow_requests',
        ]