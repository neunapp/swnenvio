from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^salidas/add/$',
        views.RegisterExpenditur.as_view(),
        name='agregar-egreso'
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
]
