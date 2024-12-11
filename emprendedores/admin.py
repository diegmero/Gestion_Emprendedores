from django.contrib import admin
from .models import Emprendedor

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
    


from .models import Emprendedor, Evento, Asesoria, Taller, MercadoCampesino, Inscripcion


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



from django.contrib.contenttypes.models import ContentType

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('get_emprendedores', 'get_evento', 'fecha_inscripcion')
    list_filter = ('tipo_evento', 'fecha_inscripcion')
    search_fields = ('emprendedores__primer_nombre', 'emprendedores__primer_apellido', 'evento__nombre')
    filter_horizontal = ('emprendedores',)

    def get_emprendedores(self, obj):
        return ", ".join([str(e) for e in obj.emprendedores.all()])
    get_emprendedores.short_description = 'Emprendedores'

    def get_evento(self, obj):
        return str(obj.evento)
    get_evento.short_description = 'Evento'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tipo_evento":
            kwargs["queryset"] = ContentType.objects.filter(
                model__in=['asesoria', 'taller', 'mercadocampesino']
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)