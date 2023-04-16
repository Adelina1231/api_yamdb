from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    signup,
    token,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UsersViewSet,
)

v1_router = DefaultRouter()
v1_router.register(r"categories", CategoryViewSet)
v1_router.register(r"genres", GenreViewSet)
v1_router.register(r"titles", TitleViewSet)
v1_router.register(r"users", UsersViewSet)

auth_patterns = [
    path("signup/", signup),
    path("token/", token),
]

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/auth/", include(auth_patterns)),
]
