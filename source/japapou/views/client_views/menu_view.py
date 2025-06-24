from django.shortcuts import render  # type: ignore


def client_menu_view(request):
    return render(request, template_name="client/menu.html", status=200)
