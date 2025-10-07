from django.shortcuts import render  # type: ignore
from japapou.models.plate import Plate
from django.db.models import Sum #type: ignore


def home_view(request):
    ranking = Plate.objects.annotate(total_vendido=Sum('items__amount')).order_by('-total_vendido')[:10]

    print(Plate.objects.annotate(total_vendido=Sum('items__amount')).order_by('-total_vendido')[:10])

    return render(request, template_name="all/home.html", context={"ranking":ranking})
