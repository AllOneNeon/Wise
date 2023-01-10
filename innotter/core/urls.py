from django.urls import include, path
from core.views import (CurrentUserPagesViewSet, PagesViewSet, TagsViewSet,
                         HomeViewSet, PostsViewSet, UserPostsViewSet)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"pages", PagesViewSet, basename="pages")
router.register(r"my-pages", CurrentUserPagesViewSet, basename="my-pages")
router.register(r"tags", TagsViewSet, basename="tags")

router.register(r"posts", PostsViewSet, basename="posts")
router.register(r"my-posts", UserPostsViewSet, basename="my-posts")
router.register(r"home", HomeViewSet, basename="home")

urlpatterns = [
    path("", include(router.urls)),
]