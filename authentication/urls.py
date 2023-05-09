from django.contrib import admin
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/login/', TokenCreateView.as_view(), name='token_create'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='token_destroy'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]