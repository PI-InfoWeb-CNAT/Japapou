from django.shortcuts import render  # type: ignore


def delivery_man_history_view(request):
    return render(request, template_name="delivery_man/history.html", status=200)
