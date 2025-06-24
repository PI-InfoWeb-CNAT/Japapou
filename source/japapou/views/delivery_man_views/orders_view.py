from django.shortcuts import render  # type: ignore


def delivery_man_orders_view(request):
    return render(request, template_name="delivery_man/orders.html", status=200)
