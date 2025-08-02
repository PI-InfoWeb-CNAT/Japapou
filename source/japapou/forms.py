from django import forms
from japapou.models import menu, plate


class PlatesForms(forms.ModelForm):
    """
    Formulário para a classe Plate.
    """

    # Adicionamos o campo 'menus' explicitamente aqui,
    # pois ele não está diretamente na Model Plate, mas queremos exibi-lo.
    menus = forms.ModelMultipleChoiceField(
        queryset=menu.Menu.objects.all(),  # Todos os objetos Menu disponíveis para seleção
        widget=forms.SelectMultiple(
            attrs={"class": "seu-estilo-css"}
        ),  # Adicione suas classes CSS
        required=False,  # Defina como True se a seleção de menus for obrigatória
        label="Menus Associados",  # Rótulo que aparecerá no formulário
    )

    class Meta:
        model = plate.Plate
        # ATENÇÃO: 'menus' NÃO pode estar nos 'fields' da Meta class,
        # porque ele não é um campo direto da Model Plate.
        fields = ["name", "price", "photo", "description"]  # Remova 'menus' daqui

        # Personaliza os widgets para os campos específicos (opcional)
        widgets = {
            "description": forms.Textarea(attrs={"rows": 8}),
            # O widget para 'menus' já foi definido no campo explícito acima
        }

        # Personaliza os rótulos (labels) para os campos (opcional)
        labels = {
            "name": "Nome",
            "price": "Preço",
            "photo": "Foto",
            "description": "Descrição",
            # O label para 'menus' já foi definido no campo explícito acima
        }
