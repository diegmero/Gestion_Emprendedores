# Generated by Django 5.1.4 on 2024-12-11 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprendedores', '0005_alter_mercadocampesino_total_venta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mercadocampesino',
            name='total_venta',
            field=models.IntegerField(default=0),
        ),
    ]
