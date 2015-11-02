from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^errors/$',
        views.ErrorView.as_view(),
        name='errors'
    ),
    url(
        r'^nota-de-ingreso/$',
        views.RegisterSlipView.as_view(),
        name='nota-ingreso'
    ),
    url(
        r'^entrega-de-paquetes/$',
        views.DeliverView.as_view(),
        name='entrega-paquete'
    ),
    url(
        r'^entrega/detalle/(?P<pk>\d+)$',
        views.DetailDeliverView.as_view(),
        name='detalle_entrega'
    ),
#url para manteniminetos de sucursales
    url(
        r'^sucursales/listar/$',
        views.ListBranch.as_view(),
        name='listar-branch'
    ),
    url(
        r'^sucursales/add/$',
        views.RegisterBranch.as_view(),
        name='agregar-branch'
    ),
    url(
        r'^sucursales/update/(?P<pk>\d+)$',
        views.UpdateBranch.as_view(),
        name='actualizar-branch'
    ),
]
