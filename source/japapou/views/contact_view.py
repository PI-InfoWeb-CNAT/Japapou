from django.shortcuts import render  # type: ignore


def contact_view(request):
    return render(request, template_name="all/contact.html", status=200)
