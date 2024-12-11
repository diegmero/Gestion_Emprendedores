from django import forms
from .models import Evento, Asesoria, Taller, MercadoCampesino, Inscripcion

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

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['emprendedores', 'tipo_evento', 'objeto_id']
        widgets = {
            'emprendedores': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emprendedores'].help_text = "Seleccione uno o más emprendedores"
        self.fields['tipo_evento'].help_text = "Seleccione el tipo de evento"
        self.fields['id_evento'].help_text = "Ingrese el ID del evento"