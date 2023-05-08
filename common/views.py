import logging

import django.conf
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constants import Constant
from common.models import User
from common.serializers import UserSerializer, UserLoginSerializer, UserPasswordSerializer
from common.utils import get_upload_file_path


def get_random_password():
    import random
    import string
    return ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 8))


class BaseError(ValidationError):
    def __init__(self, detail=None, code=None):
        super(BaseError, self).__init__(detail={'detail': detail})


class BasePagination(PageNumberPagination):
    """
        customer pagination
    """
    # default page size
    page_size = 10
    # page size param in page size
    page_size_query_param = 'page_size'
    # page param in api
    page_query_param = 'page'
    # max page size
    max_page_size = 100


class BaseViewSetMixin(object):
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def __init__(self, **kwargs):
        super(BaseViewSetMixin, self).__init__(**kwargs)
        self.filterset_fields = []
        self.init_filter_field()

    def init_filter_field(self):
        """
        Init filter field by the fields' intersection in model and serializer
        e.g. `book/?id=1&authors=2`
        :return:  None
        """
        serializer = self.get_serializer_class()
        if not hasattr(serializer, 'Meta'):
            return
        meta = serializer.Meta

        if not hasattr(meta, 'model'):
            return
        model = meta.model

        if not hasattr(meta, 'fields'):
            ser_fields = []
        else:
            ser_fields = meta.fields

        for field in ser_fields:
            if not hasattr(model, field):
                continue
            self.filterset_fields.append(field)

    def perform_update(self, serializer):
        user = self.fill_user(serializer, 'update')
        return serializer.save(**user)

    def perform_create(self, serializer):
        user = self.fill_user(serializer, 'create')
        return serializer.save(**user)

    @staticmethod
    def fill_user(serializer, mode):
        """
        before save, fill user info into para from session
        :param serializer: Model's serializer
        :param mode: create or update
        :return: None
        """
        request = serializer.context['request']

        user_id = request.user.id
        ret = {'modifier': user_id}

        if mode == 'create':
            ret['creator'] = user_id
        return ret

    def get_pk(self):
        if hasattr(self, 'kwargs'):
            return self.kwargs.get('pk')

    def is_reader(self):
        return isinstance(self.request.user, AnonymousUser) or not self.request.user.is_superuser


class BaseModelViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]



class UserLoginViewSet(GenericAPIView):
    # permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        # user_instance = User.objects.filter(username=username).first()
        # print(user_instance)
        # print(username, password)
        user = authenticate(username=username, password=password)
        # user_instance = ''
        print(user)
        if user is not None and user.is_active:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            ret = {'detail': 'Username or password is wrong'}
            return Response(ret, status=403)


class UserLogoutViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return Response({'detail': 'logout successful !'})


class PasswordUpdateViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        password = request.data.get('password', '')
        new_password = request.data.get('new_password', '')
        user = User.objects.get(id=user_id)
        if not user.check_password(password):
            ret = {'detail': 'old password is wrong !'}
            return Response(ret, status=403)

        user.set_password(new_password)
        user.save()
        return Response({
            'detail': 'password changed successful !'
        })

    def put(self, request, *args, **kwargs):
        """
        Parameter: username->user's username who forget old password
        """
        username = request.data.get('username', '')
        users = User.objects.filter(username=username)
        user: User = users[0] if users else None

        if user is not None and user.is_active:
            password = get_random_password()

            try:
                send_mail(subject="New password for Blog site",
                          message="Hi: Your new password is: \n{}".format(password),
                          from_email=django.conf.settings.EMAIL_HOST_USER,
                          recipient_list=[user.email],
                          fail_silently=False)
                user.password = make_password(password)
                user.save()
                return Response({
                    'detail': 'New password will send to your email!'
                })
            except Exception as e:
                print(e)
                return Response({
                    'detail': 'Send New email failed, Please check your email address!'
                })
        else:
            ret = {'detail': 'User does not exist(Account is incorrect !'}
            return Response(ret, status=403)


class ConstantViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPasswordSerializer
    queryset = QuerySet()

    def get(self, request, *args, **kwargs):
        ret = {}
        for key in dir(Constant):
            if not key.startswith("_"):
                ret[key] = getattr(Constant, key)
        return Response(ret)


class ImageUploadViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.method)
        try:
            if request.method == 'POST' and request.FILES:
                uploaded_file = request.FILES['file']

                full_file_path, file_path = get_upload_file_path(uploaded_file.name)
                self.handle_uploaded_file(uploaded_file, full_file_path)
                response = {
                    'url': file_path
                }
                return Response(response)

        except Exception as e:
            logging.getLogger('default').error(e, exc_info=True)
            raise BaseError(detail='Upload failed', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def handle_uploaded_file(f, file_path):
        destination = open(file_path, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
