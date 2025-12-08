from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.db.models import Sum, Avg, Count #type: ignore
from japapou.models import Plate, CourierReview # Importar o modelo CourierReview
from django.contrib.auth.decorators import login_required # type: ignore
# Assumindo que PlateReviewForm e PlateReview não são usados nesta view

def home_view(request):
    # 1. Ranking dos Pratos mais vendidos (lógica existente)
    ranking = Plate.objects.annotate(
        total_vendido=Sum('order_items_prato__amount')
    ).order_by('-total_vendido')[:10]
    
    # 2. Média de Avaliações do Entregador Logado
    average_courier_rating = None
    total_courier_reviews = 0
    
    # Verifica se o usuário está logado E se ele é um Entregador
    if request.user.is_authenticated and request.user.tipo_usuario == 'DELIVERY_MAN':
        entregador = request.user
        
        # Usa o related_name="avaliacoes_recebidas" definido no modelo CourierReview
        reviews = entregador.avaliacoes_recebidas.all()
        total_courier_reviews = reviews.count()
        
        if total_courier_reviews > 0:
            average_rating_data = reviews.aggregate(average_rating=Avg('value'))
            average_courier_rating = average_rating_data['average_rating']
            
    # O restante do código da sua view original estava incorreto ou incompleto.
    # Por exemplo, "entregador = get_object_or_404(Plate, pk=plate_id)" não fazia sentido 
    # aqui, pois a Home View não recebe 'plate_id'. 
    
    context = {
        "ranking": ranking,
        "average_courier_rating": average_courier_rating,
        "total_courier_reviews": total_courier_reviews,
    }

    return render(request, template_name="all/home.html", context=context)

# Você pode querer uma view separada para o Dashboard do Entregador,
# onde esta lógica de avaliação seria mais central, mas mantive na home_view
# conforme solicitado, apenas condicionando ao tipo de usuário.