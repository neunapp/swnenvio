from django.db import models
from django.db.models import F

from apps.users.models import User


class Client(models.Model):
    dni = models.CharField('Dni', max_length=8)
    full_name = models.CharField('Nombre', max_length=100)
    ruc = models.CharField('RUC', max_length=11)
    business_name = models.CharField('Razon Social', max_length=50)
    address = models.CharField('Direccion', max_length=15)
    phone = models.CharField('Telefono', max_length=50)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __unicode__(self):
        return str(self.full_name)


class Branch(models.Model):
    name = models.CharField('Nombre', max_length=50)
    address = models.CharField('Direccion', max_length=100)
    phone = models.CharField('Telefono', max_length=50)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __unicode__(self):
        return str(self.name)


class DepositSlip(models.Model):
    serie = models.CharField('Serie', max_length=50)
    number = models.CharField('Numero', max_length=50)
    origin = models.ForeignKey(Branch)
    destination = models.ForeignKey(Branch, related_name="Branch_destinatin")
    sender = models.ForeignKey(Client)
    addressee = models.ForeignKey(Client, related_name="Client_addressee")
    date = models.DateField()
    commited = models.BooleanField('Entregado', default=False)
    total_amount = models.DecimalField('Monto Total', max_digits=12, decimal_places=5, default=0)

    class Meta:
        verbose_name = "NotaIngreso"
        verbose_name_plural = "Nota de Ingresos"

    def __unicode__(self):
        return "%s - %s" % (str(self.serie), str(self.number))


class DetailDeposit(models.Model):
    deposit_slip = models.ForeignKey(DepositSlip, null=True)
    description = models.CharField('Descripcion', max_length=50, blank=True, null=True)
    count = models.PositiveIntegerField('Cantidad')
    been = models.BooleanField('Estado', default=False)
    user = models.ForeignKey(User, blank=True, null=True, default=1)
    class Meta:
        verbose_name = "Detalle_Ingreso"
        verbose_name_plural = "Detalle_Ingresos"
    
    def __unicode__(self):
        return str(self.deposit_slip)

class ManagerDues(models.Manager):
    def lista_no_entregado(self, destino, fecha):

        #no_etregados = self.annotate(deposit_slip__commited=False,deposit_slip__destination=destinatario)
        lista = self.annotate(
                                saldo=F('deposit_slip__total_amount')-F('amount')
                             ).filter(
                                    deposit_slip__commited=False,
                                    deposit_slip__destination=destino,
                                    date__lte=fecha,
                                    date__gte=fecha,
                                        )
        return lista

    def buscar_ingreso(self,destino,serie,numero, remitente, destinatario, fecha):
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
        ('sc','SC')
    )
    amount = models.DecimalField('Importe', max_digits=12, decimal_places=3, default=0)
    deposit_slip = models.ForeignKey(DepositSlip)
    date = models.DateField()
    proof_type = models.CharField('Tipo de Comprobate',max_length=10, choices=TIPO_COMPROBANTE, default='SC')
    igv = models.DecimalField('Igv',max_digits=12, decimal_places=3, default=0)
    sub_total = models.DecimalField('Sub Total', max_digits=12, decimal_places=3, default=0)
    discount = models.DecimalField('Descuento', max_digits=12, decimal_places=3, default=0)

    objects = ManagerDues()
    class Meta:
        verbose_name = "cuota"
        verbose_name_plural = "cuotas"

    def __unicode__(self):
        return str(self.deposit_slip)


    
            