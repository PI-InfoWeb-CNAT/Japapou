from django.shortcuts import render  # type: ignore


def delivery_man_deliver_view(request):
    return render(request, template_name="delivery_man/deliver.html", status=200)
