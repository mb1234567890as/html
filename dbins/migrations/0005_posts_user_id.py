# Generated by Django 3.2 on 2023-04-11 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbins', '0004_remove_posts_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dbins.users', verbose_name='id пользователя'),
            preserve_default=False,
        ),
    ]
