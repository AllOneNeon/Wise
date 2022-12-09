from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import UserViewSet, LoginView

# router = DefaultRouter()
# router.register(r'', UserViewSet, basename='user')
# urlpatterns = router.urls

router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = [
    path("user/", include(router.urls)),
    path("registr/", UserViewSet.as_view({"post": "create"}), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]