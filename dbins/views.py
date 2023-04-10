import django_filters.rest_framework
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework import filters

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


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


class AuthTokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'name': user.first_name,
            }
        )
    permission_classes = [IsAuthenticatedOrReadOnly]
           
class AuthTokenViewOut(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        Token.objects.filter(user=user).delete()
        return Response({
            'message': 'Logged out successfully',
        })
    permission_classes = [IsAuthenticatedOrReadOnly]

class RegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializers
    
    
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'username': user.username,
                'token': token.key
            }
        )
    permission_classes = [IsAuthenticatedOrReadOnly]


class UsersList(ListAPIView):
    serializer_class = UsersSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('user_name', 'email')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Users.objects.all()
        return queryset
    
    

class UsersCreate(CreateAPIView):
    serializer_class = UsersSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Users.objects.all()
        return  queryset
    
    

class UsersRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializers
    queryset = Users.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]


class PostsList(ListAPIView):
    serializer_class = PostsSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('body', 'title')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Posts.objects.all()
        return queryset
    
    
class PostsCreate(CreateAPIView):
    serializer_class = PostsSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Posts.objects.all()
        return queryset
    
    
    
class PostsRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = PostsDetailSerializers
    queryset = Posts.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

   


class CommentsList(ListAPIView):
    serializer_class = CommentsDetailSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('body', )
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comments.objects.all()
        return queryset
    
class CommentsCreate(CreateAPIView):
    serializer_class = CommentsSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comments.objects.all()
        return queryset
    
    
    
class CommentsRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsDetailSerializers
    queryset = Comments.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]


