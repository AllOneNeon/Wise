from core.models import Page, Tag, Post
from rest_framework import serializers
from user.models import User


class PageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages for any user."""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = (
            "id",
            "name",
            "uuid",
            "owner",
            "is_private",
            "is_blocked",
        )


class PageDetailSerializer(serializers.ModelSerializer):
    """Serializer for a simple page overview for any user."""

    owner = serializers.ReadOnlyField(source="owner.username")
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username", allow_null=True)

    class Meta:
        model = Page
        fields = ("name", "uuid", "description", "tags", "owner", "image_s3_path", "followers", "is_private")
        read_only_fields = ("name", "uuid", "description", "tags", "owner", "image_s3_path", "followers", "is_private")


class UserPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for users only"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username")
    follow_requests = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username")
    tags = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Tag.objects.all())
    is_private = serializers.BooleanField(required=True)

    class Meta:
        model = Page
        fields = (
            "id",
            "name",
            "uuid",
            "description",
            "tags",
            "owner",
            "image_s3_path",
            "followers",
            "is_private",
            "follow_requests",
        )
        read_only_fields = (
            "followers",
            "follow_requests",
        )


class AdminPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for admins only"""

    owner = serializers.ReadOnlyField(source="owner.username")
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username", allow_null=True)
    is_blocked = serializers.BooleanField()

    class Meta:
        model = Page
        fields = (
            "id",
            "name",
            "uuid",
            "description",
            "tags",
            "owner",
            "image_s3_path",
            "followers",
            "is_private",
            "unblock_date",
            "is_blocked",
        )
        read_only_fields = (
            "id",
            "name",
            "uuid",
            "description",
            "tags",
            "owner",
            "image_s3_path",
            "followers",
            "is_private",
        )


class ModerPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for moderators only"""

    owner = serializers.ReadOnlyField(source="owner.username")
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username", allow_null=True)
    unblock_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Page
        fields = (
            "id",
            "name",
            "uuid",
            "description",
            "tags",
            "owner",
            "image_s3_path",
            "followers",
            "is_private",
            "unblock_date",
            "is_blocked",
        )
        read_only_fields = (
            "id",
            "name",
            "uuid",
            "description",
            "tags",
            "owner",
            "image_s3_path",
            "followers",
            "is_private",
            "is_blocked",
        )


class FollowersListSerializer(serializers.ModelSerializer):
    """
    Serializer for list of users that following page
    Methods: list
    For any user
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "title",
            "email",
        )


class FollowerSerializer(serializers.ModelSerializer):
    """Serializer for accepting follow request"""

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email",)


class TagSerializer(serializers.ModelSerializer):
    """Tags serializer"""

    class Meta:
        model = Tag
        fields = ("id", "name")


class AddRemoveTagSerializer(serializers.ModelSerializer):
    """Tags serializer"""

    name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = Tag
        fields = ("name",)


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for list of post"""

    class Meta:
        model = Post
        fields = ("id", "content", "page", "reply_to", "created_at", "updated_at")


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate post"""

    page_name = serializers.SerializerMethodField()
    reply_to_content = serializers.SerializerMethodField(allow_null=True)
    likers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="username")

    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "page",
            "page_name",
            "reply_to",
            "reply_to_content",
            "created_at",
            "updated_at",
            "likers",
        )
        read_only_fields = ("page", "created_at", "updated_at", "likers")

    def get_page_name(self, post):
        return post.page.name

    def get_reply_to_content(self, post):
        return post.reply_to.content if post.reply_to else None


class HomeSerializer(serializers.ModelSerializer):
    """Serializer for feed with posts"""

    page = serializers.SlugRelatedField(slug_field="name", read_only=True)
    reply_to = serializers.SlugRelatedField(slug_field="content", read_only=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = Post
        fields = (
            "id",
            "page",
            "content",
            "reply_to",
            "created_at",
        )
