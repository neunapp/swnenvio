from django.db import models
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
    serie = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    origin = models.ForeignKey(Branch)
    destination = models.ForeignKey(Branch, related_name="Branch_destinatin")
    sender = models.ForeignKey(Client)
    addressee = models.ForeignKey(Client, related_name="Client_addressee")
    date = models.DateField()
    total_amount = models.DecimalField('Monto Total', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "NotaIngreso"
        verbose_name_plural = "Nota de Ingresos"

    def __unicode__(self):
        return str(self.serie)


class DetailDeposit(models.Model):
    deposit_slip = models.ForeignKey(DepositSlip)
    description = models.CharField('Descripcion', max_length=50)
    count = models.PositiveIntegerField('Cantidad')
    been = models.BooleanField('Estado')
    user = models.ForeignKey(User)
    class Meta:
        verbose_name = "Detalle_Ingreso"
        verbose_name_plural = "Detalle_Ingresos"
    
    def __unicode__(self):
        return str(self.deposit_slip)

class Dues(models.Model):
    TIPO_COMPROBANTE = (
        ('boleta', 'Boleta'),
        ('factura', 'Factura'),
    )
    amount = models.DecimalField('Importe', max_digits=5, decimal_places=3)
    deposit_slip = models.ForeignKey(DepositSlip)
    date = models.DateField()
    proof_type = models.CharField('Tipo de Comprobate',max_length=10, choices=TIPO_COMPROBANTE)
    igv = models.DecimalField('Igv', max_digits=5, decimal_places=3)
    sub_total = models.DecimalField('Sub Total', max_digits=5, decimal_places=2)
    class Meta:
        verbose_name = "cuota"
        verbose_name_plural = "cuotas"

    def __unicode__(self):
        return str(self.deposit_slip)
    
            