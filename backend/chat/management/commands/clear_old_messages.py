"""
每周清空超过 7 天的聊天记录。
可通过 --days 参数自定义天数。
用法: python manage.py clear_old_messages [--days 7]
建议通过 crontab 每周执行一次。
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from chat.models import Message


class Command(BaseCommand):
    help = '清空指定天数之前的聊天消息'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='清空多少天之前的消息（默认 7 天）',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff = timezone.now() - timedelta(days=days)
        count, _ = Message.objects.filter(created_at__lt=cutoff).delete()
        self.stdout.write(
            self.style.SUCCESS(f'已清空 {days} 天前的 {count} 条聊天记录')
        )
