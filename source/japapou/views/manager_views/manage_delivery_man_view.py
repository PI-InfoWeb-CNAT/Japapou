from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import permission_required, login_required


@login_required
@permission_required('japapou.view_customuser', login_url='home')
def manager_manage_delivery_man_view(request):
    if request.user.tipo_usuario != 'MANAGER':
        return render(request, template_name="404.html", status=404)

    return render(request, template_name="manager/manage_delivery_man.html", status=200)
