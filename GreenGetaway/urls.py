"""
URL configuration for GreenGetaway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payment.urls')),  # payment URLs including webhook
    path('', include('getaway.urls', namespace='getaway')), # getaway app
    path('accounts/', include('accounts.urls')), # accounts app
    path('api/', include('api.urls')), # API endpoints



]


# For media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)