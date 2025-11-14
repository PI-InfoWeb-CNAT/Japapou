from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Avg # <<-- Adicione esta importação
from japapou.models import Plate, PlateReview 
from japapou.forms import PlateReviewForm

@login_required
def rating_view(request, plate_id):
    plate = get_object_or_404(Plate, pk=plate_id)
    reviews = plate.avaliacoes_pratos.all().order_by('-created_at')
    average_rating_data = reviews.aggregate(average_rating=Avg('value'))
    average_rating_value = average_rating_data['average_rating'] or 0.0
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login') 
        form = PlateReviewForm(request.POST, request.FILES)

        if form.is_valid():
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
        'next': request.GET.get('next', ''), # O .get() com '' evita erros se 'next' não existir
    }
    
    return render(request, template_name="client/rating.html", context=context, status=200)

@login_required
def details_plate_view(request, plate_id):
    plate = get_object_or_404(Plate, pk=plate_id)
    reviews = plate.avaliacoes_pratos.all().order_by('-created_at')
    average_rating_data = reviews.aggregate(average_rating=Avg('value'))
    average_rating_value = average_rating_data['average_rating'] or 0.0
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login') 
        form = PlateReviewForm(request.POST, request.FILES)

        if form.is_valid():
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
        
    }
    return render(request, template_name="client/details_plate.html", context=context, status=200)
