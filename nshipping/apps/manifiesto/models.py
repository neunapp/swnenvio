from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.ingreso.models import Branch, DepositSlip
from apps.users.models import User


class Car(models.Model):
    name = models.CharField('Denominacion', max_length=50)
    plaque = models.CharField('Placa', max_length=10)
    marca = models.CharField('Marca', max_length=70)

    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"

    def __unicode__(self):
        return self.plaque


class Driver(models.Model):
    dni = models.CharField('Dni', max_length=8)
    full_name = models.CharField('Nombres', max_length=100)
    license = models.CharField('Brebete', max_length=10)
    addreess = models.CharField('Direccion', max_length=150)
    phone = models.CharField('Telefono', max_length=10)
    email = models.EmailField()

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"

    def __unicode__(self):
        return self.full_name


class Manifest(models.Model):
    driver = models.ForeignKey(Driver)
    car = models.ForeignKey(Car)
    deposit_slip = models.ManyToManyField(DepositSlip)
    destination = models.ForeignKey(Branch)
    origin = models.ForeignKey(
        Branch,
        related_name="Branch_origin",
        blank=True,
        null=True,
        default=1,
    )
    user = models.ForeignKey(User, blank=True, null=True, default=1)
    date = models.TimeField(
        blank=True,
        null=True,
        default=timezone.now(),
    )

    class Meta:
        verbose_name = "Manifiesto"
        verbose_name_plural = "Manifiestos"

    def __unicode__(self):
        return "%s - %s" % (str(self.driver), str(self.car))


class Observation(models.Model):
    description = models.TextField()
    manifest = models.ForeignKey(Manifest)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = "Observation"
        verbose_name_plural = "Observations"

    def __unicode__(self):
        return self.manifest
