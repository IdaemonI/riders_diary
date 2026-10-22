from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm, TicketForm
from .models import Ticket, Category

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)

from .utils import is_manager

from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages


def home(request):
    return render(request, "home.html")


@login_required
def ticket_list(request):
    user = request.user
    if user.has_perm("tickets.change_ticket"):
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=user)

    tickets = tickets.select_related(
        "category",
        "created_by",
    ).prefetch_related("comments")

    search = request.GET.get("search")
    category = request.GET.get("category")
    status = request.GET.get("status")
    priority = request.GET.get("priority")
    sort = request.GET.get("sort")

    if search:
        tickets = tickets.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    if category:
        tickets = tickets.filter(category_id=category)

    if status:
        tickets = tickets.filter(status=status)

    if priority:
        tickets = tickets.filter(priority=priority)

    allowed_sorting = {
        "newest": "-created_at",
        "oldest": "created_at",
        "title": "title",
    }

    if sort in allowed_sorting:
        tickets = tickets.order_by(allowed_sorting[sort])

    paginator = Paginator(tickets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    query_params = request.GET.copy()
    query_params.pop("page", None)

    context = {
        "tickets": tickets,
        "categories": categories,
        "statuses": Ticket.STATUS_CHOICES,
        "priorities": Ticket.PRIORITY_CHOICES,
        "search": search,
        "current_status": status,
        "current_category": (int(category) if category else None),
        "current_priority": priority,
        "page_obj": page_obj,
        "context_query": query_params.urlencode(),
    }

    return render(request, "tickets/ticket_list.html", context)


@login_required
def ticket_detail(request, pk):
    user = request.user

    if is_manager(user):
        ticket = get_object_or_404(Ticket, pk=pk)
    else:
        ticket = get_object_or_404(
            Ticket,
            pk=pk,
            created_by=user,
        )

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.ticket = ticket
            comment.save()

            return redirect(
                "ticket_detail",
                pk=ticket.pk,
            )

    else:
        form = CommentForm()

    context = {
        "ticket": ticket,
        "form": form,
    }

    return render(request, "tickets/ticket_detail.html", context)


def about(request):
    return render(
        request,
        "about.html",
    )


def stats(request):
    tickets = Ticket.objects.all()

    total = len(tickets)
    new = 0
    in_progress = 0

    done = len([ticket for ticket in tickets if ticket.status == "done"])

    for ticket in tickets:
        if ticket.status == "new":
            new += 1

        if ticket.status == "in_progress":
            in_progress += 1

    context = {
        "total": total,
        "new": new,
        "in_progress": in_progress,
        "done": done,
    }

    return render(request, "stats.html", context)


from django.shortcuts import render, redirect
from .models import Ticket


@login_required
@permission_required(
    "tickets.add_ticket",
    raise_exception=True,
)
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Ticket succesfully created.")
            return redirect("ticket_list")

    else:
        form = TicketForm()

    return render(
        request,
        "tickets/ticket_form.html",
        {
            "form": form,
        },
    )


@login_required
@permission_required(
    "tickets.change_ticket",
    raise_exception=True,
)
def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)

        if form.is_valid():
            form.save()
            messages.success(request, "Ticket successfully updated.")
            return redirect(
                "ticket_detail",
                pk=ticket.pk,
            )
        messages.error(request, "Something went wrong.")
        messages.warning(request, "Please check the entered data.")

    else:
        form = TicketForm(instance=ticket)

    return render(
        request,
        "tickets/ticket_form.html",
        {
            "form": form,
        },
    )


@login_required
@user_passes_test(is_manager)
@permission_required(
    "tickets.delete_ticket",
    raise_exception=True,
)
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Ticket successfully deleted.")
        return redirect("ticket_list")

    return render(
        request,
        "tickets/ticket_confirm_delete.html",
        {"ticket": ticket},
    )


def ticket_close(request, pk):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, pk=pk)

        ticket.status = "done"
        ticket.save()

    return redirect("ticket_detail", pk)


def ticket_to_work(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":

        ticket.status = "in_progress"
        ticket.save()

    return redirect(
        "ticket_detail",
        ticket.pk,
    )


def category_list(request):
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }
    return render(request, "categories/category_list.html", context)


def category_tickets(request, pk):
    category = get_object_or_404(Category, pk=pk)

    tickets = category.tickets.all()

    context = {
        "category": category,
        "tickets": tickets,
    }

    return render(request, "categories/category_tickets.html", context)
