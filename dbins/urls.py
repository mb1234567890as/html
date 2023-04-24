from django.urls import path, include
from . import views 

from django.views.generic import TemplateView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'like', views.LikeViewSet, basename='like')


urlpatterns = [

    path('api-token-auth',views.AuthTokenView.as_view(), name='api_token_auth'),
    path('api-token-authout/', views.AuthTokenViewOut.as_view(), name='api_auth'),

    path('registration/', views.RegistrationView.as_view(), name='registration'),

    path('users/', views.UsersList.as_view()),
    path('users/create/', views.UsersCreate.as_view()),
    path('users/rud/<int:pk>/', views.UsersRUD.as_view()),

    path('posts/', views.PostsList.as_view()),
    path('posts/create/', views.PostsCreate.as_view()),
    path('posts/rud/<int:pk>/', views.PostsRUD.as_view()),

    path('comment/', views.CommentsList.as_view()),
    path('comment/create/', views.CommentsCreate.as_view()),
    path('comment/rud/<int:pk>/', views.CommentsRUD.as_view()),

    path('api/', include(router.urls)),


    
    path('users1/', views.users, name='users'),
    path('posts1/', views.post, name='post'),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('user_template/', views.UserTemplateView.as_view(), name='user_template'),
    path('user_detail/<int:pk>/', views.UserTemplateDetailView.as_view(), name='user_detail'),
    path('user_create/', views.UserTemplateCreateView.as_view(), name='user_create'),

    path('user_list/', views.GenerateRandomUserView.as_view(), name='user_list'),

]

