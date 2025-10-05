from django import forms # type: ignore
from japapou.models import Menu, Plate
from japapou.models.user import CustomUser
from django.contrib.auth.forms import UserCreationForm


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
        fields = ["price", "photo", "description"]  # Remova 'menus' daqui

        # Personaliza os widgets para os campos específicos (opcional)
        widgets = {
            "description": forms.Textarea(attrs={"rows": 8}),
            # O widget para 'menus' já foi definido no campo explícito acima
        }

        # Personaliza os rótulos (labels) para os campos (opcional)
        labels = {
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
    '''
        Formulário personalizado para registro de visitantes para que um novo cliente possa se cadastrar
    '''
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    email = forms.EmailField(required=True, max_length=254)
    cpf = forms.CharField(required=True, max_length=14)
    data_nascimento = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'first_name', 'last_name']
        

class DeliveyrRegisterForm(forms.ModelForm):
    '''
        Formulário personalizado para que um gerente possa cadastrar um novo entregador
    '''

    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=254)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    telefone = forms.CharField(required=True, max_length=20)
    cpf = forms.CharField(required=True, max_length=14)
    data_nascimento = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    cnh = forms.CharField(required=True, max_length=10)
    modelo_moto = forms.CharField(required=True, max_length=20)
    cor_moto = forms.CharField(required=True, max_length=10)
    Placa_moto = forms.CharField(required=True, max_length=10)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'first_name', 'last_name',
                  'cnh', 'modelo_moto', 'cor_moto', 'Placa_moto']


class CustomUserCreationForm(UserCreationForm):
    '''
        Formulário personalizado para criação de usuários no painel de admin
    '''
    class Meta(UserCreationForm.Meta):
        model = CustomUser

        fields = ('tipo_usuario', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'telefone', 'endereco', 'cpf', 'data_nascimento', 
                  'foto_perfil', 'cnh', 'modelo_moto', 'cor_moto', 'Placa_moto')

         
