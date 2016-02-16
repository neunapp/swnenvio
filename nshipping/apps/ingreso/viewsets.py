from rest_framework import viewsets, permissions
from rest_framework.response import Response
from braces.views import LoginRequiredMixin

from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Client
from .serializer import ClientSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        print '=============ingreso al ClienteViewSet=============='
        cliente = get_object_or_404(Client, Q(dni=pk)|Q(ruc=pk))
        serializer = ClientSerializer(cliente)
        return Response(serializer.data)
