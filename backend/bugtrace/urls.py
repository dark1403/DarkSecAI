import logging
from django.contrib import admin
from django.urls import path, include

logger = logging.getLogger(__name__)

logger.info("Loading main URL configuration...")
logger.info("Including API URLs from 'api.urls'")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

logger.info(f"Main URL patterns loaded: {len(urlpatterns)} patterns")