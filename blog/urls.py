from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogCategoryViewSet, BlogPostViewSet,
    AboutUsViewSet, SocialMediaViewSet
)

router = DefaultRouter()
router.register(r'categories', BlogCategoryViewSet)
router.register(r'posts', BlogPostViewSet)
router.register(r'about', AboutUsViewSet)
router.register(r'social', SocialMediaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
