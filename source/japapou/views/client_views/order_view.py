from django.shortcuts import render  # type: ignore


def client_order_view(request):
    return render(request, template_name="client/order.html", status=200)
