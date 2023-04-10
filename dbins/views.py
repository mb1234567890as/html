import django_filters.rest_framework
from django.shortcuts import render
from .models import *
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework import filters

def index(request):
    return render(request, 'main/index.html')

def users(request):
    users = Users.objects.all()
    context = {
        'users': users
    }
    return render(request, 'main/users.html', context)

def post(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'main/posts.html', context)


class UsersList(ListAPIView):
    serializer_class = UsersSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('user_name', 'email')
    

    def get_queryset(self):
        queryset = Users.objects.all()
        return queryset

class UsersCreate(CreateAPIView):
    serializer_class = UsersSerializers

    def get_queryset(self):
        queryset = Users.objects.all()
        return  queryset

class UsersRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializers
    queryset = Users.objects.all()


class PostsList(ListAPIView):
    serializer_class = PostsSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('body', 'title')

    def get_queryset(self):
        queryset = Posts.objects.all()
        return queryset
    
class PostsCreate(CreateAPIView):
    serializer_class = PostsSerializers

    def get_queryset(self):
        queryset = Posts.objects.all()
        return queryset
    
class PostsRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = PostsDetailSerializers
    queryset = Posts.objects.all()


class CommentsList(ListAPIView):
    serializer_class = CommentsDetailSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('body', )

    def get_queryset(self):
        queryset = Comments.objects.all()
        return queryset
    
class CommentsCreate(CreateAPIView):
    serializer_class = CommentsSerializers

    def get_queryset(self):
        queryset = Comments.objects.all()
        return queryset
    
class CommentsRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsDetailSerializers
    queryset = Comments.objects.all()


