from django import forms
from japapou.views.manager_views import manage_menu_view


class SearchPeriods(forms.Form):
    period_field = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={"onchange": "submit();"}),
        label="Períodos"
    )


def period_view(request):
    pass