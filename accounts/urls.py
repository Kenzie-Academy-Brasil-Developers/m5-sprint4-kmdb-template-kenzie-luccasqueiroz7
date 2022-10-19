from django.urls import path

from .views import UserDetailView, UserGetView, UserView, LoginView

urlpatterns = [
    path(
        "users/register/",
        UserView.as_view(),
    ),
    path(
        "users/login/",
        LoginView.as_view(),
    ),
    path(
        "users/",
        UserGetView.as_view(),
    ),
    path(
        "users/<int:user_id>/",
        UserDetailView.as_view(),
    ),
]
