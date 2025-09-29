from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from japapou.forms import VisitorRegisterForm  # type: ignore

@login_required
def client_profile_view(request):
    user = request.user
    if request.method == "POST":
        form = VisitorRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redireciona após salvar
    else:
        form = VisitorRegisterForm(instance=user)
    return render(request, "client/profile.html", {"form": form, "user": user})
