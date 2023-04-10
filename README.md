Как определяется аутентификация
Схемы аутентификации всегда определяются как список классов. DRF попытается выполнить аутентификацию с каждым классом в списке, и установит request.user и request.auth, используя возвращаемое значение первого класса, который успешно аутентифицируется.
Если ни один класс не выполнит аутентификацию, request.user будет установлен в экземпляр django.contrib.auth.models.AnonymousUser, а request.auth будет установлен в None.
Значение request.user и request.auth для неаутентифицированных запросов можно изменить с помощью параметров UNAUTHENTICATED_USER и UNAUTHENTICATED_TOKEN.
Установка схемы аутентификации
Схемы аутентификации по умолчанию можно установить глобально, используя настройку DEFAULT_AUTHENTICATION_CLASSES. Например.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
Вы также можете установить схему аутентификации отдельно для каждого представления или каждого набора представлений, используя представления на основе класса APIView.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
Или, если вы используете декоратор @api_view с представлениями, основанными на функциях.
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)
Неавторизованные и запрещенные ответы
Когда неаутентифицированному запросу отказано в разрешении, существует два различных кода ошибок, которые могут быть уместны.
HTTP 401 Unauthorized
HTTP 403 Permission Denied
Ответы HTTP 401 всегда должны содержать заголовок WWW-Authenticate, который указывает клиенту, как пройти аутентификацию. Ответы HTTP 403 не включают заголовок WWW-Authenticate.
Тип ответа, который будет использоваться, зависит от схемы аутентификации. Хотя может использоваться несколько схем аутентификации, для определения типа ответа может использоваться только одна схема. Первый класс аутентификации, установленный для представления, используется при определении типа ответа.
Обратите внимание, что когда запрос может успешно пройти аутентификацию, но при этом получить отказ в разрешении на выполнение запроса, в этом случае всегда будет использоваться ответ 403 Permission Denied, независимо от схемы аутентификации.
Специфическая конфигурация Apache mod_wsgi
Обратите внимание, что при развертывании на Apache using mod_wsgi заголовок авторизации по умолчанию не передается приложению WSGI, так как предполагается, что аутентификация будет обрабатываться Apache, а не на уровне приложения.
Если вы развертываете на Apache и используете любую аутентификацию, не основанную на сеансах, вам необходимо явно настроить mod_wsgi для передачи необходимых заголовков приложению. Это можно сделать, указав директиву WSGIPassAuthorization в соответствующем контексте и установив ее в значение 'On'.
# this can go in either server config, virtual host, directory or .htaccess
WSGIPassAuthorization On

API Reference
BasicAuthentication
Эта схема аутентификации использует HTTP Basic Authentication, подписанную именем пользователя и паролем. Базовая аутентификация обычно подходит только для тестирования.
При успешной аутентификации BasicAuthentication предоставляет следующие учетные данные.
request.user будет экземпляром Django User.
request.auth будет None.
Ответы без аутентификации, которым отказано в разрешении, приведут к ответу HTTP 401 Unauthorized с соответствующим заголовком WWW-Authenticate. Например:
WWW-Authenticate: Basic realm="api"
Примечание: Если вы используете BasicAuthentication в реальном проекте, вы должны убедиться, что ваш API доступен только через https. Вы также должны убедиться, что клиенты вашего API всегда будут повторно запрашивать имя пользователя и пароль при входе в систему и никогда не будут сохранять эти данные в постоянном хранилище.
TokenAuthentication

Примечание: Аутентификация с помощью токенов, предоставляемая DRF, является довольно простой реализацией.
Для реализации, которая позволяет использовать более одного токена на пользователя, имеет некоторые более жесткие детали реализации безопасности и поддерживает истечение срока действия токена, пожалуйста, обратитесь к стороннему пакету Django REST Knox.

