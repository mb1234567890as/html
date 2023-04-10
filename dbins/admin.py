from django.contrib import admin
from .models import *

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'email', 'password', 'create_at', )
    list_filter = ('create_at',)
    search_fields = ('id', 'user_name', 'email',)
    list_display_links = ('id', 'user_name', 'email',)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'image', 'user_id', 'create_at', )
    list_filter = ('create_at',)
    search_fields = ('id', 'title', 'body', 'user_id',)
    list_display_links = ('id', 'title', 'body',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'body', 'create_at', )
    list_filter = ('create_at',)
    search_fields = ('id', 'body',)
    list_display_links = ('id', 'body', 'create_at',)


# admin.site.register(Users)
# admin.site.register(Posts)
# admin.site.register(Comments)