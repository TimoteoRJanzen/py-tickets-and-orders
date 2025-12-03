from django.db import transaction

from db.models import Ticket, Order, User


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    new_order = Order.objects.create(user=user)

    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=new_order,
            row=ticket["row"],
            seat=ticket["seat"],
        )


def get_orders(username: str = None) -> list:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
