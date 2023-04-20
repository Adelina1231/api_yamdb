from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    signup,
    token,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UsersViewSet,
    ReviewViewSet,
    CommentViewSet
)

v1_router = DefaultRouter()
v1_router.register(r"categories", CategoryViewSet, basename="categories")
v1_router.register(r"genres", GenreViewSet, basename="genres")
v1_router.register(r"titles", TitleViewSet, basename="titles")
v1_router.register(r"users", UsersViewSet)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="review"
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment"
)

auth_patterns = [
    path("signup/", signup),
    path("token/", token),
]

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/auth/", include(auth_patterns)),
]
