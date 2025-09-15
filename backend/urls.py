"""
NutriVeda URL Configuration
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

# Import API views
from . import views

urlpatterns = [
    # API endpoints
    path('api/patients/', views.patients_api, name='patients'),
    path('api/food-database/', views.food_database_api, name='food_database'),
    path('api/diet-charts/', views.diet_charts_api, name='diet_charts'),
    path('api/dosha-assessment/', views.dosha_assessment_api, name='dosha_assessment'),
    path('api/analytics/', views.analytics_api, name='analytics'),
]

# Serve static files in development
def serve_static_dev(request, path):
    """Serve static files in development"""
    document_root = os.path.join(settings.BASE_DIR, 'static')
    return serve(request, path, document_root=document_root)

urlpatterns += [
    path('<path:path>', serve_static_dev),
]

# Serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
