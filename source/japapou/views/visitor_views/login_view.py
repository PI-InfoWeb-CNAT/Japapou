
from django.contrib.auth import authenticate, login # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from japapou.forms import VisitorRegisterForm  # type: ignore

def visitor_login_register_view(request):
    login_form = AuthenticationForm()
    register_form = VisitorRegisterForm()
    login_error = None
    register_error = None

    if request.method == "POST":
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("home")
            else:
                login_error = "Usuário ou senha inválidos."
        elif 'register_submit' in request.POST:
            register_form = VisitorRegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect("home")
            else:
                register_error = "Erro ao cadastrar. Verifique os dados."

    return render(request, "visitor/login.html", {
        "login_form": login_form,
        "register_form": register_form,
        "login_error": login_error,
        "register_error": register_error,
    })
