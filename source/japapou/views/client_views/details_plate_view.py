from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from japapou.models import Plate, PlateReview # Importando os modelos
from japapou.forms import PlateReviewForm # Importando o formulário

# ATENÇÃO: Sua view agora precisa receber o ID do prato.
# Você precisará atualizar sua urls.py para algo como:


def details_plate_view(request, plate_id):
    # 1. Busca o prato ou retorna 404
    plate = get_object_or_404(Plate, pk=plate_id)
    
    # 2. Busca as avaliações existentes para este prato
    reviews = plate.avaliacoes_pratos.all().order_by('-created_at')
    
    # 3. Processa o formulário (POST)
    if request.method == "POST":
        # Um usuário deve estar logado para avaliar
        if not request.user.is_authenticated:
            # Você deve ter uma URL de login com o name='login'
            return redirect('login') 

        form = PlateReviewForm(request.POST, request.FILES)
        
        if form.is_valid():
            # O modelo PlateReview tem uma restrição 'unique_user_plate_review'
            # Vamos verificar se o usuário já avaliou
            if not PlateReview.objects.filter(usuario=request.user, plate=plate).exists():
                review = form.save(commit=False)
                review.usuario = request.user
                review.plate = plate
                review.save()
                # Redireciona para a mesma página, mostrando a nova avaliação
                return redirect('details_plate', plate_id=plate.id)
            else:
                # Adiciona um erro caso o usuário já tenha avaliado
                form.add_error(None, "Você já enviou uma avaliação para este prato.")
    
    # 4. Exibe a página (GET)
    else:
        form = PlateReviewForm()

    # 5. Monta o contexto para o template
    context = {
        'plate': plate,
        'reviews': reviews,
        'form': form
    }
    
    # 6. Renderiza o template
    return render(request, template_name="client/details_plate.html", context=context, status=200)