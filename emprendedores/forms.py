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



from django import forms
from .models import MercadoCampesino
from .fields import ThousandSeparatorField

class MercadoCampesinoForm(forms.ModelForm):
    total_venta = ThousandSeparatorField(
        label='Total de ventas',
        help_text='Ingrese el total de ventas con puntos como separadores de miles (ej. 3.000.000)',
        widget=forms.TextInput(attrs={'inputmode': 'numeric'})
    )

    class Meta:
        model = MercadoCampesino
        fields = ['nombre', 'fecha', 'descripcion', 'lugar', 'capacidad', 'tipo_productos', 'total_venta']

    def clean_total_venta(self):
        total_venta = self.cleaned_data.get('total_venta')
        if total_venta is not None and not isinstance(total_venta, int):
            raise forms.ValidationError('Ingrese un número válido sin letras ni símbolos.')
        return total_venta
    


from django import forms
from .models import Evento, Emprendedor

class InscripcionForm(forms.Form):
    evento = forms.ModelChoiceField(queryset=Evento.objects.all(), label="Evento")
    emprendedor = forms.ModelChoiceField(queryset=Emprendedor.objects.all(), label="Emprendedor")