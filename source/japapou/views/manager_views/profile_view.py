from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import render
from japapou.models import CustomUser
import json


@login_required
# @permission_required(['japapou.view_customuser', 'japapou.change_customuser'], raise_exception=True)
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

			if field == "senha":
				if value:
					user.set_password(value)
					user.save()
					update_session_auth_hash(request, user)  # 👈 mantém logado
					return JsonResponse({"status": "ok"})
				else:
					return JsonResponse({"status": "erro", "mensagem": "Senha não pode ser vazia"})
				
			elif hasattr(user, field):
				# 💡 CORREÇÃO AQUI: Se o valor for uma string vazia, salva como None
				if value == "":
					value = None
				
				setattr(user, field, value)
				user.save()
				return JsonResponse({"status": "ok"})

			elif hasattr(user, field):
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
			user_id = request.POST.get("id")
			user = CustomUser.objects.get(id=user_id)

			# Verifica se é remoção
			if request.POST.get("remover") == "true":
				user.foto_perfil = None
				user.save()
				return JsonResponse({
					"status": "ok",
					"nova_foto_url": "/static/imgs/manager/profile.png"
				})

			# Caso contrário, upload normal
			foto = request.FILES.get("foto")
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

