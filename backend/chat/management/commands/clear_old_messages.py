"""
每周清空全部聊天记录。
用法: python manage.py clear_old_messages
建议通过 crontab 每周执行一次，例如每周日凌晨 3 点：
  0 3 * * 0 cd /path/to/backend && python manage.py clear_old_messages
"""
from django.core.management.base import BaseCommand
from chat.models import Message


class Command(BaseCommand):
    help = '清空所有聊天消息，实现每周一清'

    def handle(self, *args, **options):
        count, _ = Message.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'已清空全部 {count} 条聊天记录')
        )
