from django.contrib import admin
from django.utils.html import format_html
from .models import ChatRoom, Message, Report


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ['sender', 'msg_type', 'content', 'created_at']
    readonly_fields = ['sender', 'msg_type', 'content', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'match', 'is_active', 'message_count', 'last_message_at', 'created_at']
    list_filter = ['is_active']
    search_fields = ['match__user_a__nickname', 'match__user_b__nickname']
    list_per_page = 20
    inlines = [MessageInline]

    @admin.display(description='消息数')
    def message_count(self, obj):
        count = obj.messages.count()
        return format_html('<b>{}</b> 条', count)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'chat_room', 'msg_type', 'short_content', 'created_at']
    list_filter = ['msg_type', 'created_at']
    search_fields = ['sender__nickname', 'content']
    list_per_page = 30
    date_hierarchy = 'created_at'
    readonly_fields = ['chat_room', 'sender', 'msg_type', 'content', 'created_at']

    @admin.display(description='内容')
    def short_content(self, obj):
        text = obj.content[:50]
        if obj.msg_type == 'image':
            return format_html('<span style="color:#7C5CFC;">[图片]</span>')
        return text


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'target_user', 'reason', 'colored_status', 'created_at']
    list_filter = ['status', 'reason']
    search_fields = ['reporter__nickname', 'target_user__nickname', 'description']
    list_per_page = 20
    date_hierarchy = 'created_at'
    list_editable = ['colored_status'] if False else []

    fieldsets = (
        ('举报信息', {
            'fields': ('reporter', 'target_user', 'target_message'),
        }),
        ('详情', {
            'fields': ('reason', 'description', 'status'),
        }),
    )

    actions = ['mark_reviewed', 'mark_resolved', 'mark_dismissed']

    @admin.display(description='状态', ordering='status')
    def colored_status(self, obj):
        colors = {
            'pending': '#f59e0b',
            'reviewed': '#3b82f6',
            'resolved': '#22c55e',
            'dismissed': '#9ca3af',
        }
        labels = {
            'pending': '待处理',
            'reviewed': '已审核',
            'resolved': '已处理',
            'dismissed': '已驳回',
        }
        color = colors.get(obj.status, '#9ca3af')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, label,
        )

    @admin.action(description='🔵 标记为已审核')
    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')

    @admin.action(description='✅ 标记为已处理')
    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved')

    @admin.action(description='❌ 标记为已驳回')
    def mark_dismissed(self, request, queryset):
        queryset.update(status='dismissed')
