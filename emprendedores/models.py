from django.db import models
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Emprendedor(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
    ]
    NIVEL_EDUCATIVO_CHOICES = [
        ('PR', 'Primaria'),
        ('SE', 'Secundaria'),
        ('TE', 'Técnico'),
        ('UN', 'Universitario'),
        ('PO', 'Posgrado'),
    ]
    ETAPA_EMPRENDIMIENTO_CHOICES = [
        ('ID', 'Idea'),
        ('PL', 'Planeación'),
        ('EJ', 'Ejecución'),
        ('CR', 'Crecimiento'),
    ]

    ORIENTACION_SEXUAL = [
        ('H', 'Heterosexual'),
        ('B', 'Bisexual'),
        ('G', 'Gay'),
        ('O', 'Otro'),
    ]

    # Datos Personales
    email = models.EmailField(verbose_name="Correo Electrónico")
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    cedula = models.CharField(max_length=20, unique=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    fecha_nacimiento = models.DateField()
    rango_edad = models.CharField(max_length=20, editable=False)  # He definido este campo para calcular la edad en la vista

    # Información de Contacto
    direccion_residencia = models.CharField(max_length=100)
    barrio_vereda = models.CharField(max_length=100)
    comuna_corregimiento = models.CharField(max_length=100)
    estrato = models.IntegerField()
    telefono = models.CharField(max_length=20)

    # Educación
    nivel_educativo = models.CharField(max_length=2, choices=NIVEL_EDUCATIVO_CHOICES)
    titulo_obtenido = models.CharField(max_length=100, blank=True, null=True)

    # Condiciones Especiales
    discapacidad = models.BooleanField(default=False)
    victima_conflicto = models.BooleanField(default=False)
    grupo_etnico = models.BooleanField(default=False)
    habitante_calle = models.BooleanField(default=False)
    orientacion_sexual = models.CharField(max_length=50, choices=ORIENTACION_SEXUAL, blank=True, null=True)
    victima_violencia_genero = models.BooleanField(default=False)
    cabeza_hogar = models.BooleanField(default=False)
    adulto_mayor = models.BooleanField(default=False)

    # Información Económica
    actividad_economica = models.CharField(max_length=100, default='No especificado')
    productos_servicios = models.TextField(default='', blank=True)
    nombre_negocio = models.CharField(max_length=100, default='', blank=True)
    numero_empleados = models.IntegerField(default=0)
    direccion_negocio = models.CharField(max_length=100, default='', blank=True)
    barrio_negocio = models.CharField(max_length=100, default='', blank=True)
    comuna_negocio = models.CharField(max_length=100, default='', blank=True)

    # Aspectos Legales del Negocio
    tiene_rut = models.BooleanField(default=False)
    tiene_registro_mercantil = models.BooleanField(default=False)
    tiene_facturacion_electronica = models.BooleanField(default=False)

    # Estado del Emprendimiento
    etapa_emprendimiento = models.CharField(max_length=2, choices=ETAPA_EMPRENDIMIENTO_CHOICES, default='ID')
    desafios_obstaculos = models.TextField(default='', blank=True)
    logros_importantes = models.TextField(default='', blank=True)
    tipo_apoyo_necesario = models.TextField(default='', blank=True)

    # Consentimiento
    autorizacion_tratamiento_datos = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} - {self.cedula}"
    
    def calcular_rango_edad(self):
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        
        if edad < 18:
            return 'Menor de 18'
        elif 18 <= edad <= 25:
            return '18-25'
        elif 26 <= edad <= 35:
            return '26-35'
        elif 36 <= edad <= 45:
            return '36-45'
        elif 46 <= edad <= 55:
            return '46-55'
        else:
            return 'Mayor de 55'

    def save(self, *args, **kwargs):
        self.rango_edad = self.calcular_rango_edad()
        super().save(*args, **kwargs)



from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Emprendedor)
def actualizar_rango_edad(sender, instance, **kwargs):
    instance.rango_edad = instance.calcular_rango_edad()


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    lugar = models.CharField(max_length=200)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Asesoria(Evento):
    asesor = models.CharField(max_length=100)
    duracion_horas = models.PositiveIntegerField(verbose_name="Duración (horas)", null=True, blank=True) 

class Taller(Evento):
    instructor = models.CharField(max_length=100)
    duracion = models.PositiveIntegerField(verbose_name="Duración (horas)", null=True, blank=True) 



from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

class MercadoCampesino(Evento):
    TIPO_PRODUCTOS_CHOICES = [
        ('FR', 'Frutas y Verduras'),
        ('LA', 'Lácteos'),
        ('CA', 'Carnes'),
        ('AR', 'Viveres'),
        ('OT', 'Otros'),
    ]
    tipo_productos = models.CharField(max_length=2, choices=TIPO_PRODUCTOS_CHOICES)
    total_venta = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d{1,3}(\.\d{3})*$',
                message='Ingrese un número válido con puntos como separadores de miles.',
                code='invalid_number'
            )
        ],
        help_text='Ingrese el total de ventas con puntos como separadores de miles (ej. 3.000.000)'
    )

    def clean(self):
        super().clean()
        if self.total_venta:
            try:
                # Convertir el string a un entero
                int(self.total_venta.replace('.', ''))
            except ValueError:
                raise ValidationError({'total_venta': 'Ingrese un número válido.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_total_venta_display(self):
        # Método para mostrar el total de venta con formato
        return self.total_venta
    
    @property
    def total_venta(self):
        return sum(venta.monto_venta for venta in self.ventaemprendedor_set.all())

    def get_total_venta_display(self):
        return f"{self.total_venta:,.2f}".replace(',', '.')
    


from django.db import models

class Inscripcion(models.Model):
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('emprendedor', 'evento')

    def __str__(self):
        return f"{self.emprendedor.primer_nombre} {self.emprendedor.primer_apellido} - {self.evento.nombre}"
    


class VentaEmprendedor(models.Model):
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    mercado_campesino = models.ForeignKey(MercadoCampesino, on_delete=models.CASCADE)
    monto_venta = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Ingrese el monto de la venta sin separadores de miles"
    )
    fecha_venta = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('emprendedor', 'mercado_campesino')
        verbose_name = "Venta de Emprendedor"
        verbose_name_plural = "Ventas de Emprendedores"

    def __str__(self):
        return f"{self.emprendedor} - {self.mercado_campesino} - ${self.monto_venta}"

    def venta(self):
        return f"{self.monto_venta:,.2f}".replace(',', '.')