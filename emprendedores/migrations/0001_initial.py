# Generated by Django 5.1.4 on 2024-12-10 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emprendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('primer_nombre', models.CharField(max_length=50)),
                ('segundo_nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('primer_apellido', models.CharField(max_length=50)),
                ('segundo_apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo_documento', models.CharField(choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('TI', 'Tarjeta de Identidad')], max_length=2)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('fecha_nacimiento', models.DateField()),
                ('rango_edad', models.CharField(max_length=20)),
                ('direccion_residencia', models.CharField(max_length=100)),
                ('barrio_vereda', models.CharField(max_length=100)),
                ('comuna_corregimiento', models.CharField(max_length=100)),
                ('estrato', models.IntegerField()),
                ('telefono', models.CharField(max_length=20)),
                ('nivel_educativo', models.CharField(choices=[('PR', 'Primaria'), ('SE', 'Secundaria'), ('TE', 'Técnico'), ('UN', 'Universitario'), ('PO', 'Posgrado')], max_length=2)),
                ('titulo_obtenido', models.CharField(blank=True, max_length=100, null=True)),
                ('discapacidad', models.BooleanField(default=False)),
                ('victima_conflicto', models.BooleanField(default=False)),
                ('grupo_etnico', models.BooleanField(default=False)),
                ('habitante_calle', models.BooleanField(default=False)),
                ('orientacion_sexual', models.CharField(blank=True, max_length=50, null=True)),
                ('victima_violencia_genero', models.BooleanField(default=False)),
                ('cabeza_hogar', models.BooleanField(default=False)),
                ('adulto_mayor', models.BooleanField(default=False)),
                ('actividad_economica', models.CharField(default='No especificado', max_length=100)),
                ('productos_servicios', models.TextField(blank=True, default='')),
                ('nombre_negocio', models.CharField(blank=True, default='', max_length=100)),
                ('numero_empleados', models.IntegerField(default=0)),
                ('direccion_negocio', models.CharField(blank=True, default='', max_length=100)),
                ('barrio_negocio', models.CharField(blank=True, default='', max_length=100)),
                ('comuna_negocio', models.CharField(blank=True, default='', max_length=100)),
                ('tiene_rut', models.BooleanField(default=False)),
                ('tiene_registro_mercantil', models.BooleanField(default=False)),
                ('tiene_facturacion_electronica', models.BooleanField(default=False)),
                ('etapa_emprendimiento', models.CharField(choices=[('ID', 'Idea'), ('PL', 'Planeación'), ('EJ', 'Ejecución'), ('CR', 'Crecimiento')], default='ID', max_length=2)),
                ('desafios_obstaculos', models.TextField(blank=True, default='')),
                ('logros_importantes', models.TextField(blank=True, default='')),
                ('tipo_apoyo_necesario', models.TextField(blank=True, default='')),
                ('autorizacion_tratamiento_datos', models.BooleanField(default=False)),
            ],
        ),
    ]
