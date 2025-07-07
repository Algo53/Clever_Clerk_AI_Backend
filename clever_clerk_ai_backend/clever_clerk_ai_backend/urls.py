from django.contrib import admin
from api.views import RegisterView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/user/register/', RegisterView.as_view(), name="Register"),
    path('api/auth/token', TokenObtainPairView.as_view(), name="Get Token"),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name="Get Refresh Token"),
    path('api-auth/', include('rest_framework.urls')),

    path("api/", include("tasks.urls")),
    path("api/", include("api.urls")),
]
