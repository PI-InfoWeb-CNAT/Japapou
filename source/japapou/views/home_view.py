from django.shortcuts import render  # type: ignore


def home_view(request):
    return render(request, template_name="all/home.html", status=200)
