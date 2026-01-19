from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.db.models import Sum, Avg, Count #type: ignore
from japapou.models import Plate, CourierReview # Importar o modelo CourierReview
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models.functions import Round #type: ignore

def media_estrelas_entregador(request):
    """Context processor para calcular a média de avaliações do entregador logado."""
    media_entregador = None

    if request.user.is_authenticated and request.user.tipo_usuario == 'DELIVERY_MAN':
        entregador = request.user

        # Usa o related_name="avaliacoes_recebidas" definido no modelo CourierReview
        reviews = entregador.avaliacoes_recebidas.all()
        total_courier_reviews = reviews.count()
        
        if total_courier_reviews > 0:
            average_rating_data = reviews.aggregate(average_rating=Avg('value'))
            average_courier_rating = average_rating_data['average_rating']
            
            media_entregador = round(average_courier_rating, 2)
        else:
            media_entregador = 0

    return {'media_entregador': media_entregador}