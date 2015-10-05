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
        r'^panel/usuario/$',
        views.PanelView.as_view(),
        name='panel'
    ),
]
