from django.shortcuts import render, redirect  # type: ignore
from django.contrib.auth.decorators import permission_required, login_required

@login_required
@permission_required('japapou.view_customuser', login_url='home')
def delivery_man_profile_view(request):
    if request.user.tipo_usuario != 'DELIVERY_MAN':
        return redirect('home')

    return render(request, template_name="delivery_man/profile.html", status=200)
