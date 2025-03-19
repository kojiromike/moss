"""
URL configuration for moss project.

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
from django.urls import include, path
from restframework.routers import DefaultRouter

from moss.store.views import FileViewSet, PermissionViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
]

router = DefaultRouter()
router.register(r"files", FileViewSet, basename="file")
router.register(r"permissions", PermissionViewSet, basename="permission")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
