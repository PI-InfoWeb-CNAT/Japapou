from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore


@login_required
@permission_required('japapou.view_menu', login_url='login')
def client_menu_view(request):
    return render(request, "client/menu.html", status=200)
