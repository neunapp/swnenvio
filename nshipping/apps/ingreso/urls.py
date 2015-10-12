from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^nota-de-ingreso/$',
        views.RegisterSlipView.as_view(),
        name='nota-ingreso'
    ),
]
