from django.contrib import admin
from django.utils.html import format_html
from .models import Post, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['short_content', 'author', 'is_anonymous', 'like_count', 'colored_status', 'created_at']
    list_filter = ['status', 'is_anonymous', 'created_at']
    search_fields = ['author__nickname', 'content']
    list_per_page = 20
    date_hierarchy = 'created_at'
    list_editable = ['colored_status'] if False else []

    fieldsets = (
        ('动态内容', {
            'fields': ('author', 'content', 'is_anonymous'),
        }),
        ('状态', {
            'fields': ('status', 'like_count'),
        }),
    )

    readonly_fields = ['like_count', 'created_at']

    actions = ['hide_posts', 'restore_posts']

    @admin.display(description='内容')
    def short_content(self, obj):
        text = obj.content[:30]
        if len(obj.content) > 30:
            text += '...'
        return text

    @admin.display(description='状态', ordering='status')
    def colored_status(self, obj):
        colors = {
            'active': '#22c55e',
            'hidden': '#f59e0b',
            'deleted': '#ef4444',
        }
        labels = {
            'active': '正常',
            'hidden': '隐藏',
            'deleted': '已删除',
        }
        color = colors.get(obj.status, '#9ca3af')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, label,
        )

    @admin.action(description='🙈 隐藏动态')
    def hide_posts(self, request, queryset):
        queryset.update(status='hidden')

    @admin.action(description='👁️ 恢复动态')
    def restore_posts(self, request, queryset):
        queryset.update(status='active')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    search_fields = ['user__nickname']
    list_per_page = 20
    date_hierarchy = 'created_at'
