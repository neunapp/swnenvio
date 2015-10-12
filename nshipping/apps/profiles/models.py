from django.db import models

from apps.users.models import User 
from apps.ingreso.models import Branch
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User)
    branch = models.ForeignKey(Branch)
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"