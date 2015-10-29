from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # urls para la aplicacion users
    url(r'^', include('apps.users.urls', namespace="users_app")),
    # urls para la aplicacion de ingreso
    url(r'^', include('apps.ingreso.urls', namespace="ingreso_app")),
    # urls para la aplicacion de manifiesto
    url(r'^', include('apps.manifiesto.urls', namespace="manifiesto_app")),
    # urls para la aplicacion de perfiles
    url(r'^', include('apps.profiles.urls', namespace="profiles_app")),
    # urls para la aplicacion de salida
    url(r'^', include('apps.salida.urls', namespace="salida_app")),

    url(r'^admin/', include(admin.site.urls)),
]
