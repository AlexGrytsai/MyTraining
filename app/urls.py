from django.urls import path, include

from app.views import IndexView, RegisterUserView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "registration/", RegisterUserView.as_view(), name="user-registration"
    ),
    path("", IndexView.as_view(), name="index"),
]

app_name = "app"
