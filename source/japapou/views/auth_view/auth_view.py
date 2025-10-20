from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from japapou.forms import VisitorRegisterForm, DeliveryRegisterForm  # type: ignore


def delivery_man_register_view(request):
    '''
        View para registro de entregadores (Gerente que registra entregadores).
    '''
    form = DeliveryRegisterForm()

    if request.method == "POST":
        #print(request.POST)
        
        form = DeliveryRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Salva o usuário, mas não faz commit no banco ainda
            user.tipo_usuario = 'DELIVERY_MAN'  # Define o tipo de usuário como ENTREGADOR
            user.set_password(form.cleaned_data['password'])  # Hash da senha
            user.save()  # Agora faz o commit no banco
            login(request, user)
            return redirect("home")
        else:
            print(form.errors)
            form = DeliveryRegisterForm()

    return render(request, "manager/register_delivery_man.html", context={'form': form})

def login_register_view(request):
    '''
        View para login e registro de visitantes (clientes).
    '''
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
            #print(request.POST)
            register_form = VisitorRegisterForm(request.POST)
            if register_form.is_valid():

                user = register_form.save(commit=False) # Salva o usuário, mas não faz commit no banco ainda
                user.tipo_usuario = 'CLIENT'  # Define o tipo de usuário como CLIENTE
                user.set_password(register_form.cleaned_data['password'])  # Hash da senha
                user.save()  # Agora faz o commit no banco

                login(request, user)
                return redirect("home")
            else:
                print(register_form.errors)
                register_error = "Erro ao cadastrar. Verifique os dados."

    return render(request, "visitor/login.html", {
        "login_form": login_form,
        "register_form": register_form,
        "login_error": login_error,
        "register_error": register_error,
    })



def logout_view(request):
    logout(request)
    return redirect("home")