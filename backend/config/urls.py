from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, Http404
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
frontend_dist = os.path.join(settings.BASE_DIR, 'frontend-dist')
frontend_index = os.path.join(frontend_dist, 'index.html')
if os.path.exists(frontend_index):
    # Serve Vite built assets
    assets_dir = os.path.join(frontend_dist, 'assets')

    def serve_asset(request, filename):
        filepath = os.path.join(assets_dir, filename)
        if os.path.isfile(filepath):
            import mimetypes
            content_type, _ = mimetypes.guess_type(filepath)
            return FileResponse(open(filepath, 'rb'), content_type=content_type)
        raise Http404

    urlpatterns += [
        re_path(r'^assets/(?P<filename>.+)$', serve_asset),
        re_path(r'^(?!api/|admin/|media/|assets/).*$', TemplateView.as_view(template_name='index.html')),
    ]
