from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore


@login_required
def client_cart_view(request):
    if request.user.tipo_usuario != "CLIENT":
        return redirect('home')

    return render(request, "client/cart.html", status=200)
