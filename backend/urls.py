
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Serve React static assets in /images/ path
urlpatterns += [
    re_path(r'^images/(?P<path>.*)$', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'frontend', 'build', 'images') if os.path.exists(os.path.join(settings.BASE_DIR, 'frontend', 'build', 'images')) else os.path.join(settings.BASE_DIR, 'frontend', 'public', 'images'),
    }),
]


# ── Catch-all: serve React's index.html for every other route ────────────────
# This MUST be last so API and admin routes take priority.
urlpatterns += [
    re_path(r'^(?!api/|admin/|media/|static/|images/).*$',
            TemplateView.as_view(template_name='index.html')),
]
