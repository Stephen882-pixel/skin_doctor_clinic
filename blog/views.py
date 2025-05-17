from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import BlogCategory, BlogPost, AboutUs, SocialMedia
from .serializers import (
    BlogCategorySerializer, BlogPostSerializer, 
    BlogPostDetailSerializer, AboutUsSerializer, 
    SocialMediaSerializer
)

class BlogCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for BlogCategory model"""
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class BlogPostViewSet(viewsets.ModelViewSet):
    """ViewSet for BlogPost model"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'summary']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        """
        Filter published posts for non-admin users
        """
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset
    
    def perform_create(self, serializer):
        """Set the author to the current user"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def publish(self, request, pk=None):
        """Publish a blog post"""
        post = self.get_object()
        post.is_published = True
        post.published_at = timezone.now()
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def unpublish(self, request, pk=None):
        """Unpublish a blog post"""
        post = self.get_object()
        post.is_published = False
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

class AboutUsViewSet(viewsets.ModelViewSet):
    """ViewSet for AboutUs model"""
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get the most recent AboutUs entry"""
        about = AboutUs.objects.order_by('-updated_at').first()
        if about:
            serializer = self.get_serializer(about)
            return Response(serializer.data)
        return Response({"detail": "No About Us content found."}, status=status.HTTP_404_NOT_FOUND)

class SocialMediaViewSet(viewsets.ModelViewSet):
    """ViewSet for SocialMedia model"""
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        """
        Filter only active social media for non-admin users
        """
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
    