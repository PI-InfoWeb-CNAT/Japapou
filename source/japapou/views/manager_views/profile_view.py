from django.shortcuts import render  # type: ignore


def manager_profile_view(request):
    return render(request, template_name="manager/profile.html", status=200)
