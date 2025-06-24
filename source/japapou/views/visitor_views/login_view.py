from django.shortcuts import render  # type: ignore


def visitor_login_view(request):
    return render(request, template_name="visitor/login.html", status=200)
