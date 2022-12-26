from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserUpdateAPIView, UserModelViewSet
from rest_framework.routers import DefaultRouter


app_name = 'auth'
router = DefaultRouter()
router.register(r'', UserModelViewSet, basename='users')

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user-update/', UserUpdateAPIView.as_view()),
]

urlpatterns += router.urls