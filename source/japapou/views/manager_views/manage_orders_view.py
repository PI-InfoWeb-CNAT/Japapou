from django.shortcuts import render  # type: ignore


def manager_orders_view(request):
    return render(request, template_name="manager/manage_orders.html", status=200)
