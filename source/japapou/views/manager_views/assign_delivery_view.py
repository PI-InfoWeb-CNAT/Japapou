from django.shortcuts import render  # type: ignore


def manager_assign_delivery_view(request):
    return render(request, template_name="manager/assign_delivery.html", status=200)
