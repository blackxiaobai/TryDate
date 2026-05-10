from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/questionnaire/', include('questionnaire.urls')),
    path('api/match/', include('matching.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/admin/', include('admin_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve frontend SPA (production)
frontend_index = os.path.join(settings.BASE_DIR, 'frontend-dist', 'index.html')
if os.path.exists(frontend_index):
    urlpatterns += [
        re_path(r'^(?!api/|admin/|media/).*$', TemplateView.as_view(template_name='index.html')),
    ]
