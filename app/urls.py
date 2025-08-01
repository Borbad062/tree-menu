"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.views.generic import TemplateView

from app import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('about/', TemplateView.as_view(template_name='main/about.html'), name='about'),
    path('menus/' , include('menus.urls', namespace='menus')),
    path('users/' , include('users.urls', namespace='users')),
    path('carts/' , include('carts.urls', namespace='carts')),
]

if settings.DEBUG:
  urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)