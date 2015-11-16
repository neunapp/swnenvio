from django.conf.urls import url
from . import views

urlpatterns = [     
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
    #url conductor
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
    #url para mantenimietno manifiesto
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
        views.UpdateManifestView.as_view(),
        name='actualizar-manifiesto'
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
        name='agregar-sub contrata'
    ),
    #url para reportes manifiesto
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
        views.ReportDetailM.as_view(),
        name='detalle-manifiesto'
    ),
]
