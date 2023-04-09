from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthor, IsModerator,
                             IsSuperUser)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleReadSerializer,
                             TitleWriteSerializer, UserAuthSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User


def send_confirmation_code(user):
    code = default_token_generator.make_token(user)
    user.confirmation_code = code
    user.save()

    subject = 'YaMDb. Код авторизации.'
    message = (f'Здравствуй, {user}! \n'
               f'Это твой код для авторизации {code}')
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    return send_mail(subject, message, from_email, to_email)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    """
    Мы не смогли провести рекомендуемый Вами рефакторинг, потому что
    это противоречит приложенным к проекту тестам. Все наши условия были
    написаны под запросы, в которых требовались определённые статус-коды.
    """
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    user = User.objects.filter(email=email)

    if user.exists():
        user = user.get(email=email)
        if user.username != request.data.get('username'):
            return Response(
                'Пользователь с таким логином уже существует.',
                status=status.HTTP_400_BAD_REQUEST
            )
        send_confirmation_code(user)
        return Response(
            'Код подтверждения отправлен повторно.',
            status=status.HTTP_200_OK
        )
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user, created = User.objects.get_or_create(username=username,
                                               email=email)
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_tokens_for_user(self, user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "acesses": str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticatе(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data["username"]
    conf_code = request.data["confirmation_code"]
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, conf_code):
        return Response(
            "неправильный confirmation_code",
            status=status.HTTP_400_BAD_REQUEST
        )
    tokens = get_tokens_for_user(user)
    return Response(tokens, status=status.HTTP_200_OK)


class CatGenViewSet(mixins.DestroyModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet,):
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CatGenViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CatGenViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthor
        | IsAdmin
        | IsModerator
    ]

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthor
        | IsAdmin
        | IsModerator
    ]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdmin | IsSuperUser]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me_page(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
