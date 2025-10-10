from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogTag, BlogPostTag, BlogComment


class BlogPostTagInline(admin.TabularInline):
    model = BlogPostTag
    extra = 0


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['color', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'published_at']
    list_filter = ['status', 'is_featured', 'category', 'author', 'created_at', 'published_at']
    search_fields = ['title', 'excerpt', 'content', 'author__username']
    list_editable = ['status', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogPostTagInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'allow_comments')
        }),
        ('Engagement', {
            'fields': ('views', 'likes')
        }),
    )
    
    ordering = ['-published_at', '-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(BlogPostTag)
class BlogPostTagAdmin(admin.ModelAdmin):
    list_display = ['post', 'tag']
    list_filter = ['tag', 'post__category']
    search_fields = ['post__title', 'tag__name']
    ordering = ['post', 'tag']


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'email', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post__category']
    search_fields = ['name', 'email', 'content', 'post__title']
    list_editable = ['is_approved']
    ordering = ['-created_at']