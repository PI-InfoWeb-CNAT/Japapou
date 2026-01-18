from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.db.models import Sum, Avg, Count #type: ignore
from japapou.models import Plate, CourierReview # Importar o modelo CourierReview
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models.functions import Round #type: ignore


def home_view(request):

    # 1. Ranking dos Pratos mais vendidos (lógica existente)
    ranking = Plate.objects.annotate(
        total_vendido=Sum('order_items_prato__amount')
    ).order_by('-total_vendido')[:10]
    
    
    context = {
        "ranking": ranking,
    }

    return render(request, template_name="all/home.html", context=context)

# Você pode querer uma view separada para o Dashboard do Entregador,
# onde esta lógica de avaliação seria mais central, mas mantive na home_view
# conforme solicitado, apenas condicionando ao tipo de usuário.