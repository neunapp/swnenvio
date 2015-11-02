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
    #url para la tabla mnifiesto
    url(
        r'^manifiesto/crear-manifiesto/$',
        views.RegisterManifestView.as_view(),
        name='register-manifiesto'
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
