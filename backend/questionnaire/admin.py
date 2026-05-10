from django.contrib import admin
from django.utils.html import format_html
from .models import Questionnaire


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['user', 'completion_badge', 'last_modified_at']
    search_fields = ['user__nickname', 'user__email']
    list_per_page = 20
    list_filter = ['completion_rate']
    readonly_fields = ['user', 'completion_rate', 'last_modified_at']

    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'completion_rate', 'last_modified_at'),
        }),
        ('问卷答案', {
            'fields': ('answers',),
            'description': 'JSON 格式存储的五维度问卷答案',
        }),
    )

    @admin.display(description='完成度', ordering='completion_rate')
    def completion_badge(self, obj):
        rate = obj.completion_rate
        if rate >= 70:
            color = '#22c55e'
        elif rate >= 40:
            color = '#f59e0b'
        else:
            color = '#ef4444'
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-weight:bold;">{}%</span>',
            color, rate,
        )
