from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, BlackList, VerificationCode


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'nickname', 'email', 'phone', 'gender', 'colored_status',
        'questionnaire_completion', 'is_active', 'created_at',
    ]
    list_filter = ['gender', 'status', 'grade', 'college_direction', 'is_active', 'is_staff']
    search_fields = ['nickname', 'email', 'phone']
    ordering = ['-created_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    list_editable = ['is_active']
    list_display_links = ['nickname', 'email']

    fieldsets = (
        ('账号信息', {
            'fields': ('email', 'phone'),
            'description': '用户登录凭证，邮箱或手机号至少填一项',
        }),
        ('基本信息', {
            'fields': ('nickname', 'avatar', 'bio', 'gender', 'gender_preference', 'birth_year', 'grade', 'college_direction'),
        }),
        ('状态管理', {
            'fields': ('status', 'questionnaire_completion', 'is_active'),
            'description': '控制用户账号状态和问卷进度',
        }),
        ('权限', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
            'description': '仅超级管理员可修改',
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'gender', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['questionnaire_completion', 'created_at']

    @admin.display(description='状态', ordering='status')
    def colored_status(self, obj):
        colors = {
            'active': '#22c55e',
            'banned': '#ef4444',
            'deleted': '#9ca3af',
        }
        labels = {
            'active': '正常',
            'banned': '封禁',
            'deleted': '注销',
        }
        color = colors.get(obj.status, '#9ca3af')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, label
        )

    actions = ['activate_users', 'ban_users']

    @admin.action(description='✅ 设为正常')
    def activate_users(self, request, queryset):
        queryset.update(status='active', is_active=True)

    @admin.action(description='🚫 封禁用户')
    def ban_users(self, request, queryset):
        queryset.update(status='banned', is_active=False)


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked', 'created_at']
    search_fields = ['blocker__nickname', 'blocked__nickname']
    list_per_page = 20
    date_hierarchy = 'created_at'


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['target', 'code_type', 'code', 'is_used', 'created_at']
    list_filter = ['code_type', 'is_used']
    search_fields = ['target']
    list_per_page = 20
    date_hierarchy = 'created_at'
    readonly_fields = ['target', 'code', 'code_type', 'is_used', 'created_at']
