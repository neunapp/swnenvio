# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.db.models import F

from model_utils.models import TimeStampedModel


class Client(models.Model):
    dni = models.CharField('DNI', max_length=8, blank=True, null=True)
    full_name = models.CharField('nombre', max_length=100)
    ruc = models.CharField('RUC', max_length=11)
    business_name = models.CharField(
        'razon social',
        max_length=50,
        blank=True,
        null=True
    )
    address = models.CharField('dirección', max_length=50)
    phone = models.CharField('telefono', max_length=30)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __unicode__(self):
        return u'%s' % self.full_name


class Branch(models.Model):
    name = models.CharField('nombre', max_length=50)
    address = models.CharField('direccion', max_length=100)
    phone = models.CharField('telefono', max_length=50)

    class Meta:
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"

    def __unicode__(self):
        return u'%s' % self.name


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
    igv = models.DecimalField('IGV', max_digits=7, decimal_places=2)
    count = models.PositiveIntegerField('cantidad')
    description = models.TextField('descripción')
    state = models.CharField(
        'estado',
        max_length=1,
        choices=STATE_CHOICES,
        default=CREADO
    )
    canceled = models.BooleanField('anulado')
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="depositslip_user_created"
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="depositslip_user_modified",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "nota de ingreso"
        verbose_name_plural = "notas de ingresos"
        unique_together = (('serie', 'number'),)

    def __unicode__(self):
        return u'%s - %s' % (str(self.serie), str(self.number))


# class ManagerDues(models.Manager):
#     #funcion que devuelve todos los productos no entregados
#     def lista_no_entregado(self, destino, fecha):
#         lista = self.annotate(
#             saldo=F('deposit_slip__total_amount')-F('amount')
#         ).filter(
#             deposit_slip__commited=False,
#             deposit_slip__destination=destino,
#             date__lte=fecha,
#         )
#         return lista

#     #funcion que devuelve los envios no entregados
#     def envios_no_entregados(self, destino, fecha):
#         lista = self.annotate(
#             saldo=F('deposit_slip__total_amount')-F('amount')
#         ).filter(
#             depositslip__commited=False,
#             depositslip__destination=destino,
#             depositslip__output=True,
#             date__lte=fecha,
#         )
#         return lista

#     #funcion que busca un ingreso por numero-serie remitente y destinatari
#     def buscar_ingreso(self, destino, serie, numero, remitente, destinatario):
#         resultado = self.annotate(
#             saldo=F('deposit_slip__total_amount')-F('amount')
#         ).filter(
#             depositslip__commited=False,
#             depositslip__destination=destino,
#             depositslip__output=True,
#             depositslip__serie__icontains=serie,
#             depositslip__number__icontains=numero,
#             depositslip__sender__full_name__icontains=remitente,
#             depositslip__addressee__full_name__icontains=destinatario,
#         )
#         return resultado

#     #funcion que busca una nota de ingreso en un rango de fecha de 7 dias
#     def buscar_by_fecha(self, destino, date):
#         fecha = date - datetime.timedelta(days=7)
#         resultado = self.annotate(
#             saldo=F('deposit_slip__total_amount')-F('amount')
#         ).filter(
#             deposit_slip__commited=False,
#             deposit_slip__destination=destino,
#             deposit_slip__output=True,
#             deposit_slip__date__gte=fecha,
#             deposit_slip__date__lte=date,
#         )
#         return resultado

#     def buscar_by_destino(self, destino):
#         resultado = self.filter(
#             deposit_slip__commited=False,
#             deposit_slip__destination__name__icontains=destino,
#         )
#         return resultado


class Dues(TimeStampedModel):

    depositslip = models.ForeignKey(DepositSlip)
    amount = models.DecimalField(
        'importe',
        max_digits=7,
        decimal_places=2,
    )
    canceled = models.BooleanField('anulado')
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="dues_user_created",
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="dues_user_modified",
        blank=True,
        null=True
    )

    # objects = ManagerDues()

    class Meta:
        verbose_name = "cuota"
        verbose_name_plural = "cuotas"

    def __unicode__(self):
        return u'%s' % str(self.depositslip)
