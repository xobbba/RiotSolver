from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^createTicket/$', views.ticket_create, name='ticket_create')
)