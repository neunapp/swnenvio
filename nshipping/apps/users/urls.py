from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^$',
        views.LogIn.as_view(),
        name='login'
    ),
    url(
        r'^users/salir/$',
        'apps.users.views.LogOut',
        name='logout'
    ),
    url(
        r'^panel/$',
        views.PanelView.as_view(),
        name='panel'
    ),
    url(
        r'^panel/usuario/entrega-envio/$',
        views.Panel2View.as_view(),
        name='entrega_envio'
    ),
    url(
        r'^panel/usuario/entrega-envio/100/$',
        views.Panel3View.as_view(),
        name='entrega_detalle'
    ),
]
