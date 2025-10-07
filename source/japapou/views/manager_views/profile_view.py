from django.shortcuts import render, redirect  # type: ignore
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from japapou.models import CustomUser 
import json


@permission_required(['japapou.view_customuser', 'japapou.change_customuser'], login_url='home')
def manager_profile_view(request):
    return render(request, template_name="manager/profile.html", status=200)

# Adicione a linha a seguir
@login_required
# Até aqui
def edit_produto_view(request, id=None):
    users = CustomUser.objects.all()
    if id is not None:
        users = users.filter(id=id)
    user = users.first()
    print(user)
    #adicione a lista de fabricantes e categorias no context
    context = {'user': user}
    return render(request, template_name='produto/produto-edit.html', context=context, status=200)

@login_required
def edit_produto_postback(request, id=None):
    # Processa o post back gerado pela action
    if request.method == 'POST':
        id = request.POST.get("id")
        obj_user = CustomUser.objects.filter(id=id).first()
        if not obj_user:
            return JsonResponse({"status": "erro", "mensagem": "Usuário não encontrado"})
        nome = request.POST.get("nome")
        username = request.POST.get("username")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        endereco = request.POST.get("endereco")
        cpf = request.POST.get("CPF")
        data_nascimento = request.POST.get("data_nascimento")
        foto_perfil = request.FILES.get("foto")
        # se entregador
        if obj_user.tipo_usuario == 'DELIVERY_MAN':
            cnh = request.POST.get("cnh")
            modelo_moto = request.POST.get("modelo_moto")
            cor_moto = request.POST.get("cor_moto")
            Placa_moto = request.POST.get("Placa_moto")
        print("postback")
        print(id)
        print(nome)
        print(username)
        print(telefone)
        print(endereco)
        print(cpf)
        print(data_nascimento)
        print(foto_perfil)
        if obj_user.tipo_usuario == 'DELIVERY_MAN':
            print(cnh)
            print(modelo_moto)
            print(cor_moto)
            print(Placa_moto)
        try:
            obj_user.nome = nome
            obj_user.username = username
            obj_user.email = email
            obj_user.telefone = telefone
            obj_user.endereco = endereco
            obj_user.cpf = cpf 
            obj_user.data_nascimento = data_nascimento 
            obj_user.foto_perfil = foto_perfil 
            # Se entregador
            if obj_user.tipo_usuario == 'DELIVERY_MAN':
                obj_user.cnh = cnh
                obj_user.modelo_moto = modelo_moto
                obj_user.cor_moto = cor_moto
                obj_user.Placa_moto = Placa_moto
            if username is not None:
                obj_user.username = username
                obj_user.save()
                print("Infomações %s salvas com sucesso" % username)
        except Exception as e:
            print("Erro ao salvar edição: %s" % e)
    return redirect("/profile")

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required
def update_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("id")
            field = data.get("field")
            value = data.get("value")

            user = CustomUser.objects.get(id=user_id)

            if hasattr(user, field):
                setattr(user, field, value)
                user.save()
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"status": "erro", "mensagem": "Campo inválido"})

        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)})

    return JsonResponse({"status": "erro", "mensagem": "Requisição inválida"})

@login_required
def update_photo(request):
    if request.method == 'POST':
        user = request.user  # ou use request.POST.get("id") se quiser editar outro usuário
        foto = request.FILES.get('foto')

        if foto:
            user.foto_perfil = foto
            user.save()
            return JsonResponse({
                'status': 'ok',
                'nova_foto_url': user.foto_perfil.url  # caminho da nova imagem
            })
        else:
            return JsonResponse({'status': 'erro', 'mensagem': 'Nenhuma imagem enviada'})
    return JsonResponse({'status': 'erro', 'mensagem': 'Requisição inválida'})

