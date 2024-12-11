# Generated by Django 5.1.4 on 2024-12-11 01:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('emprendedores', '0003_alter_emprendedor_orientacion_sexual'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField()),
                ('descripcion', models.TextField()),
                ('lugar', models.CharField(max_length=200)),
                ('capacidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Asesoria',
            fields=[
                ('evento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='emprendedores.evento')),
                ('asesor', models.CharField(max_length=100)),
                ('duracion_horas', models.DurationField(blank=True, null=True)),
            ],
            bases=('emprendedores.evento',),
        ),
        migrations.CreateModel(
            name='MercadoCampesino',
            fields=[
                ('evento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='emprendedores.evento')),
                ('tipo_productos', models.CharField(choices=[('FR', 'Frutas y Verduras'), ('LA', 'Lácteos'), ('CA', 'Carnes'), ('AR', 'Viveres'), ('OT', 'Otros')], max_length=2)),
            ],
            bases=('emprendedores.evento',),
        ),
        migrations.CreateModel(
            name='Taller',
            fields=[
                ('evento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='emprendedores.evento')),
                ('instructor', models.CharField(max_length=100)),
                ('duracion', models.DurationField()),
            ],
            bases=('emprendedores.evento',),
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objeto_id', models.PositiveIntegerField(default=1, verbose_name='ID del Evento')),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                ('emprendedores', models.ManyToManyField(related_name='inscripciones', to='emprendedores.emprendedor')),
                ('tipo_evento', models.ForeignKey(default=11, limit_choices_to={'model__in': ('asesoria', 'taller', 'mercadocampesino')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Tipo de Evento')),
            ],
            options={
                'verbose_name': 'Inscripción',
                'verbose_name_plural': 'Inscripciones',
                'unique_together': {('tipo_evento', 'objeto_id')},
            },
        ),
    ]