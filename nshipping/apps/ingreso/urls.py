from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^panel/nota-ingreso/$',
        views.DepositSlipView.as_view(),
        name='nota-ingreso'
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
