import random
import string
import logging
import resend
from django.conf import settings
from .models import VerificationCode

logger = logging.getLogger(__name__)
resend.api_key = settings.RESEND_API_KEY


def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_email_code(email: str) -> str:
    code = generate_code()
    VerificationCode.objects.create(target=email, code=code, code_type='email')
    try:
        resend.Emails.send({
            'from': 'TryDate <onboarding@resend.dev>',
            'to': [email],
            'subject': '【TryDate】您的验证码',
            'html': f'<p>您的验证码是：<strong>{code}</strong>，{settings.VERIFICATION_CODE_EXPIRE_MINUTES} 分钟内有效。</p>',
        })
    except Exception as e:
        logger.warning(f'邮件发送失败: {e}，验证码: {code}')
        print(f'[EMAIL FALLBACK] {email} 的验证码：{code}')
    return code
