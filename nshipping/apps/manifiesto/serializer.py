from rest_framework import serializers
from .models import Manifest
from apps.ingreso.models import DepositSlip


class ManifestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manifest
        fields = ('id','driver','deposit_slip')
