from django.contrib import admin
from .models import Emprendedor, Inscripcion

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    readonly_fields = ('rango_edad',)
    list_display = ('primer_nombre', 'primer_apellido', 'cedula', 'email', 'telefono')
    search_fields = ('primer_nombre', 'primer_apellido', 'cedula', 'email')
    list_filter = ('genero', 'nivel_educativo', 'etapa_emprendimiento')

    fieldsets = (
        ('Datos Personales', {
            'fields': ('email', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 
                       'tipo_documento', 'cedula', 'genero', 'fecha_nacimiento', 'rango_edad')
        }),
        ('Información de Contacto', {
            'fields': ('direccion_residencia', 'barrio_vereda', 'comuna_corregimiento', 'estrato', 'telefono')
        }),
        ('Educación', {
            'fields': ('nivel_educativo', 'titulo_obtenido')
        }),
        ('Condiciones Especiales', {
            'fields': ('discapacidad', 'victima_conflicto', 'grupo_etnico', 'habitante_calle', 
                       'orientacion_sexual', 'victima_violencia_genero', 'cabeza_hogar', 'adulto_mayor')
        }),
        ('Información Económica', {
            'fields': ('actividad_economica', 'productos_servicios', 'nombre_negocio', 'numero_empleados', 
                       'direccion_negocio', 'barrio_negocio', 'comuna_negocio')
        }),
        ('Aspectos Legales', {
            'fields': ('tiene_rut', 'tiene_registro_mercantil', 'tiene_facturacion_electronica')
        }),
        ('Estado del Emprendimiento', {
            'fields': ('etapa_emprendimiento', 'desafios_obstaculos', 'logros_importantes', 'tipo_apoyo_necesario')
        }),
        ('Consentimiento', {
            'fields': ('autorizacion_tratamiento_datos',)
        }),
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            if search_term.isdigit():
                queryset |= self.model.objects.filter(cedula=search_term)
        except:
            pass
        return queryset, use_distinct
    


from .models import Emprendedor, Evento, Asesoria, Taller, MercadoCampesino


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'capacidad')
    search_fields = ('nombre', 'lugar')

@admin.register(Asesoria)
class AsesoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'asesor', 'duracion_horas')

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'instructor', 'duracion')

@admin.register(MercadoCampesino)
class MercadoCampesinoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'tipo_productos')


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('evento', 'emprendedor', 'fecha_inscripcion')
    list_filter = ('evento', 'fecha_inscripcion')
    search_fields = ('evento__nombre', 'emprendedor__primer_nombre', 'emprendedor__primer_apellido')