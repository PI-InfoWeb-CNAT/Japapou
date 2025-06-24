from django.shortcuts import render  # type: ignore


def manager_orders_view(request):
    return render(request, template_name="manager/orders.html", status=200)
