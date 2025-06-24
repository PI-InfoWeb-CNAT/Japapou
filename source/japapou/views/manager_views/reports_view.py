from django.shortcuts import render  # type: ignore


def manager_reports_view(request):
    return render(request, template_name="manager/reports.html", status=200)
