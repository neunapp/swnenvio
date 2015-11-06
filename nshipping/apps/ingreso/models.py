# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models import F

from django.conf import settings

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
    serie = models.CharField('serie', max_length=5)
    number = models.CharField('numero', max_length=20)
    origin = models.ForeignKey(Branch)
    destination = models.ForeignKey(Branch, related_name="branch_destination")
    sender = models.ForeignKey(Client)
    addressee = models.ForeignKey(Client, related_name="client_addressee")
    date = models.DateField()
    total_amount = models.DecimalField(
        'monto total',
        max_digits=7,
        decimal_places=2,
        default=0.00
    )
    count = models.PositiveIntegerField('cantidad')
    description = models.TextField('descripción')
    commited = models.BooleanField('entregado')
    output = models.BooleanField('salida')
    receive = models.BooleanField('recibido')
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_created"
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_modified",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "nota de ingreso"
        verbose_name_plural = "notas de ingresos"
        unique_together = (('serie', 'number'),)

    def __unicode__(self):
        return u'%s - %s' % (str(self.serie), str(self.number))


class ManagerDues(models.Manager):
    def lista_no_entregado(self, destino, fecha):

        lista = self.annotate(
            saldo=F('deposit_slip__total_amount')-F('amount')
        ).filter(
            deposit_slip__commited=False,
            deposit_slip__destination=destino,
            date__lte=fecha,
            date__gte=fecha,
        )
        return lista

    def buscar_ingreso(self, destino, serie, numero, remitente, destinatario, fecha):
        resultado = self.annotate(
            saldo=F('deposit_slip__total_amount')-F('amount')
        ).filter(
            deposit_slip__commited=False,
            deposit_slip__destination=destino,
            deposit_slip__serie__icontains=serie,
            deposit_slip__number__icontains=numero,
            deposit_slip__sender__full_name__icontains=remitente,
            deposit_slip__addressee__full_name__icontains=destinatario,
            deposit_slip__date__icontains=fecha,
        )
        return resultado

    def buscar_by_destino(self, destino):
        resultado = self.filter(
            deposit_slip__commited=False,
            deposit_slip__destination__name__icontains=destino,
        )
        return resultado


class Dues(models.Model):
    TIPO_COMPROBANTE = (
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
        ('sc', 'SC')
    )
    amount = models.DecimalField(
        'Importe',
        max_digits=7,
        decimal_places=2,
    )
    deposit_slip = models.ForeignKey(DepositSlip)
    date = models.DateField()
    proof_type = models.CharField(
        'Tipo de Comprobate',
        max_length=10,
        choices=TIPO_COMPROBANTE,
        default='SC'
    )
    igv = models.DecimalField(
        'Igv',
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    sub_total = models.DecimalField(
        'Sub Total',
        max_digits=7,
        decimal_places=2,
        default=0.00
    )
    discount = models.DecimalField(
        'Descuento',
        max_digits=7,
        decimal_places=2,
        default=0.00
    )

    objects = ManagerDues()

    class Meta:
        verbose_name = "cuota"
        verbose_name_plural = "cuotas"

    def __unicode__(self):
        return u'%s' % str(self.deposit_slip)
