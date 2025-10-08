from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from japapou.models import CustomUser
from japapou.forms import DeliveyrRegisterForm
from django.urls import reverse
from django.http import JsonResponse




@login_required
@permission_required('japapou.change_customuser', login_url='home')
def edit_delivery_man_view(request, id):
    delivery_man = get_object_or_404(CustomUser, pk=id, tipo_usuario='DELIVERY_MAN')

    if request.method == "POST":
        form = DeliveyrRegisterForm(request.POST, request.FILES, instance=delivery_man)
        if form.is_valid():
            delivery_user = form.save(commit=False)
            delivery_user.tipo_usuario = 'DELIVERY_MAN'
            if form.cleaned_data.get("password"):
                delivery_user.set_password(form.cleaned_data["password"])
            delivery_user.save()
            messages.success(request, "Entregador atualizado com sucesso.")
            return redirect("manage_delivery_man")
    else:
        form = DeliveyrRegisterForm(instance=delivery_man)

    return render(request, "edit_delivery_man.html", {"form": form, "delivery_man": delivery_man})

