from django.shortcuts import render  # type: ignore


def manager_dashboard_view(request):
    return render(request, template_name="manager/dashboard.html", status=200)
