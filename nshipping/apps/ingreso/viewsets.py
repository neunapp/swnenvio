from rest_framework import viewsets
from .models import Client
from .serializer import ClientSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        print '=============ingreso al ClienteViewSet=============='
        cliente = get_object_or_404(Client, dni = pk)
        serializer = ClientSerializer(cliente)
        return Response(serializer.data)
