import django_filters.rest_framework
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from rest_framework import filters, status, viewsets

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .forms import *

#celery
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts
from celery import shared_task


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
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
           
class AuthTokenViewOut(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        Token.objects.filter(user=user).delete()
        return Response({
            'message': 'Logged out successfully',
        })
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

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
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class UsersList(ListAPIView):
    serializer_class = UsersSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('user_name', 'email')
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Users.objects.all()
        return queryset
    
    

class UsersCreate(CreateAPIView):
    serializer_class = UsersSerializers
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Users.objects.all()
        return  queryset
    
    

class UsersRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializers
    queryset = Users.objects.all()

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class PostsList(ListAPIView):
    serializer_class = PostsSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('body', 'title')
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Posts.objects.all()
        return queryset
    
    
class PostsCreate(CreateAPIView):
    serializer_class = PostsSerializers
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Posts.objects.all()
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    
class PostsRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = PostsDetailSerializers
    queryset = Posts.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def update(self, request, *args, **kwargs):
        # берем запись
        instance = self.get_object()
        # проверяем, что пользователь является создателем записи
        if instance.seller == request.user:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'Вы не владелец данной записи'})


class CommentsList(ListAPIView):
    serializer_class = CommentsDetailSerializers
    filter_backends = {filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend}
    filterset_fields = ('create_at',)
    search_fields = ('body', )
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Comments.objects.all()
        return queryset
    
class CommentsCreate(CreateAPIView):
    serializer_class = CommentsSerializers
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Comments.objects.all()
        return queryset
    
    
    
class CommentsRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsDetailSerializers
    queryset = Comments.objects.all()

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]



class LikeViewSet(viewsets.ModelViewSet):
     queryset = Like.objects.all()
     serializer_class = LikeSerializer
     permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
     search_fields = ['create_at']
     ordering_fields = ['create_at']

     def update(self, request, *args, **kwargs):
         return super().update(request, *args, **kwargs)

     def partial_update(self, request, *args, **kwargs):
         return super().partial_update(request, *args, **kwargs)
     


class UserTemplateView(ListView):
    template_name = 'main/users.html'
    model = Users

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['users'] = self.model.objects.all()
         return context

class UserTemplateDetailView(DetailView):
    template_name = 'main/users_detail.html'
    model = Users

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['user'] = self.model.objects.get(pk=self.kwargs['pk'])
         return context
    
class UserTemplateCreateView(CreateView):
    template_name = 'main/users_create.html'
    form_class = UserForm
    success_url = '/user_detail/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

     # redirect to movie_detail
    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.pk})
    
class GenerateRandomUserView(FormView):
    template_name = 'main/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('user_list')