Эта схема аутентификации использует простую схему аутентификации HTTP на основе токенов. Токен-аутентификация подходит для клиент-серверных установок, таких как собственные настольные и мобильные клиенты.
Для использования схемы TokenAuthentication вам необходимо настроить классы аутентификации, чтобы включить TokenAuthentication, и дополнительно включить rest_framework.authtoken в настройку INSTALLED_APPS:
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
Обязательно запустите manage.py migrate после изменения настроек.
Приложение rest_framework.authtoken обеспечивает миграцию баз данных Django.
Вам также потребуется создать токены для своих пользователей.
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
Для аутентификации клиентов ключ токена должен быть включен в HTTP-заголовок Authorization. Ключ должен иметь префикс в виде строкового литерала "Token", с пробелами, разделяющими эти две строки. Например:
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
*Если вы хотите использовать другое ключевое слово в заголовке, например Bearer, просто создайте подкласс TokenAuthentication и установите переменную класса keyword.
При успешной аутентификации TokenAuthentication предоставляет следующие учетные данные.
request.user будет экземпляром Django User.
request.auth будет экземпляром rest_framework.authtoken.models.Token.
Ответы без аутентификации, которым отказано в разрешении, приведут к ответу HTTP 401 Unauthorized с соответствующим заголовком WWW-Authenticate. Например:
WWW-Authenticate: Token
Инструмент командной строки curl может быть полезен для тестирования API с аутентификацией токенов. Например:
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

Примечание: Если вы используете TokenAuthentication в реальном проекте, вы должны убедиться, что ваш API доступен только через https.

