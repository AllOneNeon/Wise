from .views import PageModelViewSet, PostLikeModelViewSet, PostModelViewSet, SubscriberModelViewSet
from rest_framework.routers import DefaultRouter


app_name = 'core'

router = DefaultRouter()
router.register(r'', PageModelViewSet, basename='pages')
router.register(r'posts', PostModelViewSet, basename='posts')
router.register(r'likes', PostLikeModelViewSet, basename='likes')
router.register(r'', SubscriberModelViewSet, basename='subscribers')
urlpatterns = router.urls
