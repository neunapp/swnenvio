from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^ingreso/$',
        views.RegisterSlipView.as_view(),
        name='registro'
    ),
]
