# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.db.models import F
from django.utils import timezone

from decimal import Decimal
from datetime import datetime, timedelta

from model_utils.models import TimeStampedModel


class Client(models.Model):
    dni = models.CharField(
        'DNI',
        max_length=8,
        blank=True,
        null=True,
    )
    full_name = models.CharField(
        'nombre',
        max_length=100
    )
    ruc = models.CharField(
        'RUC',
        max_length=11,
        blank=True,
        null=True
    )
    business_name = models.CharField(
        'razon social',
        max_length=50,
        blank=True,
        null=True
    )
    address = models.CharField(
        'dirección',
        max_length=50,
    )
    phone = models.CharField(
        'telefono',
        max_length=30
    )

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __unicode__(self):
        return u'%s' % self.full_name


class Branch(models.Model):
    name = models.CharField(
        'nombre',
        max_length=50,
    )
    address = models.CharField(
        'direccion',
        max_length=100,
    )
    distrito = models.CharField(
        'Distrito',
        max_length=50,
    )
    provincia = models.CharField(
        'Provincia',
        max_length=50,
    )
    departamento = models.CharField(
        'Departamento',
        max_length=50,
    )
    phone = models.CharField(
        'Telefono',
        max_length=50,
    )

    class Meta:
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"

    def __unicode__(self):
        return u'%s' % self.name


class ManangerDespositSlip(models.Manager):

    def slip_by_manifest(self, manifest, branch):
        return self.filter(
            manifest__pk__startswith=manifest,
            destination__pk=branch,
            state='1',
        )


class DepositSlip(TimeStampedModel):

    COMPROBANTE_CHOICES = (
        ('Boleta', 'Boleta'),
        ('Factura', 'Factura'),
    )

    CREADO = '0'
    ENVIADO = '1'
    RECIBIDO = '2'
    ENTREGADO = '3'

    STATE_CHOICES = (
        (CREADO, 'Creado'),
        (ENVIADO, 'Enviado'),
        (RECIBIDO, 'Recibido'),
        (ENTREGADO, 'Entregado')
    )
    serie = models.CharField('serie', max_length=5)
    number = models.CharField('numero', max_length=20)
    origin = models.ForeignKey(Branch, related_name="origen")
    destination = models.ForeignKey(Branch, related_name="destino")
    sender = models.ForeignKey(Client, related_name="remitente")
    addressee = models.ForeignKey(Client, related_name="destinatario")
    voucher = models.CharField(
        'comprobante',
        max_length=10,
        choices=COMPROBANTE_CHOICES,
    )
    guide = models.CharField('nro. guia remitente', max_length=150)
    total_amount = models.DecimalField(
        'total',
        max_digits=7,
        decimal_places=2,
        default=0.00
    )
    igv = models.DecimalField(
        'IGV',
        max_digits=7,
        decimal_places=2,
        default=0.00,
        editable=False
    )
    count = models.PositiveIntegerField('cantidad')
    description = models.TextField('descripción')
    state = models.CharField(
        'estado',
        max_length=1,
        choices=STATE_CHOICES,
        default=CREADO,
    )
    canceled = models.BooleanField('anulado')
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="depositslip_user_created",
        default=CREADO,
        editable=False
    )
    canceled = models.BooleanField(
        'anulado',
        default=False,
        editable=False
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="depositslip_user_created",
        editable=False,
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="depositslip_user_modified",
        blank=True,
        null=True,
        editable=False
    )

    objects = ManangerDespositSlip()

    class Meta:
        verbose_name = "nota de ingreso"
        verbose_name_plural = "notas de ingresos"
        unique_together = (('serie', 'number'),)

    def __unicode__(self):
        return u'%s - %s' % (str(self.serie), str(self.number))

    def save(self, *args, **kwargs):
        if self.voucher == 'Factura':
            self.igv = self.total_amount*Decimal('0.18')
        super(DepositSlip, self).save(*args, **kwargs)


class ManagerDues(models.Manager):

    #funcion que busca un ingreso por numero-serie remitente y destinatari
    def search(self, serie, numero, remitente, destinatario, sucursal, fecha):
        flat = serie or numero or remitente or destinatario or fecha
        tz = timezone.get_current_timezone()
        if flat:
            if fecha:
                "si se ingreso fecha"
                date = datetime.strptime(fecha, "%d/%m/%Y")
                end_date = timezone.make_aware(date, tz)
                start_date = end_date - timedelta(days=7)
            else:

                date = datetime.strptime("01/10/2015", "%d/%m/%Y")
                end_date = timezone.now()
                start_date = timezone.make_aware(date, tz)
        else:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)

        busqueda = self.annotate(
            saldo=F('depositslip__total_amount')-F('amount')
        ).filter(
            depositslip__serie__icontains=serie,
            depositslip__number__icontains=numero,
            depositslip__sender__full_name__icontains=remitente,
            depositslip__addressee__full_name__icontains=destinatario,
            depositslip__state='0',
            depositslip__destination=sucursal,
            depositslip__created__range=(start_date, end_date)
        )
        return busqueda


class Dues(TimeStampedModel):

    depositslip = models.ForeignKey(DepositSlip)
    amount = models.DecimalField(
        'importe',
        max_digits=7,
        decimal_places=2,
    )
    canceled = models.BooleanField(
        'anulado',
        editable=False,
        default=False,
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="dues_user_created",
        editable=False,
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="dues_user_modified",
        blank=True,
        null=True,
        editable=False,
    )

    objects = ManagerDues()

    class Meta:
        verbose_name = "cuota"
        verbose_name_plural = "cuotas"

    def __unicode__(self):
        return u'%s' % str(self.depositslip)
