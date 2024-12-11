from django import forms
import re

class ThousandSeparatorField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'pattern': r'^\d{1,3}(\.?\d{3})*$'})

    def to_python(self, value):
        if value in self.empty_values:
            return None
        value = re.sub(r'[^\d.]', '', value)  # Remove any character that is not a digit or dot
        if not re.match(r'^\d{1,3}(\.?\d{3})*$', value):
            raise forms.ValidationError('Ingrese un número válido con puntos como separadores de miles.')
        return int(value.replace('.', ''))

    def prepare_value(self, value):
        if value is None:
            return ''
        return '{:,}'.format(int(value)).replace(',', '.')

    def validate(self, value):
        super().validate(value)
        if value is not None and not isinstance(value, int):
            raise forms.ValidationError('Ingrese un número válido.')