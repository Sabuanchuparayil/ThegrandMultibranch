from django.db import models
from saleor_extensions.regions.models import Region
from saleor_extensions.branches.models import Branch


class Page(models.Model):
    """Static pages (About, Policies, etc.)"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    content_html = models.TextField(blank=True)  # Rich text content
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Visibility
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Region and branch
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pages'
    )
    branches = models.ManyToManyField(
        Branch,
        related_name='pages',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cms_pages'
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['title']
        indexes = [
            models.Index(fields=['slug', 'is_published', 'is_active']),
            models.Index(fields=['region', 'is_published']),
        ]
    
    def __str__(self):
        return self.title


class Banner(models.Model):
    """Banners for homepage and inner pages"""
    BANNER_TYPE_CHOICES = [
        ('HOME_HERO', 'Homepage Hero'),
        ('HOME_FEATURED', 'Homepage Featured'),
        ('INNER_PAGE', 'Inner Page Banner'),
        ('SIDEBAR', 'Sidebar Banner'),
        ('POPUP', 'Popup Banner'),
    ]
    
    name = models.CharField(max_length=200)
    banner_type = models.CharField(max_length=50, choices=BANNER_TYPE_CHOICES)
    
    # Content
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField()
    mobile_image_url = models.URLField(blank=True)
    
    # Link
    link_url = models.CharField(max_length=500, blank=True)
    link_text = models.CharField(max_length=100, blank=True)
    opens_in_new_tab = models.BooleanField(default=False)
    
    # Display settings
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Scheduling
    display_from = models.DateTimeField(null=True, blank=True)
    display_until = models.DateTimeField(null=True, blank=True)
    
    # Region and branch
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='banners'
    )
    branches = models.ManyToManyField(
        Branch,
        related_name='banners',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_banners'
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['banner_type', 'position', '-created_at']
        indexes = [
            models.Index(fields=['banner_type', 'is_active', 'position']),
            models.Index(fields=['region', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.banner_type})"


class Widget(models.Model):
    """Promotional widgets and content blocks"""
    WIDGET_TYPE_CHOICES = [
        ('FEATURED_PRODUCTS', 'Featured Products'),
        ('CATEGORY_SHOWCASE', 'Category Showcase'),
        ('TESTIMONIALS', 'Testimonials'),
        ('NEWSLETTER', 'Newsletter Signup'),
        ('SOCIAL_MEDIA', 'Social Media'),
        ('CUSTOM_HTML', 'Custom HTML'),
    ]
    
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPE_CHOICES)
    
    # Content
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    settings = models.JSONField(default=dict, blank=True)  # Widget-specific settings
    
    # Display
    position = models.CharField(max_length=100, blank=True)  # e.g., "homepage.top", "product.sidebar"
    position_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Region and branch
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='widgets'
    )
    branches = models.ManyToManyField(
        Branch,
        related_name='widgets',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_widgets'
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'
        ordering = ['position', 'position_order', '-created_at']
        indexes = [
            models.Index(fields=['widget_type', 'is_active']),
            models.Index(fields=['position', 'position_order']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.widget_type})"


class MediaFile(models.Model):
    """Media library for images and videos"""
    MEDIA_TYPE_CHOICES = [
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
    ]
    
    name = models.CharField(max_length=200)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    
    # File information
    file_url = models.URLField()
    thumbnail_url = models.URLField(blank=True)
    file_size = models.IntegerField(null=True, blank=True)  # in bytes
    mime_type = models.CharField(max_length=100, blank=True)
    
    # Image specific
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    
    # Metadata
    alt_text = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Organization
    folder = models.CharField(max_length=200, blank=True)  # Virtual folder organization
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'cms_media_files'
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Files'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['media_type', 'created_at']),
            models.Index(fields=['folder']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.media_type})"


class BranchBranding(models.Model):
    """Branch-specific branding settings"""
    branch = models.OneToOneField(
        Branch,
        on_delete=models.CASCADE,
        related_name='branding'
    )
    
    # Logo
    logo_url = models.URLField(blank=True)
    logo_light_url = models.URLField(blank=True)  # For dark backgrounds
    favicon_url = models.URLField(blank=True)
    
    # Colors
    primary_color = models.CharField(max_length=7, blank=True)  # Hex color
    secondary_color = models.CharField(max_length=7, blank=True)
    accent_color = models.CharField(max_length=7, blank=True)
    
    # Custom CSS
    custom_css = models.TextField(blank=True)
    
    # Footer
    footer_text = models.TextField(blank=True)
    footer_html = models.TextField(blank=True)
    
    # Contact information display
    show_address = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=True)
    show_email = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_branch_branding'
        verbose_name = 'Branch Branding'
        verbose_name_plural = 'Branch Branding'
    
    def __str__(self):
        return f"Branding for {self.branch.name}"

