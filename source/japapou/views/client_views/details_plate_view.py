from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from japapou.models import Plate, PlateReview 
from japapou.forms import PlateReviewForm 


def details_plate_view(request, plate_id):
    plate = get_object_or_404(Plate, pk=plate_id)
    reviews = plate.avaliacoes_pratos.all().order_by('-created_at')
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
        'form': form
    }
    
    return render(request, template_name="client/details_plate.html", context=context, status=200)
