from django.shortcuts import render  # type: ignore


def client_cart_view(request):
    return render(request, template_name="client/cart.html", status=200)
