from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import permission_required



@permission_required(['japapou.view_customuser', 'japapou.change_customuser'], login_url='home')
def manager_profile_view(request):
    return render(request, template_name="manager/profile.html", status=200)
