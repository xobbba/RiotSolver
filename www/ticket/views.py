from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from .models import Ticket
from .forms import TicketCreateForm, TicketEditForm


def create_ticket(request, *args, **kwargs):
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


def edit_ticket(request, ticket_id):
    data = Ticket.objects.get(ticket_id=ticket_id)

    if request.POST:
        form = TicketEditForm(request.POST, instance=data)
        if form.is_valid():
            form.save()

            return redirect('index')
    else:
        form = TicketEditForm(instance=data)

        return render(
            request,
            'templates/ticket/ticket_edit.html',
            {'form': form}
        )


def delete_ticket(request, ticket_id):
    if request.POST:
        Ticket.objects.delete(ticket_id=ticket_id)

        return redirect('index')


def all_tickets(request):
    tickets = Ticket.objects.all()

    return render_to_response(
        '/all_tickets.html',
        {'tickets': tickets},
        context_instance=RequestContext(request)
    )
