from django.db import models

from apps.users.models import User
from apps.ingreso.models import Branch
# Create your models here.


class ManagerProfile(models.Manager):

    def profiles_by_user(self, usuario):
        return self.filter(user=usuario)

    def branch_by_user(self, usuario):
        perfiles = self.profiles_by_user(usuario)
        sucursales = []
        for perfil in perfiles:
            sucursales.append(perfil.branch)

        return sucursales


class Profile(models.Model):
    user = models.ForeignKey(User)
    branch = models.ForeignKey(Branch)

    objects = ManagerProfile()

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __unicode__(self):
        return str(self.branch.name)
