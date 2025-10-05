from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore


@login_required
@permission_required('japapou.view_order', login_url='login')
def client_order_view(request):
    if request.user.tipo_usuario != "CLIENT":
        return render(request, "403.html", status=403)

    return render(request, template_name="client/order.html", status=200)
