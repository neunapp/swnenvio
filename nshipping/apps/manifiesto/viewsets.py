from rest_framework import viewsets
from .models import Manifest
from .serializer import ManifestSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ManifestViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        print '==========================='
        manifiesto= get_object_or_404(Manifest, pk=pk, state=False)
        print manifiesto.deposit_slip.count()
        serializer = ManifestSerializer(manifiesto)
        return Response(serializer.data)
