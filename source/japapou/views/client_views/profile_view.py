from django.shortcuts import render  # type: ignore


def client_profile_view(request):
    return render(request, template_name="client/profile.html", status=200)
