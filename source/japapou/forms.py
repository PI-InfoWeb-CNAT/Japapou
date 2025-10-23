from django import forms # type: ignore
from japapou.models import Menu, Plate, PlateReview, CourierReview
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

    plates = PlateChoiceField(
        queryset=Plate.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Pratos"
    )

    class Meta:
        model = Menu

        fields = ["name", "plates"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(MenuForms, self).__init__(*args, **kwargs)

        self.fields['plates'].queryset = Plate.objects.all()
    
    def save(self, commit=True):
        # 1. Pega a instância do modelo, mas ainda não a guarda na base de dados.
        instance = super().save(commit=False)

        # 2. Verifica se o campo 'created_by' (ou similar) existe no seu modelo Menu.
        #    (Ajuste 'created_by' para o nome do campo correto no seu modelo)
        if hasattr(instance, 'created_by') and self.request:
            # 3. Associa o utilizador logado à instância.
            instance.created_by = self.request.user

        # 4. Se commit for True, guarda a instância na base de dados.
        if commit:
            instance.save()
            # O save_m2m() é necessário para guardar as relações ManyToMany (os 'plates')
            self.save_m2m() 
            
        return instance

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
        
class DateInput(forms.DateInput):
    input_type = 'date'
    
    def __init__(self, **kwargs):
        kwargs.setdefault('format', '%Y-%m-%d')
        super().__init__(**kwargs)

class DeliveryRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # deixa o campo de senha opcional na edição
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    '''
    Formulário personalizado para que um gerente possa cadastrar um novo entregador
    '''
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=254)
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    telefone = forms.CharField(required=True, max_length=20)
    cpf = forms.CharField(required=True, max_length=14)
    data_nascimento = forms.DateField(
        required=True, 
        widget=DateInput()
    )
    cnh = forms.CharField(required=True, max_length=10)
    modelo_moto = forms.CharField(required=True, max_length=20)
    cor_moto = forms.CharField(required=True, max_length=10)
    placa_moto = forms.CharField(required=True, max_length=10)
    foto = forms.ImageField(required=False)
    

    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'email', 'telefone', 'endereco', 'cpf', 'data_nascimento',
            'first_name', 'last_name', 'cnh', 'modelo_moto', 'cor_moto', 'placa_moto', 'foto'
        ]

class PlateReviewForm(forms.ModelForm):
    '''
        Formulário para submeter uma avaliacao de um prato
    '''
    class Meta:
        model = PlateReview
        fields = ['value', 'comment', 'image_review']

        widgets = {
            'value': forms.HiddenInput(attrs={'id': 'id_nota'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Escreva o seu comentário (opcional)...'
            }),
        }

class CourierReviewForm(forms.ModelForm):
    '''
    Formulário para submeter uma avaliação de um Entregador.
    '''
    class Meta:
        model = CourierReview
        
        fields = ['value', 'comment'] 

        widgets = {
            
            'value': forms.HiddenInput(attrs={'id': 'id_nota'}),
            
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deixe um comentário sobre o entregador...'
            }),
        }
