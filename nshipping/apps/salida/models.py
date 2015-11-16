# -*- encoding: utf-8 -*-

from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from django.db.models import F

from apps.users.models import User


class Cash(models.Model):
    userstart = models.ForeignKey(settings.AUTH_USER_MODEL)
    userfinish = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="User_userfinish",
    )
    been = models.BooleanField()
    capitel = models.DecimalField(
        'Capital',
        max_digits=5,
        decimal_places=3,
    )
    hourstart = models.DateTimeField('Fecha Inicio')
    hourfinish = models.DateTimeField('Fecha Fin')
    observations = models.TextField('Observaciones')

    class Meta:
        verbose_name = "Cash"
        verbose_name_plural = "Cashs"

    def __unicode__(self):
        return self.userstart


class ManagerExpenditur(models.Manager):
    #procedimiento que calcula la suma de los egresos
    def total_egresos(self):
        egresos_validos = self.filter(anulate=False)
        #variable suma donde se almacenara la suma total
        suma = 0
        for egreso in egresos_validos:
            #acumulamos la suma
            suma = suma + egreso.amount
        return suma


class Expenditur(TimeStampedModel):
    description = models.TextField()
    amount = models.DecimalField(
        'Importe',
        max_digits=5,
        decimal_places=2,
    )
    canceled = models.BooleanField(
        'anulado',
        default=False,
        editable=False
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_created"
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_modified",
    )

    objects = ManagerExpenditur()

    class Meta:
        verbose_name = "Expenditur"
        verbose_name_plural = "Expenditurs"

    def __unicode__(self):
        return self.description
