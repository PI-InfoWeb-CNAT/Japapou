from django.shortcuts import render  # type: ignore
from japapou.models import Plate


def manager_plates_view(request):
    plates = Plate.objects.all()

    context = {
        "plates": plates,
    }

    return render(
        request,
        template_name="manager/manage_plates.html",
        status=200,
        context=context,
    )
