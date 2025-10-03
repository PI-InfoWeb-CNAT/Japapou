"""
URL configuration for japapouAdmin project.

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

from django.urls import path  # type: ignore
from django.urls import include  # type: ignore
from django.conf import settings  # type: ignore
from django.contrib import admin  # type: ignore
from django.conf.urls.static import static  # type: ignore


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("japapou.urls.visitor_urls")),
    path("client/", include("japapou.urls.client_urls")),
    path("delivery_man/", include("japapou.urls.delivery_man_urls")),
    path("manager/", include("japapou.urls.manager_urls")),
    path("auth/", include("japapou.urls.auth_urls")),
]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
