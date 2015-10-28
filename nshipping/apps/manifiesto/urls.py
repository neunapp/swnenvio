from django.conf.urls import url
from . import views

urlpatterns = [
    #url vehiculo     
    url(
        r'^manifiesto/car/listar$',
        views.ListCarView.as_view(),
        name='listar-carro'
    ),
    url(
        r'^manifiesto/car/add$',
        views.RegisterCarView.as_view(),
        name='agregar-carro'
    ),
    url(
        r'^manifiesto/car/update/(?P<pk>\d)$',
        views.UpdateCarView.as_view(),
        name='actualizar-carro'
    ),
    url(
        r'^manifiesto/car/delete/(?P<pk>\d)$',
        views.DeleteCarView.as_view(),
        name='eliminar-carro'
    ),
    #url conductor
    url(
        r'^manifiesto/driver/listar$',
        views.ListDriverView.as_view(),
        name='listar-conductor'
    ),
    url(
        r'^manifiesto/driver/add$',
        views.RegisterDriverView.as_view(),
        name='agregar-conductor'
    ),
    url(
        r'^manifiesto/driver/update/(?P<pk>\d)$',
        views.UpdateDriverView.as_view(),
        name='actualizar-conductor'
    ),
    url(
        r'^manifiesto/driver/delete/(?P<pk>\d)$',
        views.DeleteDriverView.as_view(),
        name='eliminar-conductor'
    ),
    #url para la tabla mnifiesto
    url(
        r'^manifiesto/crear-manifiesto$',
        views.RegisterManifest.as_view(),
        name='register-manifest'
    ),
]
