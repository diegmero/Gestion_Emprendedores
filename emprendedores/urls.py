from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from emprendedores.views import EmprendedorViewSet

router = DefaultRouter()
router.register(r'emprendedores', EmprendedorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]