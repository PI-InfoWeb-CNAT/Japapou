from django import forms

class PlatesForms(forms.Form):
    '''
    Formulario para a classe Plates.
    '''
    name = forms.CharField(label='nome', max_length=100, required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    photo = forms.ImageField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 8}))