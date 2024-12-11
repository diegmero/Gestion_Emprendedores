from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Emprendedor
from .serializers import EmprendedorSerializer

class EmprendedorViewSet(viewsets.ModelViewSet):
    queryset = Emprendedor.objects.all()
    serializer_class = EmprendedorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Evento, Asesoria, Taller, MercadoCampesino, Emprendedor
from .forms import EventoForm, AsesoriaForm, TallerForm, MercadoCampesinoForm
from django.contrib.contenttypes.models import ContentType

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'emprendedores/lista_eventos.html', {'eventos': eventos})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Inscripcion
from .forms import InscripcionForm


@staff_member_required
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscripciones = Inscripcion.objects.filter(evento=evento)
    
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            emprendedor = form.cleaned_data['emprendedor']
            if not Inscripcion.objects.filter(evento=evento, emprendedor=emprendedor).exists():
                Inscripcion.objects.create(evento=evento, emprendedor=emprendedor)
                messages.success(request, f'{emprendedor.nombre} ha sido inscrito en el evento.')
            else:
                messages.warning(request, f'{emprendedor.nombre} ya está inscrito en este evento.')
            return redirect('detalle_evento', evento_id=evento.id)
    else:
        form = InscripcionForm()

    return render(request, 'emprendedores/detalle_evento.html', {
        'evento': evento,
        'inscripciones': inscripciones,
        'form': form
    })


def crear_evento(request, tipo_evento):
    if tipo_evento == 'asesoria':
        form_class = AsesoriaForm
        template_name = 'emprendedores/crear_asesoria.html'
    elif tipo_evento == 'taller':
        form_class = TallerForm
        template_name = 'emprendedores/crear_taller.html'
    elif tipo_evento == 'mercado':
        form_class = MercadoCampesinoForm
        template_name = 'emprendedores/crear_mercado.html'
    else:
        form_class = EventoForm
        template_name = 'emprendedores/crear_evento.html'

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            evento = form.save()
            messages.success(request, 'Evento creado exitosamente.')
            return redirect('detalle_evento', evento_id=evento.id)
    else:
        form = form_class()

    return render(request, template_name, {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Evento, Inscripcion

@login_required
def inscribir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        if Inscripcion.objects.filter(usuario=request.user, evento=evento).exists():
            messages.warning(request, 'Ya estás inscrito en este evento.')
        else:
            Inscripcion.objects.create(usuario=request.user, evento=evento)
            messages.success(request, 'Te has inscrito exitosamente al evento.')
    return redirect('detalle_evento', evento_id=evento.id)


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Evento, Emprendedor, Inscripcion
from .forms import InscripcionForm

@staff_member_required
def inscribir_emprendedor(request):
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            evento = form.cleaned_data['evento']
            emprendedor = form.cleaned_data['emprendedor']
            if not Inscripcion.objects.filter(evento=evento, emprendedor=emprendedor).exists():
                Inscripcion.objects.create(evento=evento, emprendedor=emprendedor)
                messages.success(request, f'{emprendedor.primer_nombre} {emprendedor.primer_apellido} ha sido inscrito en el evento {evento.nombre}.')
            else:
                messages.warning(request, f'{emprendedor.primer_nombre} {emprendedor.primer_apellido} ya está inscrito en este evento.')
            return redirect('lista_eventos')
    else:
        form = InscripcionForm()
    return render(request, 'emprendedores/inscribir_emprendedor.html', {'form': form})



from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from .models import Emprendedor

@staff_member_required
def lista_emprendedores(request):
    emprendedores_list = Emprendedor.objects.all().order_by('primer_apellido', 'primer_nombre')
    paginator = Paginator(emprendedores_list, 20)  # Mostrar 20 emprendedores por página
    
    page_number = request.GET.get('page')
    emprendedores = paginator.get_page(page_number)
    
    return render(request, 'emprendedores/lista_emprendedores.html', {'emprendedores': emprendedores})



def pagina_exportacion(request):
    return render(request, 'emprendedores/pagina_exportacion.html')


from django.http import HttpResponse
from openpyxl import Workbook
from .models import Emprendedor, Evento, Inscripcion

def exportar_excel(request, modelo):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{modelo}.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = modelo

    # Escribir encabezados
    if modelo == 'emprendedores':
        columns = ['Nombre', 'Apellido', 'Cédula', 'Teléfono']
        queryset = Emprendedor.objects.all()
    elif modelo == 'eventos':
        columns = ['Nombre', 'Fecha', 'Lugar']
        queryset = Evento.objects.all()
    elif modelo == 'inscripciones':
        columns = ['Emprendedor', 'Evento', 'Fecha de Inscripción']
        queryset = Inscripcion.objects.all()
    else:
        return HttpResponse("Modelo no válido")

    ws.append(columns)

    # Escribir datos
    for obj in queryset:
        if modelo == 'emprendedores':
            row = [obj.primer_nombre, obj.primer_apellido, obj.cedula, obj.telefono]
        elif modelo == 'eventos':
            row = [obj.nombre, str(obj.fecha), obj.lugar]
        elif modelo == 'inscripciones':
            row = [str(obj.emprendedor), str(obj.evento), str(obj.fecha_inscripcion)]
        ws.append(row)

    wb.save(response)
    return response