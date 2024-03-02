from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^create_ticket/$', views.create_ticket, name='create_ticket'),
    url(r'^edit_ticket/$', views.edit_ticket, name='edit_ticket'),
    url(r'^delete_ticket/$', views.delete_ticket, name='delete_ticket')
)