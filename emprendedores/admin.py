from django.contrib import admin
from .models import Emprendedor, Inscripcion, Evento, Asesoria, Taller, MercadoCampesino, VentaEmprendedor
from django.http import HttpResponse
import xlwt


def exportar_a_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{modeladmin.model.__name__}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(modeladmin.model.__name__)

    # Escribir encabezados
    row_num = 0
    columns = [field.name for field in modeladmin.model._meta.fields]
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Escribir datos
    for obj in queryset:
        row_num += 1
        for col_num, field in enumerate(columns):
            value = getattr(obj, field)
            ws.write(row_num, col_num, str(value))

    wb.save(response)
    return response

exportar_a_excel.short_description = "Exportar a Excel"



@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    readonly_fields = ('rango_edad',)
    list_display = ('primer_nombre', 'primer_apellido', 'cedula', 'email', 'telefono')
    search_fields = ('primer_nombre', 'primer_apellido', 'cedula', 'email')
    list_filter = ('genero', 'nivel_educativo', 'etapa_emprendimiento')
    actions = [exportar_a_excel]

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
    


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'capacidad')
    search_fields = ('nombre', 'lugar')
    actions = [exportar_a_excel]

from django.contrib import admin
from .models import Emprendedor, Inscripcion, Evento, Asesoria, Taller, MercadoCampesino
from django.http import HttpResponse
import xlwt

@admin.register(Asesoria)
class AsesoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'asesor', 'duracion_horas')
    actions = [exportar_a_excel]

    def mostrar_duracion_horas(self, obj):
        if obj.duracion_horas:
            return f"{obj.duracion_horas.total_seconds() / 3600:.0f}"
        return "-"
    mostrar_duracion_horas.short_description = "Duración (horas)"

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'instructor', 'duracion')
    actions = [exportar_a_excel]

    def mostrar_duracion(self, obj):
        if obj.duracion:
            return f"{obj.duracion.total_seconds() / 3600:.0f}"
        return "-"
    mostrar_duracion.short_description = "Duración (horas)"

@admin.register(VentaEmprendedor)
class VentaEmprendedorAdmin(admin.ModelAdmin):
    list_display = ('emprendedor', 'mercado_campesino', 'venta', 'fecha_venta')
    list_filter = ('mercado_campesino', 'fecha_venta')
    search_fields = ('emprendedor__primer_nombre', 'emprendedor__primer_apellido', 'mercado_campesino__nombre')

@admin.register(MercadoCampesino)
class MercadoCampesinoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'tipo_productos', 'total_venta')
    actions = [exportar_a_excel]


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('evento', 'emprendedor', 'fecha_inscripcion')
    list_filter = ('evento', 'fecha_inscripcion')
    search_fields = ('evento__nombre', 'emprendedor__primer_nombre', 'emprendedor__primer_apellido')
    actions = [exportar_a_excel]