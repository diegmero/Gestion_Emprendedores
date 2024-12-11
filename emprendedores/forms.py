from django import forms
from .models import Evento, Asesoria, Taller, MercadoCampesino

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha', 'descripcion', 'lugar', 'capacidad']

class AsesoriaForm(forms.ModelForm):
    class Meta:
        model = Asesoria
        fields = ['nombre', 'fecha', 'descripcion', 'lugar', 'capacidad', 'asesor', 'duracion_horas']

class TallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = ['nombre', 'fecha', 'descripcion', 'lugar', 'capacidad', 'instructor', 'duracion']

class MercadoCampesinoForm(forms.ModelForm):
    class Meta:
        model = MercadoCampesino
        fields = ['nombre', 'fecha', 'descripcion', 'lugar', 'capacidad', 'tipo_productos']


from django import forms
from .models import Evento, Emprendedor

class InscripcionForm(forms.Form):
    evento = forms.ModelChoiceField(queryset=Evento.objects.all(), label="Evento")
    emprendedor = forms.ModelChoiceField(queryset=Emprendedor.objects.all(), label="Emprendedor")