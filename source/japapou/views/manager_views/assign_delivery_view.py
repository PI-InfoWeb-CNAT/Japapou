from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import permission_required, login_required


@login_required
@permission_required('view_order', login_url='home')
def manager_assign_delivery_view(request):
    return render(request, template_name="manager/assign_delivery.html", status=200)
