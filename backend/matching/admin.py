from django.contrib import admin
from django.utils.html import format_html
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        'week_number', 'user_a', 'user_b', 'score_badge',
        'colored_status', 'user_a_action', 'user_b_action',
        'action_deadline', 'matched_at',
    ]
    list_filter = ['status', 'week_number']
    search_fields = ['user_a__nickname', 'user_b__nickname']
    list_per_page = 20
    date_hierarchy = 'matched_at'
    readonly_fields = ['compatibility_score', 'dimension_scores', 'compatibility_highlights', 'matched_at']

    fieldsets = (
        ('匹配双方', {
            'fields': ('user_a', 'user_b', 'week_number'),
        }),
        ('契合度', {
            'fields': ('compatibility_score', 'dimension_scores', 'compatibility_highlights'),
            'description': '系统自动计算的五维度契合度评分',
        }),
        ('互动状态', {
            'fields': ('user_a_action', 'user_b_action', 'status', 'action_deadline'),
        }),
    )

    @admin.display(description='契合度')
    def score_badge(self, obj):
        score = obj.compatibility_score
        if score >= 80:
            color = '#22c55e'
        elif score >= 60:
            color = '#f59e0b'
        else:
            color = '#9ca3af'
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-weight:bold;">{}%</span>',
            color, int(score),
        )

    @admin.display(description='状态', ordering='status')
    def colored_status(self, obj):
        colors = {
            'pending': '#f59e0b',
            'matched': '#22c55e',
            'missed': '#9ca3af',
        }
        labels = {
            'pending': '等待确认',
            'matched': '双向心动',
            'missed': '已错过',
        }
        color = colors.get(obj.status, '#9ca3af')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:12px;">{}</span>',
            color, label,
        )
