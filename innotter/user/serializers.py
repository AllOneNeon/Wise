from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
         'email', 'image_s3_path', 'role', 'title', 'is_blocked']
        kwargss = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        user = User(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            username = validated_data['username'],
            role = 'user',
            title = validated_data['title'],
            is_blocked = False,
            image_s3_path = validated_data['image_s3_path']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        



