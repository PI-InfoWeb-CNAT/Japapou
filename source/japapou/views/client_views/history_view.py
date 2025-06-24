from django.shortcuts import render  # type: ignore


def client_history_view(request):
    return render(request, template_name="client/history.html", status=200)
