from django.conf.urls import url, patterns, include
from rest_framework import routers
from . import views
from .viewsets import ClientViewSet, ClienteViewSet
from .models import Client

router = routers.SimpleRouter()
router.register(r'clientes',ClienteViewSet)
router.register(r'cliente', ClientViewSet,base_name = Client)
urlpatterns = [
    url(r'^api/',include(router.urls)),
    url(
        r'^panel/nota-ingreso/$',
        views.DepositSlipView.as_view(),
        name='nota-ingreso'
    ),
    url(
        r'^panel/envio/(?P<pk>\d+)/imprimir/$',
        views.EnvioPrintView.as_view(),
        name='print-envio'
    ),
    url(
        r'^panel/imprimir/nota-ingreso/(?P<pk>\d+)/$',
        views.ReportNotaView.as_view(),
        name='print-nota-ingreso'
    ),
    url(
        r'^panel/imprimir/guia/(?P<pk>\d+)/$',
        views.ReportGuiaView.as_view(),
        name='print-guia'
    ),
    url(
        r'^panel/imprimir/comprobante/(?P<pk>\d+)/$',
        views.ReportComprobanteView.as_view(),
        name='print-comprobante'
    ),
    url(
        r'^panel/entregar-envio/$',
        views.DeliverView.as_view(),
        name='lista_envio'
    ),
    url(
        r'^panel/entregar-envio/(?P<pk>\d+)/$',
        views.DetailDeliverView.as_view(),
        name='detalle_envio'
    ),
    # url para manteniminetos de sucursales
    url(
        r'^sucursales/listar/$',
        views.ListBranchView.as_view(),
        name='listar-branch'
    ),
    url(
        r'^sucursales/add/$',
        views.RegisterBranchView.as_view(),
        name='agregar-branch'
    ),
    url(
        r'^sucursales/update/(?P<pk>\d+)$',
        views.UpdateBranchView.as_view(),
        name='actualizar-branch'
    ),
    url(
        r'^sucursales/detail/(?P<pk>\d+)$',
        views.DetailBranchView.as_view(),
        name='detalle-branch'
    ),
    url(
        r'^sucursales/delete/(?P<pk>\d+)$',
        views.DeleteBranchView.as_view(),
        name='eliminar-branch'
    ),
]
