from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from emprendedores.views import EmprendedorViewSet

router = DefaultRouter()
router.register(r'emprendedores', EmprendedorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/crear/<str:tipo_evento>/', views.crear_evento, name='crear_evento'),
    path('eventos/<int:evento_id>/inscribir/', views.inscribir_evento, name='inscribir_evento'),
    path('emprendedores/', views.lista_emprendedores, name='lista_emprendedores'),
    path('inscribir/', views.inscribir_emprendedor, name='inscribir_emprendedor'),
    path('exportar/', views.pagina_exportacion, name='pagina_exportacion'),
    path('exportar/<str:modelo>/', views.exportar_excel, name='exportar_excel'),
]