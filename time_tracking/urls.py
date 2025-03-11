from django.urls import path

from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from time_tracking.views import RegisterUserViewSet


# from time_tracker import views

router = SimpleRouter(trailing_slash=False)
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

router.register(r"register", RegisterUserViewSet, basename="register")


urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
