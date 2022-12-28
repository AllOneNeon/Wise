from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'', PageViewSet, basename='page')
router.register(r'', PostViewSet, basename='post')
urlpatterns = router.urls

