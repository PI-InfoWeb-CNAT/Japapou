from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required  # type: ignore
from japapou.forms import VisitorRegisterForm  # type: ignore

@login_required
@permission_required('japapou.view_customuser', login_url='login')
def client_profile_view(request):
    if not request.user.tipo_usuario == "CLIENT":
        return redirect("login")  # Redireciona se não for cliente


    user = request.user
    if request.method == "POST":
        form = VisitorRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redireciona após salvar
    else:
        form = VisitorRegisterForm(instance=user)
    return render(request, "client/profile.html", {"form": form, "user": user})
