from django.shortcuts import render  # type: ignore


def manager_manage_delivery_man_view(request):
    return render(request, template_name="manager/manage_delivery_man.html", status=200)
