from django.shortcuts import render
from .models import Ticket
from .forms import TicketCreateForm


def ticket_create(request, *args, **kwargs):
    ticket = Ticket(request)

    if request.method == 'POST':
        form = TicketCreateForm(request.POST)

        if form.is_valid():
            ticket = form.save()

            for item in ticket:
                Ticket.objects.create(ticket=ticket,
                                      title=item.title,
                                      staff_id=item.staff_id,
                                      org_id=item.org_id,
                                      ticket_type=item.ticket_type)

                return render(
                    request,
                    'templates/ticket/created.html',
                    {'ticket': ticket}
                )
    else:
        form = TicketCreateForm()
        return render(
                    request,
                    'templates/ticket/created.html',
                    {'ticket': ticket, 'form': form},
                )