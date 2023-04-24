import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from django.utils import timezone

from celery import app
from celery import shared_task
from .send_mail import send_mail

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)

@shared_task
def send_to_users(email, title, body):
    return send_mail(email, title, body) 

@shared_task
def send_to_user(user_id):
    user = User.objects.get(id=user_id)
    # to do что мнее надо

@shared_task
def send_mail_task():
    users = User.objects.filter(is_admin=True)

    for user in users:
        send_to_users.delay(user.email, 'Отчет за неделю', f'{user.first_name} Ты забыл оправить отчет {timezone.now()}')

        # send_to_user.delay(user.id)

    return 'Отчет просрочки для админов!'


# app.conf.beat_schedule = {
#     'add-every-5 second': {
#     'tasks': 'tasks.add',
#     'schedule': 5.0,
#     'args': (12, )
#     }
# }
# app.conf.timezone = 'Asia/Bishkek'