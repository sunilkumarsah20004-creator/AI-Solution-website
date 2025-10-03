
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Import custom admin configuration
from . import admin as custom_admin

urlpatterns = [
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
