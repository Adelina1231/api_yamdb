from django.urls import path, include

from .views import signup, token

auth_patterns = [
    path('signup/', signup),
    path('token/', token),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
]
