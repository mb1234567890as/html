from django.urls import path
from . import views 

urlpatterns = [
    path('users/', views.UsersList.as_view()),
    path('users/create/', views.UsersCreate.as_view()),
    path('users/rud/<int:pk>/', views.UsersRUD.as_view()),

    path('posts/', views.PostsList.as_view()),
    path('posts/create/', views.PostsCreate.as_view()),
    path('posts/rud/<int:pk>/', views.PostsRUD.as_view()),

    path('comment/', views.CommentsList.as_view()),
    path('comment/create/', views.CommentsCreate.as_view()),
    path('comment/rud/<int:pk>/', views.CommentsRUD.as_view()),

    path('', views.index, name='home'),
    path('users1/', views.users, name='users'),
    path('posts1/', views.post, name='post'),

]