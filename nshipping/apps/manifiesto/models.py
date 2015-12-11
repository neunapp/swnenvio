# -*- encoding: utf-8 -*-
# import utils
from model_utils.models import TimeStampedModel
# import django
from django.db import models
from django.conf import settings
from django.utils import timezone
# import local
from apps.ingreso.models import Branch, DepositSlip
from apps.users.models import User


class Car(models.Model):
    STATE_CHOICES = (
        ('0', 'Propio'),
        ('1', 'Sub Contrata'),
    )
    name = models.CharField(
        'Denominacion',
        max_length=50,
    )
    plaque = models.CharField(
        'Placa',
        max_length=10
    )
    marca = models.CharField(
        'Marca',
        max_length=70,
    )
    code_ssettings_car = models.CharField(
        'Codigo de Configuracion vehicular',
        max_length=6
    )
    constancy_inscription = models.CharField(
        'N° de Contancia de Inscripcion',
        max_length=12,
    )
    condition = models.CharField(
        'Condicion',
        choices=STATE_CHOICES,
        max_length=11,
    )
    canceled = models.BooleanField(
        'anulado',
        default=False,
        editable=False
    )

    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"

    def __unicode__(self):
        return self.plaque


class Driver(models.Model):
    dni = models.CharField(
        'Dni',
        max_length=8,
    )
    full_name = models.CharField(
        'Nombres',
        max_length=100,
    )
    license = models.CharField(
        'Brebete',
        max_length=10
    )
    addreess = models.CharField(
        'Direccion',
        max_length=150
    )
    phone = models.CharField(
        'Telefono',
        max_length=10
    )
    email = models.EmailField()
    date_birth = models.DateField(
        'fecha de nacimiento',
        blank=True,
        null=True,
    )
    canceled = models.BooleanField(
        'anulado',
        default=False,
        editable=False
    )

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"

    def __unicode__(self):
        return self.full_name


class ManangerManifest(models.Manager):

    def manifest_by_user(self, branch):
        #recuperamos la lista de manifiestos enviados
        manifest_query = self.filter(reception=False, state=True)
        # recorremos el manifiesto
        lista = []
        for manifest in manifest_query:
            existe = False
            for slip in manifest.deposit_slip.all():
                if slip.destination == branch:
                    print '======pertenece al manifiesto====='
                    existe = True
            # verificamos si se encontro alguna sucursal
            if existe is True:
                print '======se agrega el manifiesto======='
                lista.append(manifest)
        # devolvemos la lista
        return lista


class Manifest(TimeStampedModel):
    driver = models.ForeignKey(Driver)
    car = models.ForeignKey(Car)
    deposit_slip = models.ManyToManyField(
        DepositSlip,
    )
    destination = models.ForeignKey(Branch)
    origin = models.ForeignKey(
        Branch,
        related_name="Branch_origin",
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="manifest_user_created"
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="manifest_user_modified",
        blank=True,
        null=True
    )
    date_shipping = models.DateField(
        'fecha de Traslado',
    )
    state = models.BooleanField('Estado')
    reception = models.BooleanField(
        default=False,
        editable=True,
    )
    canceled = models.BooleanField(
        'anulado',
        default=False,
        editable=False
    )

    objects = ManangerManifest()

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


class SubContract(models.Model):
    manifest = models.ForeignKey(Manifest)
    full_name = models.CharField(
        'Nombres/Razon social',
        max_length=70,
    )
    ruc = models.CharField(
        'Ruc',
        max_length=50,
    )
    observation = models.CharField(
        'Observaciones',
        max_length=50,
    )
    canceled = models.BooleanField(
        'anulado',
        default=False,
        editable=False
    )

    class Meta:
        verbose_name = "SubContract"
        verbose_name_plural = "SubContracts"

    def __unicode__(self):
        return self.full_name
