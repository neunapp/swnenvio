from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^salidas/add/$',
        views.RegisterExpenditur.as_view(),
        name='agregar-egreso'
    ),
    url(
        r'^salidas/ver/(?P<pk>\d+)/$',
        views.DetailExpenditur.as_view(),
        name='visualizar-egreso'
    ),
    url(
        r'^salidas/listar/$',
        views.ListExpenditur.as_view(),
        name='listar-egreso'
    ),
    url(
        r'^salidas/anular/(?P<pk>\d+)/$',
        views.AnulateExpenditur.as_view(),
        name='anular-egreso'
    ),
    url(
        r'^salidas/reporte/lista/(?P<pk>\d+)/$',
        views.CountableCahs.as_view(),
        name='reporte-salidas'
    ),
    url(
        r'^salidas/reporte/lista/$',
        views.ListActives.as_view(),
        name='users-activos'
    ),
]
