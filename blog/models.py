from django.db import models
from accounts.models import User

# Create your models here.

class BlogCategory(models.Model):
    """MOdel for blog category"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name
    

class BlogPost(models.Model):
    """Model for blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    summary = models.TextField(blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    featured_image = models.ImageField(upload_to='blog/',blank=True,null=True)
    categories = models.ManyToManyField(BlogCategory,related_name='posts')
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']


    def __str__(self):
        return self.title
    
class AboutUs(models.Model):
    """Model for About Us page content"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='about_us/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About Us"
    
    def __str__(self):
        return self.title


class SocialMedia(models.Model):
    """Model for social media links"""
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('pinterest', 'Pinterest'),
        ('other', 'Other'),
    )
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Social Media"
    
    def __str__(self):
        return self.get_platform_display()