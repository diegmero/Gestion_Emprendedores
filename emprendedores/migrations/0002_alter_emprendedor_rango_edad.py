# Generated by Django 5.1.4 on 2024-12-10 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprendedores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprendedor',
            name='rango_edad',
            field=models.CharField(editable=False, max_length=20),
        ),
    ]
