import random
import string
import logging
from django.core.mail import send_mail
from django.conf import settings
from .models import VerificationCode

logger = logging.getLogger(__name__)


def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_email_code(email: str) -> str:
    code = generate_code()
    VerificationCode.objects.create(target=email, code=code, code_type='email')
    try:
        send_mail(
            subject='【TryDate】您的验证码',
            message=f'您的验证码是：{code}，{settings.VERIFICATION_CODE_EXPIRE_MINUTES} 分钟内有效。',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        logger.warning(f'邮件发送失败: {e}，验证码: {code}')
        print(f'[EMAIL FALLBACK] {email} 的验证码：{code}')
    return code
