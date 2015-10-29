from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^perfil/listar$',
        views.ListProfile.as_view(),
        name='listar-profile'
    ),
    url(
        r'^perfil/agregar$',
        views.RegisterProfile.as_view(),
        name='agregar-profile'
    ),
    url(
        r'^perfil/actualizar/(?P<pk>\d+)$',
        views.UpdateProfile.as_view(),
        name='actualizar-profile'
    ),
]