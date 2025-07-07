from django.urls import path
from .views import ( RegisterView, LoginView, UserDetailView, UpdateUserView, ChangePasswordView, CheckUsernamesView )

urlpatterns = [
    path("auth/register/",    RegisterView.as_view()),
    path("auth/login/",        LoginView.as_view()),
    path("user/",         UserDetailView.as_view()), 
    path("user/update/",  UpdateUserView.as_view()),
    path("user/change-password/", ChangePasswordView.as_view()), 
    path("user/check-usernames/", CheckUsernamesView.as_view()),
]
