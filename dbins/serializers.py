from rest_framework import serializers
from .models import *

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
        fields = ('id', 'title', 'body', 'image','user_id', 'create_at',  )

class PostsDetailSerializers(serializers.ModelSerializer):
    detail = UsersSerializers(many=True, read_only=True)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'body', 'image' , 'user_id', 'create_at', 'detail', )


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'post', 'user', 'body', 'create_at',  )

class CommentsDetailSerializers(serializers.ModelSerializer):
    detail = UsersSerializers(many=True, read_only=True)
    class Meta:
        model = Comments
        fields = ('id', 'post', 'user', 'body', 'create_at',  'detail', )
