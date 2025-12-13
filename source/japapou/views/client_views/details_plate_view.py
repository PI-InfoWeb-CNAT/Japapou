from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Avg, Count
from japapou.models import Plate, PlateReview 
from japapou.forms import PlateReviewForm
from django.contrib import messages # Adicionado para mensagens de feedback
import json

@login_required
def rating_view(request, plate_id):
  plate = get_object_or_404(Plate, pk=plate_id)
  reviews = plate.avaliacoes_pratos.all().order_by('-created_at')
  average_rating_data = reviews.aggregate(average_rating=Avg('value'))
  average_rating_value = average_rating_data['average_rating'] or 0.0

  total_reviews = reviews.count()

  contagem_por_estrela = (
    PlateReview.objects
    .filter(plate=plate) # filtra apenas as avaliações daquele prato em especifico
    .values('value') # agrupa os dados pela coluna value
    .annotate(count=Count('value')) # aqui ele conta a quantidade de valores que existe em cada "value"
  )
  
  dados_contagem = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} # dicionario molde
  for item in contagem_por_estrela:
    # atualiza o dicionario molde com os valores reais
    dados_contagem[item['value']] = item['count']

  rating_distribution = []

  for i in range(5, 0, -1): # percoe a lista de tras pra frente, do maior para o menor
    count = dados_contagem[i]
    
    # Calcula a percentagem (evita divisão por zero)
    if total_reviews > 0:
      percentage = (count / total_reviews) * 100
    else:
      percentage = 0
      
    rating_distribution.append({
      'stars': i,     # O número (5, 4, 3, 2, 1)
      'count': count,   # A contagem (ex: 25)
      'percentage': int(percentage) # A percentagem (ex: 60.5)
    })
  
  if request.method == "POST":
    if not request.user.is_authenticated:
      return redirect('login') 
    form = PlateReviewForm(request.POST, request.FILES)

    if form.is_valid():
      # Verifica se o usuário JÁ avaliou este prato, para evitar duplicatas
      if not PlateReview.objects.filter(usuario=request.user, plate=plate).exists():
        review = form.save(commit=False)
        review.usuario = request.user
        review.plate = plate
        review.save()
        return redirect('details_plate', plate_id=plate.id)
      else:
        form.add_error(None, "Você já enviou uma avaliação para este prato.")
  
  else:
    form = PlateReviewForm()
  context = {
    'plate': plate,
    'reviews': reviews,
    'form': form,
    'average_rating': average_rating_value,
    'rating_distribution': rating_distribution,
    'next': request.GET.get('next', ''), # O .get() com '' evita erros se 'next' não existir
  }
  
  return render(request, template_name="client/rating.html", context=context, status=200)

@login_required
def details_plate_view(request, plate_id):
  plate = get_object_or_404(Plate, pk=plate_id)
  reviews = plate.avaliacoes_pratos.all().order_by('-created_at')
  average_rating_data = reviews.aggregate(average_rating=Avg('value'))
  average_rating_value = average_rating_data['average_rating'] or 0.0
  
  total_reviews = reviews.count()

  contagem_por_estrela = (
    PlateReview.objects
    .filter(plate=plate) # filtra apenas as avaliações daquele prato em especifico
    .values('value') # agrupa os dados pela coluna value
    .annotate(count=Count('value')) # aqui ele conta a quantidade de valores que existe em cada "value"
  )
  
  dados_contagem = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} # dicionario molde
  for item in contagem_por_estrela:
    # atualiza o dicionario molde com os valores reais
    dados_contagem[item['value']] = item['count']

  rating_distribution = []

  for i in range(5, 0, -1): # percoe a lista de tras pra frente, do maior para o menor
    count = dados_contagem[i]
    
    # Calcula a percentagem (evita divisão por zero)
    if total_reviews > 0:
      percentage = (count / total_reviews) * 100
    else:
      percentage = 0
      
    rating_distribution.append({
      'stars': i,     # O número (5, 4, 3, 2, 1)
      'count': count,   # A contagem (ex: 25)
      'percentage': int(percentage) # A percentagem (ex: 60.5)
    })

  if request.method == "POST":
    if not request.user.is_authenticated:
      return redirect('login') 
    form = PlateReviewForm(request.POST, request.FILES)

    if form.is_valid():
      # Verifica se o usuário JÁ avaliou este prato
      if not PlateReview.objects.filter(usuario=request.user, plate=plate).exists():
        review = form.save(commit=False)
        review.usuario = request.user
        review.plate = plate
        review.save()
        return redirect('details_plate', plate_id=plate.id)
      else:
        form.add_error(None, "Você já enviou uma avaliação para este prato.")
  
  else:
    form = PlateReviewForm()
  
  #print(rating_distribution)
  context = {
    'plate': plate,
    'reviews': reviews,
    'form': form,
    'average_rating': average_rating_value,
    'rating_distribution': rating_distribution,
    
  }
  return render(request, template_name="client/details_plate.html", context=context, status=200)

@login_required
def edit_review_view(request, review_id):
    """View para editar uma avaliação existente."""
    review = get_object_or_404(PlateReview, pk=review_id)
    plate_id = review.plate.id
    
    # 1. Verificar se o usuário é o dono da avaliação (Permissão)
    if review.usuario != request.user:
        messages.error(request, "Você não tem permissão para editar esta avaliação.")
        return redirect('details_plate', plate_id=plate_id)

    if request.method == "POST":
        # Usar instance=review para preencher e atualizar o formulário com a instância atual
        form = PlateReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Avaliação atualizada com sucesso!")
            return redirect('details_plate', plate_id=plate_id)
    else:
        # Preencher o formulário com os dados da avaliação existente
        form = PlateReviewForm(instance=review)
        
    context = {
        'plate': review.plate,
        'form': form,
        'editing': True, # Variável para indicar que é uma edição (pode ser útil no template)
        'review': review
    }
    
    # Reutilizar a template de rating (ou criar uma nova, se necessário)
    # Garanta que sua template rating.html use 'editing' para ajustar o texto do botão/título.
    return render(request, 'client/rating.html', context)


@login_required
def delete_review_view(request, review_id):
    """View para excluir uma avaliação existente."""
    review = get_object_or_404(PlateReview, pk=review_id)
    plate_id = review.plate.id
    
    # 1. Verificar se o usuário é o dono da avaliação (Permissão)
    if review.usuario != request.user:
        messages.error(request, "Você não tem permissão para excluir esta avaliação.")
        return redirect('details_plate', plate_id=plate_id)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Avaliação excluída com sucesso!")
        return redirect('details_plate', plate_id=plate_id)
    
    # Caso alguém tente acessar por GET (o que não deveria acontecer com o formulário)
    messages.error(request, "Método de requisição inválido.")
    return redirect('details_plate', plate_id=plate_id)