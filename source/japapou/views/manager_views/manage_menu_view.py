from django.shortcuts import render  # type: ignore


def manager_manage_menu_view(request):
    return render(request, template_name="manager/manage_menu.html", status=200)
