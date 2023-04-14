
from rest_framework import serializers
from .models import *

class UserRegistrationSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'user_name', 'email', 'password', 'create_at', )

class UserDetailSerializers(serializers.ModelSerializer):
    detail = UsersSerializers(many=True, read_only=True)
    class Meta:
        model = Users
        fields = ('id', 'user_name', 'email', 'password', 'create_at', 'detail', )


class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('id', 'title', 'body', 'image', 'user_id', 'create_at', 'likes' )

    

class PostsDetailSerializers(serializers.ModelSerializer):
    detail = UsersSerializers(many=True, read_only=True)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'body', 'image', 'user_id', 'create_at', 'detail', 'likes' )

    


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'post', 'user', 'body', 'create_at',  )

class CommentsDetailSerializers(serializers.ModelSerializer):
    detail = UsersSerializers(many=True, read_only=True)
    class Meta:
        model = Comments
        fields = ('id', 'post', 'user', 'body', 'create_at',  'detail', )

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('id',)

class CommentsDetailSerializers(serializers.ModelSerializer):
    detail = UsersSerializers(many=True, read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('id',)
