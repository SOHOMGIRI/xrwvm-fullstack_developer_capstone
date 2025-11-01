from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
import os

urlpatterns = [
    # 🔹 Admin panel
    path('admin/', admin.site.urls),

    # 🔹 Django app API endpoints
    path('djangoapp/', include('djangoapp.urls')),

    # 🔹 Explicitly serve manifest.json from React build
    re_path(r'^manifest\.json$', serve, {
        'path': 'manifest.json',
        'document_root': os.path.join(settings.BASE_DIR, 'frontend/build')
    }),

    # 🔹 Explicitly serve logo192.png from React build
    re_path(r'^logo192\.png$', serve, {
        'path': 'logo192.png',
        'document_root': os.path.join(settings.BASE_DIR, 'frontend/build')
    }),

    # 🔹 Explicitly serve logo512.png from React build
    re_path(r'^logo512\.png$', serve, {
        'path': 'logo512.png',
        'document_root': os.path.join(settings.BASE_DIR, 'frontend/build')
    }),
]

# 🔹 Serve React frontend for all unmatched routes — EXCLUDE /admin
urlpatterns += [
    re_path(r'^(?!admin).*$', TemplateView.as_view(template_name="index.html")),
]

# 🔹 Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)