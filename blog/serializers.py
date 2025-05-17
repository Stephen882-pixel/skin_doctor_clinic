from rest_framework import serializers
from .models import BlogCategory,BlogPost,AboutUs,SocialMedia
from accounts.serializers import UserSerializer

class  BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for BlogCategory model"""
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description']

class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""
    author_name = serializers.SerializerMethodField()
    categories_names = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'summary', 'content', 'author', 'author_name',
                  'featured_image', 'categories', 'categories_names', 'is_published',
                  'published_at', 'created_at', 'updated_at']
        extra_kwargs = {
            'author': {'read_only': True},
        }
    
    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
    
    def get_categories_names(self, obj):
        return [category.name for category in obj.categories.all()]


class BlogPostDetailSerializer(BlogPostSerializer):
    """Detailed serializer for BlogPost model"""
    author = UserSerializer(read_only=True)
    categories = BlogCategorySerializer(many=True, read_only=True)
    
    class Meta(BlogPostSerializer.Meta):
        fields = BlogPostSerializer.Meta.fields


class AboutUsSerializer(serializers.ModelSerializer):
    """Serializer for AboutUs model"""
    class Meta:
        model = AboutUs
        fields = ['id', 'title', 'content', 'mission', 'vision', 'image', 'updated_at']


class SocialMediaSerializer(serializers.ModelSerializer):
    """Serializer for SocialMedia model"""
    platform_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialMedia
        fields = ['id', 'platform', 'platform_name', 'url', 'icon', 'is_active']
    
    def get_platform_name(self, obj):
        return obj.get_platform_display()