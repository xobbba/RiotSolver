from django import forms
from .models import Ticket


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'staff_id', 'org_id', 'ticket_type']