from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from japapou.forms import VisitorRegisterForm, DeliveryRegisterForm  # type: ignore
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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
            user.set_password(form.cleaned_data['password'])  # set_password para criar o hash da senha
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
    next_url = request.POST.get('next') or request.GET.get('next')
    print(f"next url:{next_url}")

    if request.method == "POST":
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
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
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("home")
            else:
                print(register_form.errors)
                register_error = "Erro ao cadastrar. Verifique os dados."

    return render(request, "visitor/login.html", {
        "login_form": login_form,
        "register_form": register_form,
        "login_error": login_error,
        "register_error": register_error,
        'next': request.GET.get('next', '') # O .get() com '' evita erros se 'next' não existir
    })



def logout_view(request):
    logout(request)
    return redirect("home")

@login_required(login_url="login_register")
def pagina_protegida(request):
    return HttpResponse(request, "<h1>Pagina protegida</h1>")