from django import forms
from japapou.views.manager_views import manage_menu_view
from django.contrib.auth.decorators import permission_required, login_required

class SearchPeriods(forms.Form):
    period_field = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={"onchange": "submit();"}),
        label="Períodos"
    )

@login_required
@permission_required('view_period', login_url='home')
def period_view(request):
    pass