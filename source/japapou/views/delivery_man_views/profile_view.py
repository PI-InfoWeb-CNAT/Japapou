from django.shortcuts import render  # type: ignore


def delivery_man_profile_view(request):
    return render(request, template_name="delivery_man/profile.html", status=200)
