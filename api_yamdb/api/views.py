from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import filters, permissions
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)

from users.models import User
from reviews.models import Category, Comment, Genre, Review, Title
from users.serializers import UserSerializer
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    GenreTitleSerializer,
    TokenSerializer
)
from .permissions import (
    AdminOnly,
    AdminOrReadOnly,
    IsAuthorOrModerOrAdmin,
    OnlyRegistered,
)
from .filters import TitleFilter


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    username = request.data["username"]
    email = request.data["email"]
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    print(username, email)
    if not User.objects.filter(
        username=username, email=email
    ):
        serializer.save()
    user = User.objects.get(
        username=username, email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Hello! Your confirmation code: ",
        confirmation_code,
        settings.EMAIL_AUTH_NAME,
        [email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=request.data["username"])
    confirmation_code = request.data["confirmation_code"]
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        response = {"token": token}
        return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateListDestroyViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrReadOnly,)
    search_fields = ("name",)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrReadOnly,)
    search_fields = ("name",)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (AdminOrReadOnly,)
    filterset_class = TitleFilter

    # def get_queryset(self):
    #     queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    #     return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GenreTitleSerializer
        return TitleSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    permission_classes = (AdminOnly,)

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=(OnlyRegistered, IsAuthenticated),
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if "role" in request.data:
                if user.role != User.USER:
                    serializer.save()
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModerOrAdmin
    )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ("score", "author")

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModerOrAdmin]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ("review", "author")

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)
