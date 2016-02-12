from django.conf.urls import url, patterns, include
from rest_framework import routers
from django.conf.urls import url
from .models import Manifest
from .viewsets import ManifestViewSet
from . import views


router = routers.SimpleRouter()
router.register(r'manifiesto', ManifestViewSet,base_name = Manifest)

urlpatterns = [
    url(r'^api/',include(router.urls)),
    url(
        r'^manifiesto/car/listar/$',
        views.ListCarView.as_view(),
        name='listar-carro'
    ),
    url(
        r'^manifiesto/car/add/$',
        views.RegisterCarView.as_view(),
        name='agregar-carro'
    ),
    url(
        r'^manifiesto/car/update/(?P<pk>\d+)/$',
        views.UpdateCarView.as_view(),
        name='actualizar-carro'
    ),
    url(
        r'^manifiesto/car/delete/(?P<pk>\d+)/$',
        views.DeleteCarView.as_view(),
        name='eliminar-carro'
    ),
    url(
        r'^manifiesto/car/detail/(?P<pk>\d+)/$',
        views.DetailCarView.as_view(),
        name='visualizar-carro'
    ),
    # url conductor
    url(
        r'^manifiesto/driver/listar/$',
        views.ListDriverView.as_view(),
        name='listar-conductor'
    ),
    url(
        r'^manifiesto/driver/add/$',
        views.RegisterDriverView.as_view(),
        name='agregar-conductor'
    ),
    url(
        r'^manifiesto/driver/update/(?P<pk>\d+)/$',
        views.UpdateDriverView.as_view(),
        name='actualizar-conductor'
    ),
    url(
        r'^manifiesto/driver/detail/(?P<pk>\d+)/$',
        views.DetailDriverView.as_view(),
        name='visualizar-conductor'
    ),
    url(
        r'^manifiesto/driver/delete/(?P<pk>\d+)/$',
        views.DeleteDriverView.as_view(),
        name='eliminar-conductor'
    ),
    # url para mantenimietno manifiesto
    url(
        r'^manifiesto/listar/$',
        views.ManifestList.as_view(),
        name='listar-manifiesto'
    ),
    url(
        r'^manifiesto/crear-manifiesto/$',
        views.ManifestView.as_view(),
        name='agregar-manifiesto'
    ),
    url(
        r'^manifiesto/update/(?P<pk>\d+)/$',
        views.UpdateManifest.as_view(),
        name='update-manifiesto'
    ),
    url(
        r'^manifiesto/full/(?P<pk>\d+)/$',
        views.FullManifestView.as_view(),
        name='full-manifiesto'
    ),
    url(
        r'^manifiesto/delete/(?P<pk>\d+)/$',
        views.AnulateManifestView.as_view(),
        name='eliminar-manifiesto'
    ),
    url(
        r'^manifiesto/ver/(?P<pk>\d+)/$',
        views.DetailManifestView.as_view(),
        name='visualizar-manifiesto'
    ),
    url(
        r'^manifiesto/crear-manifiesto/sub-contrata$',
        views.ThirdManifestView.as_view(),
        name='agregar-sub_contrata'
    ),
    url(
        r'^manifiesto/completar-manifiesto/(?P<pk>\d+)/$',
        views.Complete_Manifest.as_view(),
        name='completar-manifiesto'
    ),
    # url para reportes manifiesto
    url(
        r'^manifiesto/crear-remision/(?P<pk>\d+)/$',
        views.RemissionView.as_view(),
        name='register-remission'
    ),
    url(
        r'^manifiesto/reporte-manifiesto/(?P<pk>\d+)/$',
        views.ReportManifest.as_view(),
        name='reporte-manifiesto'
    ),
    url(
        r'^manifiesto/detalle-manifiesto/(?P<pk>\d+)/(?P<br>\d+)/$',
        views.ReportDetailManifest.as_view(),
        name='detalle-manifiesto'
    ),
    # url para rececpcionde notas de ingreso
    url(
        r'^manifiesto/recepcion/lista/$',
        views.Manifest_no_Reception.as_view(),
        name='manifiesto-no-recepcionado'
    ),
    url(
        r'^manifiesto/recepcion/registrar/(?P<pk>\d+)/$',
        views.Slip_Reception.as_view(),
        name='registrar-recepcion'
    ),
]
