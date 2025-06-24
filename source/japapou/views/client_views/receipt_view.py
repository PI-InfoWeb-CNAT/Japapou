from django.shortcuts import render  # type: ignore


def client_receipt_view(request):
    return render(request, template_name="client/receipt.html", status=200)
