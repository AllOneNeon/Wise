from rest_framework import serializers

from .models import Post

class PostModelSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'