from django.contrib import admin
from .models import Page, Banner, Widget, MediaFile, BranchBranding


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'region', 'is_published', 'is_active',
        'published_at', 'created_at'
    )
    list_filter = ('is_published', 'is_active', 'region', 'created_at')
    search_fields = ('title', 'slug', 'content', 'meta_title')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    filter_horizontal = ['branches']
    
    fieldsets = (
        ('Page Information', {
            'fields': ('title', 'slug', 'content', 'content_html', 'is_published', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Visibility', {
            'fields': ('region', 'branches')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at')
        }),
    )


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'banner_type', 'title', 'region', 'position',
        'is_active', 'display_from', 'display_until', 'created_at'
    )
    list_filter = ('banner_type', 'is_active', 'region', 'created_at')
    search_fields = ('name', 'title', 'subtitle', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ['branches']
    
    fieldsets = (
        ('Banner Information', {
            'fields': ('name', 'banner_type', 'position', 'is_active')
        }),
        ('Content', {
            'fields': ('title', 'subtitle', 'description', 'image_url', 'mobile_image_url')
        }),
        ('Link', {
            'fields': ('link_url', 'link_text', 'opens_in_new_tab')
        }),
        ('Scheduling', {
            'fields': ('display_from', 'display_until')
        }),
        ('Visibility', {
            'fields': ('region', 'branches')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'widget_type', 'title', 'position', 'position_order',
        'region', 'is_active', 'created_at'
    )
    list_filter = ('widget_type', 'is_active', 'region', 'position')
    search_fields = ('name', 'title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ['branches']
    
    fieldsets = (
        ('Widget Information', {
            'fields': ('name', 'widget_type', 'is_active')
        }),
        ('Content', {
            'fields': ('title', 'content', 'content_html', 'settings')
        }),
        ('Display', {
            'fields': ('position', 'position_order')
        }),
        ('Visibility', {
            'fields': ('region', 'branches')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'media_type', 'folder', 'file_size', 'width', 'height',
        'created_at', 'uploaded_by'
    )
    list_filter = ('media_type', 'folder', 'created_at')
    search_fields = ('name', 'alt_text', 'description', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('File Information', {
            'fields': ('name', 'media_type', 'folder', 'file_url', 'thumbnail_url')
        }),
        ('File Details', {
            'fields': ('file_size', 'mime_type', 'width', 'height')
        }),
        ('Metadata', {
            'fields': ('alt_text', 'description', 'tags')
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(BranchBranding)
class BranchBrandingAdmin(admin.ModelAdmin):
    list_display = ('branch', 'primary_color', 'show_address', 'show_phone', 'updated_at')
    search_fields = ('branch__name', 'branch__code')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Branch', {
            'fields': ('branch',)
        }),
        ('Logo', {
            'fields': ('logo_url', 'logo_light_url', 'favicon_url')
        }),
        ('Colors', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('Custom Styling', {
            'fields': ('custom_css',)
        }),
        ('Footer', {
            'fields': ('footer_text', 'footer_html')
        }),
        ('Contact Display', {
            'fields': ('show_address', 'show_phone', 'show_email')
        }),
        ('Timestamp', {
            'fields': ('updated_at',)
        }),
    )

