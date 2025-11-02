from django.shortcuts import render  # type: ignore


def details_plate_view(request):
    return render(request, template_name="client/details_plate.html", status=200)
