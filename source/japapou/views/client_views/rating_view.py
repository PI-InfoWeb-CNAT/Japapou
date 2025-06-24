from django.shortcuts import render  # type: ignore


def client_rating_view(request):
    return render(request, template_name="client/rating.html", status=200)
