from django.shortcuts import render, redirect  # type: ignore
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from japapou.models import CustomUser 
import json


@permission_required(['japapou.view_customuser', 'japapou.change_customuser'], login_url='home')
def manager_profile_view(request):
    return render(request, template_name="japapou/templates/manager/profile.html", status=200)

@login_required
def manager_profile_view(request):
    return render(request, "manager/profile.html", {"user": request.user})

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
                return JsonResponse({"status": "erro", "mensagem": f"Campo '{field}' inválido"})
        except Exception as e:
            print("Erro update_user:", e)
            return JsonResponse({"status": "erro", "mensagem": str(e)})
    return JsonResponse({"status": "erro", "mensagem": "Método inválido"})

@login_required
def update_photo(request):
    if request.method == "POST":
        try:
            foto = request.FILES.get("foto")
            user_id = request.POST.get("id")
            user = CustomUser.objects.get(id=user_id)
            if foto:
                user.foto_perfil = foto
                user.save()
                return JsonResponse({
                    "status": "ok",
                    "nova_foto_url": user.foto_perfil.url
                })
            else:
                return JsonResponse({"status": "erro", "mensagem": "Nenhuma foto enviada"})
        except Exception as e:
            print("Erro update_photo:", e)
            return JsonResponse({"status": "erro", "mensagem": str(e)})
    return JsonResponse({"status": "erro", "mensagem": "Método inválido"})
