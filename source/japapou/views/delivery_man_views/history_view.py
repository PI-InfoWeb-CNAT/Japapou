from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore


@login_required
def delivery_man_history_view(request):
    if request.user.tipo_usuario != "DELIVERY_MAN":
        return redirect("home")

    ''' REPENSAR MELHOR ESSA VIEW, PARA EXIBIR O HISTORICO DE ENTREGAS DO ENTREGADOR LOGADO '''

    return render(request, template_name="delivery_man/history.html", status=200)
