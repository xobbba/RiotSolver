from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager)
from ..authentication.models import (Organization, User)


class TicketManager(BaseUserManager):
    def create_ticket(self, staff_id, org_id, ticket_type):
        if not staff_id and not org_id and not ticket_type:
            raise Exception('Незаполнены обязательные поля')

        ticket = self.model()


class TicketType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=256)


class Ticket(models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, null=False)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    org_id = models.ForeignKey(Organization.org_id, on_delete=models.CASCADE, null=False)
    ticket_type = models.ForeignKey(TicketType.type_id, on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created',]
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return 'Заявка'.format(self.ticket_id)

    def __unicode__(self):
        return self.ticket_id


class Document(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models)
    html_result_link = models.CharField(max_length=256)
    pdf_result_link = models.CharField(max_length=256)
    created_date = models.DateTimeField()