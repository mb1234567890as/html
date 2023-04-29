from django.contrib.auth.models import User
from django.db import models


class Users(models.Model):
    user_name = models.CharField(max_length=100, verbose_name="Имя аккаунта")
    email = models.EmailField(max_length=100, verbose_name="Почта")
    password = models.CharField(max_length=50, verbose_name="Пороль")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")

    def __str__(self):
        return str(self.user_name)

    class Meta:
        verbose_name = "Ползователь"
        verbose_name_plural = "Ползователи"
        ordering = ["user_name"]


class Posts(models.Model):
    title = models.CharField(max_length=100, verbose_name="Загаловок")
    body = models.TextField(max_length=100, verbose_name="Пост")
    image = models.ImageField(upload_to="photos/", verbose_name="Фото")
    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name="id пользователя"
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователи",
        related_name="seller",
    )
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True, verbose_name="Лайки"
    )

    def __str__(self):
        return str(self.body)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["create_at"]


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name="Пост")
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name="Ползователь"
    )
    body = models.TextField(max_length=100, verbose_name="Коментарии")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")

    def __str__(self):
        return str(self.body)

    class Meta:
        verbose_name = "Коментария"
        verbose_name_plural = "Коментарии"
        ordering = ["create_at"]


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name="Пост")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user} liked {self.post}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ("user", "post")


# class Like(models.Model):
#     post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Пост')
#     user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
#     create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


# class Post(models.Model):
#     likes = models.ManyToManyField(Like, through='PostLike')


# class PostLike(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
#     like = models.ForeignKey(Like, on_delete=models.CASCADE, verbose_name='Лайк')
