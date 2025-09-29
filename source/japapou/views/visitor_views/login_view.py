from django.contrib.auth import authenticate, login # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from japapou.forms import VisitorRegisterForm  # type: ignore

def visitor_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # Redireciona após login
    else:
        form = AuthenticationForm()
    return render(request, "visitor/login.html", {"form": form})

def visitor_register_view(request):
    if request.method == "POST":
        form = VisitorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redireciona para a página de home após o registro bem-sucedido
    else:
        form = VisitorRegisterForm()
    return render(request, template_name="client/login.html", context={"form": form} ,status=200)
