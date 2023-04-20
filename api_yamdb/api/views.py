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
from rest_framework import filters
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   DestroyModelMixin)

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
    TokenSerializer,
)
from .permissions import (
    AdminOnly,
    AdminOrReadOnly,
    IsAuthorOrModerOrAdmin,
    OnlyRegistered,
)
from .filters import TitleFilter
from .utils import check_email_exist, check_username_exist


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    username = request.data.get("username", None)
    email = request.data.get("email", None)

    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(username=username, email=email).exists():
        if check_email_exist(email) or check_username_exist(username):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
    user = User.objects.filter(email=email).first()

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Hello! Your confirmation code: ",
        confirmation_code,
        settings.EMAIL_AUTH_ADDR,
        [email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    username = request.data.get("username", None)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
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
    lookup_field = "slug"


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOrReadOnly,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (AdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GenreTitleSerializer
        return TitleSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    permission_classes = (AdminOnly,)
    http_method_names = ["get", "post", "patch", "delete"]

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
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("score", "author")

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id", None)
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        # сохранить имя автора, если правит не он
        review_id = self.kwargs.get("pk")
        author = Review.objects.get(pk=review_id).author
        serializer.save(author=author, title_id=title.id)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModerOrAdmin]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("review", "author")

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review_id=review.id)

    def perform_update(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        comment_id = self.kwargs.get("pk")
        author = Comment.objects.get(pk=comment_id).author
        serializer.save(author=author, review_id=review.id)
