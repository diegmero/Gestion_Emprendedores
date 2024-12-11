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
from .models import Evento, Asesoria, Taller, MercadoCampesino, Inscripcion, Emprendedor
from .forms import EventoForm, AsesoriaForm, TallerForm, MercadoCampesinoForm, InscripcionForm
from django.contrib.contenttypes.models import ContentType

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'emprendedores/lista_eventos.html', {'eventos': eventos})

def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscripciones = Inscripcion.objects.filter(object_id=evento.id, content_type=ContentType.objects.get_for_model(evento))
    return render(request, 'emprendedores/detalle_evento.html', {'evento': evento, 'inscripciones': inscripciones})

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

def inscribir_emprendedor(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.evento = evento
            inscripcion.save()
            messages.success(request, 'Inscripción realizada exitosamente.')
            return redirect('detalle_evento', evento_id=evento.id)
    else:
        form = InscripcionForm()
    return render(request, 'emprendedores/inscribir_emprendedor.html', {'form': form, 'evento': evento})