Генерация токенов
С помощью сигналов
Если вы хотите, чтобы у каждого пользователя был автоматически сгенерированный Token, вы можете просто перехватить сигнал post_save пользователя.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
Обратите внимание, что вам нужно убедиться, что вы поместили этот фрагмент кода в установленный модуль models.py или в другое место, которое будет импортироваться Django при запуске.
Если вы уже создали несколько пользователей, вы можете сгенерировать токены для всех существующих пользователей следующим образом:
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
Посредством конечной точки API
При использовании TokenAuthentication вы можете захотеть предоставить клиентам механизм для получения токена, заданного именем пользователя и паролем. DRF предоставляет встроенное представление для обеспечения такого поведения. Чтобы использовать его, добавьте представление obtain_auth_token в URLconf:
from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
Обратите внимание, что URL часть шаблона может быть любой, которую вы хотите использовать.
Представление obtain_auth_token вернет ответ в формате JSON, если действительные поля username и password будут отправлены в представление с помощью данных формы или JSON:
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
Обратите внимание, что представление по умолчанию obtain_auth_token явно использует JSON запросы и ответы, а не использует классы рендерера и парсера по умолчанию в ваших настройках.
По умолчанию к представлению obtain_auth_token не применяется никаких разрешений или дросселирования. Если вы хотите применить дросселирование, вам нужно переопределить класс представления и включить их с помощью атрибута throttle_classes.
Если вам нужна настраиваемая версия представления obtain_auth_token, вы можете сделать это, создав подкласс класса представления ObtainAuthToken и используя его в url conf.
Например, вы можете возвращать дополнительную информацию о пользователе помимо значения token:
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
И в вашем urls.py:
urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]
С администратором Django
Токены также можно создавать вручную через интерфейс администратора. В случае, если вы используете большую базу пользователей, мы рекомендуем вам пропатчить класс TokenAdmin, чтобы настроить его под свои нужды, в частности, объявив поле user как raw_field.
ваше_приложение/admin.py:
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
Использование команды Django manage.py
Начиная с версии 3.6.4 можно сгенерировать пользовательский токен с помощью следующей команды:
./manage.py drf_create_token <username>
эта команда вернет API-токен для данного пользователя, создав его, если он не существует:
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
Если вы хотите восстановить токен (например, если он был скомпрометирован или произошла утечка), вы можете передать дополнительный параметр:
./manage.py drf_create_token -r <username>
SessionAuthentication
Эта схема аутентификации использует бэкенд сессий Django по умолчанию для аутентификации. Сеансовая аутентификация подходит для клиентов AJAX, которые работают в том же сеансовом контексте, что и ваш сайт.
При успешной аутентификации SessionAuthentication предоставляет следующие учетные данные.
request.user будет экземпляром Django User.
request.auth будет None.
Ответы без аутентификации, которым отказано в разрешении, приведут к ответу HTTP 403 Forbidden.
Если вы используете API в стиле AJAX с SessionAuthentication, вам нужно убедиться, что вы включаете действительный CSRF токен для любых "небезопасных" вызовов HTTP методов, таких как PUT, PATCH, POST или DELETE запросы. Более подробную информацию смотрите в Django CSRF documentation.
Предупреждение: Всегда используйте стандартное представление входа Django при создании страниц входа. Это обеспечит надлежащую защиту ваших представлений входа.
Проверка CSRF в DRF работает несколько иначе, чем в стандартном Django, из-за необходимости поддерживать как сеансовую, так и несеансовую аутентификацию для одних и тех же представлений. Это означает, что только аутентифицированные запросы требуют CSRF-токенов, а анонимные запросы могут быть отправлены без CSRF-токенов. Такое поведение не подходит для представлений входа в систему, к которым всегда должна применяться проверка CSRF.
RemoteUserAuthentication
Эта схема аутентификации позволяет делегировать аутентификацию вашему веб-серверу, который устанавливает переменную окружения REMOTE_USER.
Чтобы использовать его, вы должны иметь django.contrib.auth.backends.RemoteUserBackend (или подкласс) в настройках AUTHENTICATION_BACKENDS. По умолчанию RemoteUserBackend создает объекты User для имен пользователей, которые еще не существуют. Чтобы изменить это и другое поведение, обратитесь к документации Django.
При успешной аутентификации RemoteUserAuthentication предоставляет следующие учетные данные:
request.user будет экземпляром Django User.
request.auth будет None.
Обратитесь к документации вашего веб-сервера за информацией о настройке метода аутентификации, например:
Apache Authentication How-To
NGINX (ограничение доступа)
Пользовательская аутентификация
Чтобы реализовать собственную схему аутентификации, создайте подкласс BaseAuthentication и переопределите метод .authenticate(self, request). Метод должен возвращать кортеж (user, auth), если аутентификация прошла успешно, или None в противном случае.
В некоторых случаях вместо возврата None вы можете захотеть вызвать исключение AuthenticationFailed из метода .authenticate().
Как правило, вам следует придерживаться следующего подхода:
Если попытка аутентификации не была предпринята, верните None. Любые другие схемы аутентификации, которые также используются, будут проверены.
Если попытка аутентификации была предпринята, но не удалась, вызовите исключение AuthenticationFailed. Ответ об ошибке будет возвращен немедленно, независимо от любых проверок разрешений и без проверки других схем аутентификации.
Вы можете также переопределить метод .authenticate_header(self, request). Если он реализован, он должен возвращать строку, которая будет использоваться в качестве значения заголовка WWW-Authenticate в ответе HTTP 401 Unauthorized.
Если метод .authenticate_header() не переопределен, схема аутентификации будет возвращать ответы HTTP 403 Forbidden, когда неаутентифицированному запросу будет отказано в доступе.

Примечание: Когда ваш пользовательский аутентификатор вызывается свойствами .user или .auth объекта запроса, вы можете увидеть, как AttributeError повторно выбрасывается, как WrappedAttributeError. Это необходимо для того, чтобы исходное исключение не было подавлено доступом к внешнему свойству. Python не распознает, что AttributeError исходит от вашего пользовательского аутентификатора, и вместо этого будет считать, что объект запроса не имеет свойства .user или .auth. Эти ошибки должны быть исправлены или иным образом обработаны вашим аутентификатором.

Пример
Следующий пример аутентифицирует любой входящий запрос как пользователя, указанного в имени пользователя в пользовательском заголовке запроса под названием 'X-USERNAME'.
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)