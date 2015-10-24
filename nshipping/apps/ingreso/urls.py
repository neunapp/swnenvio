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

]
