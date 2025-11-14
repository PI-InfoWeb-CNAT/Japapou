from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import login_required

@login_required
def client_receipt_view(request):
    return render(request, template_name="client/receipt.html", status=200)
