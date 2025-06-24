from django.shortcuts import render  # type: ignore


def manager_history_view(request):
    return render(request, template_name="manager/history.html", status=200)
