from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Emprendedor

@receiver(pre_save, sender=Emprendedor)
def actualizar_rango_edad(sender, instance, **kwargs):
    instance.rango_edad = instance.calcular_rango_edad()