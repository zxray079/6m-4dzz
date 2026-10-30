from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import re_path
from core.yasg import urlpatterns_yasg


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlpatterns_yasg)),
    path('api/v1/testapp/', include('apps.testapp.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]