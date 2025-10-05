from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required # type: ignore


@login_required
@permission_required('japapou.view_order_delivery', login_url='home')
def delivery_man_orders_view(request):
    if request.user.tipo_usuario != "DELIVERY_MAN":
        return redirect("home")

    return render(request, template_name="delivery_man/orders.html", status=200)
