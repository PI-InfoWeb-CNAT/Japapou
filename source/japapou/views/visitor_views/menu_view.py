from django.shortcuts import render  # type: ignore


def visitor_menu_view(request):
    return render(request, template_name="visitor/menu.html", status=200)
