from django import forms # type: ignore
from japapou.models import Menu, Plate
from japapou.models.user import CustomUser


class PlatesForms(forms.ModelForm):
    """
    Formulário para a classe Plate.
    """

    # Adicionamos o campo 'menus' explicitamente aqui,
    # pois ele não está diretamente na Model Plate, mas queremos exibi-lo.
    menus = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),  # Todos os objetos Menu disponíveis para seleção
        widget=forms.SelectMultiple(
            attrs={"class": "seu-estilo-css"}
        ),  # Adicione suas classes CSS
        required=False,  # Defina como True se a seleção de menus for obrigatória
        label="Menus Associados",  # Rótulo que aparecerá no formulário
    )

    class Meta:
        model = Plate
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
        def __init__(self, *args, **kwargs):
            super(PlatesForms, self).__init__(*args, **kwargs)
            self.fields['photo'].required = False
            if self.instance and self.instance.pk:
                self.fields['menus'].initial = self.instance.menu_set.all()

class PlateChoiceField(forms.ModelMultipleChoiceField):
    """
    Campo personalizado para exibir apenas o nome do prato no label.
    """
    # Sobrescrevemos o método 'label_from_instance'.
    # Este método é chamado para cada objeto no queryset.
    # O que ele retornar será usado como o label do checkbox.
    def label_from_instance(self, obj):
        return obj.name

class MenuForms(forms.ModelForm):

    # plates = forms.ModelMultipleChoiceField(
    #     queryset=Plate.objects.all(),
    #     widget=forms.CheckboxSelectMultiple, # para transformar em checkboxes
    #     required=False,
    #     label_from_instance=lambda plate: plate.name,
    # )

    plates = PlateChoiceField(
        queryset=Plate.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Pratos"
    )

    class Meta:
        model = Menu

        fields = ["name", "plates"]

class VisitorRegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'telefone', 'endereco', 'cpf', 'data_nascimento','nome']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.tipo = 'client'  # Define o tipo como 'client' ao salvar
        if commit:
            user.save()
        return user